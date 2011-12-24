import os
from taskbook import College
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        colleges = College.all()
        template_values = {'colleges':colleges}

        path = os.path.join(os.path.dirname(__file__), 'html/signup.html')
        self.response.out.write(template.render(path, template_values))

 
application = webapp.WSGIApplication([('/signup', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
