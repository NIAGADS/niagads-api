# adds (version) prefix to all app routes
# also redirects from url/endpoint to url/version/endopoint
# adapted from https://stackoverflow.com/a/36033627

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
                
            # add version and redirect
            start_response('302 Found', [('Location', correctedUrl)])
            return [bytes('1','utf-8')] # application must write bytes