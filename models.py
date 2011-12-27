from google.appengine.ext import db

class College(db.Model):
    col_name = db.StringProperty(required=True)

class Department(db.Model):
    dep_name = db.StringProperty(required=True)
    dep_college = db.ReferenceProperty(College, required=True)

class Resource(db.Model):
    res_filekey = db.BlobProperty(required=True)
    res_author = db.UserProperty(required=True, auto_current_user=True)
    res_title = db.StringProperty(required=False, multiline=False)
    res_add_date = db.DateTimeProperty(required=True, auto_now_add=True)
    res_dep = db.ReferenceProperty(Department, required=True)
    res_short_uri = db.LinkProperty(required=True)
    res_filekey2 = db.StringProperty(required=True)