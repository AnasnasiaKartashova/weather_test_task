from django import template


register = template.Library()


@register.simple_tag
def zip_lists(*args):
    return zip(*args)
