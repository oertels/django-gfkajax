from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from gfkajax.forms import make_GfkAjaxForm


class GfkAjaxAdmin(admin.ModelAdmin):

    form = make_GfkAjaxForm()

#def register(site):
#    from genericforeignkey.admin_register import GenericContentTypeAdmin
#    site.register(ContentType, GenericContentTypeAdmin)
