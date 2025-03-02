from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
from .models import User, Task
from django.views import View


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            tasks = Task.objects.filter(user=request.user).exclude(status='done').order_by('-deadline')
            context = {
                "tasks": tasks,
                "dones": Task.objects.filter(status='done', user=request.user),
            }
            return render(request, 'index.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            deadline = request.POST.get('deadline') if request.POST.get('deadline') != '' else None
            Task.objects.create(
                title=request.POST.get('title'),
                details=request.POST.get('details'),
                status=request.POST.get('status'),
                deadline=deadline,
                user=request.user
            )
            return redirect('home')
        return redirect("login")


class EditView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            task = get_object_or_404(Task, pk=pk, user=request.user)
            context = {"task": task}
            return render(request, "edit.html", context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            Task.objects.filter(pk=pk, user=request.user).update(
                title=request.POST.get('title'),
                details=request.POST.get('details'),
                status=request.POST.get('status'),
            )
            return redirect('home')
        return redirect('login')


class DeleteView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            task = get_object_or_404(Task, pk=pk, user=request.user)
            context = {"task": task}
            return render(request, "delete.html", context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            Task.objects.filter(pk=pk, user=request.user).delete()
            return redirect('home')
        return redirect('login')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None:
            login(request, user)
            return redirect('home')
        return redirect("login")
    return render(request, "login.html")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


kod = None
email = None
password1 = None
username = None


def register_view(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'get_code':
            if request.POST.get('password1') != request.POST.get('password2') or User.objects.filter(
                    username=request.POST.get('username')).exists():
                return redirect("register")

            kod = str(random.randint(100000, 999999))
            request.session['kod'] = kod
            request.session['username'] = request.POST.get('username')
            request.session['password1'] = request.POST.get('password1')
            request.session['email'] = request.POST.get('email')

            print(f"Kod: {kod}, Email: {request.session['email']}")  # Tekshirish uchun
            return redirect("confirm")

    return render(request, "register.html")


def confirm_view(request):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'nabiqorinabiyev35@gmail.com'
    sender_password = 'bmdwdzdrrzjbgmgk'
    receiver_email = request.session.get('email')  # Sessiyadan olib ishlatamiz
    kod = request.session.get('kod')

    if receiver_email is None:
        print("Xatolik: Email yo‘q!")
        return redirect('register')

    print(receiver_email)  # Tekshirish uchun

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Tasdiqlash kodingiz'
    msg.attach(MIMEText(f'Assalomu alaykum, bu sizning tasdiqlash kodingiz: {kod}', 'plain'))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Xabar jo‘natildi!")
    except Exception as e:
        print(f'Xatolik yuz berdi: {e}')
        import traceback
        traceback.print_exc()
    finally:
        server.quit()

    if request.method == 'POST':
        if request.POST.get('kod') == request.session.get('kod'):
            user = User.objects.create_user(
                username=request.session.get('username'),
                password=request.session.get('password1'),

            )
            login(request, user)
            return redirect("home")
        return redirect('register')

    return render(request, "confirm_html.html")
