$ = django.jQuery;

var GFK_{{ name }} = {

    init: function() {
        // Hide original fields, and complete rows
        $(".form-row:has(.gfkhidden)").hide();
        $(".column").has(".gfkhidden").hide(); // For grappelli
        $(".column").has(".gfkhidden").prev().hide(); // For grappelli
        $("#id_{{ name }}").hide();

        // Correct lookup node id
        $('#lookup_id_{{ name }}').attr('id', 'lookup_' + GFK_{{ name }}.get_fk_field().attr('id'));

        // If our widget changed the content type, copy new value to original value
        $(".gfk_widget_{{ name }}").change(function() {

            // Set original CT-field to valid value
            bits = GFK_{{ name }}.get_ct_split();
            $('#id_{{ name }}').val(bits[0]);

            // Set FK-value to nothing
            GFK_{{ name }}.set_fk_value('');

            // Set lookup-button to correct href
            GFK_{{ name }}.update_lookup_button();

        });

        // Initially, retrieve object rendering and set lookup target
        GFK_{{ name }}.update_object();
        GFK_{{ name }}.update_lookup_button();

        window.setInterval("GFK_{{ name }}.monitor()", 2000);

    },

    update_lookup_button: function() {
        bits = GFK_{{ name }}.get_ct_split();
        url = '/admin/' + bits[1] + '/' + bits[2] + '/?t=id';
        fk_field_id = GFK_{{ name }}.get_fk_field().attr('id');

        f = $('#lookup_'+fk_field_id);
        f.attr('href', url);
    },

    monitor: function() {
        GFK_{{ name }}.update_object();
    },

    get_fk_field: function() {
        field_name = $('#id_{{ name }}_value');
        field_instance = $('#id_' + field_name.val());
        return field_instance;
    },


    /*
     * Since the ct-format is is_appname_model, return a splitted version
     */
    get_ct_split: function() {
        return $(".gfk_widget_{{ name }}").val().split('_');
    },

    /*
     * Set hidden fk field and update object string
     */
    set_fk_value: function(v) {

        // Set value field to new value
        f = GFK_{{ name }}.get_fk_field();
        f.val(v);
        GFK_{{ name }}.update_object();
    },

    /*
     * Fetch object via ajax request and display as string
     */
    update_object: function() {

        params = {
            'ct': $('#id_{{ name }}').val(),
            'fk': GFK_{{ name }}.get_fk_field().val()
        };

        $.post('/gfkajax/', params, function(data) {
            $('#gfk_{{ name }}_display').html(data);
        });

    }
};

$(document).ready(function() {
   GFK_{{ name }}.init();

});

