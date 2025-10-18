from django import template
from django.urls import reverse
from maestro.settings import MENU_REGISTRY

register = template.Library()

@register.simple_tag(takes_context=True)
def get_menu(context):
    """
        Returns the consolidated sidebar menu (base + optional extra items).

        Args:
            context (dict): Template context, may contain `SIDEBAR_EXTRA`.

        Returns:
            dict: Full menu structure ready for rendering.
    """
    extra = context.get("SIDEBAR_EXTRA") or {}
    menu = {**MENU_REGISTRY, **extra}
    for _, item in menu.items():
        item["submenu"] = {
            label: (url if url.startswith("/") else reverse(url))
            for label, url in item.get("submenu", {}).items()
        }
    return menu
