from django.forms import ModelForm
from django import forms

from cellcounter.main.models import CellCountInstance, BoneMarrowBackground

class CellCountInstanceForm(ModelForm):

    overall_comment = forms.CharField(widget=forms.Textarea(attrs={'style':'width: 100%'}))

    class Meta:
        model = CellCountInstance
        exclude = ('cell_count_instance',) 

class BoneMarrowBackgroundForm(ModelForm):
    class Meta:
        model = BoneMarrowBackground
        exclude = ('cell_count_instance',) 
