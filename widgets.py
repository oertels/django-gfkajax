# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.template import loader, Context
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

def safe_int(i):
    """
    Take a parameter and try to convert it to an integer. Return a 0 if it's
    not possible.
    """
    try:
        return int(i)
    except (ValueError, TypeError):
        return 0

class GfkCtWidget(forms.TextInput):

    def __init__(self, *args, **kwargs):
        self.whitelist = kwargs.pop('whitelist', [])
        self.unique_form_id = kwargs.pop('unique_form_id', '')

        super(GfkCtWidget, self).__init__(*args, **kwargs)

    def _get_js_code(self):
        """
        Render javascript-code for widget
        """
        t = loader.get_template('gfkajax/widget.js')
        c = Context({
            'unique_form_id': self.unique_form_id,
            'name': self.name,
            'name_clean': self.name.replace('-','_'),
            'value': self.value,
        })
        return t.render(c)


    def _get_ct_verbose_name(self, content_type):
        """
        Returns a preferrably verbose name for content type
        """
        model_class = content_type.model_class()

        if hasattr(model_class._meta, 'verbose_name') \
            and model_class._meta.verbose_name != '':
                return model_class._meta.verbose_name
        else:
            return unicode(content_type.name)

    def render(self, name, value, attrs=None):

        style = attrs.get('style', '')
        style += ' display:none;'

        cls = attrs.get('class', '')
        cls += ' gfk_%s_ct' % self.unique_form_id
        attrs.update({'style': style, 'class': cls})
        ret = super(GfkCtWidget, self).render(name, value, attrs)

        self.name = name
        self.value = value
        self.attrs = attrs

        # First, add filtered droplist-list containing content type to output
        ctypes = ContentType.objects.all()
        options = ['<option value="">-- select --</option>']

        for c in ctypes:
            if self.whitelist and \
                not '%s.%s' % (c.app_label, c.model) in self.whitelist:
                    continue

            sel = u''

            if safe_int(c.pk) == safe_int(value):
                sel = u' selected'

            if hasattr(c, 'model_class') and c.model_class() is not None:
                options.append(u'<option %s value="%s">%s</option>' % (
                    sel,
                    (u'%s_%s_%s' % (c.pk, c.app_label, c.model_class().__name__.decode('utf-8'))).lower(), # Build id-string: id_appname_modelname
                    self._get_ct_verbose_name(c)
                ))
        options_str = '    \n'.join(options)

        # Append Content-Type selectbox
        ret += u'<select class="gfk_%(unique_form_id)s_input" size="1">%(options)s</select>' % ({
            'unique_form_id': self.unique_form_id,
            'options': options_str
        })


        # Append lookup-button
        ret += u'<a href="%s" class="%s" id="id_%s" onclick="return showRelatedObjectLookupPopup(this);"><img src="%simg/admin/selector-search.gif" style="margin-left:4px;" width="16" height="16"></a>' % (
            '#',
            'gfk_%s_lookup' % self.unique_form_id,
            'lookup_gfk_%s_fk' % self.unique_form_id,
            settings.ADMIN_MEDIA_PREFIX
        )

        # Append div for object display
        ret += u'<div class="gfk_%s_display" style="margin-left:8px;display: inline;"></div>' % (
            self.unique_form_id
        )

        # Append widget js-code
        ret += '<script type="text/javascript">%s</script>' % self._get_js_code()
        return mark_safe(ret)

class GfkFkWidget(forms.TextInput):

    def __init__(self, *args, **kwargs):
        self.input_name = kwargs.pop('append_input_name', '')
        self.input_value = kwargs.pop('append_input_value', '')
        self.unique_form_id = kwargs.pop('unique_form_id', '')

        super(GfkFkWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):

        cls = attrs.get('class', '')
        cls += ' gfk_%s_fk' % self.unique_form_id
        attrs.update({'class': cls})

        ret = super(GfkFkWidget, self).render(name, value, attrs)

        # Append info field
#        ret += u'<input type="hidden" name="%(name)s" id="id_%(name)s" value="%(value)s" />' % ({
#            'name': self.input_name,
#            'value': self.input_value
#        })
        return mark_safe(ret)#

