import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class College(db.Model):
    col_name = db.StringProperty(required=True)

class Department(db.Model):
    dep_name = db.StringProperty(required=True)
    dep_college = db.ReferenceProperty(College, required=True)

class Course(db.Model):
    cour_name = db.StringProperty(required=True)
    cour_department = db.ReferenceProperty(Department, required=True)
    cour_professor = db.StringProperty(required=True)

class Resource(db.Model):
    res_filekey = db.BlobProperty(required=True)
    res_author = db.UserProperty(required=True)
    res_title = db.StringProperty(required=True, multiline=False)
    res_add_date = db.DateTimeProperty(required=True, auto_now_add=True)
    res_college = db.ReferenceProperty(College, required=True)
    res_course_ = db.ReferenceProperty(Course, required=True)
    res_short_uri = db.LinkProperty(required=True)
        
class Comment(db.Model):
    co_text = db.TextProperty()
    co_user = db.UserProperty(required=True)
    co_content = db.StringProperty(required=True, multiline=True)
    co_upvotes = db.IntegerProperty(required=True)
    co_downvotes = db.IntegerProperty(required=True)
    co_title = db.StringProperty(required=True, multiline=False)
    co_resource = db.ReferenceProperty(Resource, required=True)
    co_add_date = db.DateTimeProperty(required=True, auto_now_add=True)
    
class MainPage(webapp.RequestHandler):
    def get(self):
        colleges = College.all()
        template_values = {
            'colleges':colleges,
            }

        path = os.path.join(os.path.dirname(__file__), 'html/index.html')
        self.response.out.write(template.render(path, template_values))

        
application = webapp.WSGIApplication([('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()