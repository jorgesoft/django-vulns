from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import VulnerabilitiesForm

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


