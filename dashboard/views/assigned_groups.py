from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import AssignedGroupsForm

def assigned_groups_list(request):
    search_query = request.GET.get('search', '')
    assigned_groups = []  # Initialize as an empty list

    with connection.cursor() as cursor:
        if search_query:
            # Use the created SQL view 'assigned_group_details' instead of the 'assigne_groups' table
            cursor.execute("""
                SELECT * 
                FROM assigned_group_details
                WHERE groups_name LIKE %s OR host_name LIKE %s
            """, ['%' + search_query + '%', '%' + search_query + '%'])
        else:
            cursor.execute("SELECT * FROM assigned_group_details")
        result = cursor.fetchall()
        
        if result:
            columns = [col[0] for col in cursor.description]
            assigned_groups = [dict(zip(columns, row)) for row in result]

    return render(request, 'dashboard/assigned_groups/list.html', {
        'assigned_groups': assigned_groups, 
        'search_query': search_query
    })


def create_assigned_group(request):
    if request.method == 'POST':
        form = AssignedGroupsForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group_name']
            host_id = form.cleaned_data['host_id'].id

            # Construct and execute the raw SQL query
            with connection.cursor() as cursor:
                sql = "INSERT INTO assigned_groups (groups_name, hosts_id) VALUES (%s, %s)"
                cursor.execute(sql, [group_name, host_id])
            
            messages.success(request, 'Assigned group created successfully!')
            return redirect('assigned_groups')
    else:
        form = AssignedGroupsForm()

    return render(request, 'dashboard/assigned_groups/create.html', {'form': form})

