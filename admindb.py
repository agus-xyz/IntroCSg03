import os

from taskbook import User
from taskbook import College
from taskbook import Course
from taskbook import Resource

import datetime

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        users = User.all()
        colleges = College.all()
        courses = Course.all()
        resources = Resource.all()
        
        template_values = {
            'users': users,
            'colleges': colleges,
            'courses':courses,
            'resources':resources,
            }

        path = os.path.join(os.path.dirname(__file__), 'admindb.html')
        self.response.out.write(template.render(path, template_values))

class NewUser(webapp.RequestHandler):
    def post(self):
        user = User(name=self.request.get('name'),
                    password=self.request.get('password'),
                    email=self.request.get('email'),
                    studentid=self.request.get('studentid'),
                    college=int(self.request.get('college')),
                    admin=bool(self.request.get('admin'))
                    )
        user.put()
        self.redirect('/db')

class NewCollege(webapp.RequestHandler):
    def post(self):
        college = College(name=self.request.get('name'))
        college.put()
        self.redirect('/db')
        
class NewCourse(webapp.RequestHandler):
    def post(self):
        course = Course(serialnumber=int(self.request.get('serialnumber')),
                         name=self.request.get('name'),
                         college=int(self.request.get('college')),
                         professor=self.request.get('professor'),
                         room=self.request.get('room'),
                         url=self.request.get('url'))
        course.put()
        self.redirect('/db')

class NewResource(webapp.RequestHandler):
    def post(self):
        resource = Resource(course=int(self.request.get('course')),
                            name=self.request.get('name'),
                            author=int(self.request.get('author')),
                            resourcetype=self.request.get('resourcetype'),
                            description=self.request.get('description'),
                            url=self.request.get('url'),
                            date=datetime.date(year=int(self.request.get('date.year')), month=int(self.request.get('date.month')), day=int(self.request.get('date.day'))))
        resource.put()
        self.redirect('/db')        

class RemoveUser(webapp.RequestHandler):
    def post(self):
        user = User.get_by_id(int(self.request.get('id'))) 
        user.delete()
        self.redirect('/db')
            
class RemoveCollege(webapp.RequestHandler):
    def post(self):
        college = College.get_by_id(int(self.request.get('id')))
        college.delete()
        self.redirect('/db') 
class RemoveCourse(webapp.RequestHandler):
    def post(self):
        course = Course.get_by_id(int(self.request.get('id')))
        course.delete()
        self.redirect('/db') 
        
class RemoveResource(webapp.RequestHandler):
    def post(self):  
        resource = Resource.get_by_id(int(self.request.get('id')))
        resource.delete()
        self.redirect('/db')
        
class EditUser(webapp.RequestHandler):
    def post(self):
        user = User.get_by_id(int(self.request.get('id')))
        user.name = self.request.get('name')
        user.password = self.request.get('password')
        user.email = self.request.get('email')
        user.studentid = self.request.get('studentid')
        user.college = int(self.request.get('college'))
        user.admin = bool(self.request.get('admin'))
        user.put()
        self.redirect('/db')
       
class EditCollege(webapp.RequestHandler):
    def post(self):
        college = College.get_by_id(int(self.request.get('id')))
        college.name = self.request.get('name')
        college.put()
        self.redirect('/db')
        
class EditCourse(webapp.RequestHandler):
    def post(self):
        course = Course.get_by_id(int(self.request.get('id')))
        course.serialnumber = int(self.request.get('serialnumber'))
        course.name = self.request.get('name')
        course.college = int(self.request.get('college'))
        course.professor = self.request.get('professor')
        course.room = self.request.get('room')
        course.url = self.request.get('url')
        course.put()
        self.redirect('/db')

class EditResource(webapp.RequestHandler):
    def post(self):
        resource = Resource.get_by_id(int(self.request.get('id')))
        resource.course = self.request.get('course')
        resource.name = self.request.get('name')
        resource.author = self.request.get('author')
        resource.resourcetype = self.request.get('resourcetype')
        resource.description = self.request.get('description')
        resource.url = self.request.get('url')
        resource.put()
        self.redirect('/db') 
 
application = webapp.WSGIApplication(
                                     [('/db', MainPage),
                                      ('/db/newCollege', NewCollege),
                                      ('/db/newUser', NewUser),
                                      ('/db/newCourse', NewCourse),
                                      ('/db/newResource', NewResource),
                                      ('/db/removeCollege', RemoveCollege),
                                      ('/db/removeUser', RemoveUser),
                                      ('/db/removeCourse', RemoveCourse),
                                      ('/db/removeResource', RemoveResource),
                                      ('/db/editCollege', EditCollege),
                                      ('/db/editUser', EditUser),
                                      ('/db/editCourse', EditCourse),
                                      ('/db/editResource', EditResource)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
