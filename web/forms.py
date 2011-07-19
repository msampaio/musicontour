from django.forms.models import ModelForm
from models import Contour


class ContourForm(ModelForm):
    class Meta:
        model = Contour
