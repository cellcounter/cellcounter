import simplejson as json

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.forms.models import modelformset_factory

from cellcounter.main.forms import CellCountInstanceForm, BoneMarrowBackgroundForm, CellCountForm, GranulopoiesisFindingsForm, ErythropoiesisFindingsForm, MegakaryocyteFeaturesForm

from cellcounter.main.models import BoneMarrowBackground, CellCount, CellType

def submit(request):

    celltypes = CellType.objects.all()
    celltype_list = []
    for celltype in celltypes:
        celltype_list.append({'cell': celltype})

    cellcount_formset = modelformset_factory(CellCount, form=CellCountForm, extra=len(celltype_list))

    if request.method == 'POST':
        count_instance = CellCountInstanceForm(request.POST, prefix="cellcount")
        bm_background_info = BoneMarrowBackgroundForm(request.POST, prefix="bonemarrow")
        erythropoiesis_form = ErythropoiesisFindingsForm(request.POST, prefix="erythropoiesis")
        granulopoiesis_form =  GranulopoiesisFindingsForm(request.POST, prefix="granulopoiesis")
        megakaryocyte_form = MegakaryocyteFeaturesForm(request.POST, prefix="megakaryocyte")
        cellcount_formset = cellcount_formset(request.POST, prefix='celltypecount')

        validation_list = [count_instance.is_valid(),
                           bm_background_info.is_valid(),
                           erythropoiesis_form.is_valid(),
                           granulopoiesis_form.is_valid(),
                           megakaryocyte_form.is_valid(),
                           cellcount_formset.is_valid()]

        if all(validation_list):
            return HttpResponseRedirect('/')
        else:
            return render_to_response('main/submit.html',
                    {'cellcount': count_instance, 
                     'bonemarrowbackground': bm_background_info, 
                     'erythropoiesis_form': erythropoiesis_form, 
                     'granulopoiesis_form': granulopoiesis_form,
                     'megakaryocyte_form': megakaryocyte_form,
                     'cellcount_formset': cellcount_formset},
                    context_instance=RequestContext(request))
    else:
        cellcount_form = CellCountInstanceForm(prefix="cellcount")
        bonemarrowbackground = BoneMarrowBackgroundForm(prefix="bonemarrow")
        erythropoiesis_form = ErythropoiesisFindingsForm(prefix="erythropoiesis")
        granulopoiesis_form = GranulopoiesisFindingsForm(prefix="granulopoiesis")
        megakaryocyte_form = MegakaryocyteFeaturesForm(prefix="megakaryocyte")
        cellcount_formset = cellcount_formset(initial=celltype_list, prefix='celltypecount')

    return render_to_response('main/submit.html',
            {'cellcount': cellcount_form,
             'bonemarrowbackground': bonemarrowbackground,
             'erythropoiesis_form': erythropoiesis_form,
             'granulopoiesis_form': granulopoiesis_form,
             'megakaryocyte_form': megakaryocyte_form,
             'cellcountformset': cellcount_formset,},
            context_instance=RequestContext(request))
