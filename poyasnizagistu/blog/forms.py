from django import forms
from django.forms import Textarea

from blog.models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentsPost
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


