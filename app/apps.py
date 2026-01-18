from django.apps import AppConfig

class AppConfigCustom(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from .models import AdminUser

        if not AdminUser.objects.filter(username="huzaifa").exists():
            user = AdminUser(username="huzaifa", is_active=True)
            user.set_password("Huzaifa")
            user.save()
