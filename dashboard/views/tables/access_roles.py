from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ...forms import AccessRolesForm

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


def delete_access_role(request, role_name):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                # Construct and execute the raw SQL query to delete an access role
                sql = "DELETE FROM access_roles WHERE name = %s"
                cursor.execute(sql, [role_name])
                if cursor.rowcount == 0:
                    raise Http404("Access role not found.")

                messages.success(request, 'Access role deleted successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred while deleting the access role: {e}')

        return redirect('access_roles')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('access_roles')


def update_access_role(request, role_name):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            # Construct and execute the raw SQL query to delete an access role
            cursor.execute("SELECT * FROM access_roles WHERE name = %s", [role_name])
            access_role = cursor.fetchone()
            if not access_role:
                raise Http404("Access role not found.")

            # Initialize the form with fetched data including the name
            form = AccessRolesForm(initial={
                'name': role_name,
                'access_level': access_role[1],
                'description': access_role[2]
            }, is_update=True)
            return render(request, 'dashboard/access_roles/update.html', {'form': form, 'role_name': role_name})

    elif request.method == 'POST':
        form = AccessRolesForm(request.POST, is_update=True)
        if form.is_valid():
            access_level = form.cleaned_data['access_level']
            description = form.cleaned_data['description']

            with connection.cursor() as cursor:
                # Construct and execute the raw SQL query to delete an access role
                sql = "UPDATE access_roles SET access_level = %s, description = %s WHERE name = %s"
                cursor.execute(sql, [access_level, description, role_name])
                messages.success(request, 'Access role updated successfully!')
                return redirect('access_roles')
        else:
            messages.error(request, 'Form is not valid')
            return render(request, 'dashboard/access_roles/update.html', {'form': form, 'role_name': role_name})
    else:
        return Http404
