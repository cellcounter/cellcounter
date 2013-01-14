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

        # calculate total cell count for calculating percentages
        total = 0
        for celltype in cellcount_list['counts'].keys():
            total = total + cellcount_list['counts'][celltype]['normal']

        cellcount_list['total'] = total
        
        for celltype in cellcount_list['counts'].keys():
            cellcount_list['counts'][celltype]['percent'] = "%.2f" % (float(cellcount_list['counts'][celltype]['normal'] * 100) / total)

        # build a string containing the cell count data for charting purposes
        chartdata = '[';
        for celltype in cellcount_list['counts'].keys():
            chartdata = chartdata + "['%s', %d]," % (celltype, cellcount_list['counts'][celltype]['normal'])
        chartdata = chartdata + ']'
        
        cellcount_list['chartdata'] = chartdata;

        if cellcount_list['counts']['myelo']['normal'] == 0 and cellcount_list['counts']['erythro']['normal'] == 0:
            cellcount_list['meratio'] = "N/A"
        else:
            try:
                cellcount_list['meratio'] = "%.2f" % (float(cellcount_list['counts']['myelo']['normal'])/float(cellcount_list['counts']['erythro']['normal']))
            except ZeroDivisionError:
                cellcount_list['meratio'] = "Inf"

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
