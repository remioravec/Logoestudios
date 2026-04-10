
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
