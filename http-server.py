#!/usr/bin/python
import SimpleHTTPServer
import SocketServer
import json
import time
import string
from functools import wraps

PORT = 12000
server_address = ('127.0.0.1', PORT)

def hello():
	result = {
		"test": 1
	}
	return result

def end_fin():
    result={
        "end": 3
    }
    return result

options = {
	"/helloworld" : hello,
    	"/end" : end_fin,
}

class MyHandler (SimpleHTTPServer.SimpleHTTPRequestHandler):

	def do_GET(self):
		print "do_GET"
		func = options.get(self.path, None)
		dab_response = {
			"status": 0x00,
		}
		print self.path
		try:
			if func is not None:
				dab_response.update(func())
				json.dumps(dab_response)
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				self.wfile.write(json.dumps(dab_response))
			#else:
			#	self.send_response(404)
			#	self.send_header('Content-type','text/html')
			#	self.end_headers()
			#	self.wfile.write(json.dumps({"error": 0X01}))

		except Exception as e:

			dab_response["status"]=e.code
			dab_response["message"]=e.message
			#dab_response["connected"]= 0
			self.send_response(404)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write(json.dumps(dab_response))

		except Exception:
			raise

if __name__ == '__main__':

	#httpd = server(server_address, myHandler)

	httpd = SocketServer.TCPServer(("", PORT), MyHandler)

	print("Serveur actif sur le port:127.0.0.1", PORT)

	#socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#socket.bind(('', PORT)

	#socket.listen(5)
	#client, address = socket.accept()

	httpd.serve_forever()
