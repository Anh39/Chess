class board:
    def __init__(self) -> None:
        self.container = []
        self.turn = 'down'
    def next_turn(self):
        if (self.turn == 'down'):
            self.turn = 'up'
        else:
            self.turn = 'down'
    def start(self):
        self.container = []
        for i in range(8):
            self.container.append([None]*8)
        piece_side = 'up'
        self.container[0][0] = ['rook',piece_side]
        self.container[7][0] = ['rook',piece_side]
        self.container[1][0] = ['knight',piece_side]
        self.container[6][0] = ['knight',piece_side]
        self.container[2][0] = ['bishop',piece_side]
        self.container[5][0] = ['bishop',piece_side]
        self.container[3][0] = ['queen',piece_side]
        self.container[4][0] = ['king',piece_side]
        for i in range(8):
            self.container[i][1] = ['pawn',piece_side]
        piece_side = 'down'
        self.container[0][7] = ['rook',piece_side]
        self.container[7][7] = ['rook',piece_side]
        self.container[1][7] = ['knight',piece_side]
        self.container[6][7] = ['knight',piece_side]
        self.container[2][7] = ['bishop',piece_side]
        self.container[5][7] = ['bishop',piece_side]
        self.container[3][7] = ['queen',piece_side]
        self.container[4][7] = ['king',piece_side]
        for i in range(8):
            self.container[i][6] = ['pawn',piece_side]
    def get_move(self,pos_x,pos_y):
        piece = self.container[pos_x][pos_y]
        result = []
        if (piece[0] == 'rook' or piece[0] == 'queen'):
            for i in range(1,8):
                result.append([pos_x,pos_y+i])
                if (self._has([pos_x,pos_y+i])):
                    break
            for i in range(1,8):
                result.append([pos_x,pos_y-i])
                if (self._has([pos_x,pos_y-i])):
                    break
            for i in range(1,8):
                result.append([pos_x+i,pos_y])
                if (self._has([pos_x+i,pos_y])):
                    break
            for i in range(1,8):
                result.append([pos_x-i,pos_y])
                if (self._has([pos_x-i,pos_y])):
                    break
        elif (piece[0] == 'knight'):
            result = [[pos_x-1,pos_y-2],[pos_x-2,pos_y-1],
                      [pos_x+1,pos_y-2],[pos_x+2,pos_y-1],
                      [pos_x-1,pos_y+2],[pos_x-2,pos_y+1],
                      [pos_x+1,pos_y+2],[pos_x+2,pos_y+1]]
        elif (piece[0] == 'bishop' or piece[0] == 'queen'):
            for i in range(1,8):
                result.append([pos_x+i,pos_y+i])
                if (self._has([pos_x+i,pos_y+i])):
                    break
            for i in range(1,8):
                result.append([pos_x-i,pos_y+i])
                if (self._has([pos_x-i,pos_y+i])):
                    break
            for i in range(1,8):
                result.append([pos_x+i,pos_y-i])
                if (self._has([pos_x+i,pos_y-i])):
                    break
            for i in range(1,8):
                result.append([pos_x-i,pos_y-i])
                if (self._has([pos_x-i,pos_y-i])):
                    break
        elif (piece[0] == 'king'):
            result.append([pos_x+1,pos_y+1],[pos_x-1,pos_y-1],
                          [pos_x-1,pos_y+1],[pos_x+1,pos_y-1])
        elif (piece[0] == 'pawn'):
            if (piece[1] == 'up'):
                result.append([pos_x,pos_y+1])
            elif (piece[1] == 'down'):
                result.append([pos_x,pos_y-1])
        final_result = []
        for ele in result:
            if (self._check_bound(ele)):
                final_result.append(ele)
        return final_result
    def check_move(self,to_x : int,to_y : int,side : str) -> str:
        check = self.container[to_x][to_y]
        if (check != None):
            if (check[1] == side):
                return 'overlap'
            else:
                return 'capturable'
        else:
            return 'empty'
    def move(self,from_x : int,from_y : int,to_x : int, to_y : int,side : str) -> bool:
        move_type = self.check_move(to_x,to_y,side)
        if (move_type == 'overlap'):
            return False
        elif (move_type == 'capturable' or move_type == 'empty'):
            self.container[to_x][to_y] = self.container[from_x][from_y]
            self.container[from_x][from_y] = None
            return True
        
    def _check_bound(self,move : list) -> bool:
        if (move[0] >= 0 and move[1] >= 0 and move[0] < 8 and move[1] < 8):
            return True
        return False
    def out_render(self):
        mapping = {'rook':'r','knight':'k','bishop':'b','queen':'q','king':'K','pawn':'p','-':'-'}
        for i in range(8):
            line_temp = ''
            for j in range(8):
                check = self.container[j][i] or ['-']
                line_temp += mapping[check[0]] + '|'
            print(line_temp)
    def out_moveable(self,moves : list,side : str):
        mapping = {'rook':'r','knight':'k','bishop':'b','queen':'q','king':'K','pawn':'p','-':'-'
                   ,'overlap':'o','capturable':'c','empty':'e'}
        for i in range(8):
            line_temp = ''
            for j in range(8):
                if (self.has_in_arr(moves,[j,i])):
                    line_temp += mapping[self.check_move(j,i,side)] + '|'
                    
                else:
                    check = self.container[j][i] or ['-']
                    line_temp += mapping[check[0]] + '|'
            print(line_temp)
    def _has(self,pos):
       check = self.container[pos[0]][pos[1]]
       if (check != None):
           return True
       else:
           return False
    def has_in_arr(self,arr,pos):
        for ele in arr:
            if (ele == pos):
                return True
        return False
            
    