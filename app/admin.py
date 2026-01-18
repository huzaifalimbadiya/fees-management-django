from django.contrib import admin
from .models import AdminUser, Student, Fees

# Register your models here.



admin.site.register(AdminUser)
admin.site.register(Student)
admin.site.register(Fees)