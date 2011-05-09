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
        
        
