import importlib

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "cohorts"
    label = "cohorts"
    verbose_name = _("Cohorts")

    def ready(self):
        importlib.import_module("cohorts.receivers")
