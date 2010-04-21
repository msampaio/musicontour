#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Frame, Button, Entry, Label, TOP, LEFT, END
from plot import plot_preview
from contour import Contour

program_name = "Villa Lobos Contour Module"
version = "0.1"

class App:

    def __init__(self, master):

        frame0 = Frame(master)
        frame0.pack(pady=10)

        frame1 = Frame(master)
        frame1.pack(pady=5)

        frame2 = Frame(master)
        frame2.pack(pady=5)

        frame3 = Frame(master)
        frame3.pack(pady=5)

        font = 'sans 16 bold'
        self.initial = Label(frame0, text=program_name, font=font)
        self.initial.pack(side=TOP)

        self.plot = Button(frame2, text="Plot", command=self.plot)
        self.plot.pack(side=LEFT)

        self.prime_form = Button(frame2, text="Prime form",
                                    command=self.prime_form)
        self.prime_form.pack(side=LEFT)

        self.normal_form = Button(frame2, text="Normal form",
                                     command=self.normal_form)
        self.normal_form.pack(side=LEFT)

        self.retrograde = Button(frame2, text="Retrograde",
                                    command=self.retrograde)
        self.retrograde.pack(side=LEFT)

        self.inversion = Button(frame2, text="Inversion",
                                   command=self.inversion)
        self.inversion.pack(side=LEFT)

        self.ret_inv = Button(frame2,
                                 text="Ret_inv",
                                 command=self.ret_inv)
        self.ret_inv.pack(side=LEFT)

        self.rotation = Button(frame2, text="Rotation",
                                  command=self.rotation)
        self.rotation.pack(side=LEFT)

        Label(frame1, text='cseg:').pack(side=LEFT, padx=5)

        self.cseg_entry = Entry(frame1, width=20)
        self.cseg_entry.pack(side=LEFT)
        self.cseg_entry.insert('end', "0 3 1 2")
        self.cseg_entry.get()

        Label(frame1, text='parameter:').pack(side=LEFT, padx=5)

        self.param_entry = Entry(frame1, width=5)
        self.param_entry.pack(side=LEFT)
        self.param_entry.insert("end", "1")
        self.param_entry.get()

    def plot(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        plot_preview(cseg)

    def prime_form(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        plot_preview(Contour(cseg).prime_form())

    def normal_form(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        plot_preview(Contour(cseg).translation())

    def retrograde(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        plot_preview(Contour(cseg).retrograde())

    def inversion(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        plot_preview(Contour(cseg).inversion())

    def ret_inv(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        plot_preview(Contour(Contour(cseg).retrograde()).inversion())

    def rotation(self):
        get = self.cseg_entry.get()
        param_get = int(self.param_entry.get())
        cseg = [int(x) for x in get.split(' ')]
        plot_preview(Contour(cseg).rotation(param_get))


root = Tk()
root.title(program_name + " v." + version)

app = App(root)

root.mainloop()
