from markdownx.fields import MarkdownxFormField
from django import forms


class MyForm(forms.Form):
    myfield = MarkdownxFormField()
