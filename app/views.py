from django.shortcuts import render, redirect
from .models import AdminUser, Student, Fees
from django.db.models import Sum


# ---------------- LOGIN ----------------

def login_view(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")

        try:
            admin = AdminUser.objects.get(username=u, password=p, is_active=True)
            request.session["admin_id"] = admin.id
            return redirect("home")
        except:
            return render(request, "pages/login.html", {"error": "Invalid Username or Password"})

    return render(request, "pages/login.html")


# ---------------- DASHBOARD ----------------

def home(request):
    if not request.session.get("admin_id"):
        return redirect("login")

    total_students = Student.objects.count()

    total_collected = 0
    pending_fees = 0

    students = Student.objects.all()

    for s in students:
        fee = Fees.objects.filter(student=s).first()
        if fee:
            total_collected += fee.paid_amount
            pending_fees += fee.remaining_amount

    context = {
        "total_students": total_students,
        "total_collected": total_collected,
        "pending_fees": pending_fees,
    }

    return render(request, "pages/home.html", context)


# ---------------- ADD STUDENT ----------------

def add_student(request):
    if not request.session.get("admin_id"):
        return redirect("login")

    if request.method == "POST":

        mobile = request.POST.get("mobile")

        if not mobile or not mobile.isdigit() or len(mobile) != 10:
          return render(request, "pages/add_student.html", {
    "error": "Mobile number must be exactly 10 digits",
    "old": request.POST
})


        Student.objects.create(
            first_name=request.POST.get("first_name"),
            surname=request.POST.get("surname"),
            admission_no=request.POST.get("admission_no"),
            student_class=request.POST.get("student_class"),
            mobile=mobile,
            address=request.POST.get("address"),
            previous_institute=request.POST.get("previous_institute"),
        )

        return redirect("home")

    return render(request, "pages/add_student.html")





# ---------------- STUDENT LIST ----------------

def student_list(request):
    if not request.session.get("admin_id"):
        return redirect("login")

    students = Student.objects.all().order_by("-id")

    data = []

    for s in students:
        fees = Fees.objects.filter(student=s)

        paid = fees.aggregate(total=Sum("paid_amount"))["total"] or 0
        pending = fees.aggregate(total=Sum("remaining_amount"))["total"] or 0

        data.append({
            "student": s,
            "paid": paid,
            "pending": pending,
        })

    return render(request, "pages/student_list.html", {"data": data})







# ---------------- ADD / UPDATE FEES ----------------

def add_fees(request, student_id):
    if not request.session.get("admin_id"):
        return redirect("login")

    student = Student.objects.get(id=student_id)
    fee = Fees.objects.filter(student=student).first()

    if request.method == "POST":
        paid_now = int(request.POST.get("paid_amount"))

        if fee:
            fee.paid_amount += paid_now
            fee.remaining_amount = fee.total_fees - fee.paid_amount
            fee.status = "Done" if fee.remaining_amount == 0 else "Partial"
            fee.save()
        else:
            total = int(request.POST.get("total_fees"))
            remaining = total - paid_now

            Fees.objects.create(
                student=student,
                total_fees=total,
                paid_amount=paid_now,
                remaining_amount=remaining,
                status="Done" if remaining == 0 else "Partial"
            )

        return redirect("student_list")

    return render(request, "pages/add_fees.html", {
        "student": student,
        "fee": fee
    })












# ---------------- DELETE STUDENT ----------------

def delete_student(request, student_id):
    if not request.session.get("admin_id"):
        return redirect("login")

    Student.objects.get(id=student_id).delete()
    return redirect("student_list")






# ---------------- FEES STUDENTS PAGE ----------------

def fees_students(request):
    if not request.session.get("admin_id"):
        return redirect("login")

    students = Student.objects.all()
    return render(request, "pages/fees_students.html", {"students": students})







# ---------------- EDIT STUDENT ----------------

def edit_student(request, student_id):
    if not request.session.get("admin_id"):
        return redirect("login")

    student = Student.objects.get(id=student_id)

    if request.method == "POST":

        mobile = request.POST.get("mobile")

        if not mobile or not mobile.isdigit() or len(mobile) != 10:
           return render(request, "pages/edit_student.html", {
             "student": student,
             "error": "Mobile number must be exactly 10 digits",
             "old": request.POST
})


        student.first_name = request.POST.get("first_name")
        student.surname = request.POST.get("surname")
        student.student_class = request.POST.get("student_class")
        student.mobile = mobile
        student.address = request.POST.get("address")
        student.previous_institute = request.POST.get("previous_institute")
        student.save()

        return redirect("student_list")

    return render(request, "pages/edit_student.html", {"student": student})
