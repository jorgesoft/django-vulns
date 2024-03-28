from django.urls import path
from .views import HomeView, results, vulnerabilities, hosts, users, groups

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('results/', results, name='results'),
    path('vulnerabilities/', vulnerabilities, name='vulnerabilities'),
    path('hosts/', hosts, name='hosts'),
    path('users/', users, name='users'),
    path('groups/', groups, name='groups'),
]