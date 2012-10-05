from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext

from cellcounter.main.forms import CellCountInstanceForm, BoneMarrowBackgroundForm, CellCountForm, GranulopoiesisFindingsForm, ErythropoiesisFindingsForm, MegakaryocyteFeaturesForm

from cellcounter.main.models import BoneMarrowBackground, CellCount, CellType
from cellcounter.main.utils import get_cellcount_formset, get_celltype_list

def new_count(request):
    if request.method == 'POST':
        cellcount_formset = get_cellcount_formset() 
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
            cellcount = count_instance.save()
            bm_background = bm_background_info.save(commit=False)
            erythropoiesis = erythropoiesis_form.save(commit=False)
            granulopoiesis = granulopoiesis_form.save(commit=False)
            megakaryocyte = megakaryocyte_form.save(commit=False)

            bm_background.cell_count_instance = cellcount
            bm_background.save()
            erythropoiesis.cell_count_instance = cellcount
            erythropoiesis.save()
            granulopoiesis.cell_count_instance = cellcount
            granulopoiesis.save()
            megakaryocyte.cell_count_instance = cellcount
            megakaryocyte.save()

            for cell_count in cellcount_formset.save(commit=False):
                cell_count.cell_count_instance = cellcount
                cell_count.save()

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
        cellcount_formset = get_cellcount_formset() 
        bonemarrowbackground = BoneMarrowBackgroundForm(prefix="bonemarrow")
        erythropoiesis_form = ErythropoiesisFindingsForm(prefix="erythropoiesis")
        granulopoiesis_form = GranulopoiesisFindingsForm(prefix="granulopoiesis")
        megakaryocyte_form = MegakaryocyteFeaturesForm(prefix="megakaryocyte")
        cellcount_formset = cellcount_formset(initial=get_celltype_list(), prefix='celltypecount')

    return render_to_response('main/submit.html',
            {'cellcount': cellcount_form,
             'bonemarrowbackground': bonemarrowbackground,
             'erythropoiesis_form': erythropoiesis_form,
             'granulopoiesis_form': granulopoiesis_form,
             'megakaryocyte_form': megakaryocyte_form,
             'cellcountformset': cellcount_formset,},
            context_instance=RequestContext(request))

def view_count(request):
    pass

def edit_count(request):
    pass
