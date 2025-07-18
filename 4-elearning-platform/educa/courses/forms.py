from django.forms.models import inlineformset_factory
from .models import Course, Module

ModuleFormSet = inlineformset_factory(
    Course,
    Module,
    fields=['title', 'description'],
    # ? two empty extra sets
    extra=2,
    # ? # checkbox to mark for deletion
    can_delete=True
)
