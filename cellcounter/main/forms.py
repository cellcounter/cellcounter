from django.forms import Form, HiddenInput, Textarea, CheckboxInput, Select, ValidationError


COMMENT_WIDGET = {'comment': Textarea(attrs={'rows': 2, 'placeholder': 'Comments'})}
OVERALLCOMMENT_WIDGET = {'overall_comment': Textarea(attrs={'rows': 1, 
                         'class': 'span12', 'placeholder': 'Overall comments'})}


