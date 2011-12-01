#!/usr/bin/env python
#

import os
import urllib

from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class ResourcePage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'resource.html')
        self.response.out.write(template.render(path, path))
def main():
    application = webapp.WSGIApplication(
          [('/resource', ResourcePage),
          ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
  main()