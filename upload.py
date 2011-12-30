import os
import model
from model import College
from model import Resource
from model import Department
from model import Course
from model import User
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson
from apis import bitly

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
            
        
        upload_url = blobstore.create_upload_url('/upload/submit')
                
        template_values = { 'colleges': colleges,
                            'departments_name' : simplejson.dumps(dep_name),
                            'departments_id' : simplejson.dumps(dep_id),
                            'departments_college' : simplejson.dumps(dep_college), 
                            'courses_name' : simplejson.dumps(cour_name),
                            'courses_id' : simplejson.dumps(cour_id),
                            'courses_department' :  simplejson.dumps(cour_department),
                            'action': upload_url
                            }    
        path = os.path.join(os.path.dirname(__file__), 'html/upload.html')
        self.response.out.write(template.render(path, template_values))
        
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file') 
        studentid = self.request.get('studentid')
        password = self.request.get('password')
        users = User.all()
        user = None
        for u in users:
            if u.studentid == studentid:
                if u.password == password:
                    user = u
                    break
                else:
                    break

        if user:
            title = self.request.get('title')
            course = Course.get_by_id(int(self.request.get('course')))
            blob_info = upload_files[0]
            if blob_info:
                bly = bitly.BitLy('o_2tov7hc8mi', 'R_e863d338484e0fbb60cf1416ce3ae6de')
                uri = str(os.environ.get('SERVER_NAME'))
                uri = uri + '/resource/' + str(blob_info.key())
                short = bly.shorten(uri)
                uri2 = 'http://%s' % uri
                short = short['results'][uri2]['shortUrl']
                if short:
                    pass
                else:
                    short = 'uri2'
            
                resource = Resource(res_title=title,
                                    res_filekey=str(blob_info.key()),
                                    res_course=course, 
                                    res_filekey2=str(blob_info.key()),
                                    res_short_uri=short,
                                    res_author = user)
                resource.put()
                self.redirect('/resource/%s' % str(blob_info.key()))
            else:
                self.redirect('/upload/wrong_file')
        else:
            self.redirect('/upload/wrong_user') 
        

class WrongUser(webapp.RequestHandler):
    def get(self):
        title='Authentication error'
        message='The user does not exist or the user and password provided do not match.'
        method='get'
        action='/upload'
        value='Try again'
        template_values = {'title': title,
                           'message': message,
                           'method': method,
                           'action': action,
                           'value': value}
         
        path = os.path.join(os.path.dirname(__file__), 'html/message.html')
        self.response.out.write(template.render(path, template_values))
        
class WrongFile(webapp.RequestHandler):
    def get(self):
        title='File error'
        message='Some error occurred uploading your file, please try again. Report the problem if it persists'
        method='get'
        action='/upload'
        value='Try again'
        template_values = {'title': title,
                           'message': message,
                           'method': method,
                           'action': action,
                           'value': value}
         
        path = os.path.join(os.path.dirname(__file__), 'html/message.html')
        self.response.out.write(template.render(path, template_values))        
        
def main():
    application = webapp.WSGIApplication(
          [('/upload', MainPage),
           ('/upload/submit', UploadHandler),
           ('/upload/wrong_user', WrongUser),
           ('/upload/wrong_file', WrongFile),
          ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()