from enum import IntEnum

class PieceType(IntEnum):
    Pawn = 1,
    Rook = 2,
    Knight = 3,
    Bishop = 4,
    Queen = 5,
    King = 6
class Side(IntEnum):
    Up = 7,
    Down = 8,
    Tie = 9
def check_bound(p : int):
    return p>=0 and p <=7
class Board:
    pass
class Piece:
    mapping = {
        PieceType.Pawn : "p",
        PieceType.Rook : "r",
        PieceType.Knight : "k",
        PieceType.Bishop : "b",
        PieceType.Queen : "q",
        PieceType.King : "K",
        Side.Up : "u",
        Side.Down : "d"
    }
    def __init__(self,_type : PieceType,_side : Side) -> None:
        self.type = _type
        self.side = _side
    def get_move(self,board : Board):
        method_map = {
            PieceType.Pawn : self._get_pawn_move,
            PieceType.Rook : self._get_rook_move,
            PieceType.Knight : self._get_knight_move,
            PieceType.Bishop : self._get_bishop_move,
            PieceType.Queen : self._get_queen_move,
            PieceType.King : self._get_king_move
        }
        return method_map[self.type](board)
    def _get_pawn_move(self,board : Board):
        moveable = []
        capturable = []
        defensable = []
        if (self.side == Side.Up):
            side_offset = 1
        else:
            side_offset = -1
        pos = board.get_pos(self)
        target_pos = (pos[0],pos[1]+side_offset)
        if (not board.have_piece(target_pos)):
            moveable.append(target_pos)
            if ((pos[1] == 1 and self.side == Side.Up)
            or  (pos[1] == 6 and self.side == Side.Down)):
                target_pos = (pos[0],pos[1]+2*side_offset)
                if (not board.have_piece(target_pos)):
                    moveable.append(target_pos)
        if (check_bound(pos[0]-1)):
            target_pos = (pos[0]-1,pos[1]+side_offset)
            target_piece = board.get_piece(target_pos)
            if (target_piece is not None):
                if (target_piece.side != self.side):
                    capturable.append(target_pos)
                else:
                    defensable.append(target_pos)
        if (check_bound(pos[0]+1)):
            target_pos = (pos[0]+1,pos[1]+side_offset)
            target_piece = board.get_piece(target_pos)
            if (target_piece is not None):
                if (target_piece.side != self.side):
                    capturable.append(target_pos)
                else:
                    defensable.append(target_pos)
        return (moveable,capturable,defensable)
    def __get_continous_piece_move(self,board : Board,offset_signs : list):
        moveable = []
        capturable = []
        defensable = []
        pos = board.get_pos(self)
        for offset_sign in offset_signs:
            for i in range(1,8):
                target_pos = (pos[0]+offset_sign[0]*i,pos[1]+offset_sign[1]*i)
                if (check_bound(target_pos[0]) and check_bound(target_pos[1])):
                    target_piece = board.get_piece(target_pos)
                    if (target_piece is None):
                        moveable.append(target_pos)
                    elif (target_piece.side != self.side):
                        capturable.append(target_pos)
                        break
                    else:
                        defensable.append(target_pos)
                        break
        return (moveable,capturable,defensable)
    def _get_rook_move(self,board : Board):
        offset_signs = [
            (0,1),(1,0),(0,-1),(-1,0)
        ]
        return self.__get_continous_piece_move(board,offset_signs)
    def _get_bishop_move(self,board : Board):
        offset_signs = [
            (1,1),(1,-1),(-1,1),(-1,-1)
        ]
        return self.__get_continous_piece_move(board,offset_signs)
    def _get_knight_move(self,board : Board):
        moveable = []
        capturable = []
        defensable = []
        pos = board.get_pos(self)
        offsets = [
            (1,2),(-1,2),(1,-2),(-1,-2),
            (2,1),(-2,1),(2,-1),(-2,-1)
        ]
        for offset in offsets:
            target_pos = (pos[0]+offset[0],pos[1]+offset[1])
            if (check_bound(target_pos[0]) and check_bound(target_pos[1])):
                target_piece = board.get_piece(target_pos)
                if (target_piece is None):
                    moveable.append(target_pos)
                elif (target_piece.side != self.side):
                    capturable.append(target_pos)
                else:
                    defensable.append(target_pos)
        return (moveable,capturable,defensable)
    def _get_king_move(self,board : Board):
        moveable = []
        capturable = []
        defensable = []
        pos = board.get_pos(self)
        offsets = [
            (0,1),(1,0),(-1,0),(0,-1),
            (1,1),(-1,1),(1,-1),(-1,-1)
        ]
        for offset in offsets:
            target_pos = (pos[0]+offset[0],pos[1]+offset[1])
            if (check_bound(target_pos[0]) and check_bound(target_pos[1])):
                target_piece = board.get_piece(target_pos)
                if (target_piece is None):
                    moveable.append(target_pos)
                elif (target_piece.side != self.side):
                    capturable.append(target_pos)
                else:
                    defensable.append(target_pos)
        return (moveable,capturable,defensable)
    def _get_queen_move(self,board : Board):
        offset_signs = [
            (0,1),(1,0),(0,-1),(-1,0),
            (1,1),(1,-1),(-1,1),(-1,-1)
        ]
        return self.__get_continous_piece_move(board,offset_signs)
    def to_string(self):
        return self.mapping[self.type] + self.mapping[self.side]
    def to_string_minimum(self):
        return self.mapping[self.type]