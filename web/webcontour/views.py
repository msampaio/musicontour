from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from web.webcontour.forms import ContourForm
from web.webcontour.models import Contour


def home(request):
    if request.method == "POST":
        form = ContourForm(request.POST)
        if form.is_valid():
            request.session['contour'] = form.cleaned_data['cps']
            return HttpResponseRedirect('/contour/')
    else:
        form = ContourForm()

    args = {'form': form}

    return render(request, 'home.html', args)


def contour(request):
    cont = request.session['contour']
    contornos = [int(x) + 13 for x in cont.strip().split()]
    args = {'contour': contornos}
    return render(request, 'contour.html', args)

