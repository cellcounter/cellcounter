from django.forms import ModelForm, HiddenInput, Textarea

from cellcounter.main.models import CellCount, CellCountInstance, BoneMarrowBackground, ErythropoiesisFindings, GranulopoiesisFindings, MegakaryocyteFeatures, IronStain

COMMENT_WIDGET = {'comment': Textarea(attrs={'rows': 2, 'placeholder': 'Comments'})}
OVERALLCOMMENT_WIDGET = {'overall_comment': Textarea(attrs={'rows': 1, 'class': 'span12', 'placeholder': 'Overall comments'})}

class CellCountInstanceForm(ModelForm):
    class Meta:
        model = CellCountInstance
        exclude = ('datetime_created', 'datetime_updated', 'user')
        widgets = OVERALLCOMMENT_WIDGET

class BoneMarrowBackgroundForm(ModelForm):
    class Meta:
        model = BoneMarrowBackground
        exclude = ('cell_count_instance',) 

class ErythropoiesisFindingsForm(ModelForm):
    class Meta:
        model = ErythropoiesisFindings
        exclude = ('cell_count_instance',) 
        widgets = COMMENT_WIDGET

class GranulopoiesisFindingsForm(ModelForm):
    class Meta:
        model = GranulopoiesisFindings
        exclude = ('cell_count_instance',) 
        widgets = COMMENT_WIDGET

class MegakaryocyteFeaturesForm(ModelForm):
    class Meta:
        model = MegakaryocyteFeatures
        exclude = ('cell_count_instance',) 
        widgets = COMMENT_WIDGET

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
        widgets = COMMENT_WIDGET

class IronStainForm(ModelForm):
    class Meta:
        model = IronStain
        exclude = ('cell_count_instance',) 
        widgets = COMMENT_WIDGET
