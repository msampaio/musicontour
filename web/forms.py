from django.forms.models import ModelForm
from visimus.mcontour.models import Contour


class ContourForm(ModelForm):
    class Meta:
        model = Contour
