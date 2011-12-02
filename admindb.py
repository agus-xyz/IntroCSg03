import os

from taskbook import User
from taskbook import College
from taskbook import Course
from taskbook import Resource

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
        colleges = College.all()
        currentid = 0
        for college in colleges:
            if college.collegeid > currentid:
                currentid = college.collegeid
         
        college = College(name=self.request.get('name'),
                          collegeid=currentid + 1)
        college.put()
        self.redirect('/db')
        
class NewCourse(webapp.RequestHandler):
    def post(self):
        course = Course( serialnumber = int(self.request.get('serialnumber')),
                         name=self.request.get('name'),
                         college=int(self.request.get('college')),
                         professor = self.request.get('professor'),
                         room = self.request.get('room'),
                         url = self.request.get('url'))
        course.put()
        self.redirect('/db')

class NewResource(webapp.RequestHandler):
    def post(self):
        resources = Resource.all()
        currentid = 0
        for resource in resources:
            if resource.resourceid > currentid:
                currentid = resource.resourceid
              
        resource = Resource(resourceid = currentid + 1,
                            course = self.request.get('course'),
                            name = self.request.get('name'),
                            author = self.request.get('author'),
                            resourcetype = self.request.get('resourcetype'),
                            description = self.request.get('description'),
                            url = self.request.get('url'))
        resource.put()
        self.redirect('/db')        
    
        
application = webapp.WSGIApplication(
                                     [('/db', MainPage),
                                      ('/db/newCollege', NewCollege),
                                      ('/db/newUser', NewUser),
                                      ('/db/newCourse', NewCourse),
                                      ('/db/newResource', NewResource)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
