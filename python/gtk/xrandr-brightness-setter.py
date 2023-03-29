#!/bin/env python3

import gi
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

XRANDR_OUTPUT = "eDP"
XRANDR_COMMAND = "xrandr --output {} --brightness {}"
XRANDR_READ_COMMAND = "xrandr --verbose --current"

class BrightnessWindow(Gtk.Window):
	def __init__(self):
		super().__init__(title="Xrandr Brightness")

		self.set_default_size(500,0)

		box = Gtk.Box(
			orientation=Gtk.Orientation.VERTICAL,
		)
		self.add(box)

		self.scale = Gtk.Scale.new_with_range(
			Gtk.Orientation.HORIZONTAL,
			0.1,	#min
			1.5, 	#max
			0.1		#step
		)
		self.scale.connect("value_changed", self.on_scale_value_changed)
		box.add(self.scale)

		self.button = Gtk.Button(label="Ok")
		self.button.connect("clicked", self.on_button_clicked)
		box.add(self.button)

		self.loadCurrentBrightness()

	def on_button_clicked(self, widget):
		exit(0)

	def on_scale_value_changed(self, widget):
		value = widget.get_value()

		# Execute command
		ret = subprocess.run(
			XRANDR_COMMAND.format(XRANDR_OUTPUT, value),
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			shell=True
		)
		if ret.returncode != 0:
			print('xrandr exited with error code {}'.format(ret.returncode))
			if ret.stderr:
				print('stderr:\n{}'.format(ret.stderr.decode()))
			if ret.stdout:
				stdout = ret.stdout.decode()
				print('stdout:\n{}'.format(stdout))

	def loadCurrentBrightness(self):
		ret = subprocess.run(
			XRANDR_READ_COMMAND,
			stdout=subprocess.PIPE,
			shell=True
		)
		if ret.returncode == 0:
			stdout = ret.stdout.decode()
			try:
				brightnessPosition = stdout.index("Brightness: ") + len("Brightness: ")
				brightnessValue = stdout[brightnessPosition:brightnessPosition+3]
				print(brightnessValue)
				currentBrightness = float(brightnessValue)
				self.scale.set_value(currentBrightness)
			except ValueError:
				print("Unable to read current brightness value")


win = BrightnessWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
