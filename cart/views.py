from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse

from .cart import Cart

from product.models import Product

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return render(request, 'cart/partials/menu_cart.html')


@login_required
def cart(request):
    return render(request, 'cart/cart.html')



def update_cart(request, product_id, action):
    cart = Cart(request)

    # Update the cart based on the action
    if action == 'increment':
        cart.add(product_id, 1, True)
    elif action == 'decrement':
        cart.add(product_id, -1, True)

    # After updating the cart, redirect back to the cart page to fully reload it
    return redirect('cart:cart')






@login_required
def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE 
    return render(request, 'cart/checkout.html', {'pub_key': pub_key})



import logging

logger = logging.getLogger(__name__)

@login_required
def hx_menu_cart(request):
    logger.debug("Rendering menu_cart.html")
    return render(request, 'cart/partials/menu_cart.html')

@login_required
def hx_cart_total(request):
    logger.debug("Rendering cart_total.html")
    return render(request, 'cart/partials/cart_total.html')





def success(request):
    return render(request, 'cart/success.html')




