from django.urls import path
from .views import HomeView, results, hosts, users, groups, vulnerabilities_list
from .views import create_vulnerability

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('results/', results, name='results'),
    path('hosts/', hosts, name='hosts'),
    path('users/', users, name='users'),
    path('groups/', groups, name='groups'),
    path('vulnerabilities/', vulnerabilities_list, name='vulnerabilities'),
    path('vulnerabilities/create/', create_vulnerability, name='vulnerability-create'),
]