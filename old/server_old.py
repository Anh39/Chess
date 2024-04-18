from http.server import BaseHTTPRequestHandler
import json
from game_old import board

chess_board = board()
last_move_check = None
class MyHTTPRequeestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('GET')
        handle_get_request(self)
    def do_POST(self):
        print('POST')
        handle_post_request(self)
        
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
    request_type = request.headers['Request-type']
    content_length = int(request.headers['Content-Length'])
    post_data = request.rfile.read(content_length).decode('utf-8')
    data = json.loads(post_data)
    global chess_board,last_move_check
    if (request_type=='fetch_board'):
        request.send_response(200)
        request.send_header('Content-type','text/json')
        request.end_headers()
        request.wfile.write(str(chess_board.out_server()).replace("'",'"').encode('utf-8'))
    elif (request_type=='fetch_moveable'):
        side = data['Side']
        pos_num = int(data['Position'])
        pos = [pos_num//10,pos_num%10]
        if (chess_board.get_side(pos) == side):
            last_move_check = pos
            request.send_response(200)
            request.send_header('Content-type','text/json')
            request.end_headers()
            request.wfile.write(str(chess_board.out_server_moveable(pos,side)).replace("'",'"').encode('utf-8'))
        else:
            request.send_response_only(200)
            request.send_header('Content-type','text/json')
            request.end_headers()
    elif (request_type=='move_piece'):
        side = data['Side']
        other_side = data['Other-side']
        pos_num = int(data['To'])
        pos = [pos_num//10,pos_num%10]
        if (chess_board.get_side(pos) == None or chess_board.get_side(pos) != side):
            request.send_response(200)
            request.send_header('Content-type','text/json')
            chess_board.move(last_move_check[0],last_move_check[1],pos[0],pos[1],side)
            winner = chess_board.check_win()
            if (winner == None):
                chess_board.auto_play(other_side)
                winner = chess_board.check_win()
                if (winner == None):
                    request.send_header('Game-state','continue')
                    request.end_headers()
                    request.wfile.write(str(chess_board.out_server()).replace("'",'"').encode('utf-8'))
                else:
                    request.send_header('Game-state','lose')
                    request.end_headers()
            else:
                request.send_header('Game-state','win')
                request.end_headers()
        else:
            request.send_response_only(200)
            request.send_header('Content-type','text/json')
            request.end_headers()
    elif (request_type=='reset'):
        chess_board = board()
        chess_board.start()
        request.send_response(200)
        request.send_header('Content-type','text/json')
        request.end_headers()
        request.wfile.write(str(chess_board.out_server()).replace("'",'"').encode('utf-8'))
        
    