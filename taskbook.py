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
    col_id = db.IntegerProperty(required=True)
    col_name = db.StringProperty(required=True)

class Course(db.Model):
    cour_id = db.IntegerProperty(required=True)
    cour_name = db.StringProperty(required=True)
    cour_college = db.IntegerProperty(required=True)
    cour_professor = db.StringProperty(required=True)
      

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

        path = os.path.join(os.path.dirname(__file__), 'html/index.html')
        self.response.out.write(template.render(path, template_values))


class AdminDB(webapp.RequestHandler):
    def post(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/admindb.html')
        self.response.out.write(template.render(path, template_values))

class NewCollege(webapp.RequestHandler):
    def post(self):
        college = College()
        college.name = self.request.get('name')
        college.put()
    
        
class Guestbook(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()
# college = College()
# college.name = self.request.get('content')
# college.put();
        
        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook),
                                      ('/admindb',AdminDB),
                                      ('/newCollege',NewCollege)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()