from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image

from .models import CellType, CellImage
from .serializers import CellTypeSerializer


class CellTypesListView(APIView):
    def get(self, request):
        cell_types = CellType.objects.all()
        serializer = CellTypeSerializer(cell_types, many=True)
        return Response(serializer.data)


class NewCountTemplateView(TemplateView):
    template_name = 'main/count.html'

    def get_context_data(self, **kwargs):
        context = super(NewCountTemplateView, self).get_context_data(**kwargs)
        context['logged_in'] = self.request.user.is_authenticated()


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
                              {'images': ci.similar_cells()},
                              context_instance=RequestContext(request))


def thumbnail(request, cell_image_pk):
    ci = CellImage.objects.get(pk=cell_image_pk)

    image = Image.open(ci.file.file)
    thumb_image = image.crop((ci.thumbnail_left, ci.thumbnail_top,
                              ci.thumbnail_left + ci.thumbnail_width,
                              ci.thumbnail_top + ci.thumbnail_width))
    thumb_image = thumb_image.resize((200, 200), Image.ANTIALIAS)
    response = HttpResponse(mimetype="image/png")
    thumb_image.save(response, "PNG")
    return response


def page(request, cell_image_pk):
    ci = CellImage.objects.get(pk = cell_image_pk)    
    return render_to_response('main/image_page.html',
                              {'cellimage': ci},
                              context_instance=RequestContext(request))
