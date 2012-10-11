from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from cellcounter.main.forms import CellCountInstanceForm, BoneMarrowBackgroundForm, CellCountForm, GranulopoiesisFindingsForm, ErythropoiesisFindingsForm, MegakaryocyteFeaturesForm

from cellcounter.main.models import BoneMarrowBackground, CellCount, CellType, CellCountInstance

@login_required
def new_count(request):
    if request.method == 'POST':
        celltypes = CellType.objects.all()

        count_instance = CellCountInstanceForm(request.POST, prefix="cellcount")
        bm_background_info = BoneMarrowBackgroundForm(request.POST, prefix="bonemarrow")
        erythropoiesis_form = ErythropoiesisFindingsForm(request.POST, prefix="erythropoiesis")
        granulopoiesis_form =  GranulopoiesisFindingsForm(request.POST, prefix="granulopoiesis")
        megakaryocyte_form = MegakaryocyteFeaturesForm(request.POST, prefix="megakaryocyte")
        
        cellcount_forms_list = []
        for celltype in celltypes:
            cellcount_forms_list.append(CellCountForm(request.POST, prefix=celltype.machine_name))

        validation_list = [count_instance.is_valid(),
                           bm_background_info.is_valid(),
                           erythropoiesis_form.is_valid(),
                           granulopoiesis_form.is_valid(),
                           megakaryocyte_form.is_valid(),]

        for cellcount_form in cellcount_forms_list:
            validation_list.append(cellcount_form.is_valid())

        if all(validation_list):
            cellcount = count_instance.save(commit=False)
            cellcount.user = request.user
            cellcount.save()
            bm_background = bm_background_info.save(commit=False)
            erythropoiesis = erythropoiesis_form.save(commit=False)
            granulopoiesis = granulopoiesis_form.save(commit=False)
            megakaryocyte = megakaryocyte_form.save(commit=False)
            
            for cellcount_form in cellcount_forms_list:
                form = cellcount_form.save(commit=False)
                form.cell_count_instance = cellcount
                form.save()

            bm_background.cell_count_instance = cellcount
            bm_background.save()
            erythropoiesis.cell_count_instance = cellcount
            erythropoiesis.save()
            granulopoiesis.cell_count_instance = cellcount
            granulopoiesis.save()
            megakaryocyte.cell_count_instance = cellcount
            megakaryocyte.save()

            return HttpResponseRedirect('/')
        else:
            return render_to_response('main/submit.html',
                    {'cellcount': count_instance, 
                     'bonemarrowbackground': bm_background_info, 
                     'erythropoiesis_form': erythropoiesis_form, 
                     'granulopoiesis_form': granulopoiesis_form,
                     'megakaryocyte_form': megakaryocyte_form,
                     'cellcountformslist': cellcount_form_list,},
                    context_instance=RequestContext(request))
    else:
        
        cellcount_form = CellCountInstanceForm(prefix="cellcount")
        bonemarrowbackground = BoneMarrowBackgroundForm(prefix="bonemarrow")
        erythropoiesis_form = ErythropoiesisFindingsForm(prefix="erythropoiesis")
        granulopoiesis_form = GranulopoiesisFindingsForm(prefix="granulopoiesis")
        megakaryocyte_form = MegakaryocyteFeaturesForm(prefix="megakaryocyte")

        cellcount_form_list = []
        for celltype in CellType.objects.all():
            cellcount_form_list.append(CellCountForm(initial={'cell': celltype}, prefix=celltype.machine_name))

        return render_to_response('main/submit.html',
            {'cellcount': cellcount_form,
             'bonemarrowbackground': bonemarrowbackground,
             'erythropoiesis_form': erythropoiesis_form,
             'granulopoiesis_form': granulopoiesis_form,
             'megakaryocyte_form': megakaryocyte_form,
             'cellcountformslist': cellcount_form_list,},
            context_instance=RequestContext(request))

@login_required
def view_count(request, count_id):
    cell_count = get_object_or_404(CellCountInstance, pk=count_id)

    if request.user != cell_count.user:
        return HttpResponseForbidden()

    cellcount_list = cell_count.cellcount_set.all()

    count_total = 0
    for count in cellcount_list:
        count_total = count_total + count.normal_count
        count_total = count_total + count.abnormal_count

    return render_to_response('main/report.html',
            {'cellcount': cell_count,
             'bonemarrowbackground': cell_count.bonemarrowbackground,
             'erythropoiesis': cell_count.erythropoiesisfindings,
             'granulopoiesis': cell_count.granulopoiesisfindings,
             'megakaryocytes': cell_count.megakaryocytefeatures,
             'cellcount_list': cell_count.cellcount_set.all()},
            context_instance=RequestContext(request))

def edit_count(request):
    pass
