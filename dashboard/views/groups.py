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


def delete_group(request, group_name):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                # Construct and execute the raw SQL query
                sql = "DELETE FROM `groups` WHERE name = %s"
                cursor.execute(sql, [group_name])
                if cursor.rowcount == 0:
                    raise Http404("Group not found.")

                messages.success(request, 'Group deleted successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred while deleting the group: {e}')

        return redirect('groups')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('groups')


def update_group(request, group_name):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM `groups` WHERE name = %s", [group_name])
            group = cursor.fetchone()
            if not group:
                raise Http404("Group not found.")

            # Prepare initial data for the form
            form = GroupsForm(initial={
                'name': group[0],  
                'type': group[1],  
                'description': group[2] 
            })
            return render(request, 'dashboard/group/update.html', {'form': form, 'group_name': group_name})

    elif request.method == 'POST':
        form = GroupsForm(request.POST)
        if form.is_valid():
            # Extracting form data
            group_type = form.cleaned_data['type']
            description = form.cleaned_data['description']

            with connection.cursor() as cursor:
                # Construct and execute the raw SQL query
                sql = """
                UPDATE `groups`
                SET type = %s, description = %s
                WHERE name = %s
                """
                cursor.execute(sql, [group_type, description, group_name])
                messages.success(request, 'Group updated successfully!')
                return redirect('groups')
        else:
            messages.error(request, 'Form is not valid')
            return render(request, 'dashboard/group/update.html', {'form': form, 'group_name': group_name})

    else:
        return Http404("Invalid HTTP method used.")
