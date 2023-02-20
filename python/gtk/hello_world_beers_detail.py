#!/bin/env python3

# Doc: https://python-gtk-3-tutorial.readthedocs.io

import gi
import requests
import shutil

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MyWindow(Gtk.Window):
	def __init__(self):
		super().__init__(title="Beers")
		self.beers = None
		self.setupWindow()

	def setupList(self):
		# Model
		store = Gtk.ListStore(str, str, float)
		beers = self.getBeers()
		# We store in the model more columns than needed from the list because will be used in the detail
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
		# Enable sorting for third model column
		column.set_sort_column_id(2)
		# Register for row selection events
		select = tree.get_selection()
		select.connect("changed", self.onRowSelect)
		return tree

	def setupWindow(self):
		# Window is divided in two parts: a left list and a right detail
		rootBox = Gtk.Box(spacing=10)	# Box is default horyzontal if no orientation is specified
		self.add(rootBox)

		# Add listView
		listView = self.setupList()
		rootBox.add(listView)

		# Add detail view
		detailBox = Gtk.Box(
			orientation=Gtk.Orientation.VERTICAL,
			spacing=30
		)
		self.detailTitle = Gtk.Label()
		self.detailTitle.set_line_wrap(True)
		self.detailContent = Gtk.Label()
		self.detailContent.set_line_wrap(True)
		self.detailImage = Gtk.Image()
		detailBox.add(self.detailTitle)
		detailBox.add(self.detailContent)
		detailBox.add(self.detailImage)
		rootBox.add(detailBox)


	def getBeers(self):
		if not self.beers:
			response = requests.get("https://api.punkapi.com/v2/beers")
			self.beers = response.json()
		return self.beers

	def onRowSelect(self, selection):
		# We can retrieve the selected item directly from model
		model, treeiter = selection.get_selected()
		if treeiter is None:
			return
		selectedBeer = model[treeiter]
		print("Selected {}".format(selectedBeer[0]))

		# Or we can obtain the index of selected item and look up entire obj on original data
		idx = selectedBeer.path[0]
		self.showBeerDetail(self.getBeers()[idx])

	def showBeerDetail(self, beer):
		self.detailTitle.set_markup("<big>{}</big>".format(beer['name']))
		self.detailContent.set_text(beer['description'])
		# Download image in tmp folder and open in pixbuf
		tmpImgPath = self.downloadImage(beer['image_url'])
		print(tmpImgPath)
		self.detailImage.set_from_file(tmpImgPath)

	def downloadImage(self, url):
		urlParts = url.split("/")
		tmpFilePath = "/tmp/{}".format(urlParts[len(urlParts) - 1])
		response = requests.get(url, stream=True)
		with open(tmpFilePath, 'wb') as tmpFile:
			shutil.copyfileobj(response.raw, tmpFile)
		del response
		return tmpFilePath



win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()


