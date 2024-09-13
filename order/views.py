import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
import stripe
from django.conf import settings
from .models import *

from cart.cart import Cart
# Create your views here.



def start_order(request):
    cart = Cart(request)
    data = json.loads(request.body)
    total_price = 0

    items = []

    for item in cart:
        product = item['product']
        quantity = int(item['quantity'])
        price_in_cents = int(product.price * 100)  # Convert dollars to cents
        total_price += price_in_cents * quantity

        items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.title,
                },
                'unit_amount': price_in_cents,  # Amount in cents
            },
            'quantity': quantity
        })

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items,
            mode='payment',
            success_url='http://127.0.0.1:8000/cart/success/',
            cancel_url='http://127.0.0.1:8000/cart/'
        )
    except stripe.error.InvalidRequestError as e:
        return JsonResponse({'error': str(e)}, status=400)

    payment_intent = session.payment_intent

    order = Order.objects.create(
        user=request.user, 
        first_name=data.get('first_name'), 
        last_name=data.get('last_name'), 
        email=data.get('email'), 
        phone=data.get('phone'), 
        address=data.get('address'), 
        zip_code=data.get('zip_code'), 
        place=data.get('place'),

        paid=True,
        paid_amount=total_price / 100  # Store amount in dollars
    )

    for item in cart:
        product = item['product']
        quantity = int(item['quantity'])
        price = int(product.price * 100)  # Price in cents
        total_price_item = price * quantity

        OrderItem.objects.create(order=order, product=product, price=total_price_item / 100, quantity=quantity)

    cart.clear()

    return JsonResponse({'session_id': session.id, 'payment_intent': payment_intent})