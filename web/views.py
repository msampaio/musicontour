from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from forms import ContourForm, OperationForm
from models import Contour, Operation
import MusiContour.contour.contour as cc
import MusiContour.contour.plot as cp
import MusiContour.contour.auxiliary as ca


def main_page(request):
    return render(request, 'main_page.html', {})

def contour_form(request):
    if request.method == "POST":
        form = ContourForm(request.POST)
        if form.is_valid():
            request.session['contour'] = form.cleaned_data['contour_points']
            request.session['operation'] = form.cleaned_data['operation']
            return HttpResponseRedirect('/MusiContour/show/')
    else:
        form = ContourForm()

    args = {'form': form}

    return render(request, 'contour_form.html', args)


def contour_show(request):
    cont = request.session['contour']
    ops_dic = request.session['operation'].values()
    cseg = cc.Contour([int(x) for x in cont.strip().split()])

    args = {'cseg': cseg}
    graph = [[cseg, 'k', 'Original']]
    ar = []
    for op_dic in ops_dic:
        operation = op_dic['operation']
        op_name = op_dic['op_name']
        op_color = op_dic['op_color']
        op = ca.apply_fn(cseg, operation)
        if op_dic['op_type'] == 'g':
            graph.append([op, op_color, operation])
        ar.append([op_name, op])

    cp.contour_lines_save_django(*graph)

    args = {'cseg': cseg, 'op_dicts': ar}

    return render(request, 'contour_show.html', args)
