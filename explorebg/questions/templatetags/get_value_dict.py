from django.template.defaulttags import register


@register.filter
def get_value(dd, key):
    return dd.get(key)
