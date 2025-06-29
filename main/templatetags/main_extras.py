from django import template
from django.forms.widgets import CheckboxInput, FileInput

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies the value by the argument."""
    try:
        return value * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def range_filter(value):
    """Returns a range from 0 to value."""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)

@register.filter
def repeat(string, times):
    """Repeats a string N times."""
    try:
        return string * int(times)
    except (ValueError, TypeError):
        return string

@register.filter(name='add_class')
def add_class(field, css_class):
    if isinstance(field.field.widget, CheckboxInput):
        return field.as_widget(attrs={'class': f'form-check-input {css_class}'})
    elif isinstance(field.field.widget, FileInput):
        return field.as_widget(attrs={'class': f'form-control {css_class}'})
    return field.as_widget(attrs={'class': css_class}) 