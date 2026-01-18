from django.apps import AppConfig


class AppConfigCustom(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from .models import AdminUser

        user, created = AdminUser.objects.get_or_create(
            username="huzaifa",
            defaults={"is_active": True}
        )
        user.set_password("Huzaifa")
        user.is_active = True
        user.save()
