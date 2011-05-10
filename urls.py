# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'gfkajax.views.get_object', name='gfkajax_get_object'),
)
