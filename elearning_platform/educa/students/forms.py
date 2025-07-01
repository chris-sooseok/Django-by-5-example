from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    # ? initially none query create an empty queryset that doesn't return anything and doesn't query database
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        super(CourseEnrollForm, self).__init__(*args, **kwargs)
        # ? populating coursr choices
        self.fields['course'].queryset = Course.objects.all()

