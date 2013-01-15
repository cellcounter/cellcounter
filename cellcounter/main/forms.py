from django.forms import ModelForm, HiddenInput, Textarea, CheckboxInput, Select, ValidationError

from cellcounter.main.models import CellCount, CellCountInstance, BoneMarrowBackground, ErythropoiesisFindings, GranulopoiesisFindings, MegakaryocyteFeatures, IronStain

COMMENT_WIDGET = {'comment': Textarea(attrs={'rows': 2, 'placeholder': 'Comments'})}
OVERALLCOMMENT_WIDGET = {'overall_comment': 
                            Textarea(attrs={'rows': 1,
                                            'class': 'span12',
                                            'placeholder': 'Overall comments'})}

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
        widgets = {'comment': Textarea(attrs={'rows': 2, 'placeholder': 'Comments'}),
                   'no_dysplasia': CheckboxInput(attrs={'onclick': 'erythropoiesis();'}),
                   'nuclear_asynchrony': CheckboxInput(attrs={'disabled': 'true'}),
                   'multinucleated_forms': CheckboxInput(attrs={'disabled': 'true'}),
                   'ragged_haemoglobinisation': CheckboxInput(attrs={'disabled': 'true'}),
                   'megaloblastic_change': CheckboxInput(attrs={'disabled': 'true'}),}

    def clean(self):
        cleaned_data = super(ErythropoiesisFindingsForm, self).clean()
        no_dysplasia = cleaned_data.get('no_dysplasia')
        nuclear_asynchrony = cleaned_data.get('nuclear_asynchrony')
        multinucleated_forms = cleaned_data.get('multinucleated_forms')
        ragged_haemoglobinisation = cleaned_data.get('ragged_haemoglobinisation')
        megaloblastic_change = cleaned_data.get('megaloblastic_change')

        if no_dysplasia == True:
            if any([nuclear_asynchrony,
                    multinucleated_forms,
                    ragged_haemoglobinisation,
                    megaloblastic_change]):
                raise ValidationError("Dysplasia given when No dysplasia has been ticked")
        else:
            if not any([nuclear_asynchrony,
                        multinucleated_forms,
                        ragged_haemoglobinisation,
                        megaloblastic_change]):
                raise ValidationError("Dysplasia suggested, but not characterised")

        return cleaned_data

class GranulopoiesisFindingsForm(ModelForm):
    class Meta:
        model = GranulopoiesisFindings
        exclude = ('cell_count_instance',) 
        widgets = {'comment': Textarea(attrs={'rows': 2, 'placeholder': 'Comments'}),
                   'no_dysplasia': CheckboxInput(attrs={'onclick': 'granulopoiesis();'}),
                   'hypogranular': CheckboxInput(attrs={'disabled': 'true'}),
                   'pelger': CheckboxInput(attrs={'disabled': 'true'}),
                   'nuclear_atypia': CheckboxInput(attrs={'disabled': 'true'}),
                   'dohle_bodies': CheckboxInput(attrs={'disabled': 'true'}),}

    def clean(self):
        cleaned_data = super(GranulopoiesisFindingsForm, self).clean()
        no_dysplasia = cleaned_data.get('no_dysplasia')
        hypogranular = cleaned_data.get('hypogranular ')
        pelger = cleaned_data.get('pelger')
        nuclear_atypia = cleaned_data.get('nuclear_atypia')
        dohle_bodies = cleaned_data.get('dohle_bodies')

        if no_dysplasia == True:
            if any([hypogranular, pelger, nuclear_atypia, dohle_bodies]):
                raise ValidationError("Dysplasia given when No dysplasia has been ticked")
        else:
            if not any([hypogranular, pelger, nuclear_atypia, dohle_bodies]):
                raise ValidationError("Dysplasia suggested, but not characterised")

        return cleaned_data

class MegakaryocyteFeaturesForm(ModelForm):
    class Meta:
        model = MegakaryocyteFeatures
        exclude = ('cell_count_instance',) 
        widgets = {'comment': Textarea(attrs={'rows': 2, 'placeholder': 'Comments'}),
                   'no_dysplasia': CheckboxInput(attrs={'onclick': 'megakaryocytes();'}),
                   'hypolobulated': CheckboxInput(attrs={'disabled': 'true'}),
                   'fragmented': CheckboxInput(attrs={'disabled': 'true'}),
                   'micromegakaryocytes': CheckboxInput(attrs={'disabled': 'true'}),}

    def clean(self):
        cleaned_data = super(MegakaryocyteFeaturesForm, self).clean()
        no_dysplasia = cleaned_data.get('no_dysplasia')
        hypolobulated = cleaned_data.get('hypolobulated')
        fragmented = cleaned_data.get('fragmented')
        micromegakaryocytes = cleaned_data.get('micromegakaryocytes')

        if no_dysplasia == True:
            if any([hypolobulated, fragmented, micromegakaryocytes]):
                raise ValidationError("Dysplasia characteristic given where no dysplasia has been ticked")
        else:
            if not any([hypolobulated, fragmented, micromegakaryocytes]):
                raise ValidationError("Dysplasia suggested, but not characterised")

        return cleaned_data

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
        widgets = {'comment': Textarea(attrs={'rows': 2,
                                              'placeholder': 'Comments',
                                              'disabled': True}),
                   'iron_content': Select(attrs={'disabled': True}),
                   'stain_performed': CheckboxInput(attrs={'onclick': 'ironstain();'}),
                   'ringed_sideroblasts': CheckboxInput(attrs={'disabled': True}),
                   }
