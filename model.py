from google.appengine.ext import db

class College(db.Model):
    col_name = db.StringProperty(required=True)

class Department(db.Model):
    dep_name = db.StringProperty(required=True)
    dep_college = db.ReferenceProperty(College, required=True)
    
class Course(db.Model):
    cour_name = db.StringProperty(required=True)
    cour_department = db.ReferenceProperty(Department, required=True)
    
class User(db.Model):
    name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    studentid = db.StringProperty(required=True)
    college = db.ReferenceProperty(College, required=True)
    admin = db.BooleanProperty(required=True)

class Resource(db.Model):
    res_filekey = db.BlobProperty(required=True)
    res_author = db.ReferenceProperty(User,required=True)
    res_title = db.StringProperty(required=True, multiline=False)
    res_add_date = db.DateTimeProperty(required=True, auto_now_add=True)
    res_course = db.ReferenceProperty(Course, required=True)
    res_short_uri = db.LinkProperty(required=True)
    res_filekey2 = db.StringProperty(required=True)
    
