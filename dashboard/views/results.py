from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import ResultsForm

def results_list(request):
    search_query = request.GET.get('search', '')
    results = []  # Initialize as an empty list

    with connection.cursor() as cursor:
        if search_query:
            # Use the 'DetailedVulnerabilityReport' view instead of querying the 'results' table
            cursor.execute("""
                SELECT * 
                FROM DetailedVulnerabilityReport
                WHERE hosts_name LIKE %s OR vulnerabilities_cve LIKE %s OR description LIKE %s
            """, ['%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'])
        else:
            cursor.execute("SELECT * FROM DetailedVulnerabilityReport")
        result = cursor.fetchall()
        
        if result:
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in result]
    
    return render(request, 'dashboard/results/list.html', {
        'results': results, 
        'search_query': search_query
    })

def create_result(request):
    if request.method == 'POST':
        form = ResultsForm(request.POST)
        if form.is_valid():
            hosts_id = form.cleaned_data['hosts'].id
            vulnerabilities_cve = form.cleaned_data['vulnerabilities'].cve
            proof = form.cleaned_data['proof']
            status = form.cleaned_data['status']
            first_found = form.cleaned_data['first_found']
            last_update = form.cleaned_data['last_update']

            # Construct and execute the raw SQL query
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO results (hosts_id, vulnerabilities_cve, proof, status, first_found, last_update)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, [hosts_id, vulnerabilities_cve, proof, status, first_found, last_update])
            
            messages.success(request, 'New result added successfully!')
            return redirect('results')
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = ResultsForm()

    return render(request, 'dashboard/results/create.html', {'form': form})


def delete_result(request, result_id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                # Construct and execute the raw SQL query to delete the specific result
                sql = "DELETE FROM results WHERE id = %s"
                cursor.execute(sql, [result_id])
                if cursor.rowcount == 0:
                    raise Http404("Result not found.")
                
                messages.success(request, 'Result deleted successfully!')
        except Exception as e:
            messages.error(request, 'An error occurred while deleting the result: {}'.format(e))
        
        return redirect('results')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('results')


def update_result(request, result_id):
    if request.method == 'GET':
        # Fetch the existing result details for initial form data
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM DetailedVulnerabilityReport WHERE result_id = %s
            """, [result_id])
            result = cursor.fetchone()
            if not result:
                raise Http404("Result not found.")

            # Pre-fill the form with the fetched data
            form_data = {
                'hosts': result[1],
                'vulnerabilities': result[3],
                'proof': result[7],
                'status': result[8],
                'first_found': result[9],
                'last_update': result[10]
            }
            form = ResultsForm(initial=form_data)
            return render(request, 'dashboard/results/update.html', {'form': form, 'result_id': result_id})

    elif request.method == 'POST':
        form = ResultsForm(request.POST)
        if form.is_valid():
            # Extract data from form
            hosts_id = form.cleaned_data['hosts'].id
            vulnerabilities_cve = form.cleaned_data['vulnerabilities'].cve
            proof = form.cleaned_data['proof']
            status = form.cleaned_data['status']
            first_found = form.cleaned_data['first_found']
            last_update = form.cleaned_data['last_update']

            # Update the record using raw SQL
            with connection.cursor() as cursor:
                sql = """
                UPDATE results
                SET hosts_id = %s, vulnerabilities_cve = %s, proof = %s, status = %s, first_found = %s, last_update = %s
                WHERE id = %s
                """
                cursor.execute(sql, [hosts_id, vulnerabilities_cve, proof, status, first_found, last_update, result_id])
                messages.success(request, 'Result updated successfully!')
                return redirect('results')
        else:
            messages.error(request, 'Form is not valid')
            return render(request, 'dashboard/results/update.html', {'form': form, 'result_id': result_id})

    else:
        return Http404("Invalid HTTP method used.")
