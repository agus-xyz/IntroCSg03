import os
from model import Department
from model import User
from model import College
from model import Course

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app



class Users(webapp.RequestHandler):
    def get(self):
        colleges = College.all()

        elec_engi = None
        for college in colleges:
            if college.col_name == 'College of Electrical Engineering and Computer Science':
                elec_engi = college
                break
        
        chris = User(name = 'christopher',
                     password = 'christopher',
                     email = 'christopher@taskbook.org',
                     studentid = 'b00902112',
                     college = elec_engi,
                     admin = bool(1))
        chris.put()
        
        omar = User(name = 'omar',
                     password = 'omar',
                     email = 'omar@taskbook.org',
                     studentid = 't00902109',
                     college = elec_engi,
                     admin = bool(1))
        omar.put()
        
        pitillo = User(name = 'agus',
                     password = 'agus',
                     email = 'agus@taskbook.org',
                     studentid = 't00901109',
                     college = elec_engi,
                     admin = bool(1))
        pitillo.put()
        
        template_values = {'title': 'data loaded',
                           'message': 'users loaded',
                           'method': 'get',
                           'action': '/',
                           'value': 'continue' 
                            }
        path = os.path.join(os.path.dirname(__file__), 'html/message.html')
        self.response.out.write(template.render(path, template_values))
        
class Courses(webapp.RequestHandler):
    def get(self):
        departments = Department.all()
        
        comp = None
        for dep in departments:
            if dep.dep_name == 'Department of Computer Science and Information Engineering':
                comp = dep
                break
        
        course1 = Course(cour_name = 'course 1', cour_department=comp)
        course1.put()
        course2 = Course(cour_name = 'course 2', cour_department=comp)
        course2.put()
        course3 = Course(cour_name = 'course 3', cour_department=comp)
        course3.put()
         
        template_values = {'title': 'data loaded',
                           'message': 'courses loaded',
                           'method': 'get',
                           'action': '/',
                           'value': 'continue' 
                            }
        path = os.path.join(os.path.dirname(__file__), 'html/message.html')
        self.response.out.write(template.render(path, template_values))       
                
application = webapp.WSGIApplication([('/loaddb/users', Users),
                                      ('/loaddb/courses', Courses)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()