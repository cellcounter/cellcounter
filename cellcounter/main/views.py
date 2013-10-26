from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView
from PIL import Image

from cellcounter.main.models import CellType, CellImage

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

        return render_to_response('main/count.html',
            {'cellcountformslist': cellcount_form_list,
             'logged_in': request.user.is_authenticated(),},
            context_instance=RequestContext(request))


def images_by_cell_type(request, cell_type):
    ct = CellType.objects.get(machine_name = cell_type)
    images = []
    copyrightholders = []
    for ci in ct.cellimage_set.all():
        if ci.copyright not in copyrightholders:
            copyrightholders.append(ci.copyright)
        images.append((copyrightholders.index(ci.copyright) + 1, ci))  
    return render_to_response('main/images_by_cell_type.html',
            {'images': images,
             'copyrightholders': copyrightholders},
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
