#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contour.contour
import contour.diagonal
import contour.matrix
import contour.comparison
import contour.utils
import contour.plot
import Tkinter

sw_name = "MusiContour"
version = "0.2"


class App:

    def __init__(self, master):

        # widgets

        font = 'sans 8 bold'
        font_par = ("arial", 9)

        self.initial = Tkinter.Label(master, text=sw_name + " v." + version, font=font)

        self.text_output = Tkinter.Text(master, height=10)
        self.text_scroll = Tkinter.Scrollbar(master)
        self.text_scroll.config(command=self.text_output.yview)
        self.text_output.config(yscrollcommand=self.text_scroll.set)

        # organizes widgets in labelframes
        self.frame_entry = Tkinter.LabelFrame(master, text="Entry area", padx=5, pady=5)
        self.frame_clear = Tkinter.LabelFrame(master, text="Clear buttons", padx=5, pady=5)
        self.frame_plot = Tkinter.LabelFrame(master, text="Plot operations", padx=5, pady=5)
        self.frame_matrix = Tkinter.LabelFrame(master, text="Matrix", padx=5, pady=5)
        self.frame_subsets = Tkinter.LabelFrame(master, text="Subsets", padx=5, pady=5)
        self.frame_friedmann = Tkinter.LabelFrame(master, text="Friedmann", padx=5, pady=5)
        self.frame_comparisons = Tkinter.LabelFrame(master, text="Comparison", padx=5, pady=5)

        self.main_label = Tkinter.Label(self.frame_entry, text="Main entry:", font=font_par)
        self.main_entry = Tkinter.Entry(self.frame_entry, width=17)
        self.main_entry.focus()
        self.main_entry.insert('end', "2 6 3 7 9 1")
        self.main_entry.get()

        self.secondary_label = Tkinter.Label(self.frame_entry, text="Second. entry:", font=font_par)
        self.secondary_entry = Tkinter.Entry(self.frame_entry, width=17)
        self.secondary_entry.insert("end", "1")
        self.secondary_entry.get()

        # buttons
        self.b_clear_main = Tkinter.Button(self.frame_clear, text="Main entry",
                               command=self.clear_main, width=9, font=font_par)
        self.b_clear_secondary = Tkinter.Button(self.frame_clear, text="Second. entry",
                               command=self.clear_secondary, width=9, font=font_par)
        self.b_clear_output = Tkinter.Button(self.frame_clear, text="Output area",
                                     command=self.clear_output, width=9, font=font_par)
        self.b_clear_plot = Tkinter.Button(self.frame_clear, text="Plot area",
                               command=self.clear_plot, width=9, font=font_par)

        self.b_plot = Tkinter.Button(self.frame_plot, text="Plot", command=self.plot,
                           width=9, font=font_par)
        self.b_normal_form = Tkinter.Button(self.frame_plot, text="Normal form",
                                     command=self.normal_form, width=9, font=font_par)
        self.b_prime_form = Tkinter.Button(self.frame_plot, text="Prime form",
                                    command=self.prime_form, width=9, font=font_par)
        self.b_inversion = Tkinter.Button(self.frame_plot, text="Inversion",
                                   command=self.inversion, width=9, font=font_par)
        self.b_rotation = Tkinter.Button(self.frame_plot, text="Rotation",
                               command=self.rotation, width=9, font=font_par)
        self.b_retrogression = Tkinter.Button(self.frame_plot, text="Retrogression",
                                    command=self.retrogression, width=9, font=font_par)
        self.b_ret_inv = Tkinter.Button(self.frame_plot, text="Retrograded inv.",
                                 command=self.ret_inv, width=9, font=font_par)

        self.b_comparison_matrix = Tkinter.Button(self.frame_matrix, text="COM Matrix",
                               command=self.comparison_matrix, width=13, font=font_par)
        self.b_internal = Tkinter.Button(self.frame_matrix, text="Int. Diagonal",
                               command=self.internal, width=13, font=font_par)
        self.b_csegs_from_int = Tkinter.Button(self.frame_matrix, text="Csegs from INT",
                               command=self.csegs_from_int, width=13, font=font_par)

        self.b_n_subsets = Tkinter.Button(self.frame_subsets, text="n subsets",
                               command=self.n_subsets, width=8, font=font_par)
        self.b_all_subsets = Tkinter.Button(self.frame_subsets, text="All subsets",
                               command=self.all_subsets, width=8, font=font_par)
        self.b_segment_classes = Tkinter.Button(self.frame_subsets, text="Cseg classes",
                               command=self.segment_classes, width=8, font=font_par)

        self.b_casv = Tkinter.Button(self.frame_friedmann, text="CASV",
                               command=self.casv, width=7, font=font_par)
        self.b_cis = Tkinter.Button(self.frame_friedmann, text="CIS",
                               command=self.cis, width=7, font=font_par)
        self.b_cia = Tkinter.Button(self.frame_friedmann, text="CIA",
                               command=self.cia, width=7, font=font_par)
        self.b_ccvi = Tkinter.Button(self.frame_friedmann, text="CCV I",
                               command=self.ccvi, width=7, font=font_par)
        self.b_ccvii = Tkinter.Button(self.frame_friedmann, text="CCV II",
                               command=self.ccvii, width=7, font=font_par)

        self.b_compare = Tkinter.Button(self.frame_comparisons, text="Contour comparison",
                               command=self.compare, width=13, font=font_par)
        self.b_all_embedded = Tkinter.Button(self.frame_comparisons, text="Embedded comparison",
                               command=self.all_embedded, width=13, font=font_par)
        self.b_reduction = Tkinter.Button(self.frame_comparisons, text="Contour reduction",
                               command=self.reduction, width=13, font=font_par)
        self.b_operations_comparison = Tkinter.Button(self.frame_comparisons, text="Op. relations",
                               command=self.operations_comparison, width=13, font=font_par)

        # key bindings:
        for x in [self.main_entry, master, self.secondary_entry]:
            x.bind("<Escape>", self.clear_plot)
            x.bind("<Control-Escape>", self.clear_output)
            x.bind("<Alt-Escape>", self.clear_main)

            x.bind("<Return>", self.plot)
            x.bind("<p>", self.prime_form)
            x.bind("<n>", self.normal_form)
            x.bind("<r>", self.retrogression)
            x.bind("<R>", self.rotation)
            x.bind("<i>", self.inversion)
            x.bind("<I>", self.ret_inv)

            x.bind("<M>", self.comparison_matrix)
            x.bind("<d>", self.internal)
            x.bind("<s>", self.n_subsets)
            x.bind("<S>", self.all_subsets)
            x.bind("<c>", self.csegs_from_int)
            x.bind("<C>", self.compare)
            x.bind("<E>", self.all_embedded)
            x.bind("<o>", self.operations_comparison)

            x.bind("<a>", self.casv)
            x.bind("<x>", self.cia)
            x.bind("<v>", self.ccvi)
            x.bind("<V>", self.ccvii)

            x.bind("<e>", self.reduction)

        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2, weight=1)
        master.columnconfigure(3, weight=1)

        # displacement
        # row 0
        self.initial.grid(row=0, column=0, columnspan=5)

        # output area
        self.text_output.grid(row=1, column=0, columnspan=4)
        self.text_scroll.grid(row=1, column=4, sticky=Tkinter.N + Tkinter.S)

        # entry area
        self.frame_entry.grid(columnspan=2, rowspan=2)
        self.main_label.grid(row=2, column=0, sticky=Tkinter.E)
        self.main_entry.grid(row=2, column=1)
        self.secondary_label.grid(row=3, column=0, sticky=Tkinter.E)
        self.secondary_entry.grid(row=3, column=1)

        # clear area
        self.frame_clear.grid(row=2, column=2, rowspan=2, columnspan=3, sticky=Tkinter.W)
        self.b_clear_main.grid(row=2, column=2)
        self.b_clear_output.grid(row=2, column=3)
        self.b_clear_secondary.grid(row=3, column=2)
        self.b_clear_plot.grid(row=3, column=3)

        # plot area
        self.frame_plot.grid(row=4, column=0, rowspan=7, sticky=Tkinter.W)
        self.b_plot.grid(row=4, column=0)
        self.b_normal_form.grid(row=5, column=0)
        self.b_prime_form.grid(row=6, column=0)
        self.b_inversion.grid(row=7, column=0)
        self.b_rotation.grid(row=8, column=0)
        self.b_retrogression.grid(row=9, column=0)
        self.b_ret_inv.grid(row=10, column=0)

        # matrix area
        self.frame_matrix.grid(row=4, column=1, sticky=Tkinter.W)
        self.b_comparison_matrix.grid(row=4, column=1)
        self.b_internal.grid(row=5, column=1)
        self.b_csegs_from_int.grid(row=6, column=1)

        # subsets area
        self.frame_subsets.grid(row=4, column=2, rowspan=3, sticky=Tkinter.W)
        self.b_n_subsets.grid(row=4, column=2)
        self.b_all_subsets.grid(row=5, column=2)
        self.b_segment_classes.grid(row=6, column=2)

        # friedmann area
        self.frame_friedmann.grid(row=4, column=3, rowspan=5, sticky=Tkinter.W)
        self.b_casv.grid(row=4, column=3)
        self.b_cis.grid(row=5, column=3)
        self.b_cia.grid(row=6, column=3)
        self.b_ccvi.grid(row=7, column=3)
        self.b_ccvii.grid(row=8, column=3)

        # comparisons area
        self.frame_comparisons.grid(row=8, column=1, rowspan=3, sticky=Tkinter.W)
        self.b_compare.grid(row=8, column=1)
        self.b_all_embedded.grid(row=9, column=1)
        self.b_operations_comparison.grid(row=10, column=1)
        self.b_reduction.grid(row=11, column=1)

    # functions

    def plot(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        plot_color = 'k'
        result = contour.contour.Contour(cseg)
        text = "Original: "
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, result)
        self.text_output.insert(Tkinter.END, "\n")
        contour.plot.contour_lines([result, plot_color, "Original"])

    def prime_form(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        plot_color = 'b'
        # Returns csegclass only if cseg has not repeated elements
        if len(set(cseg)) == len(cseg):
            tmp = contour.contour.Contour(cseg).segment_class()
            card, c_class, pr_form, ri = tmp
            if ri == True:
                ri = "*"
            else:
                ri = ""
            result = "{0}-{1}{2} {3}".format(card, c_class, ri, pr_form)
        else:
            pr_form = contour.contour.Contour(cseg).pr_form()
            result = "{0}".format(pr_form)
        text = "Prime form: "
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, result)
        self.text_output.insert(Tkinter.END, "\n")
        contour.plot.contour_lines([pr_form, plot_color, "Prime form"])

    def normal_form(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        plot_color = 'g'
        normal_form = contour.contour.Contour(cseg).translation()
        result = contour.contour.Contour(normal_form)
        text = "Normal form: "
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, result)
        self.text_output.insert(Tkinter.END, "\n")
        contour.plot.contour_lines([normal_form, plot_color, "Normal form"])

    def retrogression(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        plot_color = 'm'
        retrogression = contour.contour.Contour(cseg).retrogression()
        result = contour.contour.Contour(retrogression)
        text = "Retrogression: "
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, result)
        self.text_output.insert(Tkinter.END, "\n")
        contour.plot.contour_lines([retrogression, plot_color, "Retrogression"])

    def inversion(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        plot_color = 'r'
        inversion = contour.contour.Contour(cseg).inversion()
        result = contour.contour.Contour(inversion)
        text = "Inversion: "
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, result)
        self.text_output.insert(Tkinter.END, "\n")
        contour.plot.contour_lines([inversion, plot_color, "Inversion"])

    def ret_inv(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        plot_color = 'c'
        ret = contour.contour.Contour(cseg).retrogression()
        ret_inv = contour.contour.Contour(ret).inversion()
        result = contour.contour.Contour(ret_inv)
        text = "Ret. Inv.: "
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, result)
        self.text_output.insert(Tkinter.END, "\n")
        contour.plot.contour_lines([ret_inv, plot_color, "Ret.inv."])

    def rotation(self, event=None):
        get = self.main_entry.get()
        second_get = int(self.secondary_entry.get())
        cseg = [int(x) for x in get.split(' ') if x]
        size = len(get)
        # returns a color for each rotation factor
        plot_color = str((second_get / float(size) * .8) + .1)
        rotation = contour.contour.Contour(cseg).rotation(second_get)
        result = contour.contour.Contour(rotation)
        text = "Rotation ({0}): ".format(second_get)
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, result)
        self.text_output.insert(Tkinter.END, "\n")
        contour.plot.contour_lines([rotation, plot_color, "Rotation({0})".format(second_get)])

    def internal(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        second_get = int(self.secondary_entry.get())
        int_diag = contour.contour.Contour(cseg).internal_diagonals(second_get)
        format_int_diag = contour.diagonal.InternalDiagonal(int_diag)
        text = "Internal diagonal ({0}): ".format(second_get)
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, format_int_diag)
        self.text_output.insert(Tkinter.END, "\n")

    def comparison_matrix(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        com_matrix = contour.contour.Contour(cseg).comparison_matrix()
        com_matrix_str = contour.matrix.ComparisonMatrix(com_matrix)
        text = "Comparison Matrix:\n"
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, com_matrix_str)
        self.text_output.insert(Tkinter.END, "\n")

    def reduction(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        cseg_obj = contour.contour.Contour(cseg)
        [reduced_c, depth] = cseg_obj.reduction_morris()
        reduced_c_print = contour.contour.Contour(reduced_c)
        text1 = "Morris Contour Reduction\n"
        text2 = "Original:{0}\n".format(cseg_obj)
        result = "Reduction: {0}\nDepth: {1}".format(reduced_c_print, depth)
        self.text_output.insert(Tkinter.END, text1)
        self.text_output.insert(Tkinter.END, text2)
        self.text_output.insert(Tkinter.END, result)
        self.text_output.insert(Tkinter.END, "\n")

    def n_subsets(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        cseg_obj = contour.contour.Contour(cseg)
        second_get = int(self.secondary_entry.get())
        csubset_normal = cseg_obj.subsets_normal(second_get)
        normal_gr = contour.contour.subsets_grouped(csubset_normal, "normal")
        csubset_prime = contour.contour.Contour(cseg).subsets_prime(second_get)
        prime_gr = contour.contour.subsets_grouped(csubset_prime, "prime")
        plural = "s" if second_get > 1 else ""
        txt1 = "Original: {0}\n".format(cseg_obj)
        txt2 = "Contour subsets ({0} element{1}):\n".format(second_get, plural)
        sep1 = ("-" * 22) + "\n"
        sep2 = ("=" * 22) + "\n"
        txt3 = sep2 + "Grouped by normal form\n" + sep1
        txt4 = "\n" + sep2 + "Grouped by prime form\n" + sep1
        self.text_output.insert(Tkinter.END, txt1)
        self.text_output.insert(Tkinter.END, txt2)
        self.text_output.insert(Tkinter.END, txt3)
        self.text_output.insert(Tkinter.END, normal_gr)
        self.text_output.insert(Tkinter.END, txt4)
        self.text_output.insert(Tkinter.END, prime_gr)
        self.text_output.insert(Tkinter.END, "\n")

    def all_subsets(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        cseg_print = contour.contour.Contour(cseg)
        csubset_normal = contour.contour.Contour(cseg).all_subsets_normal()
        normal_gr = contour.contour.subsets_grouped(csubset_normal, "normal")
        csubset_prime = contour.contour.Contour(cseg).all_subsets_prime()
        prime_gr = contour.contour.subsets_grouped(csubset_prime, "prime")
        text1 = "Original: {0}\nAll contour subsets:\n".format(cseg_print)
        sep1 = ("-" * 22) + "\n"
        sep2 = ("=" * 22) + "\n"
        text2 = sep2 + "Grouped by normal form\n" + sep1
        text3 = "\n" + sep2 + "Grouped by prime form\n" + sep1
        self.text_output.insert(Tkinter.END, text1)
        self.text_output.insert(Tkinter.END, text2)
        self.text_output.insert(Tkinter.END, normal_gr)
        self.text_output.insert(Tkinter.END, text3)
        self.text_output.insert(Tkinter.END, prime_gr)
        self.text_output.insert(Tkinter.END, "\n")

    def csegs_from_int(self, event=None):
        get = self.main_entry.get()
        int_d = contour.utils.replace_plus_minus_to_list(get)
        if sorted(int_d)[-1] > 1:
            text = "ERROR: Insert Internal diagonal in main entry:\n- + -\n"
            self.text_output.insert(Tkinter.END, text)
        else:
            int_d = contour.diagonal.InternalDiagonal(int_d)
            second_get = int(self.secondary_entry.get())
            csegs = int_d.csegs(second_get)
            result = "\n".join([str(x) for x in csegs])
            plural = "s" if second_get > 1 else ""
            text1 = "Possible Csegs with "
            text2 = "Internal diagonal ({0}): {1}\n".format(second_get, int_d)
            self.text_output.insert(Tkinter.END, text1)
            self.text_output.insert(Tkinter.END, text2)
            self.text_output.insert(Tkinter.END, result)
            self.text_output.insert(Tkinter.END, "\n")

    def casv(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        casv = contour.contour.Contour(cseg).adjacency_series_vector()
        text = "Contour Adjacency Series Vector:\n"
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, casv)
        self.text_output.insert(Tkinter.END, "\n")

    def cis(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        cis = contour.contour.Contour(cseg).interval_succession()
        result = contour.utils.pretty_as_cseg(cis)
        text = "Contour Interval Succession:\n"
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, result)
        self.text_output.insert(Tkinter.END, "\n")

    def cia(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        cia = list(contour.contour.Contour(cseg).interval_array())
        text = "Contour Interval Array:\n"
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, cia)
        self.text_output.insert(Tkinter.END, "\n")

    def ccvi(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        ccvi = list(contour.contour.Contour(cseg).class_vector_i())
        text = "Contour class vector I:\n"
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, ccvi)
        self.text_output.insert(Tkinter.END, "\n")

    def ccvii(self, event=None):
        get = self.main_entry.get()
        cseg = [int(x) for x in get.split(' ') if x]
        ccvii = list(contour.contour.Contour(cseg).class_vector_ii())
        text = "Contour class vector II:\n"
        self.text_output.insert(Tkinter.END, text)
        self.text_output.insert(Tkinter.END, ccvii)
        self.text_output.insert(Tkinter.END, "\n")

    def compare(self, event=None):
        get1 = self.main_entry.get()
        get2 = self.secondary_entry.get()
        cseg1 = [int(x) for x in get1.split(' ') if x]
        cseg2 = [int(x) for x in get2.split(' ') if x]
        cseg1_p = contour.contour.Contour(cseg1)
        cseg2_p = contour.contour.Contour(cseg2)
        tmp = contour.comparison.cseg_similarity_compare(cseg1_p, cseg2_p)
        [operation, result] = tmp
        text1 = "{0}: {1:.2f}\n".format(operation, result)
        text2 = "Cseg 1: {0}\nCseg 2: {1}".format(cseg1_p, cseg2_p)
        self.text_output.insert(Tkinter.END, text1)
        self.text_output.insert(Tkinter.END, text2)
        self.text_output.insert(Tkinter.END, "\n")

    def all_embedded(self, event=None):
        get1 = self.main_entry.get()
        get2 = self.secondary_entry.get()
        cseg1 = [int(x) for x in get1.split(' ') if x]
        cseg2 = [int(x) for x in get2.split(' ') if x]
        cseg1_p = contour.contour.Contour(cseg1)
        cseg2_p = contour.contour.Contour(cseg2)
        result = contour.comparison.all_contour_mutually_embedded(cseg1_p, cseg2_p)
        text1 = "All mutually embedded contour comparison: {0:.2f}\n".format(result)
        text2 = "Cseg 1: {0}\nCseg 2: {1}".format(cseg1_p, cseg2_p)
        self.text_output.insert(Tkinter.END, text1)
        self.text_output.insert(Tkinter.END, text2)
        self.text_output.insert(Tkinter.END, "\n")

    def operations_comparison(self, event=None):
        get1 = self.main_entry.get()
        get2 = self.secondary_entry.get()
        cseg1 = contour.contour.Contour([int(x) for x in get1.split(' ') if x])
        cseg2 = contour.contour.Contour([int(x) for x in get2.split(' ') if x])
        result = contour.comparison.pretty_operations_comparison(cseg1, cseg2)
        text1 = "Operations contour comparison:\n{0}".format(result)
        self.text_output.insert(Tkinter.END, text1)
        self.text_output.insert(Tkinter.END, "\n")

    def segment_classes(self, event=None):
        result = contour.contour.pretty_classes(7)
        self.text_output.insert(Tkinter.END, result)
        self.text_output.insert(Tkinter.END, "\n")

    def clear_output(self, event=None):
        self.text_output.delete(0.0, Tkinter.END)

    def clear_plot(self, event=None):
        contour.plot.clear()

    def clear_main(self, event=None):
        self.main_entry.delete(0, Tkinter.END)

    def clear_secondary(self, event=None):
        self.secondary_entry.delete(0, Tkinter.END)


def gui():
    root = Tkinter.Tk()
    root.title(sw_name)
    root.geometry('450x510+0+0')
    root.resizable(Tkinter.FALSE, Tkinter.FALSE)

    app = App(root)

    root.mainloop()
