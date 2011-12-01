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
        users = User.all()
        currentid = 0
        for user in users:
            if user.userid>currentid:
                currentid=user.userid
        user = User(userid = currentid + 1,
                    name = self.request.get('name'),
                    password = self.request.get('password'),
                    email = self.request.get('email'),
                    studentid = self.request.get('studentid'),
                    college = int(self.resquest.get('college'))
                    )
        user.put()
        self.redirect('/db')

class NewCollege(webapp.RequestHandler):
    def post(self):
        colleges = College.all()
        currentid = 0
        for college in colleges:
            if college.collegeid>currentid:
                currentid=college.collegeid
         
        college = College(name = self.request.get('name'),
                          collegeid = currentid + 1)
        college.put()
        self.redirect('/db')
        
class NewCourse(webapp.RequestHandler):
    def post(self):
        college = College(name = self.request.get('name'))
        college.put()

class NewResource(webapp.RequestHandler):
    def post(self):
        college = College(name = self.request.get('name'))
        college.put()        
    
        
application = webapp.WSGIApplication(
                                     [('/db', MainPage),
                                      ('/db/newCollege',NewCollege),
                                      ('/db/newUser',NewUser),
                                      ('/db/newCourse',NewCourse),
                                      ('/db/newResource',NewResource)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()