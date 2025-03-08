from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# RegisterView is already imported through the import above

app_name = 'tasks'

urlpatterns = [
    # Home page
    path('', views.HomeView.as_view(), name='home'),
    # User registration
    path('register/', views.RegisterView.as_view(), name='register'),
    
    
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Task list with filtering
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    
    # Task CRUD operations
    path('tasks/new/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    
    # Task toggle completion
    path('tasks/<int:pk>/toggle/', views.TaskToggleCompletionView.as_view(), name='task-toggle'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password-reset-complete'),
]
