#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Frame, Button, Entry, Label, Text, Scrollbar, \
     TOP, LEFT, RIGHT, X, Y, END
from plot import plot_preview
from contour import internal_diagonal_print, Contour, Internal_diagonal

program_name = "Villa Lobos Contour Module"
version = "0.1"


class App:

    def __init__(self, master):

        title_frame = Frame(master)
        title_frame.pack(pady=5)

        frame0 = Frame(master)
        frame0.pack(side=TOP, fill=X)

        frame1 = Frame(master)
        frame1.pack(side=TOP, fill=X)

        frame2 = Frame(master)
        frame2.pack(side=TOP, fill=X)

        frame3 = Frame(master)
        frame3.pack(side=TOP, fill=X)

        toolbar1 = Frame(master)
        toolbar1.pack(side=LEFT, pady=5, fill=X)

        toolbar2 = Frame(master)
        toolbar2.pack(side=LEFT, pady=5, fill=X)

        toolbar3 = Frame(master)
        toolbar3.pack(side=TOP, pady=5, fill=X)

        font = 'sans 8 bold'
        self.initial = Label(title_frame, text=program_name, font=font)
        self.initial.pack(side=TOP)

        ## toolbar1

        self.plot = Button(toolbar1, text="Plot", command=self.plot,
                           width=10)
        self.plot.pack(side=TOP)

        self.retrograde = Button(toolbar1, text="Retrograde",
                                    command=self.retrograde, width=10)
        self.retrograde.pack(side=TOP)

        self.rotation = Button(toolbar1, text="Rotation",
                               command=self.rotation, width=10)
        self.rotation.pack(side=TOP)

        self.n_subsets = Button(toolbar1, text="n subsets",
                               command=self.n_subsets, width=10)
        self.n_subsets.pack(side=TOP)

        self.casv = Button(toolbar1, text="CASV",
                               command=self.casv, width=10)
        self.casv.pack(side=TOP)

        self.ccvi = Button(toolbar1, text="CCV I",
                               command=self.ccvi, width=10)
        self.ccvi.pack(side=TOP)

        ## toolbar2

        self.prime_form = Button(toolbar2, text="Prime form",
                                    command=self.prime_form, width=10)
        self.prime_form.pack(side=TOP)

        self.inversion = Button(toolbar2, text="Inversion",
                                   command=self.inversion, width=10)
        self.inversion.pack(side=TOP)

        self.comparison_matrix = Button(toolbar2, text="COM Matrix",
                               command=self.comparison_matrix, width=10)
        self.comparison_matrix.pack(side=TOP)

        self.n_subsets = Button(toolbar2, text="All subsets",
                               command=self.all_subsets, width=10)
        self.n_subsets.pack(side=TOP)

        self.cis = Button(toolbar2, text="CIS",
                               command=self.cis, width=10)
        self.cis.pack(side=TOP)

        self.ccvii = Button(toolbar2, text="CCV II",
                               command=self.ccvii, width=10)
        self.ccvii.pack(side=TOP)

        # toolbar3

        self.normal_form = Button(toolbar3, text="Normal form",
                                     command=self.normal_form, width=10)
        self.normal_form.pack(side=TOP)

        self.ret_inv = Button(toolbar3, text="Retrograde inv.",
                                 command=self.ret_inv, width=10)
        self.ret_inv.pack(side=TOP)

        self.internal = Button(toolbar3, text="Int. Diagonal",
                               command=self.internal, width=10)
        self.internal.pack(side=TOP)

        self.csegs_from_int = Button(toolbar3, text="Csegs from INT",
                               command=self.csegs_from_int, width=10)
        self.csegs_from_int.pack(side=TOP)

        self.cia = Button(toolbar3, text="CIA",
                               command=self.cia, width=10)
        self.cia.pack(side=TOP)

        #

        Label(frame1, text='main entry:').pack(side=LEFT)

        self.cseg_entry = Entry(frame1, width=20)
        self.cseg_entry.pack(fill=X)
        self.cseg_entry.insert('end', "0 3 1 2")
        self.cseg_entry.get()

        Label(frame2, text='parameter:').pack(side=LEFT)

        self.param_entry = Entry(frame2, width=5)
        self.param_entry.pack(fill=X)
        self.param_entry.insert("end", "1")
        self.param_entry.get()

        self.text_output = Text(frame0, width=44, height=15)
        self.text_output.pack(side=LEFT, fill=X)

        self.text_scroll = Scrollbar(frame0)
        self.text_scroll.pack(side=RIGHT, fill=Y)
        self.text_scroll.config(command=self.text_output.yview)
        self.text_output.config(yscrollcommand=self.text_scroll.set)

    def plot(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        result = Contour(cseg).cseg_visual_printing()
        text = "Plot: "
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(cseg)

    def prime_form(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        card, c_class, prime_form = Contour(cseg).contour_segment_class()
        prime_form_printed = Contour(prime_form).cseg_visual_printing()
        result = "{0}-{1} {2}".format(card, c_class, prime_form_printed)
        text = "Prime form: "
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(prime_form)

    def normal_form(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        normal_form = Contour(cseg).translation()
        result = Contour(normal_form).cseg_visual_printing()
        text = "Normal form: "
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(normal_form)

    def retrograde(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        retrograde = Contour(cseg).retrograde()
        result = Contour(retrograde).cseg_visual_printing()
        text = "Retrograde: "
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(retrograde)

    def inversion(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        inversion = Contour(cseg).inversion()
        result = Contour(inversion).cseg_visual_printing()
        text = "Inversion: "
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(inversion)

    def ret_inv(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        ret_inv = Contour(Contour(cseg).retrograde()).inversion()
        result = Contour(ret_inv).cseg_visual_printing()
        text = "Ret. Inv.: "
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(ret_inv)

    def rotation(self):
        get = self.cseg_entry.get()
        param_get = int(self.param_entry.get())
        cseg = [int(x) for x in get.split(' ') if x]
        rotation = Contour(cseg).rotation(param_get)
        result = Contour(rotation).cseg_visual_printing()
        text = "Rotation ({0}): ".format(param_get)
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(rotation)

    def internal(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        param_get = int(self.param_entry.get())
        int_diag = Contour(cseg).internal_diagonals(param_get)
        format_int_diag = internal_diagonal_print(int_diag)
        text = "Internal diagonal ({0}): ".format(param_get)
        self.text_output.insert(END, text)
        self.text_output.insert(END, format_int_diag)
        self.text_output.insert(END, "\n")

    def comparison_matrix(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        com_matrix = Contour(cseg).comparison_matrix_printing()
        text = "Comparison Matrix:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, com_matrix)
        self.text_output.insert(END, "\n")

    def n_subsets(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        param_get = int(self.param_entry.get())
        csubset = Contour(cseg).contour_subsets(param_get)
        result = "\n".join([Contour(x).cseg_visual_printing() for x in csubset])
        plural = "s" if param_get > 1 else ""
        text = "Contour subsets ({0} element{1}):\n".format(param_get, plural)
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")

    def all_subsets(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        csubset = Contour(cseg).contour_all_subsets()
        result = "\n".join([Contour(x).cseg_visual_printing() for x in csubset])
        text = "All contour subsets:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")

    def csegs_from_int(self):
        get = self.cseg_entry.get()
        int_d = [int(x) for x in get.split(' ') if x]
        param_get = int(self.param_entry.get())
        csegs = Internal_diagonal(int_d).csegs(param_get)
        result = "\n".join([Contour(x).cseg_visual_printing() for x in csegs])
        plural = "s" if param_get > 1 else ""
        text = "Csegs:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")

    def casv(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        casv = Contour(cseg).contour_adjacency_series_vector()
        text = "Contour Adjacency Series Vector:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, casv)
        self.text_output.insert(END, "\n")

    def cis(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        cis = Contour(cseg).contour_interval_succession()
        result = Contour(cis).cseg_visual_printing()
        text = "Contour Interval Succession:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")

    def cia(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        cia = list(Contour(cseg).contour_interval_array())
        text = "Contour Interval Array:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, cia)
        self.text_output.insert(END, "\n")

    def ccvi(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        ccvi = list(Contour(cseg).contour_class_vector_i())
        text = "Contour class vector I:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, ccvi)
        self.text_output.insert(END, "\n")

    def ccvii(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        ccvii = list(Contour(cseg).contour_class_vector_ii())
        text = "Contour class vector II:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, ccvii)
        self.text_output.insert(END, "\n")

root = Tk()
root.title(program_name + " v." + version)

app = App(root)

root.mainloop()
