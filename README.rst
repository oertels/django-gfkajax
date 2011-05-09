Installation
============

Create an admin.py as usual, and then change the ModelAdmin-class like this:

{{{
#!rst

.. code-block:: python

class PostAdmin(admin.ModelAdmin):
    [..]
    form = make_GfkAjaxForm(
        whitelist = [
            'myapp.mymodel_lowercased'
            'myappsecondapp.mysecondmodel_lowercased',
        ]
    )
    [..]
}}}

Foo