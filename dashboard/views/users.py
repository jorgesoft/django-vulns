# views.py

from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import UsersForm


def list_users(request):
    search_query = request.GET.get('user_search', '')
    users = []  # Initialize as an empty list

    with connection.cursor() as cursor:
        if search_query:
            # Getting users from the search bar
            cursor.execute("SELECT * FROM users WHERE name LIKE %s OR full_name LIKE %s", ['%' + search_query + '%', '%' + search_query + '%'])
        else:
            # Getting all users
            cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        
        if result:  # Ensure result is not None
            columns = [col[0] for col in cursor.description]
            users = [
                dict(zip(columns, row))
                for row in result
            ]

    return render(request, 'dashboard/users_list.html', {'users': users, 'search_query': search_query})


def create_user(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            full_name = form.cleaned_data['full_name']
            
            # Using placeholders to prevent SQL injection
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO users (name, full_name)
                VALUES (%s, %s)
                """
                cursor.execute(sql, [username, full_name])
            
            messages.success(request, 'User created successfully!')
            return redirect('users')  # Adjust the redirect to your users' listing URL
    else:
        form = UsersForm()  # An empty form for GET request to display the form

    return render(request, 'dashboard/user_create.html', {'form': form})


def update_user(request, user_name):
    if request.method == 'POST':
        # Assuming `new_full_name` is obtained from the form
        new_full_name = request.POST.get('full_name')
        if not new_full_name:
            messages.error(request, 'Full name is required.')
            return render(request, 'dashboard/user_update.html')

        with connection.cursor() as cursor:
            # Update user's full_name without altering the name
            cursor.execute("UPDATE users SET full_name = %s WHERE name = %s", [new_full_name, user_name])
            if cursor.rowcount == 0:
                raise Http404("User not found.")
            
            messages.success(request, 'User updated successfully!')
            return redirect('users')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, full_name FROM users WHERE name = %s", [user_name])
            user = cursor.fetchone()
            if not user:
                raise Http404("User not found.")
            
            # Convert the tuple from fetchone() to a dictionary
            user_data = {'name': user[0], 'full_name': user[1]}
            # Pass the user data to the template, potentially as form initial data
            return render(request, 'dashboard/user_update.html', {'user': user_data, 'user_name': user_name})


def delete_user(request, user_name):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                # Deleting query using placeholders for safety against SQL injection
                sql = "DELETE FROM users WHERE name = %s"
                cursor.execute(sql, [user_name])
                # Check if a row was deleted
                if cursor.rowcount == 0:
                    raise Http404("User not found.")

                messages.success(request, 'User deleted successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred while deleting the user: {e}')

        return redirect('users')
    else:
        # Redirecting or showing an error if the method is not POST
        messages.error(request, 'Invalid request method.')
        return redirect('users')
