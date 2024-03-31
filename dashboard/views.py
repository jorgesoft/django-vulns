from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import TemplateView
from .models import Vulnerabilities
from .forms import VulnerabilitiesForm
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView
from django.shortcuts import get_object_or_404
from django.db import connection
from django.contrib import messages

class HomeView(TemplateView):
    template_name = 'dashboard/home.html'

def results(request):
    return HttpResponse("Results Page Placeholder")

def hosts(request):
    return HttpResponse("Hosts Page Placeholder")

def users(request):
    return HttpResponse("Users Page Placeholder")

def groups(request):
    return HttpResponse("Groups Page Placeholder")

def vulnerabilities_list(request):
    search_query = request.GET.get('cve_search', '')
    vulnerabilities = []  # Initialize as an empty list

    with connection.cursor() as cursor:
        if search_query:
            # Use ILIKE for case-insensitive matching in PostgreSQL; use LIKE for other databases
            cursor.execute("SELECT * FROM vulnerabilities WHERE cve LIKE %s", ['%' + search_query + '%'])
        else:
            cursor.execute("SELECT * FROM vulnerabilities")
        result = cursor.fetchall()
        
        if result:  # Ensure result is not None
            columns = [col[0] for col in cursor.description]
            vulnerabilities = [
                dict(zip(columns, row))
                for row in result
            ]

    return render(request, 'dashboard/vulnerabilities_list.html', {'vulnerabilities': vulnerabilities, 'search_query': search_query})

def create_vulnerability(request):
    if request.method == 'POST':
        form = VulnerabilitiesForm(request.POST)
        if form.is_valid():
            cve = form.cleaned_data['cve']
            software = form.cleaned_data['software']
            description = form.cleaned_data['description']
            severity = form.cleaned_data['severity']
            cwe = form.cleaned_data['cwe']
            
            # Ensure you are preventing SQL injection by using placeholders
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

    return render(request, 'dashboard/vulnerability_create.html', {'form': form})

def delete_vulnerability(request, cve):
    # Ensure the request is a POST request for safety.
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                # Delete query using placeholders for safety against SQL injection.
                sql = "DELETE FROM vulnerabilities WHERE cve = %s"
                cursor.execute(sql, [cve])
                # Check if a row was deleted.
                if cursor.rowcount == 0:
                    raise Http404("Vulnerability not found.")
                
                messages.success(request, 'Vulnerability deleted successfully!')
        except Exception as e:
            messages.error(request, 'An error occurred while deleting the vulnerability.')
            # Optionally log the error or handle it further.
        
        return redirect('vulnerabilities')
    else:
        # Redirect or show an error if the method is not POST.
        messages.error(request, 'Invalid request method.')
        return redirect('vulnerabilities')

class VulnerabilityUpdateView(UpdateView):
    model = Vulnerabilities
    form_class = VulnerabilitiesForm
    template_name = 'dashboard/vulnerability_update.html'
    success_url = reverse_lazy('vulnerabilities')

    def get_object(self, queryset=None):
        cve = self.kwargs.get("cve")
        return get_object_or_404(Vulnerabilities, cve=cve)
