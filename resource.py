import os
import urllib
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class MainPage(webapp.RequestHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        if resource:
            blob_instance = blobstore.BlobInfo.get(resource)
        else:
            self.error(404)
        if blob_instance:
            content_type = blob_instance.content_type
            filename = blob_instance.filename
            query = db.GqlQuery("SELECT * FROM Resource WHERE res_filekey2=:1", str(resource))
            resource = ''.join([self.request.host_url, '/files/serve/', resource])
            template_values = {
            'filename': filename,
            'resource': resource,
            'type': content_type,
            'short': query[0].res_short_uri,
            }
            path = os.path.join(os.path.dirname(__file__), 'html/resource.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.error(404)
        
def main():
    application = webapp.WSGIApplication(
          [('/resource/([^/]+)?', MainPage),
          ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()