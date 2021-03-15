import logging
import os

import sys
import multiprocessing
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QFile
from PyQt5 import uic
import subprocess
import time
import threading

from .server import start_server_thread, TiaService, TemService

path = os.path.dirname(os.path.realpath(__file__))

# class ServerThread(threading.Thread):
# 	def __init__(self):
# 		self.stdout = None
# 		self.stderr = None
# 		threading.Thread.__init__(self)
#
# 	def run(self):
# 		p = subprocess.Popen(['python', 'servers/temscript_server.py'],
#                              shell=False,
#                              stdout=subprocess.PIPE)
#
# 		for stdout_line in iter(p.stdout.readline, ""):
# 			yield stdout_line
# 		p.stdout.close()
#
# 		return_code = p.wait()
#
# 		self.stdout, self.stderr = p.communicate()
#
# 	def print_stdout(self):
# 		print(self.stdout.readline)


class ServerManager:
	def __init__(self, service, port):
		self.service = service
		self.port = port
		self.thread = None
		self.server = None
		self.button = None

	def running(self):
		return self.thread is not None and self.thread.is_alive()

	def register_button(self, button):
		self.button = button
		button.clicked.connect(self.toggle_server)
		self.update_button()

	def update_button(self):
		if self.button is None:
			pass
		if self.running():
			self.button.setStyleSheet("background-color: green")
		else:
			self.button.setStyleSheet("background-color: red")

	def toggle_server(self):
		if self.running():
			self.server.close()
			self.thread.join(timeout=2)
			if self.thread.is_alive():
				logging.warning(f"Could not stop {self.service.__name__} server.")
		else:
			self.server = None
			(self.thread, self.server) = start_server_thread(self.service, self.port)

		time.sleep(0.5)
		self.update_button()


def output_reader(proc):
	for line in iter(proc.stdout.readline, b''):
		print('got line: {0}'.format(line.decode('utf-8')), end='')


def main():
	logging.basicConfig(level=logging.INFO)

	# launch the pyQt window
	app = QApplication(sys.argv)

	ui_file = QFile(path + '/server.ui')
	ui_file.open(QFile.ReadOnly)
	window = uic.loadUi(ui_file)

	window.setWindowTitle('USETEM Local Servers')

	tem_manager = ServerManager(TemService, 8001)
	tia_manager = ServerManager(TiaService, 8002)

	tem_manager.register_button(window.temscript)
	tia_manager.register_button(window.tiascript)
	window.show()

	app.setActiveWindow(window)

	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
