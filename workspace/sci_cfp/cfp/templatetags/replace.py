from django import template

register = template.Library()

@register.filter
def replace_social_img(value):
    return value.replace(".png", "_sc.png")
