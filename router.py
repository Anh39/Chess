from aiohttp import web
import os
import asyncio
import json
from enum import Enum
import time
from game import Game
from board import Board
from ai_engine import MinimaxEngine

routes = web.RouteTableDef()
no_cache = {'Cache-Control':'no-cache'}
game = Game(Board(),MinimaxEngine())
game.board.new_game()

@routes.get('/')
async def entry(request : web.Request):
    try:
        response = web.FileResponse(path='asset/index.html',status=200,headers=no_cache)
        return response
    except:
        return web.Response(text='Server error',status=500)

@routes.post('/board/{command}')
async def board_request(request : web.Request):
    try:
        command = request.match_info['command']
        if (command == 'render'):
            result = game.i_display()
            return web.Response(text=json.dumps(result),content_type='text/json',status=200,headers=no_cache)
        elif (command == 'get_move'):
            data = await request.json()
            side = data['Side']
            pos = (data['Position']['x'],data['Position']['y'])
            result = game.i_display_move(pos,side[:1])
            if (result is not None):
                return web.Response(text=json.dumps(result),content_type='text/json',status=200,headers=no_cache)
            else:
                return web.Response(text='null',content_type='text/plain',status=404,headers=no_cache)
        elif (command == 'move'):
            data = await request.json()
            from_pos = (data['From']['x'],data['From']['y'])
            to_pos = (data['To']['x'],data['To']['y'])
            game.i_player_move(from_pos,to_pos)
            result = game.i_display()
            return web.Response(text=json.dumps(result),content_type='text/json',status=200,headers=no_cache)
        elif (command == 'bot_move'):
            game.i_bot_move()
            result = game.i_display()
            return web.Response(text=json.dumps(result),content_type='text/json',status=200,headers=no_cache)
        elif (command == 'check_win'):
            result = game.i_check_win()
            return web.Response(text=result,content_type='text/plain',status=200,headers=no_cache)
        elif (command == 'new'):
            game.i_new_game()
            result = game.i_display()
            return web.Response(text=json.dumps(result),content_type='text/json',status=200,headers=no_cache)
    except Exception as e:
        print(e)
        return web.Response(text='Board Error',status= 500)

@routes.get('/{name}')
async def get_asset(request : web.Request):
    try:
        file_name = request.match_info['name']
        if (file_name.endswith('.png')):
            file_path = os.path.join('asset','img',file_name)
        else:
            file_path = os.path.join('asset',file_name)
        response = web.FileResponse(path=file_path,status=200,headers=no_cache)
        return response
    except:
        return web.Response(text="ERROR",status=500)