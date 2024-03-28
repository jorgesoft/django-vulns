from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Vulnerabilities

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
    if search_query:
        vulnerabilities = Vulnerabilities.objects.filter(cve__icontains=search_query)
    else:
        vulnerabilities = Vulnerabilities.objects.all()
    return render(request, 'dashboard/vulnerabilities_list.html', {'vulnerabilities': vulnerabilities, 'search_query': search_query})