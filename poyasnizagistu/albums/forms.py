from django import forms

from albums.models import Comments_Album
from blog.models import *

class CommentAlbumForm(forms.ModelForm):
    class Meta:
        model = Comments_Album
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


