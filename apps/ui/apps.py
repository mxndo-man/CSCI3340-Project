from django.apps import AppConfig


class UiConfig(AppConfig):
    """The shared UI pieces every page uses: the {% load ui %} helpers and the style guide.

    No models. Unlike apps.ui_preview, this app stays when the preview goes away.
    """

    name = "apps.ui"
    verbose_name = "UI"
