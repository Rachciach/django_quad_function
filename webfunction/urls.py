from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from function import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('function.urls')),
    path('login/',auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_request, name='register'),
    path('media/plots/<str:file>',views.plots, name='plots')
]