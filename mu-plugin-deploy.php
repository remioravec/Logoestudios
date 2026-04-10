<?php
/**
 * Plugin Name: Logopsi Deploy API
 * Description: Custom REST endpoint for deploying pages remotely
 */

add_action('rest_api_init', function() {
    register_rest_route('logopsi/v1', '/ping', [
        'methods'  => 'POST',
        'callback' => 'logopsi_ping',
        'permission_callback' => 'logopsi_check_key',
    ]);
    register_rest_route('logopsi/v1', '/create-page', [
        'methods'  => 'POST',
        'callback' => 'logopsi_create_page',
        'permission_callback' => 'logopsi_check_key',
    ]);
    register_rest_route('logopsi/v1', '/list-pages', [
        'methods'  => 'POST',
        'callback' => 'logopsi_list_pages',
        'permission_callback' => 'logopsi_check_key',
    ]);
});

function logopsi_check_key($request) {
    $key = $request->get_header('X-Deploy-Key');
    return $key === 'logopsi-deploy-2026-secure-key';
}

function logopsi_ping($request) {
    return new WP_REST_Response([
        'success'    => true,
        'message'    => 'Deploy endpoint ready',
        'wp_version' => get_bloginfo('version'),
    ]);
}

function logopsi_create_page($request) {
    $body = $request->get_json_params();

    if (empty($body['title']) || empty($body['content'])) {
        return new WP_REST_Response(['success' => false, 'error' => 'Missing title or content'], 400);
    }

    wp_set_current_user(1);

    $page_id = wp_insert_post([
        'post_title'   => sanitize_text_field($body['title']),
        'post_content' => $body['content'],
        'post_name'    => isset($body['slug']) ? sanitize_title($body['slug']) : '',
        'post_excerpt' => isset($body['excerpt']) ? sanitize_textarea_field($body['excerpt']) : '',
        'post_parent'  => isset($body['parent_id']) ? absint($body['parent_id']) : 0,
        'post_status'  => isset($body['status']) ? sanitize_text_field($body['status']) : 'draft',
        'post_type'    => 'page',
    ], true);

    if (is_wp_error($page_id)) {
        return new WP_REST_Response([
            'success' => false,
            'error'   => $page_id->get_error_message(),
        ], 500);
    }

    $page = get_post($page_id);

    return new WP_REST_Response([
        'success' => true,
        'page_id' => (int) $page_id,
        'slug'    => $page->post_name,
    ]);
}

function logopsi_list_pages($request) {
    $pages = get_pages(['sort_column' => 'post_title', 'post_status' => 'any']);
    $result = [];
    foreach ($pages as $p) {
        $result[] = [
            'id'        => (int) $p->ID,
            'title'     => $p->post_title,
            'slug'      => $p->post_name,
            'parent_id' => (int) $p->post_parent,
            'status'    => $p->post_status,
        ];
    }
    return new WP_REST_Response(['success' => true, 'count' => count($result), 'pages' => $result]);
}
