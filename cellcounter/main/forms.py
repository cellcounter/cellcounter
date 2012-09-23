from django.forms import ModelForm

from cellcounter.main.models import CellCountInstance, BoneMarrowBackground

class CellCountInstanceForm(ModelForm):
    class Meta:
        model = CellCountInstance
        exclude = ('cell_count_instance',) 

class BoneMarrowBackgroundForm(ModelForm):
    class Meta:
        model = BoneMarrowBackground
        exclude = ('cell_count_instance',) 
