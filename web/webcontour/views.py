from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from web.webcontour.forms import ContourForm
from web.webcontour.models import Contour
import contour.contour as cc
import contour.plot as cp

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
    cseg = cc.Contour([int(x) for x in cont.strip().split()])
    prime_s = cseg.prime_form_sampaio()
    prime_ml = cseg.prime_form_marvin_laprade()
    retrograde = cseg.retrograde()
    inversion = cseg.inversion()
    normal = cseg.translation()
    int_1 = cseg.internal_diagonals()
    cp.contour_lines_save_django([cseg, 'k', 'Original'],
                                 [prime_ml, 'r', 'Prime form ML'],
                                 [prime_s, 'b', 'Prime form S'],
                                 [retrograde, 'g', 'Retrograde'],
                                 [inversion, 'y', 'Inversion'])
    args = {'cseg': cseg, 'prime_s': prime_s, 'prime_ml': prime_ml,
            'retrograde': retrograde, 'inversion': inversion,
            'normal': normal, 'int_1': int_1}
    return render(request, 'contour.html', args)
