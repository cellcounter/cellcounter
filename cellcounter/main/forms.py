from django.forms import ModelForm, HiddenInput

from cellcounter.main.models import CellCount, CellCountInstance, BoneMarrowBackground, ErythropoiesisFindings, GranulopoiesisFindings, MegakaryocyteFeatures

class CellCountInstanceForm(ModelForm):
    class Meta:
        model = CellCountInstance
        exclude = ('datetime_created', 'datetime_updated', 'user')

class BoneMarrowBackgroundForm(ModelForm):
    class Meta:
        model = BoneMarrowBackground
        exclude = ('cell_count_instance',) 

class ErythropoiesisFindingsForm(ModelForm):
    class Meta:
        model = ErythropoiesisFindings
        exclude = ('cell_count_instance',) 

class GranulopoiesisFindingsForm(ModelForm):
    class Meta:
        model = GranulopoiesisFindings
        exclude = ('cell_count_instance',) 

class MegakaryocyteFeaturesForm(ModelForm):
    class Meta:
        model = MegakaryocyteFeatures
        exclude = ('cell_count_instance',) 

class CellCountForm(ModelForm):
    class Meta:
        model = CellCount
        widgets = {
                'cell': HiddenInput(),
                'normal_count': HiddenInput,
                'abnormal_count': HiddenInput}
        exclude = ('cell_count_instance', 'comment',)

class CellCountEditForm(ModelForm):
    class Meta:
        model = CellCount
        fields = ('normal_count', 'abnormal_count', 'comment')

class IronStainForm(ModelForm):
    class Meta:
        model = IronStain
        exclude = ('cell_count_instance',) 
