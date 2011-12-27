import cgi

from django.utils import simplejson

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch

class Index(webapp.RequestHandler):
    def get(self):

        EXPAND = "expand"
        SHORTEN = "shorten"
        INFO = "info"
        STATS = "stats"
        ERRORS = "errors"

        bitly = BitLy('your_login','your_apikey')

        self.response.out.write('')
        self.response.out.write(bitly.expand('31IqMl'))
        self.response.out.write(bitly.shorten('http://www.chrishannam.co.uk'))
        self.response.out.write(bitly.info('31IqMl'))
        self.response.out.write(bitly.stats('http://bit.ly/31IqMl'))
        self.response.out.write(bitly.errors())
        self.response.out.write('')

class BitLy():
    def __init__(self, login, apikey):
        self.login = login
        self.apikey = apikey

    def expand(self,param):
        request = "http://api.bit.ly/expand?version=2.0.1&shortUrl=http://bit.ly/"
        request += param
        request += "&login=" + self.login + "&apiKey=" +self.apikey

        result = urlfetch.fetch(request)
        json = simplejson.loads(result.content)
        return json

    def shorten(self,param):
        url = "http://" + param
        request = "http://api.bit.ly/shorten?version=2.0.1&longUrl="
        request += url
        request += "&login=" + self.login + "&apiKey=" +self.apikey

        result = urlfetch.fetch(request)
        json = simplejson.loads(result.content)
        return json

    def info(self,param):
        request = "http://api.bit.ly/info?version=2.0.1&hash="
        request += param
        request += "&login=" + self.login + "&apiKey=" +self.apikey

        result = urlfetch.fetch(request)
        json = simplejson.loads(result.content)
        return json

    def stats(self,param):
        request = "http://api.bit.ly/stats?version=2.0.1&shortUrl="
        request += param
        request += "&login=" + self.login + "&apiKey=" +self.apikey

        result = urlfetch.fetch(request)
        json = simplejson.loads(result.content)
        return json

    def errors(self):
        request += "http://api.bit.ly/errors?version=2.0.1&login=" + self.login + "&apiKey=" +self.apikey

        result = urlfetch.fetch(request)
        json = simplejson.loads(result.content)
        return json

application = webapp.WSGIApplication(
                                     [('/', Index)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()