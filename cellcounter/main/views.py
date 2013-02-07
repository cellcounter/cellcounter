from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.core import exceptions
from django.conf import settings
from PIL import Image
import os.path

from cellcounter.main.models import CellType, CellImage

from cellcounter.main.decorators import user_is_owner
from cellcounter.mixins import JSONResponseMixin

class ListCellTypesView(JSONResponseMixin, ListView):
    model = CellType

    def get_context_data(self, *args, **kwargs):
        objects = self.object_list
        new_context = {}
        for cell in objects:
            cell_dict = {
                'id': cell.pk,
                'name': cell.readable_name,
                'slug': cell.machine_name,
                'abbr': cell.abbr_name,
                'colour': cell.visualisation_colour
            }
            new_context[cell.pk] = cell_dict

        return new_context

def new_count(request):
        cellcount_form_list = []
        for celltype in CellType.objects.all():
            cellcount_form_list.append(celltype)

        return render_to_response('main/submit.html',
            {'cellcountformslist': cellcount_form_list,
             'logged_in': request.user.is_authenticated(),},
            context_instance=RequestContext(request))


def images_by_cell_type(request, cell_type):
    if request.user.is_active and request.user.is_staff:
        ct = CellType.objects.get(machine_name = cell_type)
        return render_to_response('main/images_by_cell_type.html',
                {'images': ct.cellimage_set.all(),},
                context_instance=RequestContext(request))
    else:
        return render_to_response('main/images_by_cell_type.html',
                {'images': {}},
                context_instance=RequestContext(request))

def similar_images(request, cell_image_pk):
    ci = CellImage.objects.get(pk = cell_image_pk)
    return render_to_response('main/images_by_cell_type.html',
                {'images': ci.similar_cells(),},
                context_instance=RequestContext(request))

def thumbnail(request, cell_image_pk):
    ci = CellImage.objects.get(pk = cell_image_pk)

    image = Image.open(ci.file.file)
    thumb_image = image.crop((ci.thumbnail_left, ci.thumbnail_top, ci.thumbnail_left + ci.thumbnail_width, ci.thumbnail_top + ci.thumbnail_width))
    thumb_image = thumb_image.resize((200, 200), Image.ANTIALIAS)
    response = HttpResponse(mimetype="image/png")
    thumb_image.save(response, "PNG")
    return response

def page(request, cell_image_pk):
    ci = CellImage.objects.get(pk = cell_image_pk)    
    return render_to_response('main/image_page.html',
                {'cellimage': ci},
                context_instance=RequestContext(request))
