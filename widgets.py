from django.conf import settings
from django import forms
from django.template import loader, Context
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType


class GfkCtWidget(forms.TextInput):

    def __init__(self, *args, **kwargs):
        self.whitelist = kwargs.pop('whitelist', '')

        super(GfkCtWidget, self).__init__(*args, **kwargs)

    def _get_js_code(self):
        """
        Render javascript-code for widget
        """
        t = loader.get_template('gfkajax/widget.js')
        c = Context({
            'name': self.name,
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
                return unicode(model_class._meta.verbose_name)
        else:
            return content_type.name

    def render(self, name, value, attrs=None):

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
            if c.pk == value:
                sel = u' selected'
            options.append('<option %s value="%s">%s</option>' % (
                sel,
                ('%s_%s_%s' % (c.pk, c.app_label, c.model_class().__name__)).lower(), # Build id-string: id_appname_modelname
                self._get_ct_verbose_name(c)
            ))
        options_str = '    \n'.join(options)

        # Append Content-Type selectbox
        ret += u'<select class="gfk_widget_%(name)s" size="1" id="gfk_%(name)s">%(options)s</select>' % ({
            'name': name,
            'options': options_str
        })

        # Append lookup-button
        ret += u'<a href="%s" id="%s" onclick="return showRelatedObjectLookupPopup(this);"><img src="%simg/admin/selector-search.gif" style="margin-left:4px;" width="16" height="16"></a>' % (
            '#',
            'lookup_id_%s' % name,
            settings.ADMIN_MEDIA_PREFIX
        )

        # Append div for object display
        ret += u'<div class="gfk_display_object" id="gfk_%s_display" style="margin-left:8px;display: inline;"></div>' % (
            name,
        )

        # Append widget js-code
        ret += '<script type="text/javascript">%s</script>' % self._get_js_code()
        return mark_safe(ret)

class GfkFkWidget(forms.TextInput):

    def __init__(self, *args, **kwargs):
        self.input_name = kwargs.pop('append_input_name', '')
        self.input_value = kwargs.pop('append_input_value', '')
        super(GfkFkWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):

        ret = super(GfkFkWidget, self).render(name, value, attrs)

        # Append info field
        ret += u'<input type="hidden" name="%(name)s" id="id_%(name)s" value="%(value)s" />' % ({
            'name': self.input_name,
            'value': self.input_value
        })
        return mark_safe(ret)#

