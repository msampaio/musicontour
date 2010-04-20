#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Frame, Button, Entry, LEFT, END
import plot as p
import contour as c


class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.plot = Button(frame, text="Plot", command=self.plot)
        self.plot.pack(side=LEFT)

        self.prime_form = Button(frame, text="Prime form",
                                    command=self.prime_form)
        self.prime_form.pack(side=LEFT)

        self.normal_form = Button(frame, text="Normal form",
                                     command=self.normal_form)
        self.normal_form.pack(side=LEFT)

        self.retrograde = Button(frame, text="Retrograde",
                                    command=self.retrograde)
        self.retrograde.pack(side=LEFT)

        self.inversion = Button(frame, text="Inversion",
                                   command=self.inversion)
        self.inversion.pack(side=LEFT)

        self.ret_inv = Button(frame,
                                 text="Ret_inv",
                                 command=self.ret_inv)
        self.ret_inv.pack(side=LEFT)

        self.rotation = Button(frame, text="Rotation",
                                  command=self.rotation)
        self.rotation.pack(side=LEFT)

        self.cseg_entry = Entry(frame)
        self.cseg_entry.pack(side=LEFT)
        self.cseg_entry.delete(0, END)
        self.cseg_entry.insert(0, "0 3 1 2")
        self.cseg_entry.get()

        self.param_entry = Entry(frame)
        self.param_entry.pack(side=LEFT)
        self.param_entry.delete(0, END)
        self.param_entry.insert(0, "1")
        self.param_entry.get()

    def plot(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        p.plot_preview(cseg)

    def prime_form(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        p.plot_preview(c.Contour(cseg).prime_form())

    def normal_form(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        p.plot_preview(c.Contour(cseg).translation())

    def retrograde(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        p.plot_preview(c.Contour(cseg).retrograde())

    def inversion(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        p.plot_preview(c.Contour(cseg).inversion())

    def ret_inv(self):
        get = self.cseg_entry.get()
        cseg = [int(x) for x in get.split(' ')]
        p.plot_preview(c.Contour(c.Contour(cseg).retrograde()).inversion())

    def rotation(self):
        get = self.cseg_entry.get()
        param_get = int(self.param_entry.get())
        cseg = [int(x) for x in get.split(' ')]
        p.plot_preview(c.Contour(cseg).rotation(param_get))


root = Tk()
root.title("Villa Lobos Contour Module")

app = App(root)

root.mainloop()
