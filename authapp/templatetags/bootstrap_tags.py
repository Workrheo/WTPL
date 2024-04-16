from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})

@register.filter
def add_name(field, atrname):
    return field.as_widget(attrs={'name': atrname})

@register.filter
def mul(value, arg):
    return value * arg

@register.filter(name='attr')
def attr(field, attribute):
    attr_name, attr_value = attribute.split('=') 
    attrs = {attr_name: attr_value}
    return field.as_widget(attrs=attrs)

@register.filter
def stars_range(value):
    return range(value)