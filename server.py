#  coding: utf-8 
import SocketServer

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
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


class MyWebServer(SocketServer.BaseRequestHandler):

    def getRequest(self,dataStr):
        temp = ""
        for char in dataStr:
            if char == "\n":
                break
            temp += char
        return temp 
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        httpHeader200 = "HTTP/1.1 200"
        httpHeader404 = "HTTP/1.1 404"
        getrequest  = str(self.getRequest(self.data)).split()
        pagerequest = getrequest[1]
        if pagerequest not in ["/","/index.html","/base.css","/deep/deep.css","/deep/index.html" ]:
            self.request.sendall(httpHeader404)
            return
        myfile = open("www/index.html", 'r')
        self.request.sendall(httpHeader200 + " \nContent-Type: text/css\r\n\r\n" + myfile.read() )
        #self.request.sendall("OK")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
