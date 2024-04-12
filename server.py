import aiohttp
from aiohttp import web
from router import routes



app = web.Application()
app.add_routes(routes)
def start(port : int = 8080):
    """Khởi động sever

    Args:
        port (str, optional): Vị trí port, mặc định là 8080.
    """
    web.run_app(app,port=port)

start()