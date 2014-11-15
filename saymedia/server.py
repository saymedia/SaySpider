import cherrypy

class Crawler(object):
    exposed = True

    # def GET(self, id=None):
    #     return id

    def POST(self, url, since=None, report=None):
        return url, since, report

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
