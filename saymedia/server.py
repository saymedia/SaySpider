import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

class Crawler(object):
	exposed = True

	def GET(self, id=None):
		print id

	def POST(self):
		print "CREATE NEW"

	def DELETE(self, id):
		print "Stopping %s" % id


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(Crawler(), '/', conf)
