#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
import plot as p


class App:

    def __init__(self, master):

        frame = tk.Frame(master)
        frame.pack()

        self.plot = tk.Button(frame, text="Plot", command=self.plot)
        self.plot.pack(side=tk.LEFT)

        self.entry = tk.Entry(frame)
        self.entry.pack(side=tk.LEFT)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "0 1 2")
        self.entry.get()

    def plot(self):
        get = self.entry.get()
        out = [int(x) for x in get.split(' ')]
        p.plot_preview(out)

root = tk.Tk()

app = App(root)

root.mainloop()
