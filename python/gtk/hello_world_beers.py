#!/bin/env python3

# Doc: https://python-gtk-3-tutorial.readthedocs.io

import gi
import requests

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MyWindow(Gtk.Window):
	def __init__(self):
		super().__init__(title="Beers")

		# Model
		store = Gtk.ListStore(str, str, float)
		beers = self.getBeers()
		for beer in beers:
			store.append([beer["name"], beer["tagline"], beer["abv"]])

		# Create ListView
		tree = Gtk.TreeView(model=store)
		# Create text renderer (used for both columns)
		textRenderer = Gtk.CellRendererText()
		# Add first column
		column = Gtk.TreeViewColumn("Beer name", textRenderer, text=0, weight=1)
		tree.append_column(column)
		# Add second column
		column = Gtk.TreeViewColumn("Description", textRenderer, text=1, weight=1)
		tree.append_column(column)
		# Add third column
		column = Gtk.TreeViewColumn("Alc %", textRenderer, text=2, weight=1)
		tree.append_column(column)
		self.add(tree)

	def getBeers(self):
		response = requests.get("https://api.punkapi.com/v2/beers")
		return response.json()


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()


