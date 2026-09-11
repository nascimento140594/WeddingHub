import hashlib
import hmac
from decimal import Decimal

import requests
from django.conf import settings


class MercadoPagoError(Exception):
    """Base exception for Mercado Pago integration errors."""


class MercadoPagoConfigurationError(MercadoPagoError):
    """Raised when Mercado Pago credentials are missing."""


class MercadoPagoAPIError(MercadoPagoError):
    """Raised when Mercado Pago rejects an API request."""


def _get_access_token():
    token = getattr(settings, "MERCADO_PAGO_ACCESS_TOKEN", "")

    if not token:
        raise MercadoPagoConfigurationError(
            "MERCADO_PAGO_ACCESS_TOKEN is not configured."
        )

    return token


def _headers():
    return {
        "Authorization": f"Bearer {_get_access_token()}",
        "Content-Type": "application/json",
    }


def create_preference(payment):
    """Create a Mercado Pago Checkout Pro preference."""
    data = {
        "items": [
            {
                "id": str(payment.gift.id),
                "title": payment.gift.name,
                "description": payment.gift.description,
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(payment.amount),
            }
        ],
        "payer": {
            "name": payment.guest_name,
            "email": payment.guest_email,
        },
        "external_reference": str(payment.id),
        "payment_methods": {
            "installments": 12,
        },
    }

    notification_url = getattr(
        settings,
        "MERCADO_PAGO_NOTIFICATION_URL",
        "",
    )
    if notification_url:
        data["notification_url"] = notification_url

    public_base_url = getattr(settings, "PUBLIC_BASE_URL", "").rstrip("/")
    if public_base_url.startswith("https://"):
        data["back_urls"] = {
            "success": f"{public_base_url}/pagamento/sucesso/",
            "pending": f"{public_base_url}/pagamento/pendente/",
            "failure": f"{public_base_url}/pagamento/falhou/",
        }
        data["auto_return"] = "approved"

    response = requests.post(
        "https://api.mercadopago.com/checkout/preferences",
        headers=_headers(),
        json=data,
        timeout=20,
    )

    if not response.ok:
        raise MercadoPagoAPIError(
            f"Mercado Pago returned HTTP {response.status_code}: "
            f"{response.text[:500]}"
        )

    return response.json()


def get_payment(payment_id):
    """Retrieve a payment from Mercado Pago by its payment ID."""
    response = requests.get(
        f"https://api.mercadopago.com/v1/payments/{payment_id}",
        headers=_headers(),
        timeout=20,
    )

    if not response.ok:
        raise MercadoPagoAPIError(
            f"Mercado Pago returned HTTP {response.status_code}: "
            f"{response.text[:500]}"
        )

    return response.json()


def validate_webhook_signature(request, data_id):
    """Validate Mercado Pago's HMAC webhook signature."""
    secret = getattr(settings, "MERCADO_PAGO_WEBHOOK_SECRET", "")
    x_signature = request.headers.get("x-signature", "")
    x_request_id = request.headers.get("x-request-id", "")

    if not secret or not x_signature or not x_request_id or not data_id:
        return False

    parts = {}
    for item in x_signature.split(","):
        key, separator, value = item.strip().partition("=")
        if separator:
            parts[key] = value

    timestamp = parts.get("ts")
    received_signature = parts.get("v1")

    if not timestamp or not received_signature:
        return False

    manifest = (
        f"id:{data_id};"
        f"request-id:{x_request_id};"
        f"ts:{timestamp};"
    )

    expected_signature = hmac.new(
        secret.encode("utf-8"),
        manifest.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(
        expected_signature,
        received_signature,
    )


def normalize_amount(value):
    return Decimal(str(value)).quantize(Decimal("0.01"))
