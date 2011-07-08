from django.forms.models import ModelForm
from web.webcontour.models import Contour


class ContourForm(ModelForm):
    class Meta:
        model = Contour
