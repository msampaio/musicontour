from django.forms.models import ModelForm
from models import Contour, Operation


class OperationForm(ModelForm):
    class Meta:
        model = Operation


class ContourForm(ModelForm):
    class Meta:
        model = Contour
