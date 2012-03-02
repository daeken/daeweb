import json, os, urllib
from BaseHTTPServer import *
from glob import glob
from model import *
import handler
import handlers
from handlers import *

PORT = 8080

if os.path.exists('index.html'):
	cindex = file('index.html', 'r').read()
else:
	cindex = None

methodStubTemplate = '''%s: function(%s, callback) {
	$.ajax('/', 
		{
			success: function(data) {
				if(callback !== undefined)
					callback(data)
			}, 
			error: function() {
				if(callback !== undefined)
					callback()
			}, 
			dataType: 'json', 
			data: JSON.stringify([%r, %r, [%s]]), 
			type: 'POST'
		}
	)
}'''

def buildHandlerStubs():
	moduleStubs = ''
	for module, methods in handler.all.items():
		methodStubs = []
		for name, (types, args, _) in methods.items():
			methodStubs.append(methodStubTemplate % (name, ', '.join(args), module, name, ', '.join(args)))
		moduleStubs += 'var %s = {%s};\n' % (module, ', '.join(methodStubs))
	return moduleStubs

def getIndex():
	if cindex == None:
		index = file('index.tpl', 'r').read()
		script = buildHandlerStubs()
		script += '\n'.join(file(name, 'r').read() for name in sorted(glob('js/*.js')))
		index = index.replace('%SCRIPT%', script)
		style = '\n'.join(file(name, 'r').read() for name in glob('css/*.css'))
		index = index.replace('%STYLE%', style)
		return index
	else:
		return cindex

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		path = self.path
		if path == '/':
			self.respond('text/html', getIndex())
		elif path == '/favicon.ico':
			self.respond('image/x-icon', file('images/favicon.ico', 'rb').read())
		elif path.startswith('/images/'):
			self.respond('image/png', file('images/' + path.rsplit('/', 1)[1], 'rb').read(), forever=True)
		else:
			self.send_response(404)
			self.end_headers()
	
	def do_POST(self):
		#if state.user == None and 'Cookie' in self.headers:
		#	cookies = dict(cookie.strip().split('=', 1) for cookie in self.headers['Cookie'].split(';'))
		#	if 'usertoken' in cookies:
		#		handlers.user.token(cookies['usertoken'])
		obj = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
		if not isinstance(obj, list) or len(obj) != 3:
			return
		reload(handlers)
		module, method, data = obj
		print module, method, data
		if not hasattr(handlers, module):
			print 'module not found'
			return
		reload(getattr(handlers, module))
		module = getattr(handlers, module)
		if not hasattr(module, method):
			print 'method not found'
			return
		method = getattr(module, method)
		resp = method(*data)
		self.respond('text/x-json', json.dumps(resp))
	
	def respond(self, type, data, forever=False):
		self.send_response(200)
		self.send_header('Content-Type', type)
		if forever:
			self.send_header('Expires', 'Sun, 17-Jan-2038')
			self.send_header('Cache-control', 'public')
		self.send_header('Content-Length', len(data))
		#if state.loggedOut == True:
		#	self.send_header('Set-Cookie', 'usertoken=')
		#	state.loggedOut = False
		#elif state.user != None:
		#	self.send_header('Set-Cookie', 'usertoken=' + state.usertoken)
		self.end_headers()
		self.wfile.write(data)

def run():
	server = HTTPServer(('', PORT), Handler)
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass

if __name__=='__main__':
	run()
