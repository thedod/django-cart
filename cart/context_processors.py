from django.conf import settings
from cart import Cart

def cart(request):
    "Supplies cart-related context variables"
    return { 'CART': Cart(request) }
