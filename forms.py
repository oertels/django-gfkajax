from django import forms
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from gfkajax.widgets import GfkCtWidget, GfkFkWidget

def make_GfkAjaxForm(whitelist=None):
    """
    Form factory, needed because we have to pass the whitelist to
    the widget.
    """
    class GfkAjaxForm(forms.ModelForm):

        def __init__(self, *args, **kwargs):
            super(GfkAjaxForm, self).__init__(*args, **kwargs)
            obj = getattr(self, 'instance', None)

            ATTRS_HIDDEN = {'class': 'hidden'}

            gfk_fields = []

            virtual_fields = getattr(obj.__class__._meta, 'virtual_fields', [])
            for virtual_field  in virtual_fields:
                if isinstance(virtual_field, GenericForeignKey):

                    ct_field_obj = getattr(
                        obj.__class__, virtual_field.ct_field, None
                    )

                    gfk_fields.append({
                        'verbose_name': getattr(ct_field_obj.field, 'verbose_name'),
                        'ct_field': {
                            'name': virtual_field.ct_field,
                            'value': getattr(obj, virtual_field.ct_field)
                        },
                        'fk_field': {
                            'name': virtual_field.fk_field,
                            'value': getattr(obj, virtual_field.fk_field)
                        }
                    })

            self.gfk_fields = gfk_fields

            # Now replace widgets
            for field in gfk_fields:

                self.fields[field['ct_field']['name']].widget = GfkCtWidget(
                    whitelist=whitelist
                )
                self.fields[field['ct_field']['name']].label = field['verbose_name']

                self.fields[field['fk_field']['name']].widget = GfkFkWidget(
                    attrs=ATTRS_HIDDEN,
                    append_input_name = u'%s_value' % field['ct_field']['name'],
                    append_input_value = field['fk_field']['name'],
                )
                self.fields[field['fk_field']['name']].label = ''
    return GfkAjaxForm

