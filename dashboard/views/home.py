# myapp/views/home.py
from django.views.generic import TemplateView
from django.db import connection

class HomeView(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adding a count of results to show the counter
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM results")
            count_results = cursor.fetchone()[0]
        context['count_results'] = count_results

        # Query HostVulnerabilitySummary view
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM HostVulnerabilitySummary")
            host_vulnerability_summary = cursor.fetchall()
        context['host_vulnerability_summary'] = host_vulnerability_summary

        # Query DetailedVulnerabilityReport view
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM DetailedVulnerabilityReport")
            detailed_vulnerability_report = cursor.fetchall()
        context['detailed_vulnerability_report'] = detailed_vulnerability_report

        return context
