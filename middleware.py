# part of adding (version) prefix to all app routs
# adapted from https://stackoverflow.com/a/36033627

from flask import redirect

class PrefixMiddleware(object):
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            endpoint = environ['RAW_URI'] 
            correctedEndpoint = str(self.prefix) + endpoint
            correctedUrl = environ['wsgi.url_scheme'] + '://' \
                + environ['HTTP_HOST'] + correctedEndpoint
                
            start_response('302 Found', [('Location', correctedUrl)])
            return ['1']