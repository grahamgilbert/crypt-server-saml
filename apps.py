from django.apps import AppConfig


class ServerAppConfig(AppConfig):
    name = "server"

    def ready(self):
        import server.signals