
jQuery(document).ready(function($) {

    // Deploy all pages (batch mode)
    $('#logopsi-deploy-all').on('click', function() {
        if (!confirm('Déployer toutes les pages sur WordPress ?')) return;

        var $btn = $(this);
        $btn.prop('disabled', true).text('Déploiement en cours...');
        $('#logopsi-progress').show();
        $('#logopsi-result').hide();

        var totalCreated = 0;
        var totalUpdated = 0;
        var allErrors = [];

        function deployBatch(offset) {
            $.ajax({
                url: logopsiAjax.ajaxurl,
                type: 'POST',
                timeout: 120000,
                data: {
                    action: 'logopsi_deploy',
                    nonce: logopsiAjax.nonce,
                    offset: offset
                },
                success: function(response) {
                    if (response.success) {
                        var d = response.data;
                        totalCreated += d.created;
                        totalUpdated += d.updated;
                        allErrors = allErrors.concat(d.errors);

                        var pct = Math.round((d.processed / d.total) * 100);
                        $('#logopsi-progress-fill').css('width', pct + '%');
                        $('#logopsi-progress-text').text('Déploiement : ' + d.processed + ' / ' + d.total + ' pages (' + pct + '%)');

                        if (d.done) {
                            $('#logopsi-progress-fill').css('width', '100%');
                            $('#logopsi-progress-text').text('Terminé !');
                            $('#logopsi-result').show().removeClass('notice-error').addClass('notice-success');
                            $('#logopsi-result-text').text(
                                totalCreated + ' pages créées, ' + totalUpdated + ' mises à jour. ' +
                                (allErrors.length ? allErrors.length + ' erreur(s).' : 'Aucune erreur.')
                            );
                            if (allErrors.length) console.log('Erreurs:', allErrors);
                            $btn.prop('disabled', false).html('<span class="dashicons dashicons-upload"></span> Déployer tout le site');
                            setTimeout(function() { location.reload(); }, 2000);
                        } else {
                            deployBatch(d.next_offset);
                        }
                    } else {
                        alert('Erreur: ' + response.data);
                        $btn.prop('disabled', false).html('<span class="dashicons dashicons-upload"></span> Déployer tout le site');
                    }
                },
                error: function(xhr, status) {
                    alert('Erreur de connexion (batch offset ' + offset + '). Status: ' + status + '. Vous pouvez relancer le déploiement, il reprendra là où il s\'est arrêté.');
                    $btn.prop('disabled', false).html('<span class="dashicons dashicons-upload"></span> Déployer tout le site');
                }
            });
        }

        deployBatch(0);
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
