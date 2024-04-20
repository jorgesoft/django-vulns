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


def delete_assigned_group(request, group_name, host_id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                # Construct and execute the raw SQL query
                sql = "DELETE FROM assigned_groups WHERE groups_name = %s AND hosts_id = %s"
                cursor.execute(sql, [group_name, host_id])
                if cursor.rowcount == 0:
                    raise Http404("Assigned group not found.")

                messages.success(request, 'Assigned group deleted successfully!')
        except Exception as e:
            messages.error(request, 'An error occurred while deleting the assigned group: {}'.format(e))

        return redirect('assigned_groups')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('assigned_groups_list')  
    

def update_assigned_group(request, group_name, host_id):
    # Fetch the existing assigned group details for initial form data
    if request.method == 'GET':
        with connection.cursor() as cursor:
            # Execute the raw SQL query to fetch the assigned group
            cursor.execute("SELECT * FROM assigned_groups WHERE groups_name = %s AND hosts_id = %s", [group_name, host_id])
            assigned_group = cursor.fetchone()
            if not assigned_group:
                raise Http404("Assigned Group not found.")

            # Initialize the form with the fetched data
            form = AssignedGroupsForm(initial={
                'group_name': assigned_group[0],
                'host_id': assigned_group[1],
            })
            return render(request, 'dashboard/assigned_groups/update.html', {'form': form, 'group_name': group_name, 'host_id': host_id})

    # Process the form submission and update the assigned group
    elif request.method == 'POST':
        form = AssignedGroupsForm(request.POST)
        if form.is_valid():
            # Extract the data for updating
            groups_name = form.cleaned_data['group_name']
            hosts_id = form.cleaned_data['host_id'].id

            with connection.cursor() as cursor:
                # Construct and execute the raw SQL query
                sql = """
                UPDATE assigned_groups
                SET groups_name = %s, hosts_id = %s
                WHERE groups_name = %s AND hosts_id = %s
                """
                cursor.execute(sql, [groups_name, hosts_id, group_name, host_id])
                messages.success(request, 'Assigned group updated successfully!')
                return redirect('assigned_groups')
        else:
            messages.error(request, 'Form is not valid')
            return render(request, 'dashboard/assigned_groups/update.html', {'form': form, 'group_name': group_name, 'host_id': host_id})

    else:
        # If the request method isn't GET or POST, return an error
        return Http404