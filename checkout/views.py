from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51OJbrRHh9GY1eZx3sg152ws6J4C8Zuj2LjYEtxcE6ygS5It8wzk12Zds43LtmTSM9sfRwnUJ1W9Mtow9yaVypWWA00Yq7E6Bkx',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)