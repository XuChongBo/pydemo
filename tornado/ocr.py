import tornado.ioloop
import tornado.web
import tornado.escape
import tornado.httpclient
import requests
import json
import urllib

APP_KEY = 'ae46e6ad-fe81-465d-bc38-6cae1d3fd0b2'
RECOG_URL = 'http://cloud.myscript.com/api/v3.0/recognition/rest/text/doSimpleRecognition.json'


class MainHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def post(self):
        applicationKey = self.get_argument('applicationKey')
        text_input = self.get_argument('textInput')
        data = {'applicationKey': APP_KEY, 'textInput': text_input}
        req = tornado.httpclient.HTTPRequest(
            url=RECOG_URL,
            method='POST',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            body=urllib.urlencode(data),
            request_timeout=10)
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(req, callback=self.on_response)

    def on_response(self, response):
        print response
        if response.error:
            raise tornado.web.HTTPError(500)
        json_response = tornado.escape.json_decode(response.body)
        print json_response
    
        self.write(tornado.escape.json_encode(json_response))
        self.finish()
        

def make_app():
    return tornado.web.Application([
        (r"/api/v1.0/text/doRecognition.json", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(7001)
    tornado.ioloop.IOLoop.current().start()
