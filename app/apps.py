from django.apps import AppConfig


class AppConfigCustom(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from .models import AdminUser

        if not AdminUser.objects.filter(username="admin").exists():
            AdminUser.objects.create(
                username="huzaifa",
                password="91Huzaifa",
                is_active=True
            )
