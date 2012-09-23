from django.forms import ModelForm

from cellcounter.main.models import CellCountInstance

class CellCountInstanceForm(ModelForm):
    class Meta:
        model = CellCountInstance 
