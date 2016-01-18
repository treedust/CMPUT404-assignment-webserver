#  coding: utf-8 
import SocketServer

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#	 http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/
from os import listdir
from os import path

class MyWebServer(SocketServer.BaseRequestHandler):

	def getRequest(self,dataStr):
		temp = ""
		for char in dataStr:
			if char == "\n":
				break
			temp += char
		return temp 

	def myExplore(self,mypath):
		pathparts = mypath.split("/")[1:]
		beforeFile = ""
		#if path is directory 
		if path.isdir("./www"+mypath):
			temp = ""
			backCount = 0
			forwardCount = 0
			n = len(pathparts)-1
			for i in pathparts[n:]:
				if i == '..':
					backCount += 1
				else:
					forwardCount += 1
				if i == '':
					temp += '/'
				else:
					temp += i + '/'
			if backCount > forwardCount:
				self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n<html><body>404 Not Found</body></html>")
				return False
			#if path does not end in / redirect 
			if pathparts[-1] != '':
				self.request.sendall("HTTP/1.1 302 Found \nLocation: "+temp+"\r\n\r\n")
				return False
			#if index.html exists display page 
			if "index.html" in listdir("./www"+mypath):
				myfile = open("www"+mypath+"index.html",'r')
			else:
				self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n<html><body>404 Not Found</body></html>")
				return False
		else:
			#get directory 
			backCount = 0
			forwardCount = 0
			for i in pathparts[:-1]:
				if i == '..':
					backCount += 1
				else:
					forwardCount += 1
				if i == '':
					beforeFile += '/'
				else:
					beforeFile += i + '/'
			if backCount > forwardCount:
				self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n<html><body>404 Not Found</body></html>")
				return False
			#check can vist directory 
			try:
				listdir("./www/"+beforeFile)
			except:
				self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n<html><body>404 Not Found</body></html>")
				return False
			#if page does not exists send 404
			if pathparts[-1] not in listdir("./www/"+beforeFile):
				self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n<html><body>404 Not Found</body></html>")
				return False
			#if path ends in / then index.html for given path.
			if pathparts[-1] != '':
				myfile = open("www"+mypath,'r')
			else:
				myfile = opend("www"+mypath+"index.html",'r')
		return myfile
	
	def handle(self):
		self.data = self.request.recv(1024).strip()
		print ("Got a request of: %s\n" % self.data)
		getrequest  = str(self.getRequest(self.data)).split()
		pagerequest = getrequest[1]
		myfile = self.myExplore(pagerequest)
		if myfile == False:
			return
		if pagerequest.split(".")[-1] == "css":
			self.request.sendall("HTTP/1.1 200 OK\nContent-Type: text/css \r\n\r\n" 
				+ myfile.read() )
		else:
			self.request.sendall("HTTP/1.1 200 OK\nContent-Type: text/html \r\n\r\n" 
				+ myfile.read() )
		#self.request.sendall("OK")

if __name__ == "__main__":
	HOST, PORT = "localhost", 8080

	SocketServer.TCPServer.allow_reuse_address = True
	# Create the server, binding to localhost on port 8080
	server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
