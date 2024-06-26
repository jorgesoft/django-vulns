from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ...forms import OsForm

def os_list(request):
    search_query = request.GET.get('os_search', '') 
    operating_systems = [] 

    with connection.cursor() as cursor:
        if search_query:
            # Construct and execute the raw SQL query using the os_summary view
            cursor.execute("SELECT * FROM os_summary WHERE os_name LIKE %s OR family LIKE %s", 
                           ['%' + search_query + '%', '%' + search_query + '%'])
        else:
            cursor.execute("SELECT * FROM os_summary")
        result = cursor.fetchall()
        
        if result:
            columns = [col[0] for col in cursor.description]
            operating_systems = [
                dict(zip(columns, row))
                for row in result
            ]

    return render(request, 'dashboard/os/list.html', {'operating_systems': operating_systems, 'search_query': search_query})


def create_os(request):
    if request.method == 'POST':
        form = OsForm(request.POST)
        if form.is_valid():
            family = form.cleaned_data['family']
            version = form.cleaned_data['version']
            patch = form.cleaned_data['patch']
            
            # Construct and execute the raw SQL query
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO os (family, version, patch)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, [family, version, patch])
            
            messages.success(request, 'Operating System created successfully!')
            return redirect('os')
    else:
        form = OsForm()

    return render(request, 'dashboard/os/create.html', {'form': form})

def delete_os(request, os_id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                # Construct and execute the raw SQL query
                sql = "DELETE FROM os WHERE id = %s"
                cursor.execute(sql, [os_id])
                if cursor.rowcount == 0:
                    raise Http404("Operating System not found.")
                
                messages.success(request, 'Operating System deleted successfully!')
        except Exception as e:
            messages.error(request, 'An error occurred while deleting the Operating System.')
        
        return redirect('os')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('os-list')

def update_os(request, os_id):
    # Fetch the existing OS details for initial form data
    if request.method == 'GET':
        with connection.cursor() as cursor:
            # Construct and execute the raw SQL query
            cursor.execute("SELECT * FROM os WHERE id = %s", [os_id])
            os = cursor.fetchone()
            if not os:
                raise Http404("OS not found.")

            form = OsForm(initial={
                'family': os[1], 
                'version': os[2],
                'patch': os[3]
            })
            return render(request, 'dashboard/os/update.html', {'form': form, 'os_id': os_id})

    elif request.method == 'POST':
        form = OsForm(request.POST)
        if form.is_valid():
            family = form.cleaned_data['family']
            version = form.cleaned_data['version']
            patch = form.cleaned_data['patch']

            # Construct and execute the raw SQL query
            with connection.cursor() as cursor:
                sql = """
                UPDATE os
                SET family = %s, version = %s, patch = %s
                WHERE id = %s
                """
                cursor.execute(sql, [family, version, patch, os_id])
                messages.success(request, 'OS updated successfully!')
                return redirect('os')
        else:
            messages.error(request, 'Form is not valid')
            return render(request, 'dashboard/os/update.html', {'form': form, 'os_id': os_id})

    else:
        # If the request method isn't GET or POST, return an error
        return Http404