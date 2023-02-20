#!/bin/env python3

# Doc: https://doc.qt.io/qtforpython-6

import sys
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Hello")

		self.button = QtWidgets.QPushButton("Click me!")
		self.text = QtWidgets.QLabel(
			"Click button",
			alignment=QtCore.Qt.AlignCenter
		)

		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.addWidget(self.text)
		self.layout.addWidget(self.button)

		self.button.clicked.connect(self.magic)

	@QtCore.Slot()
	def magic(self):
		self.text.setText("Hello world")


if __name__ == "__main__":
	app = QtWidgets.QApplication([])

	widget = MyWidget()
	widget.resize(320, 240)
	widget.show()

	sys.exit(app.exec())