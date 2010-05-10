#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import (Tk, Frame, Button, Entry, Label, Text, Scrollbar,
     TOP, LEFT, RIGHT, X, Y, END)
from contour_module.contour import (Contour, Internal_diagonal,
     cseg_similarity, replace_plus_minus_to_list, Comparison_matrix)
from contour_module.plot import (plot_preview, clear_plot)

program_name = "Villa-Lobos Contour Module"
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

        toolbar0 = Frame(master)
        toolbar0.pack(side=TOP, fill=X)

        toolbar1 = Frame(master)
        toolbar1.pack(side=LEFT, pady=5, fill=X)

        toolbar2 = Frame(master)
        toolbar2.pack(side=LEFT, pady=5, fill=X)

        toolbar3 = Frame(master)
        toolbar3.pack(side=LEFT, pady=5, fill=X)

        font = 'sans 8 bold'
        self.initial = Label(title_frame, text=program_name + " v." + version, font=font)
        self.initial.pack(side=TOP)

        ## toolbar0

        self.b_clear_output = Button(toolbar0, text="Clear Output",
                               command=self.clear_output, width=10)
        self.b_clear_output.pack(side=TOP)

        self.b_clear_plot = Button(toolbar0, text="Clear Plot",
                               command=self.clear_plot, width=10)
        self.b_clear_plot.pack(side=TOP)

        ## toolbar1

        self.b_plot = Button(toolbar1, text="Plot", command=self.plot,
                           width=10)
        self.b_plot.pack(side=TOP)

        self.b_retrograde = Button(toolbar1, text="Retrograde",
                                    command=self.retrograde, width=10)
        self.b_retrograde.pack(side=TOP)

        self.b_rotation = Button(toolbar1, text="Rotation",
                               command=self.rotation, width=10)
        self.b_rotation.pack(side=TOP)

        self.b_n_subsets = Button(toolbar1, text="n subsets",
                               command=self.n_subsets, width=10)
        self.b_n_subsets.pack(side=TOP)

        self.b_casv = Button(toolbar1, text="CASV",
                               command=self.casv, width=10)
        self.b_casv.pack(side=TOP)

        self.b_ccvi = Button(toolbar1, text="CCV I",
                               command=self.ccvi, width=10)
        self.b_ccvi.pack(side=TOP)

        ## toolbar2

        self.b_prime_form = Button(toolbar2, text="Prime form",
                                    command=self.prime_form, width=10)
        self.b_prime_form.pack(side=TOP)

        self.b_inversion = Button(toolbar2, text="Inversion",
                                   command=self.inversion, width=10)
        self.b_inversion.pack(side=TOP)

        self.b_comparison_matrix = Button(toolbar2, text="COM Matrix",
                               command=self.comparison_matrix, width=10)
        self.b_comparison_matrix.pack(side=TOP)

        self.b_all_subsets = Button(toolbar2, text="All subsets",
                               command=self.all_subsets, width=10)
        self.b_all_subsets.pack(side=TOP)

        self.b_cis = Button(toolbar2, text="CIS",
                               command=self.cis, width=10)
        self.b_cis.pack(side=TOP)

        self.b_ccvii = Button(toolbar2, text="CCV II",
                               command=self.ccvii, width=10)
        self.b_ccvii.pack(side=TOP)

        # toolbar3

        self.b_normal_form = Button(toolbar3, text="Normal form",
                                     command=self.normal_form, width=10)
        self.b_normal_form.pack(side=TOP)

        self.b_ret_inv = Button(toolbar3, text="Retrograde inv.",
                                 command=self.ret_inv, width=10)
        self.b_ret_inv.pack(side=TOP)

        self.b_internal = Button(toolbar3, text="Int. Diagonal",
                               command=self.internal, width=10)
        self.b_internal.pack(side=TOP)

        self.b_csegs_from_int = Button(toolbar3, text="Csegs from INT",
                               command=self.csegs_from_int, width=10)
        self.b_csegs_from_int.pack(side=TOP)

        self.b_cia = Button(toolbar3, text="CIA",
                               command=self.cia, width=10)
        self.b_cia.pack(side=TOP)

        self.b_csim = Button(toolbar3, text="Contour simil.",
                               command=self.csim, width=10)
        self.b_csim.pack(side=TOP)

        #

        Label(frame1, text='main entry:').pack(side=LEFT)

        self.main_entry = Entry(frame1, width=20)
        self.main_entry.focus()
        self.main_entry.pack(fill=X)
        self.main_entry.insert('end', "2 6 3 7 9 1")
        self.main_entry.get()

        Label(frame2, text='second. entry:').pack(side=LEFT)

        self.secondary_entry = Entry(frame2, width=5)
        self.secondary_entry.pack(fill=X)
        self.secondary_entry.insert("end", "1")
        self.secondary_entry.get()

        self.text_output = Text(frame0, width=44, height=15)
        self.text_output.pack(side=LEFT, fill=X)

        self.text_scroll = Scrollbar(frame0)
        self.text_scroll.pack(side=RIGHT, fill=Y)
        self.text_scroll.config(command=self.text_output.yview)
        self.text_output.config(yscrollcommand=self.text_scroll.set)

        ## key bindings:

        self.main_entry.bind("<Escape>", self.clear_plot)
        self.main_entry.bind("<Control-Escape>", self.clear_output)
        self.main_entry.bind("<Alt-Escape>", self.clear_main)

        self.main_entry.bind("<Return>", self.plot)
        self.main_entry.bind("<p>", self.prime_form)
        self.main_entry.bind("<n>", self.normal_form)
        self.main_entry.bind("<r>", self.retrograde)
        self.main_entry.bind("<R>", self.rotation)
        self.main_entry.bind("<i>", self.inversion)
        self.main_entry.bind("<I>", self.ret_inv)

        self.main_entry.bind("<M>", self.comparison_matrix)
        self.main_entry.bind("<d>", self.internal)
        self.main_entry.bind("<s>", self.n_subsets)
        self.main_entry.bind("<S>", self.all_subsets)
        self.main_entry.bind("<c>", self.csegs_from_int)
        self.main_entry.bind("<C>", self.csim)

        self.main_entry.bind("<a>", self.casv)
        self.main_entry.bind("<x>", self.cia)
        self.main_entry.bind("<v>", self.ccvi)
        self.main_entry.bind("<V>", self.ccvii)


    def plot(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        plot_color = 'k'
        result = Contour(cseg).str_print()
        text = "Plot: "
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(cseg, plot_color, "Original")

    def prime_form(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        plot_color = 'b'
        # Returns csegclass only if cseg has not repeated elements
        if len(set(cseg)) == len(cseg):
            card, c_class, prime_form = Contour(cseg).contour_segment_class()
            prime_form_printed = Contour(prime_form).str_print()
            result = "{0}-{1} {2}".format(card, c_class, prime_form_printed)
        else:
            prime_form = Contour(cseg).prime_form()
            prime_form_printed = Contour(prime_form).str_print()
            result = "{0}".format(prime_form_printed)
        text = "Prime form: "
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(prime_form, plot_color, "Prime form")

    def normal_form(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        plot_color = 'g'
        normal_form = Contour(cseg).translation()
        result = Contour(normal_form).str_print()
        text = "Normal form: "
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(normal_form, plot_color, "Normal form")

    def retrograde(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        plot_color = 'm'
        retrograde = Contour(cseg).retrograde()
        result = Contour(retrograde).str_print()
        text = "Retrograde: "
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(retrograde, plot_color, "Retrograde")

    def inversion(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        plot_color = 'r'
        inversion = Contour(cseg).inversion()
        result = Contour(inversion).str_print()
        text = "Inversion: "
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(inversion, plot_color, "Inversion")

    def ret_inv(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        plot_color = 'c'
        ret_inv = Contour(Contour(cseg).retrograde()).inversion()
        result = Contour(ret_inv).str_print()
        text = "Ret. Inv.: "
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(ret_inv, plot_color, "Ret.inv.")

    def rotation(self, event=None):
        get = self.main_entry.get()
        second_get = int(self.secondary_entry.get())
        cseg = [int(x) for x in get.split(' ') if x]
        size = len(get)
        # returns a color for each rotation factor
        plot_color = str((second_get / float(size) * .8) + .1)
        rotation = Contour(cseg).rotation(second_get)
        result = Contour(rotation).str_print()
        text = "Rotation ({0}): ".format(second_get)
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")
        plot_preview(rotation, plot_color, "Rotation({0})".format(second_get))

    def internal(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        second_get = int(self.secondary_entry.get())
        int_diag = Contour(cseg).internal_diagonals(second_get)
        format_int_diag = Internal_diagonal(int_diag).str_print()
        text = "Internal diagonal ({0}): ".format(second_get)
        self.text_output.insert(END, text)
        self.text_output.insert(END, format_int_diag)
        self.text_output.insert(END, "\n")

    def comparison_matrix(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        com_matrix = Contour(cseg).comparison_matrix()
        com_matrix_str = Comparison_matrix(com_matrix).str_print()
        text = "Comparison Matrix:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, com_matrix_str)
        self.text_output.insert(END, "\n")

    def n_subsets(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        second_get = int(self.secondary_entry.get())
        csubset = Contour(cseg).subsets(second_get)
        result = "\n".join([Contour(x).str_print() for x in csubset])
        plural = "s" if second_get > 1 else ""
        text = "Contour subsets ({0} element{1}):\n".format(second_get, plural)
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")

    def all_subsets(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        csubset = Contour(cseg).all_subsets()
        result = "\n".join([Contour(x).str_print() for x in csubset])
        text = "All contour subsets:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")

    def csegs_from_int(self, event=None):
        get = self.main_entry.get()
        int_d = replace_plus_minus_to_list(get)
        if sorted(int_d)[-1] > 1:
            text = "ERROR: Insert Internal diagonal in main entry:\n- + -\n"
            self.text_output.insert(END, text)
        else:
            second_get = int(self.secondary_entry.get())
            csegs = Internal_diagonal(int_d).csegs(second_get)
            print(int_d)
            result = "\n".join([Contour(x).str_print() for x in csegs])
            plural = "s" if second_get > 1 else ""
            text = "Csegs:\n"
            self.text_output.insert(END, text)
            self.text_output.insert(END, result)
            self.text_output.insert(END, "\n")

    def casv(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        casv = Contour(cseg).contour_adjacency_series_vector()
        text = "Contour Adjacency Series Vector:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, casv)
        self.text_output.insert(END, "\n")

    def cis(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        cis = Contour(cseg).contour_interval_succession()
        result = Contour(cis).str_print()
        text = "Contour Interval Succession:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, result)
        self.text_output.insert(END, "\n")

    def cia(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        cia = list(Contour(cseg).contour_interval_array())
        text = "Contour Interval Array:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, cia)
        self.text_output.insert(END, "\n")

    def ccvi(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        ccvi = list(Contour(cseg).contour_class_vector_i())
        text = "Contour class vector I:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, ccvi)
        self.text_output.insert(END, "\n")

    def ccvii(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        ccvii = list(Contour(cseg).contour_class_vector_ii())
        text = "Contour class vector II:\n"
        self.text_output.insert(END, text)
        self.text_output.insert(END, ccvii)
        self.text_output.insert(END, "\n")

    def csim(self, event=None):
        get1 = self.main_entry.get()
        get2 = self.secondary_entry.get()
        cseg1 = [int(x) for x in get1.split(' ') if x]
        cseg2 = [int(x) for x in get2.split(' ') if x]
        if len(cseg1) == len(cseg2):
            csim = cseg_similarity(cseg1, cseg2)
            text1 = "Contour similarity: {0:.2f}\n".format(csim)
            text2 = "Cseg 1:{0}\nCseg 2:{1}: ".format(cseg1, cseg2)
            self.text_output.insert(END, text1)
            self.text_output.insert(END, text2)
            self.text_output.insert(END, "\n")
        else:
            text3 = "ERROR: Insert csegs with the same cardinality\n"
            self.text_output.insert(END, text3)

    def clear_output(self, event=None):
        self.text_output.delete(0.0, END)

    def clear_plot(self, event=None):
        clear_plot()

    def clear_main(self, event=None):
        self.main_entry.delete(0, END)

    def clear_secondary(self, event=None):
        self.secondary_entry.delete(0.0, END)


root = Tk()
root.title(program_name)

app = App(root)

root.mainloop()
