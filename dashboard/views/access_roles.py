from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import AccessRolesForm

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


def create_access_role(request):
    if request.method == 'POST':
        form = AccessRolesForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            access_level = form.cleaned_data['access_level']
            description = form.cleaned_data['description']
            
            # Construct and execute the raw SQL query
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO access_roles (name, access_level, description)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, [name, access_level, description])
            
            messages.success(request, 'Access role created successfully!')
            return redirect('access_roles')
    else:
        form = AccessRolesForm()

    return render(request, 'dashboard/access_roles/create.html', {'form': form})