from django.urls import reverse
from .models import Notification, NotificationTemplate


def notify(
    user,
    title: str,
    message: str,
    level="info",
    category="system",
    url: str = "",
    template: NotificationTemplate | None = None,
):
    """
    Création brute d'une notification.
    """
    if user is None:
        return None

    return Notification.objects.create(
        recipient=user,
        template=template,
        title=title,
        message=message,
        level=level,
        category=category,
        url=url or "",
    )


def notify_code(user, code: str, context: dict | None = None, url: str = "", level="info", category="system"):
    """
    Création d'une notification à partir d'un code de template + contexte.

    context = dict pour remplir {variables} dans le titre et le message.
    """
    if user is None:
        return None

    context = context or {}
    try:
        template = NotificationTemplate.objects.get(code=code)
    except NotificationTemplate.DoesNotExist:
        # fallback : on met un titre générique
        title = code
        message = context.get("message", "")
        return notify(user, title, message, level=level, category=category, url=url)

    # On remplace les variables dans le template
    try:
        title = template.title_template.format(**context)
        message = template.body_template.format(**context)
    except KeyError:
        # En cas de variable manquante, on ne plante pas
        title = template.title_template
        message = template.body_template

    return notify(user, title, message, level=level, category=category, url=url, template=template)
