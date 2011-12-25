import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django.utils import simplejson

class College(db.Model):
    col_name = db.StringProperty(required=True)
    
class User(db.Model):
    name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    studentid = db.StringProperty(required=True)
    college = db.ReferenceProperty(College, required=True)
    admin = db.BooleanProperty(required=True)

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
        departments = Department.all()
        courses = Course.all()
        
        dep_name = []
        dep_id = []
        dep_college = []
        
        cour_name = []
        cour_id = []
        cour_department = []
        
        for department in departments:
            dep_name.append(department.dep_name)
            dep_id.append(department.key().id())
            dep_college.append(department.dep_college.key().id())
            
        for course in courses:
            cour_name.append(course.cour_name)
            cour_id.append(course.key().id())
            cour_department.append(course.cour_department.key().id())    
        
        template_values = { 'colleges': colleges,
                            'departments_name' : simplejson.dumps(dep_name),
                            'departments_id' : simplejson.dumps(dep_id),
                            'departments_college' : simplejson.dumps(dep_college), 
                            'courses_name' : simplejson.dumps(cour_name),
                            'courses_id' : simplejson.dumps(cour_id),
                            'courses_department' :  simplejson.dumps(cour_department)
                            }

        path = os.path.join(os.path.dirname(__file__), 'html/taskbook.html')
        self.response.out.write(template.render(path, template_values))

                
application = webapp.WSGIApplication([('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()