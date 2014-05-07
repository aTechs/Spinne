'''
Spinne.py is a micro web framework for python 3.x
This project is the copyright of aTechs
https://github.com/aTechs
'''
### Imports
# Importing the http server and handler
from http.server import HTTPServer, BaseHTTPRequestHandler
# The template
from string import Template
# Parsing query strings
from urllib.parse import urlparse, parse_qs
# Cookies
from http.cookies import SimpleCookie
# Forms
from cgi import FieldStorage
import codecs
import os

c = SimpleCookie()

# Error handler (displayed in the console)
Error = {
    403:'Error: Forbidden.',
    404:'Error: Not found.',
    405:'Error: Method not allowed.',
    500:'Error: Internal server error.'
    }

# Files where method=post
POST = []

# A function which will return the output of a template (ending with .stmp)
def stmp(tmp):
    # It's suggested to use other template engines like mako
    t = Template(tmp)
    return t.template

## The index file, root of the website and template (can be changed)
# The directory which contains the files of the web app (root)
# The file which the path '/' will open (home)
root = './'
home = 'home.html'
# The function for the template
template = stmp

## The class which will handle requests
class Spinne(BaseHTTPRequestHandler):
    def do_GET(self):
        global Handler, path
        # Setting the handler to self (BaseHTTPRequestHandler)
        Handler = self
        # Setting the path to self.path
        path = self.path
        # Removing query strings from the current path
        self.path = urlparse(self.path).path
        # Check if the path method is POST
        if self.path in POST:
            # 405 error (method not allowed)
            self.send_error(405, Error[405])
            return
        try:
            # If current path is '/', open the home file
            if self.path == '/':
                filepath = root + '/' + home
                filepath = os.path.abspath(filepath)
                if filepath.startswith(os.path.abspath(root)):
                    file = codecs.open(filepath)
                else:
                    self.send_error(403, Error[403])
                    return
            # If not, open the file path
            else:
                filepath = root + '/' + self.path
                filepath = os.path.abspath(filepath)
                if filepath.startswith(os.path.abspath(root)):
                    file = codecs.open(filepath)
                else:
                    self.send_error(403, Error[403])
                    return
            # Read file
            try:
                c = file.read()
            except UnicodeDecodeError:
                file = codecs.open(filepath, 'rb')
                c = file.read()
            # Close file
            file.close()
            # Check the file extension
            ext = filepath.split('.')[-1]
            # If file extension is stmp, use the template function
            if ext == 'stmp':
                try:
                    c = template(c)
                except Exception as e:
                    # If any error is returned
                    # 500 error (Internal server error)
                    self.send_error(500, Error[500])
                    # Raise the error
                    raise e
                    return
                # Change the extension to html (for the content-type)
                ext = 'html'
            self.send_response(200)
            self.send_header('Content-type', 'text/'+ext)
            self.end_headers()
            # Write the file contents to the web page
            try:
                self.wfile.write(c.encode('utf-8'))
            except AttributeError:
                self.wfile.write(c)
        except IOError:
            # If file doesn't exist
            # 404 error (File not found)
            self.send_error(404, Error[404])
        return
    def do_POST(self):
        global Handler, path
        Handler = self
        path = self.path
        self.path = urlparse(self.path).path
        if self.path not in POST:
            self.send_error(405, Error[405])
            return
        try:
            if self.path == '/':
                filepath = root + '/' + home
                filepath = os.path.abspath(filepath)
                if filepath.startswith(os.path.abspath(root)):
                    file = codecs.open(filepath)
                else:
                    self.send_error(403, Error[403])
                    return
            else:
                filepath = root + '/' + self.path
                filepath = os.path.abspath(filepath)
                if filepath.startswith(os.path.abspath(root)):
                    file = codecs.open(filepath)
                else:
                    self.send_error(403, Error[403])
                    return
            try:
                c = file.read()
            except UnicodeDecodeError:
                file = codecs.open(filepath, 'rb')
                c = file.read()
            file.close()
            ext = filepath.split('.')[-1]
            if ext == 'stmp':
                try:
                    c = template(c)
                except Exception as e:
                    self.send_error(500, Error[500])
                    raise e
                    return
                ext = 'html'
            self.send_response(200)
            self.send_header('Content-type', 'text/'+ext)
            self.end_headers()
            try:
                self.wfile.write(c.encode('utf-8'))
            except AttributeError:
                self.wfile.write(c)
        except IOError:
            self.send_error(404, Error[404])
        return

# A class for responses
class response:
    # Redirection
    def redirect(path):
        # Send response and header to change the location/path to another
        Handler.send_response(302)
        Handler.send_header('Location', path)
        Handler.end_headers()
        return
    # Setting a cookie
    def cookie(name, value, path, expires=None, maxage=None):
        # Setting the name, value, path and expiration date and maxage (in seconds)
        c[name] = value
        c[name]['path'] = path
        # Expirse and maxage can be left empty
        if expires is not None:
            c[name]['expires'] = expires
        if maxage is not None:
            c[name]['max-age'] = maxage
        co = c.output().split(': ')
        # Send the header which sets the cookie
        Handler.send_header(co[0], co[1])
        # Clear the simple cookie
        c.clear()
        return
    def delete_cookie(name):
        # Get the list of cookies
        co = Handler.headers.get('Cookie')
        if co == None:
            return None
        # Load them to simple cookie
        c.load(co)
        # Find the cookie which you want to delete
        cv = c[name]
        # Clear the simple cookie
        c.clear()
        # Delete the cookie
        Handler.send_header('Set-Cookie', '%s=%s;path=%s;expires=Thu, 01 Jan 1970 00:00:00 GMT' %(name, cv.value, cv['path']))
        return

# A class for requests
class request:
    # Query strings
    def query_strings():
        # Parse the path and store the query strings
        qs = urlparse(path).query
        # Parse the query strings
        qsd = parse_qs(qs)
        # Return the query strings
        return qsd
    # Get a cookie
    def cookie(name):
        # Get the list of cookies
        co = Handler.headers.get('Cookie')
        if co == None:
            return None
        # Load them to simple cookie
        c.load(co)
        # Find the cookie which you want and store it's value
        cv = c[name].value
        # Clear the simple cookie
        c.clear()
        # Return the cookie value
        return cv
    # Get form input
    def form(name):
        f = FieldStorage(fp=Handler.rfile, headers=Handler.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':Handler.headers['Content-Type']})
        # Return value
        return f[name].value
    # Get file input
    def file(name):
        f = FieldStorage(fp=Handler.rfile, headers=Handler.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':Handler.headers['Content-Type']})
        # Return name and value
        return [f[name].filename, f[name].value]

# A class for the server
class Server(object):
    # Setting the host and port
    def __init__(self, host, port):
        self.host = host
        self.port = port
    # Running the server
    def run(self):
        try:
            s = HTTPServer((self.host, self.port), Spinne)
            print('Starting Spinne server.')
            print('Version: 1.0')
            print('Copyright: aTechs.')
            print('Serving at (%s, %s).' %(self.host, str(self.port)))
            print('Close the server by Ctrl-C.')
            s.serve_forever()
        # If Ctrl-C is pressed, close the server
        except KeyboardInterrupt:
            print('Closing sever.')
