import simplejson as json

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.forms.models import modelformset_factory

from cellcounter.main.forms import CellCountInstanceForm, BoneMarrowBackgroundForm
from cellcounter.main.models import BoneMarrowBackground

def submit(request):
    if request.method == 'POST':
        cellcount_instance = CellCountInstanceForm(request.POST, prefix="cellcount")
        bonemarrowbackground = BoneMarrowBackgroundForm(request.POST, prefix="bonemarrow")

        cellcount_list = {}
        cellcount_list['counts'] = {}
        data = json.loads(request.POST['counter'])

        for cell in data.keys():
            cellcount_list['counts'][cell] = data[cell]

        cellcount_list['site'] = request.POST['bonemarrow-site']
        cellcount_list['ease_of_aspiration'] = request.POST['bonemarrow-ease_of_aspiration']

        return render_to_response('main/report.html', {'cellcount_list': cellcount_list}, 
            context_instance=RequestContext(request))
            
    else:
        cellcount_form = CellCountInstanceForm(prefix="cellcount")
        bonemarrowbackground = BoneMarrowBackgroundForm(prefix="bonemarrow")

    return render_to_response('main/submit.html',
            {'cellcount': cellcount_form,
             'bonemarrowbackground': bonemarrowbackground},
            context_instance=RequestContext(request))
