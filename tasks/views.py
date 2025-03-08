from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q

from .models import Task
from .forms import UserRegistrationForm, TaskForm

# Home page view (landing page)
class HomeView(TemplateView):
    template_name = 'tasks/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Task Manager - Home'
        return context

# User registration view
class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('tasks:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your account has been created! You can now log in.')
        return response
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

# Dashboard view (requires login)
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/dashboard.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        # Get count of total, completed, and pending tasks
        user = self.request.user
        context['total_tasks'] = Task.objects.filter(
            Q(assigned_to=user) | Q(created_by=user)
        ).distinct().count()
        context['completed_tasks'] = Task.objects.filter(
            (Q(assigned_to=user) | Q(created_by=user)) & Q(completed=True)
        ).distinct().count()
        context['pending_tasks'] = Task.objects.filter(
            (Q(assigned_to=user) | Q(created_by=user)) & Q(completed=False)
        ).distinct().count()
        
        # Get recent tasks
        context['recent_tasks'] = Task.objects.filter(
            Q(assigned_to=user) | Q(created_by=user)
        ).distinct().order_by('-created_date')[:5]
        
        return context

# Task list view (with filtering options)
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    login_url = 'login'
    paginate_by = 10
    
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(
            Q(assigned_to=user) | Q(created_by=user)
        ).distinct()
        
        # Filter by status (completed or not)
        status = self.request.GET.get('status', None)
        if status == 'completed':
            queryset = queryset.filter(completed=True)
        elif status == 'pending':
            queryset = queryset.filter(completed=False)
            
        # Filter by priority
        priority = self.request.GET.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
            
        # Filter by search query
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
            
        # Sort by due date (default) or other fields
        sort_by = self.request.GET.get('sort', 'due_date')
        if sort_by == 'title':
            queryset = queryset.order_by('title')
        elif sort_by == 'priority':
            # Custom ordering for priority (High, Medium, Low)
            priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
            queryset = sorted(queryset, key=lambda x: priority_order.get(x.priority, 99))
        else:
            queryset = queryset.order_by('due_date')
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Task List'
        # Add filter parameters to context for form persistence
        context['status'] = self.request.GET.get('status', '')
        context['priority'] = self.request.GET.get('priority', '')
        context['search'] = self.request.GET.get('search', '')
        context['sort'] = self.request.GET.get('sort', 'due_date')
        return context

# Task create view
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-list')
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Task'
        context['is_create'] = True
        return context

# Task detail view
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    login_url = 'login'
    
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(assigned_to=user) | Q(created_by=user)
        ).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Task: {self.object.title}'
        return context

# Task update view
class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    login_url = 'login'
    
    def test_func(self):
        task = self.get_object()
        # Only the creator or the assigned user can update the task
        return self.request.user == task.created_by or self.request.user == task.assigned_to
    
    def get_success_url(self):
        return reverse('tasks:task-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Task'
        context['is_update'] = True
        return context

# Task delete view
class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task-list')
    login_url = 'login'
    
    def test_func(self):
        task = self.get_object()
        # Only the creator can delete the task
        return self.request.user == task.created_by
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Task'
        return context

# Task completion toggle view
class TaskToggleCompletionView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login'
    
    def test_func(self):
        task_id = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        # Only the creator or the assigned user can toggle task completion
        return self.request.user == task.created_by or self.request.user == task.assigned_to
    
    def post(self, request, *args, **kwargs):
        task_id = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        
        # Toggle completion status
        task.completed = not task.completed
        task.save()
        
        # Return JSON response for AJAX requests
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'task_id': task_id,
                'completed': task.completed
            })
        
        # Redirect to the referring page for non-AJAX requests
        messages.success(request, f'Task "{task.title}" marked as {"completed" if task.completed else "pending"}')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('tasks:task-list')))
