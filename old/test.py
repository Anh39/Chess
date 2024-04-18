from board import Board
from ai_engine import MinimaxEngine
from game import Game

board = Board()
engine = MinimaxEngine()
board.new_game()

game = Game(board,engine)
game.cli_play()

# board = Board()
# engine = MinimaxEngine()
# board.new_game()
# print(board.to_string())
# engine.caculate(board,'u')