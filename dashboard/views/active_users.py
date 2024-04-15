from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import AccessRolesForm

def active_users_list(request):
    search_query = request.GET.get('search', '')
    active_users = []  # Initialize as an empty list

    with connection.cursor() as cursor:
        if search_query:
            # Execute a search query to the active_users_details view
            cursor.execute("""
                SELECT * FROM active_users_details
                WHERE users_name LIKE %s OR host_name LIKE %s OR access_roles_name LIKE %s
                """, ['%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'])
        else:
            # Fetch all records from the view
            cursor.execute("SELECT * FROM active_users_details")
        result = cursor.fetchall()

        if result:
            columns = [col[0] for col in cursor.description]
            active_users = [dict(zip(columns, row)) for row in result]

    return render(request, 'dashboard/active_users/list.html', {'active_users': active_users, 'search_query': search_query})
