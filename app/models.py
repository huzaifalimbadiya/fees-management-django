from django.db import models

# Create your models here.

class AdminUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=200)  
    full_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


#  Student model
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    admission_no = models.CharField(max_length=50, unique=True)
    student_class = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    previous_institute = models.CharField(max_length=150)
    admission_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.surname}"




# Fees model
class Fees(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_fees = models.IntegerField()
    paid_amount = models.IntegerField()
    remaining_amount = models.IntegerField(blank=True, null=True)
    last_paid_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        self.remaining_amount = self.total_fees - self.paid_amount

        if self.remaining_amount == 0:
            self.status = "Paid"
        elif self.paid_amount == 0:
            self.status = "Pending"
        else:
            self.status = "Partial"

        super().save(*args, **kwargs)






# new user and pasword
from django.apps import AppConfig

class AppConfigCustom(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from django.contrib.auth.models import User
        import os

        username = os.environ.get("DJANGO_ADMIN_USER", "admin")
        password = os.environ.get("DJANGO_ADMIN_PASS", "admin12345")
        email = os.environ.get("DJANGO_ADMIN_EMAIL", "admin@example.com")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            print("✅ Superuser created automatically")
