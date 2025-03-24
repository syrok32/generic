import stripe
from django.conf import settings
from dotenv import load_dotenv
import os
load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


def create_stripe_product(payment):
    product = stripe.Product.create(name=f"Курс: {payment.paid_course.title}")
    return product.id


def create_stripe_price(amount, product_id):
    price = stripe.Price.create(
        unit_amount=int(amount * 100),  # Цена в центах!
        currency="usd",
        product=product_id,
    )
    return price.id


def create_stripe_sessions(price_id):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        success_url="https://your-site.com/success",
        cancel_url="https://your-site.com/cancel",
    )
    return session.id, session.url