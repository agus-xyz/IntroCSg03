import os
from model import College
from model import Department
from model import Course
from model import Resource
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson


class MainPage(webapp.RequestHandler):
    def get(self):
        colleges = College.all()
        departments = Department.all()
        courses = Course.all()
        
        dep_name = []
        dep_id = []
        dep_college = []
        
        cour_name = []
        cour_id = []
        cour_department = []
        
        for department in departments:
            dep_name.append(department.dep_name)
            dep_id.append(department.key().id())
            dep_college.append(department.dep_college.key().id())
            
        for course in courses:
            cour_name.append(course.cour_name)
            cour_id.append(course.key().id())
            cour_department.append(course.cour_department.key().id())    
        
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