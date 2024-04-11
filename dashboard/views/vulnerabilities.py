from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import VulnerabilitiesForm

def vulnerabilities_list(request):
    search_query = request.GET.get('cve_search', '')
    vulnerabilities = []  # Initialize as an empty list

    with connection.cursor() as cursor:
        if search_query:
            # Construct and execute the raw SQL query
            cursor.execute("SELECT * FROM vulnerabilities WHERE cve LIKE %s", ['%' + search_query + '%'])
        else:
            cursor.execute("SELECT * FROM vulnerabilities")
        result = cursor.fetchall()
        
        if result:
            columns = [col[0] for col in cursor.description]
            vulnerabilities = [
                dict(zip(columns, row))
                for row in result
            ]

    return render(request, 'dashboard/vulnerability/list.html', {'vulnerabilities': vulnerabilities, 'search_query': search_query})

def create_vulnerability(request):
    if request.method == 'POST':
        form = VulnerabilitiesForm(request.POST)
        if form.is_valid():
            cve = form.cleaned_data['cve']
            software = form.cleaned_data['software']
            description = form.cleaned_data['description']
            severity = form.cleaned_data['severity']
            cwe = form.cleaned_data['cwe']
            
            # Construct and execute the raw SQL query
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO vulnerabilities (cve, software, description, severity, cwe)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, [cve, software, description, severity, cwe])
            
            messages.success(request, 'Vulnerability created successfully!')
            return redirect('vulnerabilities')
    else:
        form = VulnerabilitiesForm()

    return render(request, 'dashboard/vulnerability/create.html', {'form': form})

def delete_vulnerability(request, cve):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                # Construct and execute the raw SQL query
                sql = "DELETE FROM vulnerabilities WHERE cve = %s"
                cursor.execute(sql, [cve])
                if cursor.rowcount == 0:
                    raise Http404("Vulnerability not found.")
                
                messages.success(request, 'Vulnerability deleted successfully!')
        except Exception as e:
            messages.error(request, 'An error occurred while deleting the vulnerability.')
        
        return redirect('vulnerabilities')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('vulnerabilities')

def update_vulnerability(request, cve):
    # Fetch the existing vulnerability details for initial form data
    if request.method == 'GET':
        with connection.cursor() as cursor:
            # Construct and execute the raw SQL query
            cursor.execute("SELECT * FROM vulnerabilities WHERE cve = %s", [cve])
            vulnerability = cursor.fetchone()
            if not vulnerability:
                raise Http404("Vulnerability not found.")

            form = VulnerabilitiesForm(initial={
                'cve': vulnerability[0], 'software': vulnerability[1],
                'description': vulnerability[2], 'severity': vulnerability[3],
                'cwe': vulnerability[4]
            })
            return render(request, 'dashboard/vulnerability/update.html', {'form': form, 'cve': cve})

    elif request.method == 'POST':
        form = VulnerabilitiesForm(request.POST)
        if form.is_valid():
            software = form.cleaned_data['software']
            description = form.cleaned_data['description']
            severity = form.cleaned_data['severity']
            cwe = form.cleaned_data['cwe']

            # Construct and execute the raw SQL query
            with connection.cursor() as cursor:
                sql = """
                UPDATE vulnerabilities
                SET software = %s, description = %s, severity = %s, cwe = %s
                WHERE cve = %s
                """
                cursor.execute(sql, [software, description, severity, cwe, cve])
                messages.success(request, 'Vulnerability updated successfully!')
                return redirect('vulnerabilities')
        else:
            messages.error(request, 'Form is not valid')
            return render(request, 'dashboard/vulnerability/update.html', {'form': form, 'cve': cve})

    else:
        return Http404