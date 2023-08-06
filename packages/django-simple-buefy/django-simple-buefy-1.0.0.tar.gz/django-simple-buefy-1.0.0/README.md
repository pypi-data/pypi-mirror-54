django-simple-buefy
===================

[![Build Status](https://dev.azure.com/comect/Comect/_apis/build/status/Django%20Simple%20Buefy?branchName=master)](https://dev.azure.com/comect/Comect/_build/latest?definitionId=2&branchName=master)

This project aims to provide an easy, automatic way to include 
[Buefy](https://buefy.org/), [Bulma](https://bulma.io/) and 
[Vue](https://vuejs.org/) alongside your Django project.

This project currently make use of **VERSIONS**. If you need something
in a newer version of these libraries, please feel free to
[create an issue](https://github.com/comect/django-simple-buefy/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc)
and we'll get around to it when we can.

This project is a direct fork of Python Discord's excellent
[django-simple-bulma](https://github.com/python-discord/django-simple-bulma)
project, and it therefore has many similarities with it. Big thanks to
the [Python Discord](https://pythondiscord.com) team for their work on 
that project!

Setup
=====

To get `django-simple-buefy` up and running for your Django project, 
follow these simple steps:

1. Install it via Pip (`pip install django-simple-buefy`) or other dependency
   management tool
2. In your `settings.py` file:
   * Add `django_simple_buefy` to your `INSTALLED_APPS`
   * Add `django_simple_buefy.finders.SimpleBuefyFinder` to your `STATICFILES_FINDERS`
3. Run `python manage.py collectstatic` in order to build and collect all of
   the assets handled by `django-simple-buefy`; please note that you'll need to do
   this again when you change your `django-simple-buefy` configuration
4. In your templates, load `django_simple_buefy` to make use of its template tags:
   * `{% buefy %}` placed in your template's `<head>` will insert script and link tags
     for the files `django-simple-buefy` provides
5. Create your Vue app and get hacking!

Please note that unlike `django-simple-bulma`, `django-simple-buefy` does not provide
any icon sets. Buefy recommends [Material Design Icons](https://materialdesignicons.com/),
but [Font-Awesome 5](https://fontawesome.com/) is also fully compatible.

Customisation
=============

Like `django-simple-bulma`, this project supports customisation of the SASS variables
that are used by Bulma and Buefy. You can do this in a similar fashion, by creating
the `BUEFY_SETTINGS` dictionary within your `setup.py`.

```python
BUEFY_SETTINGS = {
    "variables": {
        "primary": "#000",
        "size-1": "6rem"
    }
}
```

All values must be valid SASS or CSS. For more information on the variables you
can customise, please see [the Buefy documentation](https://buefy.org/documentation/customization/).

Additional SCSS Files
=====================

If your project also includes additional SCSS files, you may specify them in your
`settings.py` file in a similar manner.

```python
BUEFY_SETTINGS = {
    "custom_scss": [
        "myapp/static/css/base/base.scss",
    ],
}
```

**Please note**: The default Django behavior when collecting static files is to keep 
the containing file structure for them when they're copied over to the final static 
files directory. We attempt to do the same thing by parsing the given path to your 
`.scss` file, using the following strategy:

* If a containing path exists in the `STATICFILES_DIRS` setting, assume that this 
  is the base path to use, and the directory structure below it will be used to 
  contain the resulting `.css` file
* Otherwise, if the path contains `static/`, assume that the base path ends there 
  and use the rest of the path below it to contain the resulting `.css` file.

If both of these strategies fail to figure out what base path to use, an exception will be raised.

Troubleshooting
===============

1. If you have the Python module `sass` installed, please note that it is incompatible
   with this project. There is a namespace conflict between `sass` and `libsass` which
   will make `django-simple-buefy` crash when you attempt to do a `collectstatic`. To
   solve this, just uninstall `sass` and use `libsass` instead.
2. If you're having trouble getting your Vue apps and components correctly, remember to
   double-check that Buefy has been loaded in advance of your own JavaScript being loaded.

If you run into any other problems with this app, please 
[create an issue](https://github.com/comect/django-simple-buefy/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc)
and we'll be happy to help you out.
