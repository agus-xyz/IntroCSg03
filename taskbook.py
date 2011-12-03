import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

 
class User(db.Model):
    
    name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    studentid = db.StringProperty(required=True)
    college = db.IntegerProperty(required=True)
    admin = db.BooleanProperty(required=True)

class College(db.Model):
    name = db.StringProperty(required=True)

class Course(db.Model):
    serialnumber = db.IntegerProperty(required=True)
    name = db.StringProperty(required=True)
    college = db.IntegerProperty(required=True)
    professor = db.StringProperty()
    room = db.StringProperty()
    url = db.StringProperty()
      
class Resource(db.Model):
    name = db.StringProperty(required=True)
    course = db.IntegerProperty(required=True)
    author = db.IntegerProperty(required=True)
    resourcetype = db.StringProperty()
    date = db.DateProperty(required=True)
    description = db.StringProperty(multiline=True)
    url = db.StringProperty(required=True)
    dateUploaded = db.DateTimeProperty(auto_now_add=True)  

class MainPage(webapp.RequestHandler):
    def get(self):
        colleges = College.all()
        
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'colleges':colleges,
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


class AdminDB(webapp.RequestHandler):
    def post(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'admindb.html')
        self.response.out.write(template.render(path, template_values))

class NewCollege(webapp.RequestHandler):
    def post(self):
        college = College(name=self.request.get('name'))
        college.put()
    
        
application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
