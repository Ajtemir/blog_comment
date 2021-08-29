from django import forms
from blog.models import Article, Category
from .models import Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['user', 'create', 'uploaded']

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.exclude(parent_id=None)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text'
        ]
