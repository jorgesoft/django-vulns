from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ...forms import ActiveUsersForm

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


def create_active_user(request):
    if request.method == 'POST':
        form = ActiveUsersForm(request.POST)
        if form.is_valid():
            # Directly accessing the id attribute of the model instance
            hosts_id = form.cleaned_data['hosts'].id
            users_name = form.cleaned_data['users'].name
            access_roles_name = form.cleaned_data['access_roles'].name
            
            # Raw SQL Execution
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO active_users (hosts_id, users_name, access_roles_name)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, [hosts_id, users_name, access_roles_name])
            
            messages.success(request, 'Active user added successfully!')
            return redirect('active_users')
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = ActiveUsersForm()

    return render(request, 'dashboard/active_users/create.html', {'form': form})


def delete_active_user(request, hosts_id, users_name, access_roles_name):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                # Construct and execute the raw SQL query
                sql = """
                DELETE FROM active_users 
                WHERE hosts_id = %s AND users_name = %s AND access_roles_name = %s
                """
                cursor.execute(sql, [hosts_id, users_name, access_roles_name])
                if cursor.rowcount == 0:
                    raise Http404("Active user not found.")

                messages.success(request, 'Active user deleted successfully!')
        except Exception as e:
            messages.error(request, 'An error occurred while deleting the active user: {}'.format(e))

        return redirect('active_users')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('active_users')


def update_active_user(request, hosts_id, users_name, access_roles_name):
    if request.method == 'GET':
        # Fetch the existing active user using raw SQL
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT hosts_id, users_name, access_roles_name 
                FROM active_users 
                WHERE hosts_id = %s AND users_name = %s AND access_roles_name = %s
            """, [hosts_id, users_name, access_roles_name])
            active_user = cursor.fetchone()
            if not active_user:
                raise Http404("Active user not found.")

            # Initialize form with the fetched data
            form = ActiveUsersForm(initial={
                'hosts': active_user[0],
                'users': active_user[1],
                'access_roles': active_user[2]
            })
    elif request.method == 'POST':
        form = ActiveUsersForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            hosts_id_new = form.cleaned_data['hosts'].id
            users_name_new = form.cleaned_data['users'].name
            access_roles_name_new = form.cleaned_data['access_roles'].name

            # Update the database entry using raw SQL
            with connection.cursor() as cursor:
                update_sql = """
                UPDATE active_users
                SET hosts_id = %s, users_name = %s, access_roles_name = %s
                WHERE hosts_id = %s AND users_name = %s AND access_roles_name = %s
                """
                cursor.execute(update_sql, [hosts_id_new, users_name_new, access_roles_name_new, hosts_id, users_name, access_roles_name])
                messages.success(request, 'Active user updated successfully!')
                return redirect('active_users')
        else:
            messages.error(request, 'Form is not valid')
            # Render the form with errors while keeping initial data
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT hosts_id, users_name, access_roles_name 
                    FROM active_users 
                    WHERE hosts_id = %s AND users_name = %s AND access_roles_name = %s
                """, [hosts_id, users_name, access_roles_name])
                active_user = cursor.fetchone()
                form = ActiveUsersForm(initial={
                    'hosts': active_user[0],
                    'users': active_user[1],
                    'access_roles': active_user[2]
                })

    return render(request, 'dashboard/active_users/update.html', {
        'form': form,
        'hosts_id': hosts_id,
        'users_name': users_name,
        'access_roles_name': access_roles_name
    })
