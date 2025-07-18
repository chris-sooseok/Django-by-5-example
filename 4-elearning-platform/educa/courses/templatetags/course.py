from django import template

register = template.Library()
@register.filter
def model_name(obj):
    """
    ? custom filter to be used in templates to retreive model name of content
    """
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
