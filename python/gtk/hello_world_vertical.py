#!/bin/env python3

# Doc: https://python-gtk-3-tutorial.readthedocs.io

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MyWindow(Gtk.Window):
	def __init__(self):
		super().__init__(title="Ciao")

		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.add(box)

		self.button = Gtk.Button(label="Bottone")
		self.button.connect("clicked", self.on_button_clicked)
		box.add(self.button)

		self.label = Gtk.Label(label="Clicka il bottone")
		box.add(self.label)

	def on_button_clicked(self, widget):
		print("Clickato")
		self.label.set_text("Hello world")

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()


