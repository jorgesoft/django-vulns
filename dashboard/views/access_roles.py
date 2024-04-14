from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import VulnerabilitiesForm

def access_roles_list(request):
    search_query = request.GET.get('search', '') 
    access_roles = []

    with connection.cursor() as cursor:
        if search_query:
            # Construct and execute the raw SQL query to search
            cursor.execute("SELECT * FROM access_roles WHERE name LIKE %s OR access_level LIKE %s OR description LIKE %s", 
                           ['%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'])
        else:
            # Get all access roles if no search query
            cursor.execute("SELECT * FROM access_roles")
        result = cursor.fetchall()
        
        if result:
            columns = [col[0] for col in cursor.description]
            access_roles = [
                dict(zip(columns, row))
                for row in result
            ]

    return render(request, 'dashboard/access_roles/list.html', {'access_roles': access_roles, 'search_query': search_query})
