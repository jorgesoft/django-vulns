from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import VulnerabilitiesForm

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