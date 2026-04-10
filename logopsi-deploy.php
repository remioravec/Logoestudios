<?php
/**
 * Logopsi Deploy Endpoint
 *
 * Place this file at the WordPress root directory.
 * It provides a simple API for creating pages remotely.
 */

// Load WordPress
require_once __DIR__ . '/wp-load.php';

// Configuration
define('DEPLOY_API_KEY', 'logopsi-deploy-2026-secure-key');

// Set JSON content type for all responses
header('Content-Type: application/json; charset=utf-8');

/**
 * Send a JSON response and exit.
 */
function deploy_respond($data, $http_code = 200) {
    http_response_code($http_code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

// --- Authentication ---

$provided_key = isset($_SERVER['HTTP_X_DEPLOY_KEY']) ? $_SERVER['HTTP_X_DEPLOY_KEY'] : '';

if ($provided_key !== DEPLOY_API_KEY) {
    deploy_respond(['success' => false, 'error' => 'Forbidden: invalid or missing API key'], 403);
}

// --- Parse request ---

$raw_body = file_get_contents('php://input');
$body = json_decode($raw_body, true);

if (!is_array($body) || empty($body['action'])) {
    deploy_respond(['success' => false, 'error' => 'Invalid request: JSON body with "action" field required'], 400);
}

$action = $body['action'];

// --- Route actions ---

switch ($action) {

    case 'ping':
        deploy_respond([
            'success'    => true,
            'message'    => 'Deploy endpoint ready',
            'wp_version' => get_bloginfo('version'),
        ]);
        break;

    case 'list_pages':
        $pages = get_pages([
            'sort_column' => 'post_title',
            'sort_order'  => 'ASC',
            'post_status' => 'any',
        ]);

        $result = [];
        foreach ($pages as $page) {
            $result[] = [
                'id'        => (int) $page->ID,
                'title'     => $page->post_title,
                'slug'      => $page->post_name,
                'parent_id' => (int) $page->post_parent,
                'status'    => $page->post_status,
            ];
        }

        deploy_respond([
            'success' => true,
            'count'   => count($result),
            'pages'   => $result,
        ]);
        break;

    case 'create_page':
        // Only allow POST
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            deploy_respond(['success' => false, 'error' => 'create_page requires POST method'], 405);
        }

        // Validate required fields
        if (empty($body['title']) || empty($body['content'])) {
            deploy_respond(['success' => false, 'error' => 'Missing required fields: title, content'], 400);
        }

        // Set current user to admin so wp_insert_post has proper permissions
        wp_set_current_user(1);

        $post_data = [
            'post_title'   => sanitize_text_field($body['title']),
            'post_content' => $body['content'],
            'post_name'    => isset($body['slug']) ? sanitize_title($body['slug']) : '',
            'post_excerpt' => isset($body['excerpt']) ? sanitize_textarea_field($body['excerpt']) : '',
            'post_parent'  => isset($body['parent_id']) ? absint($body['parent_id']) : 0,
            'post_status'  => isset($body['status']) ? sanitize_text_field($body['status']) : 'draft',
            'post_type'    => 'page',
        ];

        $page_id = wp_insert_post($post_data, true);

        if (is_wp_error($page_id)) {
            deploy_respond([
                'success' => false,
                'error'   => 'Failed to create page: ' . $page_id->get_error_message(),
            ], 500);
        }

        $created_page = get_post($page_id);

        deploy_respond([
            'success' => true,
            'page_id' => (int) $page_id,
            'slug'    => $created_page->post_name,
        ]);
        break;

    default:
        deploy_respond(['success' => false, 'error' => 'Unknown action: ' . $action], 400);
        break;
}
