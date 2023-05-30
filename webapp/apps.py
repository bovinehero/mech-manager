""" Contains the app config """
# django imports occur at runtime, so fail linter
# pylint:disable=import-error
from django.apps import AppConfig
# pylint:enable=import-error


class WebappConfig(AppConfig):
    """ Deals with the webapp app config """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webapp'
