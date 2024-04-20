from board import Board
from ai_engine import Engine

class Game:
    def __init__(self,board : Board,engine : Engine) -> None:
        self.board = board
        self.engine = engine
    def _bot_turn(self):
        self.board = self.engine.caculate(self.board,'u')
    def player_turn(self,from_pos,to_pos):
        return self.board.move_piece(from_pos,to_pos)
    def cli_play(self):
        while(True):
            self._bot_turn()
            print(f'BOT TURN')
            print(self.board.to_string())
            from_pos = (int(input())-1,int(input())-1)
            to_pos = (int(input())-1,int(input())-1)
            while (self.player_turn(from_pos,to_pos) != True):
                pass
            print(f'PLAYER TURN')
            print(self.board.to_string())
    def i_new_game(self):
        self.board = Board()
        self.board.new_game()
    def i_display(self):
        result = []
        for i in range(8):
            inner_result = []
            for j in range(8):
                piece = self.board.get_piece((i,j))
                if (piece is None):
                    inner_result.append('-')
                else:
                    inner_result.append(piece[0]+piece[1])
            result.append(inner_result)
        return result
    def i_display_move(self,pos,input_side):
        side = self.board.sides[pos[0]][pos[1]]
        if (side != input_side):
            return
        result = []
        type = self.board.types[pos[0]][pos[1]]
        if (type is not None):
            move,capture,defense = self.board.get_moves(pos)
            result = []
            for i in range(8):
                inner_result = []
                for j in range(8):
                    local_piece = self.board.get_piece((i,j))
                    if ((i,j) in capture):
                        inner_result.append('c')
                    elif ((i,j) in move):
                        inner_result.append('m')
                    elif (local_piece is None):
                        inner_result.append('-')
                    else:
                        inner_result.append('-')
                        # inner_result.append(local_piece[0]+local_piece[1])
                result.append(inner_result)
        return result
    def i_player_move(self,from_pos,to_pos):
        return self.player_turn(from_pos,to_pos)
    def i_bot_move(self):
        self._bot_turn()
    def i_check_win(self):
        result = self.board.check_win()
        if (result == 'u'):
            return 'up'
        elif (result == 'd'):
            return 'down'
        elif (result == 'tie'):
            return 'tie'
        else:
            return 'not_end'