from django.forms import ModelForm, HiddenInput

from cellcounter.main.models import CellCount, CellCountInstance, BoneMarrowBackground, ErythropoiesisFindings, GranulopoiesisFindings, MegakaryocyteFeatures

class CellCountInstanceForm(ModelForm):
    class Meta:
        model = CellCountInstance
        exclude = ('cell_count_instance', 'datetime_created', 'datetime_updated', 'user')

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
    auto_id = False

    class Meta:
        model = CellCount
        widgets = {
                'cell': HiddenInput(),
                'normal_count': HiddenInput,
                'abnormal_count': HiddenInput}
        exclude = ('cell_count_instance', 'comment',)
