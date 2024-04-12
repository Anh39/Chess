from enum import IntEnum
import ai_engine
from pieces import Piece,PieceType,Side

class Board:
    def __init__(self) -> None:
        self.container = [[None for i in range(8)] for j in range(8)]
        self.pos_map = {}
        self.engine = None
    def _add_piece(self,pos,piece : Piece):
        self.container[pos[1]][pos[0]] = piece
        self.pos_map[piece] = pos
    def get_pos(self,piece : Piece):
        return self.pos_map[piece]
    def get_piece(self,pos : tuple):
        return self.container[pos[1]][pos[0]]
    def have_piece(self,pos : tuple):
        return self.container[pos[1]][pos[0]] is not None
    def _remove_piece(self,pos : tuple):
        piece = self.container[pos[1]][pos[0]] 
        self.container[pos[1]][pos[0]] = None
        self.pos_map.pop(piece)
    def _move_piece(self,from_pos : tuple, to_pos : tuple):
        previous_piece = self.container[to_pos[1]][to_pos[0]]
        if (previous_piece is  not None):
            self.pos_map.pop(previous_piece)
        piece = self.container[from_pos[1]][from_pos[0]] 
        self.container[from_pos[1]][from_pos[0]] = None
        self.container[to_pos[1]][to_pos[0]] = piece
        self.pos_map[piece] = to_pos
    def get_piece_move(self,pos : tuple):
        piece = self.get_piece(pos)
        moveable,capturable,defensable = piece.get_move(self)
        return (moveable,capturable,defensable)
    def show_piece_move(self,pos : tuple):
        moveable,capturable,defensable = self.get_piece_move(pos)
        result = ""
        for i in range(8):
            line_result = ""
            for j in range(8):
                target_pos = (j,i)
                if (target_pos == pos):
                    line_result += 'cc'
                elif (target_pos in moveable):
                    line_result += 'mo'
                elif (target_pos in capturable):
                    line_result += 'co'
                elif (target_pos in defensable):
                    line_result += 'do'
                else:
                    line_result += '--'
                line_result += " "
            result += line_result + "\n"
        return result
    def new_board(self):
        for i in range(8):
            for j in range(8):
                self.container[i][j] = None
        self.pos_map = {}
        pos_side = [(0,Side.Up),(7,Side.Down)]
        for y,side in pos_side:
            self._add_piece((0,y),Piece(PieceType.Rook,side))
            self._add_piece((1,y),Piece(PieceType.Knight,side))
            self._add_piece((2,y),Piece(PieceType.Bishop,side))
            self._add_piece((3,y),Piece(PieceType.Queen,side))
            self._add_piece((4,y),Piece(PieceType.King,side))
            self._add_piece((5,y),Piece(PieceType.Bishop,side))
            self._add_piece((6,y),Piece(PieceType.Knight,side))
            self._add_piece((7,y),Piece(PieceType.Rook,side))
        for i in range(8):
            self._add_piece((i,1),Piece(PieceType.Pawn,Side.Up))
        for i in range(8):
            self._add_piece((i,6),Piece(PieceType.Pawn,Side.Down))
    def to_string(self):
        result = ""
        for i in range(8):
            line_result = ""
            for j in range(8):
                target_node = self.get_piece((j,i))
                if (target_node == None):
                    line_result += '--'
                else:
                    line_result += target_node.to_string()
                line_result += " "
            result += line_result + "\n"
        return result
    def validate_move(self,from_pos : tuple,to_pos : tuple):
        from_piece = self.get_piece(from_pos)
        to_piece = self.get_piece(to_pos)
        if (from_piece is not None):
            if (to_piece is None or to_piece.side != from_piece.side):
                return True
        return False
    def player_move(self,from_pos : tuple,to_pos :tuple):
        from_piece = self.get_piece(from_pos)
        if (self.validate_move(from_pos,to_pos)):
            if (from_piece.side == Side.Down):
                self._move_piece(from_pos,to_pos)
                return
        print("Player move error")
    def bot_move(self,from_pos : tuple,to_pos :tuple):
        from_piece = self.get_piece(from_pos)
        if (self.validate_move(from_pos,to_pos)):
            if (from_piece.side == Side.Up):
                self._move_piece(from_pos,to_pos)
                return
        print("Bot move error")
    def _get_all_board(self):
        up_pieces = {}
        down_pieces = {}
        for i in range(8):
            for j in range(8):
                target_piece = self.get_piece((i,j))
                if (target_piece == None):
                    continue
                moveable,capturable,defensable = target_piece.get_move(self)
                capturable_string = []
                defensable_string = []
                for ele in capturable:
                    capturable_string.append({
                        'pos' : ele,
                        'type' : self.get_piece(ele).to_string_minimum()
                    })
                for ele in defensable:
                    defensable_string.append({
                        'pos' : ele,
                        'type' : self.get_piece(ele).to_string_minimum()
                    })
                key = target_piece.to_string_minimum()+'1'
                if (target_piece.side == Side.Up):
                    while(key in up_pieces):
                        key=key[:-1]+str(int(key[-1])+1)
                    up_pieces[key] = {
                        'pos' : (i,j),
                        'mov' : moveable,
                        'capture' : capturable_string,
                        'defense' : defensable_string
                    }
                else:
                    while(key in up_pieces):
                        key=key[:-1]+str(int(key[-1])+1)
                    down_pieces[key] = {
                        'pos' : (i,j),
                        'mov' : moveable,
                        'capture' : capturable_string,
                        'defense' : defensable_string
                    }
        return (up_pieces,down_pieces)
    def _get_next_pos(self):
        from_pos,to_pos = self.engine.calculate(self._get_all_board())
        return(from_pos,to_pos)
    def check_win(self):
        up_king = False
        down_king = False
        for piece in self.pos_map:
            if (piece.type == PieceType.King):
                if (piece.side == Side.Up):
                    up_king = True
                else:
                    down_king = True
        if (up_king and down_king):
            return None
        elif (up_king):
            return Side.Up
        elif (down_king):
            return Side.Down
        else:
            return Side.Tie
    def cli_play(self):
        while(True):
            from_pos,to_pos = self._get_next_pos()
            self.bot_move(from_pos,to_pos)
            print(self.to_string())
            from_pos,to_pos = (int(input()),int(input())),(int(input()),int(input()))
            self.player_move(from_pos,to_pos)
            print(self.to_string())
    def i_bot_move(self):
        from_pos,to_pos = self._get_next_pos()
        self.bot_move(from_pos,to_pos)
    def i_get_moveable(self,pos : tuple,side):
        piece = self.get_piece(pos)
        if (side == 'down'):
            side = Side.Down
        elif (side == 'up'):
            side = Side.Up
        else:
            print("SIDE ERROR",side)
        if (piece.side != side):
            return
        result = []
        if (piece is not None):
            move,capture,defense = piece.get_move(self)
            result = []
            for i in range(8):
                inner_result = []
                for j in range(8):
                    piece = self.get_piece((j,i))
                    if ((j,i) in capture):
                        inner_result.append('c')
                    elif ((j,i) in move):
                        inner_result.append('m')
                    elif (piece is None):
                        inner_result.append('-')
                    else:
                        inner_result.append(piece.to_string())
                result.append(inner_result)
        return result
    def i_get_display(self):
        result = []
        for i in range(8):
            inner_result = []
            for j in range(8):
                piece = self.get_piece((j,i))
                if (piece is None):
                    inner_result.append('-')
                else:
                    inner_result.append(piece.to_string())
            result.append(inner_result)
        return result
    def i_check_win(self):
        result = self.check_win()
        if (result == Side.Up):
            return 'up'
        elif (result == Side.Down):
            return 'down'
        elif (result == Side.Tie):
            return 'tie'
        else:
            return 'not_end'
# board = Board()
# board.new_board()
# board.engine = ai_engine.RandomEngine()
# print(board.to_string())
# board.cli_play()