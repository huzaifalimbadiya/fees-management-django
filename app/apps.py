def ready(self):
    from .models import AdminUser

    user, created = AdminUser.objects.get_or_create(
        username="huzaifa",
        defaults={"is_active": True}
    )

    user.set_password("huzaifa")   # 🔥 hamesha password update hoga
    user.is_active = True
    user.save()
