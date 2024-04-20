from django.views.generic import TemplateView
from django.db import connection

class ReportView(TemplateView):
    template_name = 'dashboard/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Count of all results
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM results")
            count_results = cursor.fetchone()[0]
        context['count_results'] = count_results

        # Call the stored procedures for aggregation report and fetch their results
        with connection.cursor() as cursor:
            cursor.callproc('GetVulnerabilityCountsByRating')
            vulnerabilities_by_rating = cursor.fetchall()
            cursor.nextset()

            cursor.callproc('GetHostsAndVulnerabilitiesCountByOS')
            hosts_vulnerabilities_by_os = cursor.fetchall()
            cursor.nextset()

            cursor.callproc('GetAverageAndMaxSeverity')
            avg_max_severity = cursor.fetchall()
            cursor.nextset()

            cursor.callproc('GetVulnerabilityStatsBySoftware')
            vulnerability_stats_by_software = cursor.fetchall()

        # Adding results to context for template
        context['vulnerabilities_by_rating'] = vulnerabilities_by_rating
        context['hosts_vulnerabilities_by_os'] = hosts_vulnerabilities_by_os
        context['avg_max_severity'] = avg_max_severity
        context['vulnerability_stats_by_software'] = vulnerability_stats_by_software

        # DetailedVulnerabilityReport view just to add total information

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM DetailedVulnerabilityReport")
            detailed_vulnerability_report = cursor.fetchall()
        context['detailed_vulnerability_report'] = detailed_vulnerability_report

        return context
