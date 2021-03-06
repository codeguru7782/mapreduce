#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep,popen
import cgi

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index_example3.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests
	def do_POST(self):
		if self.path=="/send":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})
			cmd = "/home/hduser/mapreduce.sh "
	                cmd = cmd +  form["lat"].value + " "
                	cmd = cmd + form["lon"].value + " "
                	cmd = cmd + form["type"].value + " "
                	cmd = cmd + form["out"].value
                	f = popen(cmd)
                	now = f.read()
			dfs_cmd = "/usr/local/hadoop/bin/hadoop dfs -cat " + "/user/hduser/vikram/" + form["out"].value + "/part-00000" + " > /home/hduser/data/tmp/test"
			f = popen(dfs_cmd)
			print dfs_cmd
			ins = open( "/home/hduser/data/tmp/test", "r" )
			print ins.readline()
			self.send_response(200)
			self.send_header('Content-type','text/html')
                        self.end_headers()
			print ins.name
			self.wfile.write("<h1>Result of the Query</h1>" +  "<br>")
			for line in reversed(list(ins)):
				print line
				amenity = line.split()
				rest = " ".join(amenity[1:])
				self.wfile.write(rest.split(':')[1])
				self.wfile.write("<br>")
			ins.close()
			return			
			
			
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	
