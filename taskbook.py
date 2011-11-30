import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

 
class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    
class College(db.Model):
    name = db.StringProperty()

class User(db.Model):
    name = db.StringProperty()
    studentid = db.StringProperty()
    college = db.IntegerProperty()

class Course(db.Model):
    name = db.StringProperty()
    college = db.StringProperty()
    url = db.StringProperty()
      
class Resource(db.Model):
    author = db.IntegerProperty()
    resourcetype = db.StringProperty()
    date = db.StringProperty()
    description = db.StringProperty(multiline=True)
    url = db.StringProperty
    dateUploaded = db.DateTimeProperty(auto_now_add=True)  
    

class MainPage(webapp.RequestHandler):
    def get(self):
        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)
        colleges = College.all()
        
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
            'colleges': colleges,
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Guestbook(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()
#        college = College()
#        college.name = self.request.get('content')
#        college.put();
        
        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()