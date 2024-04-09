from django.urls import path
from .views.home import HomeView
from .views.vulnerabilities import (
    vulnerabilities_list, 
    create_vulnerability, 
    delete_vulnerability, 
    update_vulnerability,
)
from .views.hosts import (
    hosts_list,
    create_host,
    delete_host,
    update_host,
)

urlpatterns = [
    # Vulnerabilities URLs
    path('', HomeView.as_view(), name='home'),
    path('vulnerabilities/', vulnerabilities_list, name='vulnerabilities'),
    path('vulnerabilities/create/', create_vulnerability, name='vulnerability-create'),
    path('vulnerabilities/delete/<str:cve>/', delete_vulnerability, name='vulnerability-delete'),
    path('vulnerability/update/<str:cve>/', update_vulnerability, name='vulnerability-update'),
    # Host URLs
    path('hosts/', hosts_list, name='hosts'),
    path('hosts/create/', create_host, name='host-create'),
    path('hosts/delete/<int:host_id>/', delete_host, name='host-delete'),
    path('host/update/<int:host_id>/', update_host, name='host-update'),
]
