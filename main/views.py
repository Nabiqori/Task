from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout


from .models import *

class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            tasks = Task.objects.filter(user=request.user).exclude(status='done').order_by('-deadline')
            context = {
                "tasks":tasks,
                "dones":Task.objects.filter(status='done', user=request.user),
            }
            return render(request, 'index.html', context)
        return redirect('login')
    def post(self,request):
        if request.user.is_authenticated:
            if request.POST.get('deadline') == '':
                deadline=None
            else:
                deadline=request.POST.get('deadline')
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
            context = {
                "task":task,
            }
            return render(request, "edit.html", context)
        return redirect('login')
    def post(self,request,pk):
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
            context = {
                "task": task,
            }
            return render(request, "delete.html", context)
        return redirect('login')
    def post(self,request,pk):
        if request.user.is_authenticated:
            Task.objects.filter(pk=pk, user=request.user).delete()
            return redirect('home')
        redirect('login')

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
def register_view(request):
    if request.method == 'POST':
        if request.POST.get('password1') != request.POST.get('password2') or request.POST.get('username') in User.objects.values_list('username', flat=True):
            return redirect("register")
        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password1'),
        )
        if user is not None:
            login(request, user)
            return redirect("home")
        return redirect('register')
    return render(request, "register.html")