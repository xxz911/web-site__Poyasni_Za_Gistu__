from django import forms

from articles.models import Comments_Article


class CommentArticleForm(forms.ModelForm):
    class Meta:
        model = Comments_Article
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


