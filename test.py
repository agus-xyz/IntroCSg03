from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache

class Test(webapp.RequestHandler):
    def get(self):
        
        stats = memcache.get_stats()
        self.response.out.write('misses: '+str(stats['misses'])+'<br>')
        self.response.out.write('hits: '+str(stats['hits'])+'<br>')
        self.response.out.write('items: '+str(stats['items'])+'<br>')
class Flush(webapp.RequestHandler):
    def get(self):
        a = memcache.flush_all()
        if a == True:
            self.response.out.write('Flush Succesfully Completed')  

def main():
    application = webapp.WSGIApplication(
          [('/test/', Test),
           ('/test/flush', Flush),
          ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()