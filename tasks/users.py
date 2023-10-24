from celery import shared_task

from common.email import ActivationEmail, ChangePasswordEmail, SetPasswordEmail


@shared_task(bind=True)
def send_activation_email(self, user_pk: int, is_created: bool) -> None:
    """
    Sends signup email
    Args:
        self:
        user_pk(int): ID of User
    """
    from apps.users.models import User

    user = User.objects.get(pk=user_pk)
    context = {"user": user}
    ActivationEmail(context=context).send([user.email])
    if not is_created:
        user.requests_quantity += 1
        user.save()


@shared_task(bind=True)
def send_password_activation(self, user_email: str) -> None:
    """
    Sends changing password email
    Args:
        self:
        user_email(str): email of User
    """
    from apps.users.models import User

    user = User.objects.get(email=user_email)
    context = {"user": user}
    SetPasswordEmail(context=context).send([user.email])
    user.requests_quantity += 1
    user.save()


@shared_task(bind=True)
def send_email_confirmation(self, user_pk: int, email: str) -> None:
    """
    Sends changing email request
    Args:
        self:
        user_pk(int): ID of User
        email(str): email:
    """
    from apps.users.models import User

    user = User.objects.get(pk=user_pk)
    context = {"user": user, "email": email}
    ChangePasswordEmail(context=context).send([email])
    user.requests_quantity += 1
    user.save()
