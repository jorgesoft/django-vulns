from django.shortcuts import render, redirect
from django.http import Http404 
from django.db import connection
from django.contrib import messages
from ..forms import GroupsForm

def groups_list(request):
    search_query = request.GET.get('group_search', '')
    groups = []

    with connection.cursor() as cursor:
        if search_query:
            # Construct and execute the raw SQL query
            cursor.execute("SELECT * FROM `groups` WHERE name LIKE %s OR type LIKE %s OR description LIKE %s", 
                        ['%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'])
        else:
            cursor.execute("SELECT * FROM `groups`")
        result = cursor.fetchall()

        
        if result:
            columns = [col[0] for col in cursor.description]
            groups = [
                dict(zip(columns, row))
                for row in result
            ]

    return render(request, 'dashboard/group/list.html', {'groups': groups, 'search_query': search_query})
