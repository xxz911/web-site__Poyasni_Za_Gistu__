from django import forms


from blog.models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments_Post
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


