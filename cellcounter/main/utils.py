"""Utility module for cellcounter"""
from django.forms.models import modelformset_factory

from cellcounter.main.models import CellCount, CellType
from cellcounter.main.forms import CellCountForm

def get_cellcount_formset():
    return modelformset_factory(CellCount, form=CellCountForm, extra=len(get_celltype_list()))

def get_celltype_list():
    celltypes = CellType.objects.all()
    celltype_list = []
    for celltype in celltypes:
        celltype_list.append({'cell': celltype})
    return celltype_list
