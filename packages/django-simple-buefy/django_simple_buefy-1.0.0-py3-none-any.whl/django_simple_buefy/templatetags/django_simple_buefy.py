"""
Template tags loaded in by the Django
templating engine when {% load django_simple_buefy %}
is called.
"""

from pathlib import Path

from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.safestring import mark_safe

register = template.Library()
simple_buefy_path = Path(__file__).resolve().parent.parent
js_folder = simple_buefy_path / "js"


@register.simple_tag
def buefy():
    """
    Build and return all the HTML required to import buefy, bulma and vue.
    """

    # Build the html to include the stylesheet
    css = static("css/buefy.css")
    html = [f'<link rel="stylesheet" href="{css}">']

    # Build html to include all the js files required.
    for filename in js_folder.iterdir():
        js_file = static(f"js/{filename.name}")
        html.append(f'{" " * 8}<script type="text/javascript" src="{js_file}"></script>')

    return mark_safe("\n".join(html))  # noqa
