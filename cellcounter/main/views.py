from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, ListView, DetailView
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
        return context


class CellImageListView(ListView):
    model = CellImage
    template_name = 'main/images_by_cell_type.html'

    def get_queryset(self):
        return CellImage.objects.filter(celltype__machine_name__iexact=self.kwargs['cell_type'])

    def get_context_data(self, **kwargs):
        copyright_holders = []
        image_list = []
        context = super(CellImageListView, self).get_context_data(**kwargs)
        if context['object_list']:
            for image in self.object_list:
                if image.copyright not in copyright_holders:
                    copyright_holders.append(image.copyright)
                image_list.append((copyright_holders.index(image.copyright) + 1, image))
            context.pop('object_list')
            context['images'] = image_list
            context['copyrightholders'] = copyright_holders
        return context


class CellImageDetailView(DetailView):
    model = CellImage
    context_object_name = 'cellimage'
    template_name = 'main/image_page.html'
    pk_url_kwarg = 'cell_image_pk'


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