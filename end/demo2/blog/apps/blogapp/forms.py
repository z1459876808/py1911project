from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'url', 'email', 'body']
        lables = {
            'name': '名字:',
            'url': '主页:',
            'email': '邮箱:',
            'body': '正文:'

        }
        widgets = {
            'body': forms.Textarea()
        }
