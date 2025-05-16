from django.apps import AppConfig


class ModuleAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module_app'

    def ready(self):
        import module_app.signals
