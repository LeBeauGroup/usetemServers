import threading
import logging

import rpyc
from rpyc.utils.server import ThreadedServer


class TemService(rpyc.Service):

	def __init__(self):
		from .temscript.instrument import Instrument
		self.instrument = Instrument()

	def on_connect(self):
		pass

	def on_disconnect(self):
		pass


class TiaService(rpyc.Service):

	def __init__(self):
		from .tiascript.application import Application
		self.application = Application()

	def on_connect(self):
		pass

	def on_disconnect(self):
		pass


def make_server(service: type, port: int) -> ThreadedServer:
	return ThreadedServer(service, port=port, protocol_config={
		"allow_public_attrs": True,
		"allow_setattr": True,
		"allow_delattr": False,
		"instantiate_custom_exceptions": True,
	})


def run_server(server: ThreadedServer):
	server.service = server.service()  # pre-instantiate Service
	server.start()


def start_server_thread(service: type, port: int) -> (threading.Thread, ThreadedServer):
	server = make_server(service, port)

	thread = threading.Thread(name=f"{service.__name__} Server",
	                          target=lambda: run_server(server),
	                          daemon=True)
	thread.start()

	return (thread, server)


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	server = make_server(TemService, 8081)
	run_server(server)
