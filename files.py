#!/usr/bin/env python
#
import os
import urllib
import sys

from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django.utils import simplejson
from apis import bitly

class TestHandler(webapp.RequestHandler):
    def get(self):
        colleges = db.GqlQuery("SELECT * FROM College")
        departments = db.GqlQuery("SELECT * FROM Department").run()
        dep_name = []
        dep_college = []
        for department in departments:
            dep_col = db.GqlQuery("SELECT * FROM College WHERE __key__ = KEY('College', :1)",  department.dep_college.key().id())
            dep_name.append(department.dep_name)
            dep_college.append(dep_col[0].col_name)
        upload_url = blobstore.create_upload_url('/files/upload')
        template_values = { 'action': upload_url, 
                            'colleges': colleges,
                            'departments': simplejson.dumps(dep_name),
                            'dep_colleges': simplejson.dumps(dep_college), }
        path = os.path.join(os.path.dirname(__file__), 'html/upload.html')
        self.response.out.write(template.render(path, template_values))
        
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        if blob_info:
            
            self.redirect('/resource/%s' % str(blob_info.key()))
        else:
            self.error(404)
			
class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)
        
def main():
    application = webapp.WSGIApplication(
          [('/files/upload.html', TestHandler),
           ('/files/upload', UploadHandler),
           ('/files/serve/([^/]+)?', ServeHandler),
          ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
  main()