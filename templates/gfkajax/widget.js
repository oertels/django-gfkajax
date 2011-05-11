$ = django.jQuery;

var GFK_{{ unique_form_id }} = {

    init: function() {
        // Hide original fields, and complete rows
        $(".form-row:has(.gfk_{{ unique_form_id }}_fk").hide();
        $(".column").has(".gfk_{{ unique_form_id }}_fk").hide(); // For grappelli
        $(".column").has(".gfk_{{ unique_form_id }}_fk").prev().hide(); // For grappelli
        $(".gfk_{{ unique_form_id }}_lookup").attr('id', 'lookup_'+$('.gfk_{{ unique_form_id }}_fk').attr('id'));

        old_fk_val_{{ unique_form_id}} = -1;

        // If our widget changed the content type, copy new value to original value
        $(".gfk_{{ unique_form_id }}_input").change(function() {

            // Set original CT-field to valid value
            bits = GFK_{{ unique_form_id }}.get_ct_split();
            $('.gfk_{{ unique_form_id }}_ct').val(bits[0]);

            // Set FK-value to nothing
            $('.gfk_{{ unique_form_id }}_fk').val('');

            // Set lookup-button to correct href
            GFK_{{ unique_form_id }}.update_lookup_button();

        });

        // Initially, retrieve object rendering and set lookup target
        GFK_{{ unique_form_id }}.update_object();
        GFK_{{ unique_form_id }}.update_lookup_button();

        window.setInterval("GFK_{{ unique_form_id }}.monitor()", 2000);

    },

    update_lookup_button: function() {
        bits = GFK_{{ unique_form_id }}.get_ct_split();
        console.log(bits);
        url = '/admin/' + bits[1] + '/' + bits[2] + '/?t=id';

        $('.gfk_{{ unique_form_id }}_lookup').attr('href', url);
    },

    monitor: function() {
        GFK_{{ unique_form_id }}.update_object();
    },

    /*
     * Since the ct-format is is_appname_model, return a splitted version
     */
    get_ct_split: function() {
        return $(".gfk_{{ unique_form_id }}_input").val().split('_');
    },

    /*
     * Fetch object via ajax request and display as string
     */
    update_object: function() {

        var ct_val = $('.gfk_{{ unique_form_id }}_ct').val();
        var fk_val = $('.gfk_{{ unique_form_id }}_fk').val();

        if ((old_fk_val_{{ unique_form_id }} == -1) || (old_fk_val_{{ unique_form_id }} != fk_val)) {
            old_fk_val_{{ unique_form_id }} = fk_val;
            params = {
                'ct': ct_val,
                'fk': fk_val
            };
            $('.gfk_{{ unique_form_id }}_display').html('Updating...')
            $.post('/gfkajax/', params, function(data) {
                $('.gfk_{{ unique_form_id }}_display').html(data);
            });
        }
    }
};

$(document).ready(function() {
   GFK_{{ unique_form_id }}.init();

});

