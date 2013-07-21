from django.forms import Textarea


COMMENT_WIDGET = {'comment': Textarea(attrs={'rows': 2, 'placeholder': 'Comments'})}
OVERALLCOMMENT_WIDGET = {'overall_comment': Textarea(attrs={'rows': 1, 
                         'class': 'span12', 'placeholder': 'Overall comments'})}


