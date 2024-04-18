from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import ActiveUsersForm

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
    print(results)
    return render(request, 'dashboard/results/list.html', {
        'results': results, 
        'search_query': search_query
    })
