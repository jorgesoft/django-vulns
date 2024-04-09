from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection, IntegrityError
from django.contrib import messages
from ..forms import HostForm

def hosts_list(request):
    search_query = request.GET.get('host_search', '')
    hosts = []  # Initialize as an empty list

    with connection.cursor() as cursor:
        if search_query:
            cursor.execute("SELECT * FROM hosts WHERE name LIKE %s", ['%' + search_query + '%'])
        else:
            cursor.execute("SELECT * FROM hosts")
        result = cursor.fetchall()
        
        if result:
            columns = [col[0] for col in cursor.description]
            hosts = [dict(zip(columns, row)) for row in result]

    return render(request, 'dashboard/hosts_list.html', {'hosts': hosts, 'search_query': search_query})

def delete_host(request, host_id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM hosts WHERE id = %s", [host_id])
                if cursor.rowcount == 0:
                    raise Http404("Host not found.")
                messages.success(request, 'Host deleted successfully!')
        except IntegrityError as e:
            messages.error(request, "This host cannot be deleted because it is referenced by another record.")
        except Exception as e:
            messages.error(request, 'An error occurred while deleting the host.')
        return redirect('hosts')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('hosts')


def create_host(request):
    if request.method == 'POST':
        form = HostForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            ip = form.cleaned_data['ip']
            os_id = form.cleaned_data['os_id'].id  # Assuming 'os' is the name of the field in your HostForm

            # Construct and execute the raw SQL query
            with connection.cursor() as cursor:
                sql = "INSERT INTO hosts (name, ip, os_id) VALUES (%s, %s, %s)"
                cursor.execute(sql, [name, ip, os_id])
            
            messages.success(request, 'Host created successfully!')
            return redirect('hosts')  # Replace 'some-view' with the actual view you want to redirect to
    else:
        form = HostForm()  # Assuming your form for creating hosts is named HostForm

    return render(request, 'dashboard/host_create.html', {'form': form})

def update_host(request, host_id):
    # Fetch the existing host details for initial form data
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM hosts WHERE id = %s", [host_id])
            host = cursor.fetchone()
            if not host:
                raise Http404("Host not found.")
            
            # Assuming the host form includes fields for 'name', 'ip', and a dropdown for 'os_id'
            form = HostForm(initial={
                'name': host[1], 'ip': host[2], 'os_id': host[3]
            })
            return render(request, 'dashboard/host_update.html', {'form': form, 'host_id': host_id})

    # Process form submission and update the host
    elif request.method == 'POST':
        form = HostForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            ip = form.cleaned_data['ip']
            os_id = form.cleaned_data['os_id'].id  # Assuming 'os_id' is the name of the field in your HostForm
            
            with connection.cursor() as cursor:
                sql = """
                UPDATE hosts
                SET name = %s, ip = %s, os_id = %s
                WHERE id = %s
                """
                cursor.execute(sql, [name, ip, os_id, host_id])
                
            messages.success(request, 'Host updated successfully!')
            return redirect('hosts')  # Redirect to your hosts list view
        else:
            messages.error(request, 'Form is not valid')
            return render(request, 'dashboard/host_update.html', {'form': form, 'host_id': host_id})

    else:
        return Http404
   