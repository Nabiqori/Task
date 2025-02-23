from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *

class HomeView(View):
    def get(self, request):
        tasks = Task.objects.exclude(status='done').order_by('-deadline')
        context = {
            "tasks":tasks,
            "dones":Task.objects.filter(status='done'),
        }
        return render(request, 'index.html', context)
    def post(self,request):
        Task.objects.create(
            title=request.POST.get('title'),
            details=request.POST.get('details'),
            status=request.POST.get('status'),
            deadline=request.POST.get('deadline'),
            user=User.objects.last()
        )
        return redirect('home')
class EditView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        context = {
            "task":task,
        }
        return render(request, "edit.html", context)
    def post(self,request,pk):
        Task.objects.filter(pk=pk).update(
            title=request.POST.get('title'),
            details=request.POST.get('details'),
            status=request.POST.get('status'),

        )
        return redirect('home')
class DeleteView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        context = {
            "task": task,
        }
        return render(request, "delete.html", context)
    def post(self,request,pk):
        Task.objects.filter(pk=pk).delete()
        return redirect('home')