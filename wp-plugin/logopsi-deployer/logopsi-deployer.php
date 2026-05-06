<?php
/**
 * Plugin Name: Logopsi Studios Deployer
 * Description: Déploie le site complet Logopsi Studios sur WordPress.
 * Version: 2.0.0
 * Author: Logopsi Studios
 * Text Domain: logopsi-deployer
 */

if (!defined('ABSPATH')) exit;

define('LOGOPSI_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('LOGOPSI_PLUGIN_URL', plugin_dir_url(__FILE__));

// ============================================================
// ACTIVATION / DEACTIVATION
// ============================================================

register_activation_hook(__FILE__, function() { flush_rewrite_rules(); });
register_deactivation_hook(__FILE__, function() { flush_rewrite_rules(); });

// ============================================================
// LOAD PAGE DATA
// ============================================================

function logopsi_get_pages_data() {
    static $data = null;
    if ($data === null) {
        $data = json_decode(file_get_contents(LOGOPSI_PLUGIN_DIR . 'data/pages.json'), true);
    }
    return $data;
}

function logopsi_get_html_content($slug) {
    $safe_name = str_replace('/', '__', $slug);
    $path = LOGOPSI_PLUGIN_DIR . 'data/html/' . $safe_name . '.html';
    return file_exists($path) ? file_get_contents($path) : '';
}

// ============================================================
// SERVE HTML AT RUNTIME (no DB storage of HTML)
// ============================================================

add_action('template_redirect', 'logopsi_serve_page', 1);
function logopsi_serve_page() {
    if (!is_page() && !is_front_page()) return;

    $post_id = is_front_page() ? get_option('page_on_front') : get_the_ID();
    if (!$post_id) return;

    $slug = get_post_meta($post_id, '_logopsi_slug', true);
    if (empty($slug)) return;

    $html = logopsi_get_html_content($slug);
    if (empty($html)) return;

    // Apply image mapping
    $map = get_option('logopsi_image_map', []);
    foreach ($map as $original => $replacement) {
        if (!empty($replacement)) {
            $html = str_replace($original, $replacement, $html);
        }
    }

    // Fix links
    $html = logopsi_fix_links($html, $slug);

    // Fix logo
    $logo_url = LOGOPSI_PLUGIN_URL . 'admin/logo-logopsi.png';
    $html = preg_replace('/src="[^"]*logo-logopsi\.png"/', 'src="' . $logo_url . '"', $html);

    echo $html;
    exit;
}

// ============================================================
// FIX INTERNAL LINKS FOR WORDPRESS
// ============================================================

function logopsi_fix_links($html, $current_slug) {
    $site_url = home_url();

    // Phase 1: href="(relative).html"
    $html = preg_replace_callback(
        '/href="((?!https?:\/\/|#|mailto:|tel:|javascript:)[^"]*?\.html)"/i',
        function($matches) use ($current_slug, $site_url) {
            $resolved = logopsi_resolve_path($current_slug, $matches[1]);
            $resolved = preg_replace('/\.html$/', '', $resolved);
            $resolved = rtrim($resolved, '/');
            $resolved = preg_replace('/\/index$/', '', $resolved);

            if ($resolved === 'accueil' || $resolved === '' || $resolved === 'index') {
                return 'href="' . $site_url . '/"';
            }
            return 'href="' . $site_url . '/' . $resolved . '/"';
        },
        $html
    );

    // Phase 2: directory links href="../orthophonie/"
    $html = preg_replace_callback(
        '/href="((?!https?:\/\/|#|mailto:|tel:|javascript:)[^"]*?)"/i',
        function($matches) use ($current_slug, $site_url) {
            $href = $matches[1];
            if (strpos($href, '.') !== false && strpos($href, '/') === false) return $matches[0];
            if (preg_match('/\.(css|js|png|jpg|jpeg|gif|svg|webp|ico|pdf)$/i', $href)) return $matches[0];

            if (strpos($href, '../') !== false || strpos($href, './') !== false) {
                $resolved = logopsi_resolve_path($current_slug, $href);
                $resolved = rtrim($resolved, '/');
                $resolved = preg_replace('/\/index$/', '', $resolved);
                if ($resolved === '' || $resolved === 'accueil') {
                    return 'href="' . $site_url . '/"';
                }
                return 'href="' . $site_url . '/' . $resolved . '/"';
            }
            return $matches[0];
        },
        $html
    );

    return $html;
}

function logopsi_resolve_path($base_slug, $relative) {
    $base_parts = explode('/', $base_slug);
    array_pop($base_parts);
    foreach (explode('/', $relative) as $part) {
        if ($part === '..') array_pop($base_parts);
        elseif ($part !== '.' && $part !== '') $base_parts[] = $part;
    }
    return implode('/', $base_parts);
}

// ============================================================
// ADMIN
// ============================================================

add_action('admin_menu', function() {
    add_menu_page('Logopsi Deployer', 'Logopsi Deploy', 'manage_options', 'logopsi-deployer', 'logopsi_admin_page', 'dashicons-upload', 30);
    add_submenu_page('logopsi-deployer', 'Gestion des images', 'Images', 'manage_options', 'logopsi-images', 'logopsi_images_page');
});

add_action('admin_enqueue_scripts', function($hook) {
    if (strpos($hook, 'logopsi') === false) return;
    wp_enqueue_media();
    wp_enqueue_style('logopsi-admin', LOGOPSI_PLUGIN_URL . 'admin/admin.css', [], '2.0.0');
    wp_enqueue_script('logopsi-admin', LOGOPSI_PLUGIN_URL . 'admin/admin.js', ['jquery'], '2.0.0', true);
    wp_localize_script('logopsi-admin', 'logopsiAjax', [
        'ajaxurl' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('logopsi_deploy_nonce'),
    ]);
});

// ============================================================
// AJAX: DEPLOY BATCH (lightweight - no HTML in DB)
// ============================================================

add_action('wp_ajax_logopsi_deploy', 'logopsi_ajax_deploy');
function logopsi_ajax_deploy() {
    check_ajax_referer('logopsi_deploy_nonce', 'nonce');
    if (!current_user_can('manage_options')) wp_die('Unauthorized');

    @set_time_limit(120);

    $offset = isset($_POST['offset']) ? intval($_POST['offset']) : 0;
    $batch_size = 25;

    $pages_data = logopsi_get_pages_data();

    // Sort by depth (parents first)
    usort($pages_data, function($a, $b) {
        return substr_count($a['slug'], '/') - substr_count($b['slug'], '/');
    });

    $total = count($pages_data);
    $batch = array_slice($pages_data, $offset, $batch_size);
    $created = 0;
    $updated = 0;
    $errors = [];

    foreach ($batch as $page) {
        $slug = $page['slug'];

        // Find existing page
        $existing = get_posts([
            'post_type' => 'page',
            'posts_per_page' => 1,
            'post_status' => 'any',
            'meta_key' => '_logopsi_slug',
            'meta_value' => $slug,
            'fields' => 'ids',
            'no_found_rows' => true,
        ]);

        // Find parent
        $parent_id = 0;
        if (!empty($page['parent_slug'])) {
            $parents = get_posts([
                'post_type' => 'page',
                'posts_per_page' => 1,
                'post_status' => 'any',
                'meta_key' => '_logopsi_slug',
                'meta_value' => $page['parent_slug'],
                'fields' => 'ids',
                'no_found_rows' => true,
            ]);
            if (!empty($parents)) $parent_id = $parents[0];
        }

        $post_data = [
            'post_title'   => wp_strip_all_tags($page['title']),
            'post_name'    => sanitize_title(basename($slug)),
            'post_content' => '',
            'post_status'  => 'publish',
            'post_type'    => 'page',
            'post_parent'  => $parent_id,
        ];

        if (!empty($existing)) {
            $post_data['ID'] = $existing[0];
            $post_id = wp_update_post($post_data);
            $updated++;
        } else {
            $post_id = wp_insert_post($post_data);
            $created++;
        }

        if (is_wp_error($post_id)) {
            $errors[] = $slug . ': ' . $post_id->get_error_message();
            continue;
        }

        // Only store the slug reference (no HTML!)
        update_post_meta($post_id, '_logopsi_slug', $slug);
    }

    $next_offset = $offset + $batch_size;
    $done = $next_offset >= $total;

    if ($done) {
        // Set homepage
        $accueil = get_posts([
            'post_type' => 'page', 'posts_per_page' => 1, 'post_status' => 'publish',
            'meta_key' => '_logopsi_slug', 'meta_value' => 'accueil', 'fields' => 'ids',
        ]);
        if (!empty($accueil)) {
            update_option('show_on_front', 'page');
            update_option('page_on_front', $accueil[0]);
        }
        update_option('permalink_structure', '/%postname%/');
        flush_rewrite_rules();
    }

    wp_send_json_success([
        'created'     => $created,
        'updated'     => $updated,
        'errors'      => $errors,
        'total'       => $total,
        'next_offset' => $done ? -1 : $next_offset,
        'done'        => $done,
        'processed'   => min($next_offset, $total),
    ]);
}

// ============================================================
// AJAX: DEPLOY SINGLE PAGE
// ============================================================

add_action('wp_ajax_logopsi_deploy_single', 'logopsi_ajax_deploy_single');
function logopsi_ajax_deploy_single() {
    check_ajax_referer('logopsi_deploy_nonce', 'nonce');
    if (!current_user_can('manage_options')) wp_die('Unauthorized');

    $slug = isset($_POST['slug']) ? sanitize_text_field($_POST['slug']) : '';
    if (empty($slug)) wp_send_json_error('Slug manquant');

    $pages_data = logopsi_get_pages_data();
    $page = null;
    foreach ($pages_data as $p) {
        if ($p['slug'] === $slug) { $page = $p; break; }
    }
    if (!$page) wp_send_json_error('Page non trouvée');

    $existing = get_posts([
        'post_type' => 'page', 'meta_key' => '_logopsi_slug', 'meta_value' => $slug,
        'posts_per_page' => 1, 'post_status' => 'any',
    ]);

    $parent_id = 0;
    if (!empty($page['parent_slug'])) {
        $pp = get_posts([
            'post_type' => 'page', 'meta_key' => '_logopsi_slug', 'meta_value' => $page['parent_slug'],
            'posts_per_page' => 1, 'post_status' => 'any',
        ]);
        if (!empty($pp)) $parent_id = $pp[0]->ID;
    }

    $post_data = [
        'post_title' => wp_strip_all_tags($page['title']),
        'post_name' => sanitize_title(basename($slug)),
        'post_content' => '',
        'post_status' => 'publish',
        'post_type' => 'page',
        'post_parent' => $parent_id,
    ];

    if (!empty($existing)) {
        $post_data['ID'] = $existing[0]->ID;
        $post_id = wp_update_post($post_data);
    } else {
        $post_id = wp_insert_post($post_data);
    }

    update_post_meta($post_id, '_logopsi_slug', $slug);
    wp_send_json_success(['post_id' => $post_id, 'slug' => $slug]);
}

// ============================================================
// AJAX: SAVE IMAGE / RESET / STATUS
// ============================================================

add_action('wp_ajax_logopsi_save_image', function() {
    check_ajax_referer('logopsi_deploy_nonce', 'nonce');
    if (!current_user_can('manage_options')) wp_die('Unauthorized');
    $map = get_option('logopsi_image_map', []);
    $map[sanitize_text_field($_POST['original_url'])] = esc_url_raw($_POST['new_url']);
    update_option('logopsi_image_map', $map);
    wp_send_json_success(['saved' => true]);
});

add_action('wp_ajax_logopsi_reset', function() {
    check_ajax_referer('logopsi_deploy_nonce', 'nonce');
    if (!current_user_can('manage_options')) wp_die('Unauthorized');
    $pages = get_posts(['post_type' => 'page', 'meta_key' => '_logopsi_slug', 'posts_per_page' => -1, 'post_status' => 'any']);
    $deleted = 0;
    foreach ($pages as $p) { wp_delete_post($p->ID, true); $deleted++; }
    wp_send_json_success(['deleted' => $deleted]);
});

add_action('wp_ajax_logopsi_status', function() {
    check_ajax_referer('logopsi_deploy_nonce', 'nonce');
    $deployed = get_posts(['post_type' => 'page', 'meta_key' => '_logopsi_slug', 'posts_per_page' => -1, 'post_status' => 'publish', 'fields' => 'ids']);
    wp_send_json_success(['deployed' => count($deployed), 'total' => count(logopsi_get_pages_data())]);
});

// ============================================================
// ADMIN PAGE: MAIN DASHBOARD
// ============================================================

function logopsi_admin_page() {
    $pages_data = logopsi_get_pages_data();
    $deployed_pages = get_posts(['post_type' => 'page', 'meta_key' => '_logopsi_slug', 'posts_per_page' => -1, 'post_status' => 'any', 'fields' => 'ids']);
    $deployed_slugs = [];
    foreach ($deployed_pages as $pid) {
        $s = get_post_meta($pid, '_logopsi_slug', true);
        $deployed_slugs[$s] = $pid;
    }

    $groups = [];
    foreach ($pages_data as $p) {
        $parts = explode('/', $p['slug']);
        $group = isset($parts[0]) ? $parts[0] : 'accueil';
        $labels = ['accueil' => 'Accueil', 'orthophonie' => 'Orthophonie', 'psychologie' => 'Psychologie', 'soutien-scolaire' => 'Soutien Scolaire'];
        $group = isset($labels[$group]) ? $labels[$group] : ucfirst($group);
        $groups[$group][] = $p;
    }
    ?>
    <div class="wrap logopsi-wrap">
        <h1><span class="dashicons dashicons-upload" style="font-size:30px;margin-right:10px;color:#05C86B;"></span> Logopsi Studios Deployer</h1>
        <div class="logopsi-stats">
            <div class="logopsi-stat-card"><div class="logopsi-stat-number"><?php echo count($pages_data); ?></div><div class="logopsi-stat-label">Pages totales</div></div>
            <div class="logopsi-stat-card"><div class="logopsi-stat-number" style="color:#05C86B;"><?php echo count($deployed_slugs); ?></div><div class="logopsi-stat-label">Pages déployées</div></div>
            <div class="logopsi-stat-card"><div class="logopsi-stat-number" style="color:#e67e22;"><?php echo count($pages_data) - count($deployed_slugs); ?></div><div class="logopsi-stat-label">En attente</div></div>
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
            <div class="logopsi-progress-bar"><div class="logopsi-progress-fill" id="logopsi-progress-fill"></div></div>
            <p id="logopsi-progress-text">Déploiement en cours...</p>
        </div>
        <div id="logopsi-result" style="display:none;" class="notice notice-success"><p id="logopsi-result-text"></p></div>
        <?php foreach ($groups as $group_name => $group_pages): ?>
        <div class="logopsi-group">
            <h2 class="logopsi-group-title"><?php echo esc_html($group_name); ?> <span class="logopsi-group-count">(<?php echo count($group_pages); ?>)</span></h2>
            <table class="wp-list-table widefat fixed striped"><thead><tr><th style="width:30px;">Status</th><th>Titre</th><th>Slug</th><th style="width:100px;">Action</th></tr></thead><tbody>
                <?php foreach ($group_pages as $p): $is_deployed = isset($deployed_slugs[$p['slug']]); ?>
                <tr>
                    <td><?php echo $is_deployed ? '<span class="dashicons dashicons-yes-alt" style="color:#05C86B;"></span>' : '<span class="dashicons dashicons-clock" style="color:#ccc;"></span>'; ?></td>
                    <td><strong><?php echo esc_html($p['title']); ?></strong></td>
                    <td><code>/<?php echo esc_html($p['slug']); ?>/</code></td>
                    <td><button class="button button-small logopsi-deploy-single" data-slug="<?php echo esc_attr($p['slug']); ?>"><?php echo $is_deployed ? 'Re-push' : 'Push'; ?></button></td>
                </tr>
                <?php endforeach; ?>
            </tbody></table>
        </div>
        <?php endforeach; ?>
    </div>
    <?php
}

// ============================================================
// ADMIN PAGE: IMAGES
// ============================================================

function logopsi_images_page() {
    $pages_data = logopsi_get_pages_data();
    $image_map = get_option('logopsi_image_map', []);
    $all_images = [];
    foreach ($pages_data as $p) {
        foreach ($p['images'] as $img) {
            if (!isset($all_images[$img])) $all_images[$img] = ['url' => $img, 'pages' => []];
            $all_images[$img]['pages'][] = $p['slug'];
        }
    }
    ?>
    <div class="wrap logopsi-wrap">
        <h1><span class="dashicons dashicons-format-image" style="font-size:30px;margin-right:10px;color:#05C86B;"></span> Gestion des images</h1>
        <p>Remplacez les images Unsplash par vos propres images.</p>
        <table class="wp-list-table widefat fixed striped"><thead><tr><th style="width:80px;">Aperçu</th><th>URL originale</th><th>URL de remplacement</th><th style="width:60px;">Pages</th><th style="width:200px;">Actions</th></tr></thead><tbody>
            <?php foreach ($all_images as $img_url => $img_data): $mapped = isset($image_map[$img_url]) ? $image_map[$img_url] : ''; ?>
            <tr>
                <td><img src="<?php echo esc_url($mapped ? $mapped : $img_url); ?>" style="width:60px;height:40px;object-fit:cover;border-radius:4px;"></td>
                <td><small style="word-break:break-all;"><?php echo esc_html($img_url); ?></small></td>
                <td><input type="text" class="logopsi-img-input regular-text" data-original="<?php echo esc_attr($img_url); ?>" value="<?php echo esc_attr($mapped); ?>" placeholder="Collez une URL ou utilisez le bouton" style="width:100%;"></td>
                <td><span class="logopsi-badge"><?php echo count($img_data['pages']); ?></span></td>
                <td>
                    <button class="button logopsi-img-upload" data-original="<?php echo esc_attr($img_url); ?>"><span class="dashicons dashicons-upload" style="vertical-align:middle;"></span> Choisir</button>
                    <button class="button logopsi-img-save" data-original="<?php echo esc_attr($img_url); ?>"><span class="dashicons dashicons-saved" style="vertical-align:middle;"></span></button>
                </td>
            </tr>
            <?php endforeach; ?>
        </tbody></table>
    </div>
    <?php
}
