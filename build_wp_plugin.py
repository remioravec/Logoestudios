#!/usr/bin/env python3
"""
Build a WordPress plugin that deploys the entire Logopsi Studios static site
into a blank WordPress installation.
"""

import os
import json
import zipfile
import re
from pathlib import Path
from html import escape

SITE_DIR = "/workspaces/Logoestudios/site"
OUTPUT_DIR = "/workspaces/Logoestudios/wp-plugin"
PLUGIN_SLUG = "logopsi-deployer"
PLUGIN_NAME = "Logopsi Studios Deployer"

def collect_pages(site_dir):
    """Collect all HTML pages and their metadata."""
    pages = []
    for root, dirs, files in os.walk(site_dir):
        for fname in sorted(files):
            if not fname.endswith('.html'):
                continue
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, site_dir)

            with open(full_path, 'r', encoding='utf-8') as f:
                html = f.read()

            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
            title = title_match.group(1).strip() if title_match else fname.replace('.html', '')

            # Extract meta description
            desc_match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html, re.DOTALL)
            meta_desc = desc_match.group(1).strip() if desc_match else ''

            # Build WordPress slug from path
            slug = rel_path.replace('.html', '').replace('index', '').rstrip('/')
            if not slug:
                slug = 'accueil'

            # Determine parent slug for hierarchy
            parts = slug.split('/')
            parent_slug = '/'.join(parts[:-1]) if len(parts) > 1 else ''

            # Collect all image URLs used in this page
            img_urls = list(set(re.findall(r'(?:src|href)=["\']([^"\']*(?:unsplash|\.png|\.jpg|\.jpeg|\.gif|\.svg|\.webp)[^"\']*)["\']', html, re.I)))

            pages.append({
                'rel_path': rel_path,
                'slug': slug,
                'parent_slug': parent_slug,
                'title': title,
                'meta_desc': meta_desc,
                'html': html,
                'images': img_urls,
            })

    return pages


def build_pages_json(pages):
    """Build the JSON data file with all page content."""
    data = []
    for p in pages:
        data.append({
            'rel_path': p['rel_path'],
            'slug': p['slug'],
            'parent_slug': p['parent_slug'],
            'title': p['title'],
            'meta_desc': p['meta_desc'],
            'images': p['images'],
        })
    return json.dumps(data, ensure_ascii=False, indent=2)


def build_html_files_map(pages):
    """Build a map of slug -> HTML content for storage."""
    return {p['slug']: p['html'] for p in pages}


def generate_main_plugin_php(pages):
    """Generate the main plugin PHP file."""
    total_pages = len(pages)

    # Collect all unique images across all pages
    all_images = set()
    for p in pages:
        all_images.update(p['images'])
    all_images = sorted(all_images)

    return f'''<?php
/**
 * Plugin Name: {PLUGIN_NAME}
 * Description: Déploie le site complet Logopsi Studios sur WordPress. Interface d'admin pour mapper les images et pousser toutes les pages.
 * Version: 1.0.0
 * Author: Logopsi Studios
 * Text Domain: logopsi-deployer
 */

if (!defined('ABSPATH')) exit;

define('LOGOPSI_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('LOGOPSI_PLUGIN_URL', plugin_dir_url(__FILE__));
define('LOGOPSI_TOTAL_PAGES', {total_pages});

// ============================================================
// ACTIVATION / DEACTIVATION
// ============================================================

register_activation_hook(__FILE__, 'logopsi_activate');
function logopsi_activate() {{
    // Flush rewrite rules
    flush_rewrite_rules();
}}

register_deactivation_hook(__FILE__, 'logopsi_deactivate');
function logopsi_deactivate() {{
    flush_rewrite_rules();
}}

// ============================================================
// ADMIN MENU
// ============================================================

add_action('admin_menu', 'logopsi_admin_menu');
function logopsi_admin_menu() {{
    add_menu_page(
        'Logopsi Deployer',
        'Logopsi Deploy',
        'manage_options',
        'logopsi-deployer',
        'logopsi_admin_page',
        'dashicons-upload',
        30
    );
    add_submenu_page(
        'logopsi-deployer',
        'Gestion des images',
        'Images',
        'manage_options',
        'logopsi-images',
        'logopsi_images_page'
    );
}}

// ============================================================
// ADMIN STYLES
// ============================================================

add_action('admin_enqueue_scripts', 'logopsi_admin_assets');
function logopsi_admin_assets($hook) {{
    if (strpos($hook, 'logopsi') === false) return;
    wp_enqueue_media();
    wp_enqueue_style('logopsi-admin', LOGOPSI_PLUGIN_URL . 'admin/admin.css', [], '1.0.0');
    wp_enqueue_script('logopsi-admin', LOGOPSI_PLUGIN_URL . 'admin/admin.js', ['jquery'], '1.0.0', true);
    wp_localize_script('logopsi-admin', 'logopsiAjax', [
        'ajaxurl' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('logopsi_deploy_nonce'),
    ]);
}}

// ============================================================
// CUSTOM PAGE TEMPLATE (BLANK - bypasses theme)
// ============================================================

add_filter('template_include', 'logopsi_custom_template');
function logopsi_custom_template($template) {{
    if (is_page()) {{
        $custom_html = get_post_meta(get_the_ID(), '_logopsi_full_html', true);
        if (!empty($custom_html)) {{
            // Serve the raw HTML directly
            echo $custom_html;
            exit;
        }}
    }}
    return $template;
}}

// Make the homepage work too
add_action('template_redirect', 'logopsi_homepage_redirect');
function logopsi_homepage_redirect() {{
    if (is_front_page()) {{
        $front_page_id = get_option('page_on_front');
        if ($front_page_id) {{
            $custom_html = get_post_meta($front_page_id, '_logopsi_full_html', true);
            if (!empty($custom_html)) {{
                echo $custom_html;
                exit;
            }}
        }}
    }}
}}

// ============================================================
// LOAD PAGE DATA
// ============================================================

function logopsi_get_pages_data() {{
    static $data = null;
    if ($data === null) {{
        $json_path = LOGOPSI_PLUGIN_DIR . 'data/pages.json';
        $data = json_decode(file_get_contents($json_path), true);
    }}
    return $data;
}}

function logopsi_get_html_content($slug) {{
    $safe_name = str_replace('/', '__', $slug);
    $html_path = LOGOPSI_PLUGIN_DIR . 'data/html/' . $safe_name . '.html';
    if (file_exists($html_path)) {{
        return file_get_contents($html_path);
    }}
    return '';
}}

// ============================================================
// IMAGE MAPPING
// ============================================================

function logopsi_get_image_map() {{
    return get_option('logopsi_image_map', []);
}}

function logopsi_apply_image_mapping($html) {{
    $map = logopsi_get_image_map();
    foreach ($map as $original => $replacement) {{
        if (!empty($replacement)) {{
            $html = str_replace($original, $replacement, $html);
        }}
    }}
    return $html;
}}

// ============================================================
// FIX INTERNAL LINKS FOR WORDPRESS
// ============================================================

function logopsi_fix_links($html, $current_slug) {{
    // Fix relative links to point to WordPress permalink structure
    // Replace href="../orthophonie/dyslexie.html" with href="/orthophonie/dyslexie/"
    // Replace href="./orthophonie/" with href="/orthophonie/"
    // Replace href="villes/dyslexie-paris.html" with proper path

    $site_url = home_url();

    // Determine base path for relative resolution
    $parts = explode('/', $current_slug);
    $depth = count($parts);

    // Pattern: href="(relative path).html"
    $html = preg_replace_callback(
        '/href="((?!https?:\\/\\/|#|mailto:|tel:|javascript:)[^"]*?\\.html)"/i',
        function($matches) use ($current_slug, $site_url, $parts) {{
            $href = $matches[1];

            // Resolve relative path
            $resolved = logopsi_resolve_path($current_slug, $href);
            // Remove .html and ensure trailing slash
            $resolved = preg_replace('/\\.html$/', '', $resolved);
            $resolved = rtrim($resolved, '/');

            // Handle index pages
            $resolved = preg_replace('/\\/index$/', '', $resolved);

            if ($resolved === 'accueil' || $resolved === '' || $resolved === 'index') {{
                return 'href="' . $site_url . '/"';
            }}

            return 'href="' . $site_url . '/' . $resolved . '/"';
        }},
        $html
    );

    // Fix directory links (href="../orthophonie/")
    $html = preg_replace_callback(
        '/href="((?!https?:\\/\\/|#|mailto:|tel:|javascript:)[^"]*?)"/i',
        function($matches) use ($current_slug, $site_url) {{
            $href = $matches[1];
            if (strpos($href, '.') !== false && strpos($href, '/') === false) return $matches[0]; // skip anchors, etc
            if (preg_match('/\\.(css|js|png|jpg|jpeg|gif|svg|webp|ico|pdf)$/i', $href)) return $matches[0]; // skip assets

            if (strpos($href, '../') !== false || strpos($href, './') !== false) {{
                $resolved = logopsi_resolve_path($current_slug, $href);
                $resolved = rtrim($resolved, '/');
                $resolved = preg_replace('/\\/index$/', '', $resolved);
                if ($resolved === '' || $resolved === 'accueil') {{
                    return 'href="' . $site_url . '/"';
                }}
                return 'href="' . $site_url . '/' . $resolved . '/"';
            }}
            return $matches[0];
        }},
        $html
    );

    return $html;
}}

function logopsi_resolve_path($base_slug, $relative) {{
    // Get directory of current slug
    $base_parts = explode('/', $base_slug);
    array_pop($base_parts); // remove filename part

    $rel_parts = explode('/', $relative);

    foreach ($rel_parts as $part) {{
        if ($part === '..') {{
            array_pop($base_parts);
        }} elseif ($part === '.' || $part === '') {{
            continue;
        }} else {{
            $base_parts[] = $part;
        }}
    }}

    return implode('/', $base_parts);
}}

// ============================================================
// AJAX: DEPLOY ALL PAGES
// ============================================================

add_action('wp_ajax_logopsi_deploy', 'logopsi_ajax_deploy');
function logopsi_ajax_deploy() {{
    check_ajax_referer('logopsi_deploy_nonce', 'nonce');
    if (!current_user_can('manage_options')) wp_die('Unauthorized');

    $pages_data = logopsi_get_pages_data();
    $created = 0;
    $updated = 0;
    $errors = [];

    // First pass: create all pages (without parents)
    $slug_to_id = [];

    foreach ($pages_data as $page) {{
        $slug = $page['slug'];
        $wp_slug = str_replace('/', '-', $slug);

        // Get HTML content
        $html = logopsi_get_html_content($slug);
        if (empty($html)) {{
            $errors[] = "HTML manquant pour: " . $slug;
            continue;
        }}

        // Apply image mapping
        $html = logopsi_apply_image_mapping($html);

        // Fix internal links for WordPress
        $html = logopsi_fix_links($html, $slug);

        // Check if page already exists
        $existing = get_posts([
            'post_type' => 'page',
            'name' => sanitize_title(basename($slug)),
            'posts_per_page' => 1,
            'post_status' => 'any',
            'meta_key' => '_logopsi_slug',
            'meta_value' => $slug,
        ]);

        $post_data = [
            'post_title' => wp_strip_all_tags($page['title']),
            'post_name' => sanitize_title(basename($slug)),
            'post_content' => '<!-- Logopsi page: ' . esc_html($slug) . ' -->',
            'post_status' => 'publish',
            'post_type' => 'page',
        ];

        if (!empty($existing)) {{
            $post_data['ID'] = $existing[0]->ID;
            $post_id = wp_update_post($post_data);
            $updated++;
        }} else {{
            $post_id = wp_insert_post($post_data);
            $created++;
        }}

        if (is_wp_error($post_id)) {{
            $errors[] = "Erreur pour $slug: " . $post_id->get_error_message();
            continue;
        }}

        // Store full HTML as meta
        update_post_meta($post_id, '_logopsi_full_html', $html);
        update_post_meta($post_id, '_logopsi_slug', $slug);
        update_post_meta($post_id, '_logopsi_rel_path', $page['rel_path']);

        // Store meta description for SEO
        if (!empty($page['meta_desc'])) {{
            update_post_meta($post_id, '_logopsi_meta_desc', $page['meta_desc']);
        }}

        $slug_to_id[$slug] = $post_id;
    }}

    // Second pass: set parent relationships
    foreach ($pages_data as $page) {{
        if (empty($page['parent_slug'])) continue;
        $slug = $page['slug'];
        $parent_slug = $page['parent_slug'];

        if (isset($slug_to_id[$slug]) && isset($slug_to_id[$parent_slug])) {{
            wp_update_post([
                'ID' => $slug_to_id[$slug],
                'post_parent' => $slug_to_id[$parent_slug],
            ]);
        }}
    }}

    // Set homepage
    if (isset($slug_to_id['accueil'])) {{
        update_option('show_on_front', 'page');
        update_option('page_on_front', $slug_to_id['accueil']);
    }}

    // Update permalink structure
    update_option('permalink_structure', '/%postname%/');
    flush_rewrite_rules();

    wp_send_json_success([
        'created' => $created,
        'updated' => $updated,
        'errors' => $errors,
        'total' => count($pages_data),
    ]);
}}

// ============================================================
// AJAX: DEPLOY SINGLE PAGE
// ============================================================

add_action('wp_ajax_logopsi_deploy_single', 'logopsi_ajax_deploy_single');
function logopsi_ajax_deploy_single() {{
    check_ajax_referer('logopsi_deploy_nonce', 'nonce');
    if (!current_user_can('manage_options')) wp_die('Unauthorized');

    $slug = sanitize_text_field($_POST['slug'] ?? '');
    if (empty($slug)) wp_send_json_error('Slug manquant');

    $pages_data = logopsi_get_pages_data();
    $page = null;
    foreach ($pages_data as $p) {{
        if ($p['slug'] === $slug) {{ $page = $p; break; }}
    }}
    if (!$page) wp_send_json_error('Page non trouvée');

    $html = logopsi_get_html_content($slug);
    $html = logopsi_apply_image_mapping($html);
    $html = logopsi_fix_links($html, $slug);

    $existing = get_posts([
        'post_type' => 'page',
        'meta_key' => '_logopsi_slug',
        'meta_value' => $slug,
        'posts_per_page' => 1,
        'post_status' => 'any',
    ]);

    $post_data = [
        'post_title' => wp_strip_all_tags($page['title']),
        'post_name' => sanitize_title(basename($slug)),
        'post_content' => '<!-- Logopsi page: ' . esc_html($slug) . ' -->',
        'post_status' => 'publish',
        'post_type' => 'page',
    ];

    if (!empty($existing)) {{
        $post_data['ID'] = $existing[0]->ID;
        $post_id = wp_update_post($post_data);
    }} else {{
        $post_id = wp_insert_post($post_data);
    }}

    update_post_meta($post_id, '_logopsi_full_html', $html);
    update_post_meta($post_id, '_logopsi_slug', $slug);

    wp_send_json_success(['post_id' => $post_id, 'slug' => $slug]);
}}

// ============================================================
// AJAX: SAVE IMAGE MAPPING
// ============================================================

add_action('wp_ajax_logopsi_save_image', 'logopsi_ajax_save_image');
function logopsi_ajax_save_image() {{
    check_ajax_referer('logopsi_deploy_nonce', 'nonce');
    if (!current_user_can('manage_options')) wp_die('Unauthorized');

    $original_url = sanitize_text_field($_POST['original_url'] ?? '');
    $new_url = esc_url_raw($_POST['new_url'] ?? '');

    $map = logopsi_get_image_map();
    $map[$original_url] = $new_url;
    update_option('logopsi_image_map', $map);

    wp_send_json_success(['saved' => true]);
}}

// ============================================================
// AJAX: RESET ALL PAGES
// ============================================================

add_action('wp_ajax_logopsi_reset', 'logopsi_ajax_reset');
function logopsi_ajax_reset() {{
    check_ajax_referer('logopsi_deploy_nonce', 'nonce');
    if (!current_user_can('manage_options')) wp_die('Unauthorized');

    $pages = get_posts([
        'post_type' => 'page',
        'meta_key' => '_logopsi_slug',
        'posts_per_page' => -1,
        'post_status' => 'any',
    ]);

    $deleted = 0;
    foreach ($pages as $page) {{
        wp_delete_post($page->ID, true);
        $deleted++;
    }}

    wp_send_json_success(['deleted' => $deleted]);
}}

// ============================================================
// AJAX: GET DEPLOY STATUS
// ============================================================

add_action('wp_ajax_logopsi_status', 'logopsi_ajax_status');
function logopsi_ajax_status() {{
    check_ajax_referer('logopsi_deploy_nonce', 'nonce');

    $deployed = get_posts([
        'post_type' => 'page',
        'meta_key' => '_logopsi_slug',
        'posts_per_page' => -1,
        'post_status' => 'publish',
        'fields' => 'ids',
    ]);

    $total = count(logopsi_get_pages_data());

    wp_send_json_success([
        'deployed' => count($deployed),
        'total' => $total,
    ]);
}}

// ============================================================
// ADMIN PAGE: MAIN DASHBOARD
// ============================================================

function logopsi_admin_page() {{
    $pages_data = logopsi_get_pages_data();
    $deployed_pages = get_posts([
        'post_type' => 'page',
        'meta_key' => '_logopsi_slug',
        'posts_per_page' => -1,
        'post_status' => 'any',
    ]);
    $deployed_slugs = [];
    foreach ($deployed_pages as $dp) {{
        $s = get_post_meta($dp->ID, '_logopsi_slug', true);
        $deployed_slugs[$s] = $dp->ID;
    }}

    // Group pages by category
    $groups = [];
    foreach ($pages_data as $p) {{
        $parts = explode('/', $p['slug']);
        $group = $parts[0] ?? 'accueil';
        if ($group === 'accueil') $group = 'Accueil';
        elseif ($group === 'orthophonie') $group = 'Orthophonie';
        elseif ($group === 'psychologie') $group = 'Psychologie';
        elseif ($group === 'soutien-scolaire') $group = 'Soutien Scolaire';
        $groups[$group][] = $p;
    }}

    ?>
    <div class="wrap logopsi-wrap">
        <h1><span class="dashicons dashicons-upload" style="font-size:30px;margin-right:10px;color:#05C86B;"></span> Logopsi Studios Deployer</h1>

        <div class="logopsi-stats">
            <div class="logopsi-stat-card">
                <div class="logopsi-stat-number"><?php echo count($pages_data); ?></div>
                <div class="logopsi-stat-label">Pages totales</div>
            </div>
            <div class="logopsi-stat-card">
                <div class="logopsi-stat-number" style="color:#05C86B;"><?php echo count($deployed_slugs); ?></div>
                <div class="logopsi-stat-label">Pages déployées</div>
            </div>
            <div class="logopsi-stat-card">
                <div class="logopsi-stat-number" style="color:#e67e22;"><?php echo count($pages_data) - count($deployed_slugs); ?></div>
                <div class="logopsi-stat-label">En attente</div>
            </div>
        </div>

        <div class="logopsi-actions">
            <button id="logopsi-deploy-all" class="button button-primary button-hero logopsi-btn-deploy">
                <span class="dashicons dashicons-upload"></span> Déployer tout le site (<?php echo count($pages_data); ?> pages)
            </button>
            <button id="logopsi-reset-all" class="button button-secondary" style="margin-left:10px;">
                <span class="dashicons dashicons-trash"></span> Supprimer toutes les pages
            </button>
        </div>

        <div id="logopsi-progress" style="display:none;">
            <div class="logopsi-progress-bar">
                <div class="logopsi-progress-fill" id="logopsi-progress-fill"></div>
            </div>
            <p id="logopsi-progress-text">Déploiement en cours...</p>
        </div>

        <div id="logopsi-result" style="display:none;" class="notice notice-success">
            <p id="logopsi-result-text"></p>
        </div>

        <?php foreach ($groups as $group_name => $group_pages): ?>
        <div class="logopsi-group">
            <h2 class="logopsi-group-title"><?php echo esc_html($group_name); ?> <span class="logopsi-group-count">(<?php echo count($group_pages); ?>)</span></h2>
            <table class="wp-list-table widefat fixed striped">
                <thead>
                    <tr>
                        <th style="width:30px;">Status</th>
                        <th>Titre</th>
                        <th>Slug</th>
                        <th>Fichier source</th>
                        <th style="width:100px;">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($group_pages as $p):
                        $is_deployed = isset($deployed_slugs[$p['slug']]);
                    ?>
                    <tr>
                        <td>
                            <?php if ($is_deployed): ?>
                                <span class="dashicons dashicons-yes-alt" style="color:#05C86B;" title="Déployée"></span>
                            <?php else: ?>
                                <span class="dashicons dashicons-clock" style="color:#ccc;" title="En attente"></span>
                            <?php endif; ?>
                        </td>
                        <td><strong><?php echo esc_html($p['title']); ?></strong></td>
                        <td><code>/<?php echo esc_html($p['slug']); ?>/</code></td>
                        <td><small><?php echo esc_html($p['rel_path']); ?></small></td>
                        <td>
                            <button class="button button-small logopsi-deploy-single" data-slug="<?php echo esc_attr($p['slug']); ?>">
                                <?php echo $is_deployed ? 'Re-push' : 'Push'; ?>
                            </button>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endforeach; ?>
    </div>
    <?php
}}

// ============================================================
// ADMIN PAGE: IMAGES
// ============================================================

function logopsi_images_page() {{
    $pages_data = logopsi_get_pages_data();
    $image_map = logopsi_get_image_map();

    // Collect all unique images
    $all_images = [];
    foreach ($pages_data as $p) {{
        foreach ($p['images'] as $img) {{
            if (!isset($all_images[$img])) {{
                $all_images[$img] = ['url' => $img, 'pages' => []];
            }}
            $all_images[$img]['pages'][] = $p['slug'];
        }}
    }}

    ?>
    <div class="wrap logopsi-wrap">
        <h1><span class="dashicons dashicons-format-image" style="font-size:30px;margin-right:10px;color:#05C86B;"></span> Gestion des images</h1>
        <p>Remplacez les images Unsplash par vos propres images. Cliquez sur "Choisir" pour sélectionner une image depuis la bibliothèque WordPress, ou collez une URL.</p>

        <table class="wp-list-table widefat fixed striped">
            <thead>
                <tr>
                    <th style="width:80px;">Aperçu</th>
                    <th>URL originale</th>
                    <th>URL de remplacement</th>
                    <th style="width:60px;">Pages</th>
                    <th style="width:200px;">Actions</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($all_images as $img_url => $img_data):
                    $mapped = $image_map[$img_url] ?? '';
                ?>
                <tr>
                    <td><img src="<?php echo esc_url($mapped ?: $img_url); ?>" style="width:60px;height:40px;object-fit:cover;border-radius:4px;"></td>
                    <td><small style="word-break:break-all;"><?php echo esc_html($img_url); ?></small></td>
                    <td>
                        <input type="text" class="logopsi-img-input regular-text" data-original="<?php echo esc_attr($img_url); ?>" value="<?php echo esc_attr($mapped); ?>" placeholder="Collez une URL ou utilisez le bouton" style="width:100%;">
                    </td>
                    <td><span class="logopsi-badge"><?php echo count($img_data['pages']); ?></span></td>
                    <td>
                        <button class="button logopsi-img-upload" data-original="<?php echo esc_attr($img_url); ?>">
                            <span class="dashicons dashicons-upload" style="vertical-align:middle;"></span> Choisir
                        </button>
                        <button class="button logopsi-img-save" data-original="<?php echo esc_attr($img_url); ?>">
                            <span class="dashicons dashicons-saved" style="vertical-align:middle;"></span>
                        </button>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <?php
}}
'''


def generate_admin_css():
    return '''
.logopsi-wrap { max-width: 1200px; }
.logopsi-wrap h1 { display: flex; align-items: center; margin-bottom: 20px; font-size: 24px; }

.logopsi-stats { display: flex; gap: 20px; margin-bottom: 30px; }
.logopsi-stat-card {
    background: #fff; border: 1px solid #e0e0e0; border-radius: 12px;
    padding: 24px 32px; text-align: center; flex: 1; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.logopsi-stat-number { font-size: 36px; font-weight: 700; color: #111; }
.logopsi-stat-label { font-size: 13px; color: #777; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }

.logopsi-actions { margin-bottom: 30px; display: flex; align-items: center; }
.logopsi-btn-deploy {
    background: #05C86B !important; border-color: #04b05e !important;
    font-size: 15px !important; padding: 10px 30px !important; border-radius: 8px !important;
    display: flex; align-items: center; gap: 8px;
}
.logopsi-btn-deploy:hover { background: #04b05e !important; }

.logopsi-progress-bar {
    width: 100%; height: 8px; background: #e0e0e0; border-radius: 4px;
    margin: 20px 0 10px; overflow: hidden;
}
.logopsi-progress-fill {
    height: 100%; background: #05C86B; border-radius: 4px;
    transition: width 0.3s ease; width: 0%;
}

.logopsi-group { margin-bottom: 30px; }
.logopsi-group-title {
    font-size: 18px; font-weight: 600; margin-bottom: 10px;
    padding-bottom: 8px; border-bottom: 2px solid #05C86B;
}
.logopsi-group-count { color: #999; font-weight: 400; font-size: 14px; }

.logopsi-badge {
    background: #f0f0f0; border-radius: 10px; padding: 2px 8px;
    font-size: 12px; font-weight: 600;
}
'''


def generate_admin_js():
    return '''
jQuery(document).ready(function($) {

    // Deploy all pages
    $('#logopsi-deploy-all').on('click', function() {
        if (!confirm('Déployer toutes les pages sur WordPress ?')) return;

        var $btn = $(this);
        $btn.prop('disabled', true).text('Déploiement en cours...');
        $('#logopsi-progress').show();
        $('#logopsi-result').hide();

        $.ajax({
            url: logopsiAjax.ajaxurl,
            type: 'POST',
            data: {
                action: 'logopsi_deploy',
                nonce: logopsiAjax.nonce
            },
            success: function(response) {
                if (response.success) {
                    var d = response.data;
                    $('#logopsi-progress-fill').css('width', '100%');
                    $('#logopsi-progress-text').text('Terminé !');
                    $('#logopsi-result').show().removeClass('notice-error').addClass('notice-success');
                    $('#logopsi-result-text').text(
                        d.created + ' pages créées, ' + d.updated + ' mises à jour. ' +
                        (d.errors.length ? d.errors.length + ' erreur(s).' : 'Aucune erreur.')
                    );
                    if (d.errors.length) {
                        console.log('Erreurs:', d.errors);
                    }
                    setTimeout(function() { location.reload(); }, 2000);
                } else {
                    alert('Erreur: ' + response.data);
                }
            },
            error: function() {
                alert('Erreur de connexion.');
            },
            complete: function() {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-upload"></span> Déployer tout le site');
            }
        });
    });

    // Deploy single page
    $('.logopsi-deploy-single').on('click', function() {
        var $btn = $(this);
        var slug = $btn.data('slug');
        $btn.prop('disabled', true).text('...');

        $.ajax({
            url: logopsiAjax.ajaxurl,
            type: 'POST',
            data: {
                action: 'logopsi_deploy_single',
                nonce: logopsiAjax.nonce,
                slug: slug
            },
            success: function(response) {
                if (response.success) {
                    $btn.text('OK').css('color', '#05C86B');
                    $btn.closest('tr').find('.dashicons-clock')
                        .removeClass('dashicons-clock').addClass('dashicons-yes-alt')
                        .css('color', '#05C86B');
                } else {
                    alert('Erreur: ' + response.data);
                }
            },
            complete: function() {
                $btn.prop('disabled', false);
                setTimeout(function() { $btn.text('Re-push'); }, 1500);
            }
        });
    });

    // Reset all
    $('#logopsi-reset-all').on('click', function() {
        if (!confirm('ATTENTION: Supprimer toutes les pages Logopsi de WordPress ?')) return;

        $.ajax({
            url: logopsiAjax.ajaxurl,
            type: 'POST',
            data: {
                action: 'logopsi_reset',
                nonce: logopsiAjax.nonce
            },
            success: function(response) {
                if (response.success) {
                    alert(response.data.deleted + ' pages supprimées.');
                    location.reload();
                }
            }
        });
    });

    // Image upload via media library
    $('.logopsi-img-upload').on('click', function(e) {
        e.preventDefault();
        var $btn = $(this);
        var originalUrl = $btn.data('original');
        var $input = $('input[data-original="' + originalUrl + '"]');

        var frame = wp.media({
            title: 'Choisir une image',
            multiple: false,
            library: { type: 'image' }
        });

        frame.on('select', function() {
            var attachment = frame.state().get('selection').first().toJSON();
            $input.val(attachment.url);
            // Auto save
            $btn.siblings('.logopsi-img-save').trigger('click');
            $btn.closest('tr').find('img').attr('src', attachment.url);
        });

        frame.open();
    });

    // Save image mapping
    $('.logopsi-img-save').on('click', function() {
        var $btn = $(this);
        var originalUrl = $btn.data('original');
        var $input = $('input[data-original="' + originalUrl + '"]');

        $.ajax({
            url: logopsiAjax.ajaxurl,
            type: 'POST',
            data: {
                action: 'logopsi_save_image',
                nonce: logopsiAjax.nonce,
                original_url: originalUrl,
                new_url: $input.val()
            },
            success: function(response) {
                if (response.success) {
                    $btn.find('.dashicons').css('color', '#05C86B');
                    setTimeout(function() { $btn.find('.dashicons').css('color', ''); }, 1500);
                }
            }
        });
    });
});
'''


def main():
    print("Building WordPress plugin...")

    # Collect all pages
    pages = collect_pages(SITE_DIR)
    print(f"  Found {len(pages)} pages")

    # Create output dirs
    os.makedirs(f"{OUTPUT_DIR}/{PLUGIN_SLUG}/admin", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/{PLUGIN_SLUG}/data/html", exist_ok=True)

    # 1. Write main plugin PHP
    with open(f"{OUTPUT_DIR}/{PLUGIN_SLUG}/{PLUGIN_SLUG}.php", 'w', encoding='utf-8') as f:
        f.write(generate_main_plugin_php(pages))
    print("  Generated: main plugin PHP")

    # 2. Write pages.json (metadata only, no HTML)
    pages_json = build_pages_json(pages)
    with open(f"{OUTPUT_DIR}/{PLUGIN_SLUG}/data/pages.json", 'w', encoding='utf-8') as f:
        f.write(pages_json)
    print("  Generated: pages.json")

    # 3. Write individual HTML files
    html_map = build_html_files_map(pages)
    for slug, html in html_map.items():
        safe_name = slug.replace('/', '__')
        with open(f"{OUTPUT_DIR}/{PLUGIN_SLUG}/data/html/{safe_name}.html", 'w', encoding='utf-8') as f:
            f.write(html)
    print(f"  Generated: {len(html_map)} HTML files")

    # 4. Write admin CSS
    with open(f"{OUTPUT_DIR}/{PLUGIN_SLUG}/admin/admin.css", 'w', encoding='utf-8') as f:
        f.write(generate_admin_css())
    print("  Generated: admin.css")

    # 5. Write admin JS
    with open(f"{OUTPUT_DIR}/{PLUGIN_SLUG}/admin/admin.js", 'w', encoding='utf-8') as f:
        f.write(generate_admin_js())
    print("  Generated: admin.js")

    # 6. Create ZIP
    zip_path = f"{OUTPUT_DIR}/{PLUGIN_SLUG}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(f"{OUTPUT_DIR}/{PLUGIN_SLUG}"):
            for fname in files:
                full_path = os.path.join(root, fname)
                arc_name = os.path.relpath(full_path, OUTPUT_DIR)
                zf.write(full_path, arc_name)

    zip_size = os.path.getsize(zip_path)
    print(f"\n  Plugin ZIP created: {zip_path}")
    print(f"  Size: {zip_size / 1024 / 1024:.1f} MB")
    print(f"\n  Installation:")
    print(f"  1. Téléchargez le fichier {PLUGIN_SLUG}.zip")
    print(f"  2. WordPress Admin > Extensions > Ajouter > Téléverser")
    print(f"  3. Activez le plugin")
    print(f"  4. Allez dans 'Logopsi Deploy' dans le menu admin")
    print(f"  5. (Optionnel) Mappez vos images dans l'onglet 'Images'")
    print(f"  6. Cliquez 'Déployer tout le site'")


if __name__ == "__main__":
    main()
