from google.appengine.ext import db
from google.appengine.api import memcache

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


def get_colleges():
    """ model is a string with the name of one of the models above """
    data = memcache.get("College")
    if data is not None:
        return data
    else:
        data = {}
        colleges = College.all()
        for college in colleges:
            data[college.key().id()] = college.col_name
        memcache.add("College", data, 3600)
        return data

def get_departments():
    """ model is a string with the name of one of the models above """
    data = memcache.get("Department")
    if data is not None:
        return data
    else:
        data = [0, 1, 2]
        data[0] = []
        data[1] = []
        data[2] = []
        departments = Department.all()
        for department in departments:
            data[0].append(department.dep_name)
            data[1].append(department.key().id())
            data[2].append(department.dep_college.key().id())
        memcache.add("Department", data, 3600)
        return data

def get_courses():
    """ model is a string with the name of one of the models above """
    data = memcache.get("Course")
    if data is not None:
        return data
    else:
        data = [0, 1, 2]
        data[0] = []
        data[1] = []
        data[2] = []
        courses = Course.all()
        for course in courses:
            data[0].append(course.cour_name)
            data[1].append(course.key().id())
            data[2].append(course.cour_department.key().id())
        memcache.add("Course", data, 3600)
        return data