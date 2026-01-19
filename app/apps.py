from django.apps import AppConfig

class AppConfigCustom(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from django.contrib.auth.models import User

        try:
            if not User.objects.filter(username="huzaifa").exists():
                User.objects.create_superuser(
                    username="huzaifa",
                    email="hujuhujju729@gmail.com",
                    password="Huzaifa@123"
                )
                print("✅ Superuser created")
        except Exception as e:
            print("❌ Superuser not created:", e)
