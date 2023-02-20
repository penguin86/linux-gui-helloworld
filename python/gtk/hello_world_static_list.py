#!/bin/env python3

# Doc: https://python-gtk-3-tutorial.readthedocs.io

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MyWindow(Gtk.Window):
	def __init__(self):
		super().__init__(title="Ciao")

		# Model
		store = Gtk.ListStore(str, float)
		store.append(["Uno", 3.6])
		store.append(["Due", 7.5])

		# Create ListView
		tree = Gtk.TreeView(model=store)
		# Create text renderer (used for both columns)
		textRenderer = Gtk.CellRendererText()
		# Add first column
		column = Gtk.TreeViewColumn("Beer name", textRenderer, text=0, weight=1)
		tree.append_column(column)
		# Add second column
		column = Gtk.TreeViewColumn("Alc %", textRenderer, text=1, weight=1)
		tree.append_column(column)
		self.add(tree)

	def on_button_clicked(self, widget):
		print("Clickato")
		self.label.set_text("Hello world")

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()


