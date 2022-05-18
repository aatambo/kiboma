from django import forms
from django.core.validators import FileExtensionValidator


class FileUploadForm(forms.Form):
    csv = forms.FileField(validators=[FileExtensionValidator(["csv"])])
    min_support = forms.FloatField()
