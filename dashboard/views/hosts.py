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
            # Use the created SQL view 'host_details' instead of the 'hosts' table
            cursor.execute("SELECT * FROM host_details WHERE name LIKE %s", ['%' + search_query + '%'])
        else:
            cursor.execute("SELECT * FROM host_details")
        result = cursor.fetchall()
        
        if result:
            columns = [col[0] for col in cursor.description]
            hosts = [dict(zip(columns, row)) for row in result]

    return render(request, 'dashboard/host/list.html', {'hosts': hosts, 'search_query': search_query})

def delete_host(request, host_id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                # Construct and execute the raw SQL query
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
            os_id = form.cleaned_data['os_id'].id

            # Construct and execute the raw SQL query
            with connection.cursor() as cursor:
                sql = "INSERT INTO hosts (name, ip, os_id) VALUES (%s, %s, %s)"
                cursor.execute(sql, [name, ip, os_id])
            
            messages.success(request, 'Host created successfully!')
            return redirect('hosts')
    else:
        form = HostForm()  

    return render(request, 'dashboard/host/create.html', {'form': form})

def update_host(request, host_id):
    # Fetch the existing host details for initial form data
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM hosts WHERE id = %s", [host_id])
            host = cursor.fetchone()
            if not host:
                raise Http404("Host not found.")
            
            form = HostForm(initial={
                'name': host[1], 'ip': host[2], 'os_id': host[3]
            })
            return render(request, 'dashboard/host/update.html', {'form': form, 'host_id': host_id})

    # Process form submission and update the host
    elif request.method == 'POST':
        form = HostForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            ip = form.cleaned_data['ip']
            os_id = form.cleaned_data['os_id'].id
            
            # Construct and execute the raw SQL query
            with connection.cursor() as cursor:
                sql = """
                UPDATE hosts
                SET name = %s, ip = %s, os_id = %s
                WHERE id = %s
                """
                cursor.execute(sql, [name, ip, os_id, host_id])
                
            messages.success(request, 'Host updated successfully!')
            return redirect('hosts')
        else:
            messages.error(request, 'Form is not valid')
            return render(request, 'dashboard/host/update.html', {'form': form, 'host_id': host_id})

    else:
        return Http404

def clear_host_results(request, host_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # Use the DeleteHostResults procedure, this cannot be called raw
            cursor.callproc('DeleteHostResults', [host_id])
            messages.success(request, 'Results for the host have been cleared successfully!')
        return redirect('hosts')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('hosts')   
    

def host_detail(request, host_id):
    host_data = {}
    with connection.cursor() as cursor:
        # Get basic host details
        cursor.execute("SELECT name, ip, id FROM hosts WHERE id = %s", [host_id])
        host = cursor.fetchone()
        if not host:
            raise Http404("Host not found.")
        host_data['name'] = host[0]
        host_data['ip'] = host[1]
        host_data['id'] = host[2]

        # Get the average severity
        cursor.execute("SELECT AverageSeverity(%s)", [host_id])
        host_data['average_severity'] = cursor.fetchone()[0]

        # Get the highest risk
        cursor.execute("SELECT HighestRiskForHost(%s)", [host_id])
        host_data['highest_risk'] = cursor.fetchone()[0]

        # Get the last found date
        cursor.execute("SELECT LastVulnerabilityFoundDate(%s)", [host_id])
        host_data['last_found_date'] = cursor.fetchone()[0]

        # Check if the host has high vulnerabilities
        severity_threshold = 7.0  # Define a threshold for high risk
        cursor.execute("SELECT HasHighRiskVulnerabilities(%s, %s)", [host_id, severity_threshold])
        host_data['has_high_risk_vulnerabilities'] = cursor.fetchone()[0]

    return render(request, 'dashboard/host/detail.html', {'host': host_data})
