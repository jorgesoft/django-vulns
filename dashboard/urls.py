from django.urls import path
from .views.home import HomeView
from .views.vulnerabilities import (
    vulnerabilities_list, 
    create_vulnerability, 
    delete_vulnerability, 
    update_vulnerability
)
# Import other view functions if they are split into different modules

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # Add paths for results, hosts, users, groups if you have corresponding views
    path('vulnerabilities/', vulnerabilities_list, name='vulnerabilities'),
    path('vulnerabilities/create/', create_vulnerability, name='vulnerability-create'),
    path('vulnerabilities/delete/<str:cve>/', delete_vulnerability, name='vulnerability-delete'),
    path('vulnerability/update/<str:cve>/', update_vulnerability, name='vulnerability-update'),
]
