from django.urls import path
from . import views

urlpatterns = [
    path('', views.root_redirect, name='root_redirect'),
    path('login/', views.login_view, name='login'),  # Assuming you have a custom login view
    path('home/', views.home, name='home'),
    # Other paths
]
