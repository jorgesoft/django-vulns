from django.shortcuts import render
from django.views.generic import TemplateView
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder
import json

class HomeView(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with connection.cursor() as cursor:
            # Count of all results
            cursor.execute("SELECT COUNT(*) FROM results")
            count_results = cursor.fetchone()[0]
            context['count_results'] = count_results

            # Count of all hosts
            cursor.execute("SELECT COUNT(*) FROM hosts")
            count_hosts = cursor.fetchone()[0]
            context['count_hosts'] = count_hosts

            # Average and Maximum Severity of Vulnerabilities
            cursor.callproc('GetAverageAndMaxSeverity')
            context['avg_max_severity'] = cursor.fetchall()
            
            # Vulns by rating graph
            cursor.nextset()
            cursor.callproc('GetVulnerabilityCountsByRating')
            vulnerabilities_by_rating = cursor.fetchall()[0]
            context['vulnerabilities_by_rating'] = json.dumps(vulnerabilities_by_rating, cls=DjangoJSONEncoder)

            # Host by OS 
            cursor.nextset()
            cursor.callproc('GetHostsAndVulnerabilitiesCountByOS')
            data = cursor.fetchall()
            context['hosts_vulnerabilities_by_os'] = json.dumps({
                'labels': [item[0] for item in data],
                'data': [item[1] for item in data]
            }, cls=DjangoJSONEncoder)

            # Vulns by Host
            cursor.nextset()
            cursor.callproc('CountVulnerabilitiesByHost')
            host_vulns_data = cursor.fetchall()
            context['host_vulns_data'] = json.dumps({
                'labels': [item[0] for item in host_vulns_data],
                'data': [item[1] for item in host_vulns_data]
            }, cls=DjangoJSONEncoder)

        return context
