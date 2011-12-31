import os
import model
from model import Course
from model import Resource
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson


class MainPage(webapp.RequestHandler):
    def get(self):
        colleges = model.get_colleges()
        departments = model.get_departments()
        courses = model.get_courses()
        
        dep_name = departments[0]
        dep_id = departments[1]
        dep_college = departments[2]
        
        cour_name = courses[0]
        cour_id = courses[1]
        cour_department = courses[2]
              
        template_values = { 'colleges': colleges,
                            'departments_name' : simplejson.dumps(dep_name),
                            'departments_id' : simplejson.dumps(dep_id),
                            'departments_college' : simplejson.dumps(dep_college), 
                            'courses_name' : simplejson.dumps(cour_name),
                            'courses_id' : simplejson.dumps(cour_id),
                            'courses_department' :  simplejson.dumps(cour_department)
                            }

        path = os.path.join(os.path.dirname(__file__), 'html/taskbook.html')
        self.response.out.write(template.render(path, template_values))

class GetResources(webapp.RequestHandler):
    def post(self):
        resources = Resource.all()
        course = Course.get_by_id(int(self.request.get('course')))
        selected_resources = []
        
        for r in resources:
            if r.res_course.key().id() == course.key().id():
                selected_resources.append(r)
        
        template_values = {'course' : course,
                           'resources' : selected_resources
                           }      
        path = os.path.join(os.path.dirname(__file__), 'html/results.html')
        self.response.out.write(template.render(path, template_values))
        
                
application = webapp.WSGIApplication([('/', MainPage),
                                      ('/getResources',GetResources)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()