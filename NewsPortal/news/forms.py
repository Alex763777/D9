from django import forms
from django.core.exceptions import ValidationError

from .models import Post
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'category']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        name = cleaned_data.get("title")

        if name == description:
            raise ValidationError(
                "Содержание не должно быть идентично названию новости."
            )

        return cleaned_data

class ArticlesForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'category']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        name = cleaned_data.get("title")

        if name == description:
            raise ValidationError(
                "Содержание не должно быть идентично названию статьи."
            )

        return cleaned_data
