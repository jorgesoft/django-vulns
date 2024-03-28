from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from .models import Vulnerabilities
from .forms import VulnerabilitiesForm
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView
from django.shortcuts import get_object_or_404

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

def create_vulnerability(request):
    if request.method == 'POST':
        form = VulnerabilitiesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vulnerabilities')  # Redirect to the vulnerabilities list
    else:
        form = VulnerabilitiesForm()
    return render(request, 'dashboard/vulnerability_create.html', {'form': form})

def delete_vulnerability(request, cve):
    vulnerability = get_object_or_404(Vulnerabilities, cve=cve)
    vulnerability.delete()
    return redirect('vulnerabilities')

from django.shortcuts import get_object_or_404

class VulnerabilityUpdateView(UpdateView):
    model = Vulnerabilities
    form_class = VulnerabilitiesForm
    template_name = 'dashboard/vulnerability_update.html'
    success_url = reverse_lazy('vulnerabilities')

    def get_object(self, queryset=None):
        cve = self.kwargs.get("cve")
        return get_object_or_404(Vulnerabilities, cve=cve)
