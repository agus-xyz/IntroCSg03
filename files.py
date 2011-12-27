#!/usr/bin/env python
#
import os
import urllib
import sys
import models

from google.appengine.api import users
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
        title = self.request.get('title')
        college = self.request.get('college')
        department = self.request.get('department')
        dep = db.GqlQuery("SELECT * FROM Department WHERE dep_name = :dep_name", dep_name=department)
        dep.run()
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
            resource = models.Resource(res_title=title, res_filekey=str(blob_info.key()), res_dep=dep[0], res_filekey2=str(blob_info.key()), res_short_uri=short)
            resource.put()
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