from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import GroupsForm

def groups_list(request):
    search_query = request.GET.get('group_search', '')
    groups = []

    with connection.cursor() as cursor:
        if search_query:
            # Construct and execute the raw SQL query
            cursor.execute("SELECT * FROM `groups` WHERE name LIKE %s OR type LIKE %s OR description LIKE %s", 
                        ['%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'])
        else:
            cursor.execute("SELECT * FROM `groups`")
        result = cursor.fetchall()

        
        if result:
            columns = [col[0] for col in cursor.description]
            groups = [
                dict(zip(columns, row))
                for row in result
            ]

    return render(request, 'dashboard/group/list.html', {'groups': groups, 'search_query': search_query})


def create_group(request):
    if request.method == 'POST':
        form = GroupsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            group_type = form.cleaned_data['type']
            description = form.cleaned_data['description']
            
            # Construct and execute the raw SQL query
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO `groups` (name, type, description)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, [name, group_type, description])
            
            messages.success(request, 'Group created successfully!')
            return redirect('groups')  
    else:
        form = GroupsForm()

    return render(request, 'dashboard/group/create.html', {'form': form})
