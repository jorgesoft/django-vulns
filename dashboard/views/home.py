# myapp/views/home.py
from django.views.generic import TemplateView
from django.db import connection

class HomeView(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Example: Adding a count of vulnerabilities to the context
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM vulnerabilities")
            count_vulnerabilities = cursor.fetchone()[0]
        context['count_vulnerabilities'] = count_vulnerabilities

        # Add more context as needed
        return context
