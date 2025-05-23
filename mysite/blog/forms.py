from django import forms
from .models import Comment

""" ? Django comes with two base classes to build forms
Form: This allows you to build standard forms by defining fields and validations.
ModelForm: This allows you to build forms tied to model instances. It provides all the func-
tionalities of the base Form class, but form fields can be explicitly declared, or automatically
generated, from model fields. The form can be used to create or edit model instances.
"""

class EmailPostForm(forms.Form):
    #? forms provide widget of HTML elements

    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
                required=False,
                widget=forms.Textarea
            )

class CommentForm(forms.ModelForm):
    #? Each model field type has a corresponding default form field type
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class SearchForm(forms.Form):
    query = forms.CharField()