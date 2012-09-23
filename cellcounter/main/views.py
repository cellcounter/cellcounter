from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.forms.models import modelformset_factory

from cellcounter.main.forms import CellCountInstanceForm, BoneMarrowBackgroundForm
from cellcounter.main.models import BoneMarrowBackground

def submit(request):
    if request.method == 'POST':
        cellcount_instance = CellCountInstanceForm(request.POST, prefix="cellcount")
        bonemarrowbackground = BoneMarrowBackgroundForm(request.POST, prefix="bonemarrow")
        
        if cellcount_instance.is_valid() and bonemarrowbackground.is_valid():
            cellcount_instance = cellcount_instance.save()
            bonemarrowbackground = BoneMarrowBackground(cell_count_instance=cellcount_instance)
            form = BoneMarrowBackgroundForm(request.POST, prefix="bonemarrow", instance=bonemarrowbackground)
            form.save()
            return HttpResponseRedirect('/')

        else:
            cellcount_form = CellCountInstanceForm(request.POST, prefix="cellcount")
            bonemarrowbackground = BoneMarrowBackgroundForm(request.POST, prefix="bonemarrow")
            
    else:
        cellcount_form = CellCountInstanceForm(prefix="cellcount")
        bonemarrowbackground = BoneMarrowBackgroundForm(prefix="bonemarrow")

    return render_to_response('main/submit.html',
            {'cellcount': cellcount_form,
             'bonemarrowbackground': bonemarrowbackground},
            context_instance=RequestContext(request))
