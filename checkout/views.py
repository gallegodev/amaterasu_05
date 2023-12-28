from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents

import stripe


def checkout(request):
    stripe_public_key = "pk_live_51OJbrRHh9GY1eZx3ZikENdUFRAsQLE7TWpvkJYY3OgzUQ9U2hoHuyzbgSQVV6IHP3tZIytbZqOycsENndMBrm6QO00bd63mmNP"
    stripe_secret_key = "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"

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)