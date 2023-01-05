from django import forms

from .models import Comment

# code line


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 사용하고 싶은 것을 선택할때는 fields,
        # 빼고싶은것을 등록할때는 exclude
        fields = ('content',)
