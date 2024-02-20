from http.server import BaseHTTPRequestHandler


class MyHTTPRequeestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('GET')
        handle_get_request(self)
    def do_POST(self):
        print('POST')
        
def handle_get_request(request:MyHTTPRequeestHandler):
    if (request.path == '/'):
        handle_read_file(request,'/index.html')
    else:
        handle_read_file(request,request.path)
def handle_read_file(request:MyHTTPRequeestHandler,path : str):
    file_type = path.split('.')[-1]
    content_type = ''
    folder = ''
    if (file_type=='html'):
        content_type = 'text/html'
    elif (file_type=='css'):
        content_type = 'text/css'
    elif (file_type == 'ico'):
        content_type = 'image/x-ico'
    elif (file_type == 'js'):
        content_type = 'text/javascript'
    elif (file_type == 'png'):
        content_type = 'image/png'
        folder = '/asset'
    with open('.' + folder + path,'rb') as file:
        request.send_response(200)
        request.send_header('Content-type',content_type)
        request.end_headers()
        request.wfile.write(file.read())
    
def handle_post_request(request:MyHTTPRequeestHandler):
    pass