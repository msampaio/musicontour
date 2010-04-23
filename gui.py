#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Frame, Button, Entry, Label, TOP, LEFT, X
from plot import plot_preview
from contour import internal_diagonal_print, Contour

program_name = "Villa Lobos Contour Module"
version = "0.1"


class App:

    def __init__(self, master):

        title_frame = Frame(master)
        title_frame.pack(pady=5)

        frame1 = Frame(master)
        frame1.pack(side=TOP, fill=X)

        frame2 = Frame(master)
        frame2.pack(side=TOP, fill=X)

        frame3 = Frame(master)
        frame3.pack(side=TOP, fill=X)

        toolbar1 = Frame(master)
        toolbar1.pack(side=LEFT, pady=5, fill=X)

        toolbar2 = Frame(master)
        toolbar2.pack(side=TOP, pady=5, fill=X)

        font = 'sans 8 bold'
        self.initial = Label(title_frame, text=program_name, font=font)
        self.initial.pack(side=TOP)

        self.plot = Button(toolbar1, text="Plot", command=self.plot,
                           width=10)

        self.plot.pack(side=TOP)

        self.prime_form = Button(toolbar2, text="Prime form",
                                    command=self.prime_form, width=10)
        self.prime_form.pack(side=TOP)

        self.normal_form = Button(toolbar2, text="Normal form",
                                     command=self.normal_form, width=10)
        self.normal_form.pack(side=TOP)

        self.retrograde = Button(toolbar1, text="Retrograde",
                                    command=self.retrograde, width=10)
        self.retrograde.pack(side=TOP)

        self.inversion = Button(toolbar1, text="Inversion",
                                   command=self.inversion, width=10)
        self.inversion.pack(side=TOP)

        self.ret_inv = Button(toolbar1, text="Retrograde inv.",
                                 command=self.ret_inv, width=10)
        self.ret_inv.pack(side=TOP)

        self.rotation = Button(toolbar2, text="Rotation",
                               command=self.rotation, width=10)
        self.rotation.pack(side=TOP)

        self.internal = Button(toolbar2, text="Int. Diagonal",
                               command=self.internal, width=10)
        self.internal.pack(side=TOP)

        Label(frame1, text='cseg:').pack(side=LEFT)

        self.cseg_entry = Entry(frame1, width=20)
        self.cseg_entry.pack(fill=X)
        self.cseg_entry.insert('end', "0 3 1 2")
        self.cseg_entry.get()

        Label(frame2, text='parameter:').pack(side=LEFT)

        self.param_entry = Entry(frame2, width=5)
        self.param_entry.pack(fill=X)
        self.param_entry.insert("end", "1")
        self.param_entry.get()

        Label(frame3, text='output:').pack(side=LEFT)

        self.output = Label(frame3, width=12)
        self.output.pack(side=LEFT, fill=X)

    def plot(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        result = Contour(cseg).cseg_visual_printing()
        self.output.configure(text=result)
        plot_preview(cseg)

    def prime_form(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        prime_form = Contour(cseg).prime_form()
        result = Contour(prime_form).cseg_visual_printing()
        self.output.configure(text=result)
        plot_preview(prime_form)

    def normal_form(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        normal_form = Contour(cseg).translation()
        result = Contour(normal_form).cseg_visual_printing()
        self.output.configure(text=result)
        plot_preview(normal_form)

    def retrograde(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        retrograde = Contour(cseg).retrograde()
        result = Contour(retrograde).cseg_visual_printing()
        self.output.configure(text=result)
        plot_preview(retrograde)

    def inversion(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        plot_preview(Contour(cseg).inversion())

    def ret_inv(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        ret_inv = Contour(Contour(cseg).retrograde()).inversion()
        result = Contour(ret_inv).cseg_visual_printing()
        self.output.configure(text=result)
        plot_preview(ret_inv)

    def rotation(self):
        get = self.cseg_entry.get()
        param_get = int(self.param_entry.get())
        cseg = [int(x) for x in get.split(' ')]
        rotation = Contour(cseg).rotation(param_get)
        result = Contour(rotation).cseg_visual_printing()
        self.output.configure(text=result)
        plot_preview(rotation)

    def internal(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        param_get = int(self.param_entry.get())
        int_diag = Contour(cseg).internal_diagonals(param_get)
        format_int_diag = internal_diagonal_print(int_diag)
        self.output.configure(text=format_int_diag)


root = Tk()
root.title(program_name + " v." + version)

app = App(root)

root.mainloop()
