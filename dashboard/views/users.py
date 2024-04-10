# views.py

from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import UserForm


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
        form = UserForm(request.POST)
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
        form = UserForm()  # An empty form for GET request to display the form

    return render(request, 'dashboard/user_create.html', {'form': form})