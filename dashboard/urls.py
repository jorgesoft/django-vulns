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
    clear_host_results,
)
from .views.users import (
    list_users,
    create_user,
    delete_user,
    update_user,
)
from .views.groups import (
    groups_list,
    create_group,
    delete_group,
    update_group,
)
from .views.os import (
    os_list,
    create_os,
    delete_os,
    update_os,
)
from .views.assigned_groups import (
    assigned_groups_list,
    create_assigned_group,
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
    path('host/clear-results/<int:host_id>/', clear_host_results, name='clear-host-results'),
    # Users URLs
    path('users/', list_users, name='users'),
    path('users/create/', create_user, name='user-create'),
    path('users/delete/<str:user_name>/', delete_user, name='user-delete'),
    path('users/update/<str:user_name>/', update_user, name='user-update'),
    # Group URLs
    path('groups/', groups_list, name='groups'),
    path('groups/create/', create_group, name='group-create'),
    path('groups/delete/<str:group_name>/', delete_group, name='group-delete'),
    path('group/update/<str:group_name>/', update_group, name='group-update'),
    # OS URLs
    path('os/', os_list, name='os'),
    path('os/create/', create_os, name='os-create'),
    path('os/delete/<str:os_id>/', delete_os, name='os-delete'),
    path('os/update/<str:os_id>/', update_os, name='os-update'),
    # Assigned_groups URLs
    path('assigned_groups/', assigned_groups_list, name='assigned_groups'),
    path('assigned_groups/create/', create_assigned_group, name='assigned-group-create'),
]