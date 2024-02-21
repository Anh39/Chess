from http.server import HTTPServer
from game import board
from server import MyHTTPRequeestHandler
import server as server

test_board = board()
test_board.start()
server.chess_board = test_board

local_add = '127.0.0.1'
port = 6969
def run(server_class = HTTPServer,handler_class=MyHTTPRequeestHandler,port=port,local = local_add):
    server_address = (local,port)
    httpd = server_class(server_address,handler_class)
    print(f'Server is listening on: http://{local}:{port}')
    httpd.serve_forever()
run()