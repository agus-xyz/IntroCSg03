import os
import model
from model import College
from model import User
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        colleges = model.get_colleges()
        template_values = {'colleges':colleges}

        path = os.path.join(os.path.dirname(__file__), 'html/signup.html')
        self.response.out.write(template.render(path, template_values))

class NewUser(webapp.RequestHandler):
    def post(self):
        user = User(name=self.request.get('name'),
                    password=self.request.get('password'),
                    email=self.request.get('email'),
                    studentid=self.request.get('studentid'),
                    college=College.get_by_id(int(self.request.get('college'))),
                    admin=bool('')
                    )
        user.put()
         
        title='Thank you, ' + self.request.get('name')
        message='The new user was successfully created. Now you can share your resources. Enjoy.'
        method='get'
        action='/'
        value='continue'
        template_values = {'title': title,
                           'message': message,
                           'method': method,
                           'action': action,
                           'value': value}
         
        path = os.path.join(os.path.dirname(__file__), 'html/message.html')
        self.response.out.write(template.render(path, template_values))
                

 
application = webapp.WSGIApplication([('/signup', MainPage),
                                      ('/signup/newUser', NewUser)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
