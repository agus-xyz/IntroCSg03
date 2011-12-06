import os

from taskbook import Course

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        
        courses = Course.all()
      
        
        template_values = {
            'courses':courses
            }

        path = os.path.join(os.path.dirname(__file__), 'html/courses.html')
        self.response.out.write(template.render(path, template_values))

 
application = webapp.WSGIApplication(
                                     [('/courses', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
