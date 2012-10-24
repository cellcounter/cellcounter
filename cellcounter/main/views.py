from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.core import exceptions

from cellcounter.main.forms import CellCountInstanceForm, BoneMarrowBackgroundForm, CellCountForm, GranulopoiesisFindingsForm, ErythropoiesisFindingsForm, MegakaryocyteFeaturesForm, CellCountEditForm

from cellcounter.main.models import BoneMarrowBackground, ErythropoiesisFindings, GranulopoiesisFindings, MegakaryocyteFeatures, CellCount, CellType, CellCountInstance

from cellcounter.main.decorators import user_is_owner

class ListMyCountsView(ListView):

    template_name = "main/count_list.html"
    context_object_name = "count_list"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListMyCountsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return CellCountInstance.objects.filter(user=self.request.user)

class UserDetailView(DetailView):

    template_name = "main/user_detail.html"
    context_object_name = "user"
    model = User

    @method_decorator(login_required)
    @method_decorator(user_is_owner)
    def dispatch(self, *args, **kwargs):
        return super(UserDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['cellcount_list'] = CellCountInstance.objects.filter(user=self.request.user).order_by('datetime_submitted')[:5]
        return context

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

            messages.add_message(request, messages.INFO, 'Count submitted successfully')
            return HttpResponseRedirect(reverse('edit_count', kwargs={'count_id': cellcount.id}))

        else:
            return render_to_response('main/submit.html',
                    {'cellcount': count_instance, 
                     'bonemarrowbackground': bm_background_info, 
                     'erythropoiesis_form': erythropoiesis_form, 
                     'granulopoiesis_form': granulopoiesis_form,
                     'megakaryocyte_form': megakaryocyte_form,
                     'cellcountformslist': cellcount_forms_list,},
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

    return render_to_response('main/report.html',
            {'cellcount': cell_count,
             'bonemarrowbackground': cell_count.bonemarrowbackground,
             'erythropoiesis': cell_count.erythropoiesisfindings,
             'granulopoiesis': cell_count.granulopoiesisfindings,
             'megakaryocytes': cell_count.megakaryocytefeatures,
             'cellcount_list': cell_count.cellcount_set.all()},
            context_instance=RequestContext(request))

@login_required
def edit_count(request, count_id):
    cell_count = get_object_or_404(CellCountInstance, pk=count_id)
   
    if request.user != cell_count.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        celltypes = CellType.objects.all()
        count_instance = CellCountInstanceForm(request.POST,
                                               prefix="cellcount",
                                               instance=cell_count)
        
        instance = BoneMarrowBackground.objects.get(cell_count_instance=cell_count)
        bm_background_info = BoneMarrowBackgroundForm(request.POST,
                                                      prefix="bonemarrow",
                                                      instance=instance)
        
        instance = ErythropoiesisFindings.objects.get(cell_count_instance=cell_count)
        erythropoiesis_form = ErythropoiesisFindingsForm(request.POST,
                                                         prefix="erythropoiesis",
                                                         instance=instance)
        
        instance = GranulopoiesisFindings.objects.get(cell_count_instance=cell_count)
        granulopoiesis_form =  GranulopoiesisFindingsForm(request.POST,
                                                          prefix="granulopoiesis",
                                                          instance=instance)
        
        instance = MegakaryocyteFeatures.objects.get(cell_count_instance=cell_count)
        megakaryocyte_form = MegakaryocyteFeaturesForm(request.POST, 
                                                       prefix="megakaryocyte",
                                                       instance=instance)

        cellcount_form_list = []
        for celltype in celltypes:
            instance = CellCount.objects.get(cell_count_instance=cell_count,
                                             cell=celltype)
            cellcount_form_list.append(CellCountEditForm(request.POST,
                                                         prefix=celltype.machine_name,
                                                         instance=instance))

        validation_list = [count_instance.is_valid(),
                           bm_background_info.is_valid(),
                           erythropoiesis_form.is_valid(),
                           granulopoiesis_form.is_valid(),
                           megakaryocyte_form.is_valid(),]

        for cellcount_form in cellcount_form_list:
            validation_list.append(cellcount_form.is_valid())

        if all(validation_list):
            count_instance.save()
            bm_background_info.save()
            erythropoiesis_form.save()
            granulopoiesis_form.save()
            megakaryocyte_form.save()

            for cellcount_form in cellcount_form_list:
                cellcount_form.save()

            messages.add_message(request, messages.INFO, 'Count edited successfully')
            return HttpResponseRedirect(reverse('view_count', kwargs={'count_id': cell_count.id}))

        else:
            return render_to_response('main/edit.html',
                    {'cellcountinstance_form': count_instance, 
                     'bonemarrowbackground_form': bm_background_info, 
                     'erythropoiesis_form': erythropoiesis_form, 
                     'granulopoiesis_form': granulopoiesis_form,
                     'megakaryocyte_form': megakaryocyte_form,
                     'cellcount_form_list': cellcount_form_list,},
                    context_instance=RequestContext(request))

    else:
        cellcountinstance_form = CellCountInstanceForm(prefix="cellcount", instance=cell_count)
        bonemarrowbackground_form = BoneMarrowBackgroundForm(prefix="bonemarrow", instance=cell_count.bonemarrowbackground)
        erythropoiesis_form = ErythropoiesisFindingsForm(prefix="erythropoiesis", instance=cell_count.erythropoiesisfindings)
        granulopoiesis_form = GranulopoiesisFindingsForm(prefix="granulopoiesis", instance=cell_count.granulopoiesisfindings)
        megakaryocyte_form = MegakaryocyteFeaturesForm(prefix="megakaryocyte", instance=cell_count.megakaryocytefeatures)

        cellcount_form_list = []
        for cellcount in cell_count.cellcount_set.all():
            cellcount_form = CellCountEditForm(instance=cellcount, prefix=cellcount.cell.machine_name)
            cellcount_form_list.append(cellcount_form) 

        return render_to_response('main/edit.html',
                {'cellcountinstance_form': cellcountinstance_form,
                'bonemarrowbackground_form': bonemarrowbackground_form,
                'erythropoiesis_form': erythropoiesis_form,
                'granulopoiesis_form': granulopoiesis_form,
                'megakaryocyte_form': megakaryocyte_form,
                'cellcount_form_list': cellcount_form_list},
                context_instance=RequestContext(request))
