from abc import ABC
from datetime import timedelta
from typing import Dict

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now

from apps.users import constants
from apps.users.models import ActivationCode
from common.utils.uid import encode_uid


class BaseEmail(ABC):
    template_name: str = ""
    subject: str = ""

    def __init__(self, context: dict, request=None):
        self._request = request
        self._context = context
        self._subject = self.get_subject()

    def get_subject(self):
        return self.subject

    def _get_context_data(self) -> Dict:
        context = self._context
        if self._request:
            site = get_current_site(self._request)
            domain = getattr(settings, "DOMAIN", "") or site.domain
            protocol = "https" if self._request.is_secure() else "http"
            site_name = getattr(settings, "SITE_NAME", "") or site.name
            user = self._request.user
        else:
            domain = getattr(settings, "DOMAIN", "")
            protocol = "https"
            site_name = getattr(settings, "SITE_NAME", "")
            user = self._context.get("user")

        context.update(
            {
                "domain": domain,
                "protocol": protocol,
                "site_name": site_name,
                "user": user,
            }
        )
        return context

    def send(self, recipient_list: list) -> None:
        context = self._get_context_data()
        html_message = render_to_string(self.template_name, context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=self._subject,
            message=plain_message,
            from_email=settings.EMAIL_SENDER,
            recipient_list=recipient_list,
            fail_silently=False,
            html_message=html_message,
        )


class ActivationEmail(BaseEmail):
    template_name = "email/activation.html"
    subject = f"Activation account at {settings.SITE_NAME}"

    def _get_context_data(self):
        context = super()._get_context_data()
        user = context.get("user")
        context["uid"] = encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context[
            "url"
        ] = f"{context['protocol']}://{settings.SITE_DOMAIN}/activate?uid={context['uid']}&token={context['token']}"
        return context


class SetPasswordEmail(BaseEmail):
    template_name = "email/password_confirmation.html"
    subject = f"Password change request at {settings.SITE_NAME}"

    def _get_context_data(self):
        context = super()._get_context_data()
        user = context.get("user")
        expire_date = now() + timedelta(days=constants.RESET_PASSWORD_LINK_LIFETIME)
        context["uid"] = encode_uid(f"{user.pk}_{user.requests_quantity}")
        context["token"] = default_token_generator.make_token(user)
        context["url"] = (
            f"{context['protocol']}://{settings.SITE_DOMAIN}"
            f"/reset-password?uid={context['uid']}&token={context['token']}"
        )
        ActivationCode.objects.create(
            user=user,
            uid=context["uid"],
            code=context["token"],
            expiration_date=expire_date,
        )
        return context


class ChangePasswordEmail(BaseEmail):
    template_name = "email/email_confirmation.html"
    subject = f"Email change request at {settings.SITE_NAME}"

    def _get_context_data(self):
        context = super()._get_context_data()
        user = context.get("user")
        expire_date = now() + timedelta(days=constants.RESET_PASSWORD_LINK_LIFETIME)
        context["uid"] = encode_uid(f"{user.pk}_{user.requests_quantity}")
        context["token"] = default_token_generator.make_token(user)
        context["url"] = (
            f"{context['protocol']}://{settings.SITE_DOMAIN}"
            f"/confirm-email?uid={context['uid']}&token={context['token']}"
        )
        ActivationCode.objects.create(
            user=user,
            uid=context["uid"],
            code=context["token"],
            expiration_date=expire_date,
            email=context.get("email"),
        )
        return context
