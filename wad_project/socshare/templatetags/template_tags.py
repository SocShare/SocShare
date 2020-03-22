from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def get_search_bar():
    return mark_safe("<div class=\"input-group mb-3\"><div class=\"input-group-prepend\"><span class=\"input-group-text\"><i class=\"fas fa-search\"></i></span></div><input type=\"text\" class=\"form-control\" placeholder=\"Search\"></div>")