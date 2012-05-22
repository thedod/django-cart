"""
    Example:
        {% include cart_filters %}
        {{ product|cart_product_as_p:CART }}
    In order to have CART,
    you need to add 'cart.context_processors.cart'
    to TEMPLATE_CONTEXT_PROCESSORS
"""
from django import template

register = template.Library()

@register.filter(is_safe=True)
def cart_product_as_p(product,cart):
    return cart.get_product_form(product).as_p()

@register.filter(is_safe=True)
def cart_product_as_ul(product,cart):
    return cart.get_product_form(product).as_ul()
