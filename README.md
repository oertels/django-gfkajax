# About

"gfkajax" = "Generic Foreign Keys with Ajax". Inspired by [django-genericadmin](http://code.google.com/p/django-genericadmin/) (which does not work here, unfortunately).

# Installation

Install gfkajax and add gfkajax to INSTALLED_APPS. 

In your root urls.py, add this line:

    (r'^gfkajax/', include('gfkajax.urls')),


# Usage
Create an admin.py as usual, and then change the ModelAdmin-class like this:


    from gfkajax.forms import make_GfkAjaxForm
    
    class FooAdmin(admin.ModelAdmin):
        form = make_GfkAjaxForm()
        [..]


You may pass gfkajax a whitelist containing allowed content types, in format "app_name.modelname_". The Admin form could look like this then:

    from gfkajax.forms import make_GfkAjaxForm

    class FooAdmin(admin.ModelAdmin):
        form = make_GfkAjaxForm(
            whitelist = [
                'myapp.mymodel_lowercased'
                'myappsecondapp.mysecondmodel_lowercased',
            ]
        )
        [..]
        
        
# Advanced usage

You can tell gfkajax how to render selected objects. This is useful, if you offer e.g. images or videos as generic relations.

To do so, just add a "gfk_render()" method to your model, like:
 
 
 
    class MyModel(models.Model):
        def gfk_render(self):
            return u'%s&nbsp;<img src="myimage.jpg" />&nbsp;' % self.mytitle

If your form needs additional fields, you can pass them as.. "additional_fields":

        form = make_GfkAjaxForm(
            whitelist = [
                'myapp.mymodel_lowercased'
                'myappsecondapp.mysecondmodel_lowercased',
            ],
            additional_fields=[
                'my_field': AutoCompleteSelectMultipleField('foo', required=False)
            ],
        )
        [..]

# Todo

* Related objects must be removable
* Make translatable
* Add example project

