from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from forms import ContourForm
from models import Contour
import MusiContour.contour.contour as cc
import MusiContour.contour.plot as cp
import MusiContour.contour.auxiliary as ca


def main_page(request):
    return render(request, 'main_page.html', {})

def contour_form(request):
    if request.method == "POST":
        form = ContourForm(request.POST)
        if form.is_valid():
            request.session['contour'] = form.cleaned_data['cps']
            request.session['operation'] = form.cleaned_data['operation']
            if form.cleaned_data['operation'] == 'all':
                return HttpResponseRedirect('/MusiContour/show_all/')
            else:
                return HttpResponseRedirect('/MusiContour/show_one/')
    else:
        form = ContourForm()

    args = {'form': form}

    return render(request, 'contour_form.html', args)


def contour_show_all(request):
    cont = request.session['contour']
    cseg = cc.Contour([int(x) for x in cont.strip().split()])
    round_ind = 2

    prime_s = cseg.prime_form_sampaio()
    prime_ml = cseg.prime_form_marvin_laprade()
    retrograde = cseg.retrograde()
    inversion = cseg.inversion()
    normal = cseg.translation()
    int_1 = cseg.internal_diagonals()
    morris_reduction = cseg.reduction_morris()
    casv = cseg.adjacency_series_vector()
    cia = cseg.interval_array()
    class_index_i = round(cseg.class_index_i(), round_ind)
    class_index_ii = round(cseg.class_index_ii(), round_ind)
    symmetry_index = round(cseg.symmetry_index(), round_ind)

    cp.contour_lines_save_django([cseg, 'k', 'Original'],
                                 [prime_ml, 'r', 'Prime form ML'],
                                 [prime_s, 'b', 'Prime form S'],
                                 [retrograde, 'g', 'Retrograde'],
                                 [inversion, 'y', 'Inversion'])

    args = {'cseg': cseg, 'prime_s': prime_s, 'prime_ml': prime_ml,
            'retrograde': retrograde, 'inversion': inversion,
            'normal': normal, 'int_1': int_1, 'reduction': morris_reduction,
            'casv': casv, 'class_index_i': class_index_i,
            'class_index_ii': class_index_ii, 'symmetry_index': symmetry_index}

    return render(request, 'contour_show_all.html', args)


def contour_show_one(request):
    cont = request.session['contour']
    operation = request.session['operation']
    cseg = cc.Contour([int(x) for x in cont.strip().split()])
    op = ca.apply_fn(cseg, operation)
    cp.contour_lines_save_django([cseg, 'k', 'Original'],
                                 [op, 'b', operation])
    args = {'cseg': cseg, 'op_name': operation, 'op': op}

    return render(request, 'contour_show_one.html', args)
