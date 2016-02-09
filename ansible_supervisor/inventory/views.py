from django.shortcuts import get_object_or_404, render


# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from .models import Host, HostVar
from .forms import HostForm, HostVarForm
from django.forms import modelformset_factory


def index(request):
    all_host_list = Host.objects.all()
    context = {'all_host_list': all_host_list}
    return render(request, 'inventory/index.html', context)


def detail(request, host_id):
    host = get_object_or_404(Host, pk=host_id)
    return render(request, 'inventory/detail.html', {'host': host})


def results(request, host_id):
    response = "You're looking at the results of host %s."
    return HttpResponse(response % host_id)


def change(request, host_id):
    host = Host.objects.get(pk=host_id)
    if request.POST['hostvar']:
        hostvar_id_list = request.POST.getlist('hostvar')
    for hostvar_id in hostvar_id_list:
        hostvar = HostVar.objects.get(pk=hostvar_id)
        hostvar_name = request.POST['hostvarname_'+hostvar_id]
        hostvar_value = request.POST['hostvarvalue_'+hostvar_id]
        hostvar.var_name = hostvar_name
        hostvar.var_value = hostvar_value
        hostvar.save()
        return render(request, 'inventory/detail.html', {'host': host})


def testchange(request, host_id):
    host = Host.objects.get(pk=host_id)
    HostVarFormSet = modelformset_factory(HostVar, fields=['var_name', 'var_value'])
    if request.method == 'POST':
        if request.POST['hostvar']:
            hostvar_id_list = request.POST.getlist('hostvar')
            for hostvar_id in hostvar_id_list:
                hostvar = HostVar.objects.get(pk=hostvar_id)
                hostvar_name = request.POST['hostvarname_'+hostvar_id]
                hostvar_value = request.POST['hostvarvalue_'+hostvar_id]
                hostvar.var_name = hostvar_name
                hostvar.var_value = hostvar_value
                hostvar.save()
        return render(request, 'inventory/detail.html', {'host': host})

    else:
        formset = HostVarFormSet(queryset=HostVar.objects.filter(host=host_id))

    return render(request, 'inventory/manage_hostvar.html', {'formset': formset, 'host': host})
