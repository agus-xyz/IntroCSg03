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
import apis.googl

class Resource(db.Model):
    res_id = db.IntegerProperty(required=True)
    res_filekey = db.StringProperty(required=True, multiline=False)
    res_author = db.UserProperty(required=True)
    res_title = db.StringProperty(required=True, multiline=False)
    res_date = db.DateTimeProperty(required=True, auto_now_add=True)
    res_college_id = db.IntegerProperty(required=True)
    res_course_id = db.IntegerProperty(required=True)
    res_short_uri = db.LinkProperty(required=True)
    
class Comments(db.Model):
    co_id = db.IntegerProperty(required=True)
    co_user = db.UserProperty(required=True)
    co_content = db.StringProperty(required=True, multiline=True)
    co_upvotes = db.IntegerProperty(required=True)
    co_downvotes = db.IntegerProperty(required=True)
    co_title = db.StringProperty(required=True, multiline=False)
    co_res_id = db.IntegerProperty(required=True)

class TestHandler(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/files/upload')
        template_values = { 'action': upload_url, }
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