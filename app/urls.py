from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("home/", views.home, name="home"),
    path("add-student/", views.add_student, name="add_student"),
    path("students/", views.student_list, name="student_list"),
    path("add-fees/<int:student_id>/", views.add_fees, name="add_fees"),
    path("delete-student/<int:student_id>/", views.delete_student, name="delete_student"),
    path("fees/", views.fees_students, name="fees_students"),
    path("edit-student/<int:student_id>/", views.edit_student, name="edit_student"),




]
