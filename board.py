import copy

class PieceMove:
    Castling = True
    Enpassant = True
    @classmethod
    def get_move(self,pos,types,sides,other_properties):
        piece_type = types[pos[0]][pos[1]]
        mapping = {
            'p' : self._pawn_move,
            'r' : self._rook_move,
            'k' : self._knight_move,
            'b' : self._bishop_move,
            'q' : self._queen_move,
            'K' : self._king_move,
            None : self._none_move
        }
        return mapping[piece_type](pos,types,sides,other_properties)
    @classmethod
    def _switch_side(self,side):
        if (side == 'u'):
            return 'd'
        else:
            return 'u'
    @classmethod
    def check_bound(self,single_axis_pos):
        return single_axis_pos >= 0 and single_axis_pos <=7
    @classmethod
    def _none_move(Self,pos,types,sides,other_properties):
        return ([],[],[])
    @classmethod
    def _pawn_move(self,pos,types,sides,other_properties):
        moveable = []
        capturable = []
        defensable = []
        side = sides[pos[0]][pos[1]]
        if (side == 'u'):
            side_offset = 1
        else:
            side_offset = -1
        target_pos = (pos[0],pos[1]+side_offset)
        target_side = sides[target_pos[0]][target_pos[1]]
        if target_side == None:
            moveable.append(target_pos)
            if ((pos[1] == 1 and side == 'u')
            or  (pos[1] == 6 and side == 'd')):
                target_pos = (pos[0],pos[1]+2*side_offset)
                if sides[target_pos[0]][target_pos[1]] == None:
                    moveable.append(target_pos)
        if (self.check_bound(pos[0]-1)):
            target_pos = (pos[0]-1,pos[1]+side_offset)
            target_side = sides[target_pos[0]][target_pos[1]]
            if target_side != None:
                if (target_side != side):
                    capturable.append(target_pos)
                else:
                    defensable.append(target_pos)
            elif other_properties[self._switch_side(side)]['last_pawn_two_step'] == target_pos:
                capturable.append(target_pos)
        if (self.check_bound(pos[0]+1)):
            target_pos = (pos[0]+1,pos[1]+side_offset)
            target_side = sides[target_pos[0]][target_pos[1]]
            if target_side != None:
                if (target_side != side):
                    capturable.append(target_pos)
                else:
                    defensable.append(target_pos)
            elif other_properties[self._switch_side(side)]['last_pawn_two_step'] == target_pos:
                capturable.append(target_pos)
        return (moveable,capturable,defensable)
    @classmethod
    def _rook_move(self,pos,types,sides,other_properties):
        offset_signs = [
            (0,1),(1,0),(0,-1),(-1,0)
        ]
        return self.__get_continous_piece_move(pos,types,sides,offset_signs)
    @classmethod
    def _knight_move(self,pos,types,sides,other_properties):
        moveable = []
        capturable = []
        defensable = []
        offsets = [
            (1,2),(-1,2),(1,-2),(-1,-2),
            (2,1),(-2,1),(2,-1),(-2,-1)
        ]
        side = sides[pos[0]][pos[1]]
        for offset in offsets:
            target_pos = (pos[0]+offset[0],pos[1]+offset[1])
            if (self.check_bound(target_pos[0]) and self.check_bound(target_pos[1])):
                target_side = sides[target_pos[0]][target_pos[1]]
                if (target_side == None):
                    moveable.append(target_pos)
                elif (target_side != side):
                    capturable.append(target_pos)
                else:
                    defensable.append(target_pos)
        return (moveable,capturable,defensable)
    @classmethod
    def _bishop_move(self,pos,types,sides,other_properties):
        offset_signs = [
            (1,1),(-1,1),(1,-1),(-1,-1)
        ]
        return self.__get_continous_piece_move(pos,types,sides,offset_signs)
    @classmethod
    def _queen_move(self,pos,types,sides,other_properties):
        offset_signs = [
            (0,1),(1,0),(0,-1),(-1,0),
            (1,1),(1,-1),(-1,1),(-1,-1)
        ]
        return self.__get_continous_piece_move(pos,types,sides,offset_signs)
    @classmethod
    def _king_move(self,pos,types,sides,other_properties):
        moveable = []
        capturable = []
        defensable = []
        offsets = [
            (0,1),(1,0),(-1,0),(0,-1),
            (1,1),(-1,1),(1,-1),(-1,-1)
        ]
        side = sides[pos[0]][pos[1]]
        if (self.Castling == True and other_properties[side]['king_moved'] == False):
            if (side == 'd'):
                if (other_properties[side]['right_rook_moved'] == False):
                    flag = False
                    for i in range(pos[0]+1,7):
                        target_pos = (i,7)
                        if (sides[target_pos[0]][target_pos[1]] != None):
                            flag = True
                    if (flag == False):
                        moveable.append((6,7))
                if (other_properties[side]['left_rook_moved'] == False):
                    flag = False
                    for i in range(1,pos[0]):
                        target_pos = (i,7)
                        if (sides[target_pos[0]][target_pos[1]] != None):
                            flag = True
                    if (flag == False):
                        moveable.append((2,7))
            else:
                if (other_properties[side]['right_rook_moved'] == False):
                    flag = False
                    for i in range(pos[0]+1,7):
                        target_pos = (i,0)
                        if (sides[target_pos[0]][target_pos[1]] != None):
                            flag = True
                    if (flag == False):
                        moveable.append((6,0))
                if (other_properties[side]['left_rook_moved'] == False):
                    flag = False
                    for i in range(1,pos[0]):
                        target_pos = (i,0)
                        if (sides[target_pos[0]][target_pos[1]] != None):
                            flag = True
                    if (flag == False):
                        moveable.append((2,0))         
        for offset in offsets:
            target_pos = (pos[0]+offset[0],pos[1]+offset[1])
            if (self.check_bound(target_pos[0]) and self.check_bound(target_pos[1])):
                target_side = sides[target_pos[0]][target_pos[1]]
                if (target_side == None):
                    moveable.append(target_pos)
                elif (target_side != side):
                    capturable.append(target_pos)
                else:
                    defensable.append(target_pos)
        return (moveable,capturable,defensable)
    @classmethod
    def __get_continous_piece_move(self,pos,types,sides,offset_signs):
        moveable = []
        capturable = []
        defensable = []
        side = sides[pos[0]][pos[1]]
        for offset_sign in offset_signs:
            for i in range(1,8):
                target_pos = (pos[0]+offset_sign[0]*i,pos[1]+offset_sign[1]*i)
                if (self.check_bound(target_pos[0]) and self.check_bound(target_pos[1])):
                    target_side = sides[target_pos[0]][target_pos[1]]
                    if (target_side == None):
                        moveable.append(target_pos)
                    elif (target_side != side):
                        capturable.append(target_pos)
                        break
                    else:
                        defensable.append(target_pos)
                        break
        return (moveable,capturable,defensable)
class Board:
    def __init__(self) -> None:
        self.types = [[None for i in range(8)] for j in range(8)]
        self.sides = [[None for i in range(8)] for j in range(8)]
        self.other_properties = {
            'u' : {
                'left_rook_moved' : False,
                'right_rook_moved' : False,
                'king_moved' : False,
                'last_pawn_two_step' : None 
            },
            'd' : {
                'left_rook_moved' : False,
                'right_rook_moved' : False,
                'king_moved' : False,
                'last_pawn_two_step' : None
            }
        }
    def _add_piece(self,pos,piece : tuple = ('p','u')):
        self.types[pos[0]][pos[1]] = piece[0]
        self.sides [pos[0]][pos[1]] = piece[1]
    def _remove_piece(self,pos):
        self.types[pos[0]][pos[1]] = None
        self.sides[pos[0]][pos[1]] = None
    def get_piece(self,pos):
        result = self.types[pos[0]][pos[1]],self.sides[pos[0]][pos[1]]
        if (result[0] == None):
            return None
        else:
            return result
    def _move_piece(self,from_pos,to_pos):
        from_type = self.types[from_pos[0]][from_pos[1]]
        from_side = self.sides[from_pos[0]][from_pos[1]]
        if (from_type == 'p'):
            if (from_side == 'd'):
                if (to_pos[1]-from_pos[1] == -2):
                    self.other_properties['d']['last_pawn_two_step'] = (to_pos[0],to_pos[1]+1)
                elif(to_pos == self.other_properties['u']['last_pawn_two_step']):
                    self._remove_piece((to_pos[0],to_pos[1]+1))
                    self.other_properties[from_side]['last_pawn_two_step'] = None
            if (from_side == 'u'):
                if (to_pos[1]-from_pos[1] == 2):
                    self.other_properties['u']['last_pawn_two_step'] = (to_pos[0],to_pos[1]-1)
                elif(to_pos == self.other_properties['d']['last_pawn_two_step']):
                    self._remove_piece((to_pos[0],to_pos[1]-1))
                    self.other_properties[from_side]['last_pawn_two_step'] = None
        else:
            self.other_properties[from_side]['last_pawn_two_step'] = None
        if (from_type == 'K' and self.other_properties[from_side]['king_moved'] == False):
            self.other_properties[from_side]['king_moved'] = True
            if (self.other_properties[from_side]['left_rook_moved'] == False):
                if (from_side == 'u' and to_pos==(6,0)):
                    self._remove_piece(from_pos)
                    self._remove_piece((7,0))
                    self._add_piece(to_pos,('K','u'))
                    self._add_piece((5,0),('r','u'))
                    self.other_properties[from_side]['left_rook_moved'] == True
                    return
                elif (from_side == 'd' and to_pos==(2,7)):
                    self._remove_piece(from_pos)
                    self._remove_piece((0,7))
                    self._add_piece(to_pos,('K','d'))
                    self._add_piece((3,7),('r','d'))
                    self.other_properties[from_side]['left_rook_moved'] == True
                    return
            if (self.other_properties[from_side]['right_rook_moved'] == False):
                if (from_side == 'u' and to_pos==(2,0)):
                    self._remove_piece(from_pos)
                    self._remove_piece((0,0))
                    self._add_piece(to_pos,('K','u'))
                    self._add_piece((3,0),('r','u'))
                    self.other_properties[from_side]['left_rook_moved'] == True
                    return
                elif (from_side == 'd' and to_pos==(6,7)):
                    self._remove_piece(from_pos)
                    self._remove_piece((7,7))
                    self._add_piece(to_pos,('K','d'))
                    self._add_piece((5,7),('r','d'))
                    self.other_properties[from_side]['left_rook_moved'] == True
                    return
        if (from_type == 'r'):
            if (self.other_properties[from_side]['left_rook_moved'] == False):
                if ((from_side == 'u' and from_pos==(7,0))
                or (from_side == 'd' and from_pos==(0,7))):
                    self.other_properties[from_side]['left_rook_moved'] = True
            if (self.other_properties[from_side]['right_rook_moved'] == False):
                if ((from_side == 'u' and from_pos==(0,0))
                or (from_side == 'd' and from_pos==(7,7))):
                    self.other_properties[from_side]['right_rook_moved'] = True
                    
        self.sides[from_pos[0]][from_pos[1]] = None
        self.types[from_pos[0]][from_pos[1]] = None
        self.sides[to_pos[0]][to_pos[1]] = from_side
        self.types[to_pos[0]][to_pos[1]] = from_type
    def _valid_move(self,from_pos,to_pos) -> bool:
        from_piece = self.get_piece(from_pos)
        to_piece = self.get_piece(to_pos)
        if (from_piece != None and to_piece != None):
            if (from_piece[1] == to_piece[1]):
                return False
        elif (from_piece == None and to_piece == None):
            return False
        return True
    def move_piece(self,from_pos,to_pos):
        if (self._valid_move(from_pos,to_pos) == True):
            self._move_piece(from_pos,to_pos)
            return True
        return False
    def new_game(self):
        pos_side = [(0,'u'),(7,'d')]
        for y,side in pos_side:
            self._add_piece((0,y),('r',side))
            self._add_piece((1,y),('k',side))
            self._add_piece((2,y),('b',side))
            self._add_piece((3,y),('q',side))
            self._add_piece((4,y),('K',side))
            self._add_piece((5,y),('b',side))
            self._add_piece((6,y),('k',side))
            self._add_piece((7,y),('r',side))
        for i in range(8):
            self._add_piece((i,1),('p','u'))
        for i in range(8):
            self._add_piece((i,6),('p','d'))
    def get_moves(self,pos):
        return PieceMove.get_move(pos,self.types,self.sides,self.other_properties)
    def clone(self):
        result = Board()
        result.types = copy.deepcopy(self.types)
        result.sides = copy.deepcopy(self.sides)
        result.other_properties = copy.deepcopy(self.other_properties)
        return result
    def to_log(self):
        result = {
            'board' : self.to_string().split('\n')[:8],
            'other' : self.other_properties
        }
        return result
    def to_string(self):
        result = ""
        for i in range(8):
            line_result = ""
            for j in range(8):
                target_node = self.get_piece((j,i))
                if (target_node == None):
                    line_result += '--'
                else:
                    line_result += target_node[0]+target_node[1]
                line_result += " "
            result += line_result + "\n"
        return result
    def check_win(self):
        up_flag = False
        down_flag = False
        for i in range(8):
            for j in range(8):
                if (self.types[i][j] == 'K'):
                    if (self.sides[i][j] == 'u'):
                        up_flag = True
                    else:
                        down_flag = True
        if (up_flag and down_flag):
            return None
        elif (up_flag):
            return 'u'
        elif (down_flag):
            return 'd'
        else:
            return 'tie'