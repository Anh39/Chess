from random import Random
import random


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
    def get_move(self,pos_x,pos_y,side):
        piece = self.container[pos_x][pos_y]
        result = []
        if (piece[0] == 'rook' or piece[0] == 'queen'):
            for i in range(1,8):
                ele = [pos_x,pos_y+i]
                if (self._check_bound(ele)):
                    result.append(ele)
                    if (self._has(ele)):
                        break
            for i in range(1,8):
                ele = [pos_x,pos_y-i]
                if (self._check_bound(ele)):
                    result.append(ele)
                    if (self._has(ele)):
                        break
            for i in range(1,8):
                ele = [pos_x+i,pos_y]
                if (self._check_bound(ele)):
                    result.append(ele)
                    if (self._has(ele)):
                        break
            for i in range(1,8):
                ele = [pos_x-i,pos_y]
                if (self._check_bound(ele)):
                    result.append(ele)
                    if (self._has(ele)):
                        break
        elif (piece[0] == 'knight'):
            temp = [[pos_x-1,pos_y-2],[pos_x-2,pos_y-1],
                      [pos_x+1,pos_y-2],[pos_x+2,pos_y-1],
                      [pos_x-1,pos_y+2],[pos_x-2,pos_y+1],
                      [pos_x+1,pos_y+2],[pos_x+2,pos_y+1]]
            for ele in temp:
                if (self._check_bound(ele)):
                    result.append(ele)
        elif (piece[0] == 'king'):
            temp = [[pos_x+1,pos_y],[pos_x-1,pos_y],
                          [pos_x,pos_y+1],[pos_x,pos_y-1]]
            for ele in temp:
                if (self._check_bound(ele)):
                    result.append(ele)
        elif (piece[0] == 'pawn'):
            if (piece[1] == 'up'):
                temp = [[pos_x+1,pos_y+1],[pos_x-1,pos_y+1]]
                for ele in temp:
                    if (self._check_bound(ele) and self.check_move(ele[0],ele[1],side) == 'capturable'):
                        result.append(ele)
                ele = [pos_x,pos_y+1]
                if (self._check_bound(ele) and self.check_move(ele[0],ele[1],side) == 'moveable'):
                        result.append(ele)
            elif (piece[1] == 'down'):
                temp = [[pos_x+1,pos_y-1],[pos_x-1,pos_y-1]]
                for ele in temp:
                    if (self._check_bound(ele) and self.check_move(ele[0],ele[1],side) == 'capturable'):
                        result.append(ele)
                ele = [pos_x,pos_y-1]
                if (self._check_bound(ele) and self.check_move(ele[0],ele[1],side) == 'moveable'):
                        result.append(ele)
        elif (piece[0] != 'bishop'):
            print('ERROR PIECE TYPE',piece[0])
        if (piece[0] == 'bishop' or piece[0] == 'queen'):
            for i in range(1,8):
                ele = [pos_x+i,pos_y+i]
                if (self._check_bound(ele)):
                    result.append(ele)
                    if (self._has(ele)):
                        break
            for i in range(1,8):
                ele = [pos_x-i,pos_y+i]
                if (self._check_bound(ele)):
                    result.append(ele)
                    if (self._has(ele)):
                        break
            for i in range(1,8):
                ele = [pos_x+i,pos_y-i]
                if (self._check_bound(ele)):
                    result.append(ele)
                    if (self._has(ele)):
                        break
            for i in range(1,8):
                ele = [pos_x-i,pos_y-i]
                if (self._check_bound(ele)):
                    result.append(ele)
                    if (self._has(ele)):
                        break
        return result
    def check_move(self,to_x : int,to_y : int,side : str) -> str:
        check = self.container[to_x][to_y]
        if (check != None):
            if (check[1] == side):
                return 'overlap'
            else:
                return 'capturable'
        else:
            return 'moveable'
    def move(self,from_x : int,from_y : int,to_x : int, to_y : int,side : str) -> bool:
        move_type = self.check_move(to_x,to_y,side)
        if (move_type == 'overlap'):
            return False
        elif (move_type == 'capturable' or move_type == 'moveable'):
            self.container[to_x][to_y] = self.container[from_x][from_y]
            self.container[from_x][from_y] = None
            return True
        
    def _check_bound(self,move : list) -> bool:
        if (move[0] >= 0 and move[1] >= 0 and move[0] < 8 and move[1] < 8):
            return True
        return False
    def out_server(self):
        mapping = {'rook':'r','knight':'k','bishop':'b','queen':'q','king':'K','pawn':'p','empty':'e',
                   'up':'u','down':'d','neural':''}
        result = []
        for i in range(8):
            inner_list = []
            for j in range(8):
                check = self.container[j][i] or ['empty','neural']
                inner_list.append(mapping[check[0]]+mapping[check[1]])
            result.append(inner_list)
        return result
    def out_server_moveable(self,pos : list,side : str):
        mapping = {'rook':'r','knight':'k','bishop':'b','queen':'q','king':'K','pawn':'p','empty':'e',
                   'up':'u','down':'d','capturable':'c','moveable':'m','neural':''}
        result = []
        moves = self.get_move(pos[0],pos[1],side)
        for i in range(8):
            inner_list = []
            for j in range(8):
                if (self.has_in_arr(moves,[j,i]) and self.check_move(j,i,side) != 'overlap'):
                    inner_list.append(mapping[self.check_move(j,i,side)])
                else: 
                    check = self.container[j][i] or ['empty','neural']
                    inner_list.append(mapping[check[0]]+mapping[check[1]])
            result.append(inner_list)
        return result
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
                   ,'overlap':'o','capturable':'c','movable':'m'}
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
    def get_side(self,pos):
        check = self.container[pos[0]][pos[1]]
        if (check != None):
            return check[1]
        else:
            return None
    def auto_play(self,side : str):
        side_pieces = []
        all_moves = []
        capture_moves = []
        for i in range(8):
            for j in range(8):
                ele = self.container[i][j]
                if (ele != None and ele[1] == side):
                    side_pieces.append([i,j])
                    move_getted = self.get_move(i,j,side)
                    print(i,j,':',move_getted)
                    for ele in move_getted:
                        move_type = self.check_move(ele[0],ele[1],side)
                        if (move_type == 'moveable'):
                            all_moves.append([[i,j],ele])
                        elif (move_type == 'capturable'):
                            capture_moves.append([[i,j],ele])
        
        if (len(capture_moves) > 0):
            it = random.randint(0,len(capture_moves)-1)
            move = capture_moves[it]
            self.move(move[0][0],move[0][1],move[1][0],move[1][1],side)
            return self.out_server()
        elif (len(all_moves) > 0):
            it = random.randint(0,len(all_moves)-1)
            move = all_moves[it]
            self.move(move[0][0],move[0][1],move[1][0],move[1][1],side)
            return self.out_server()
        else:
            print("No move available")
            return None
    def check_win(self):
        up_flag = True
        down_flag = True
        for i in range(8):
            for j in range(8):
                ele = self.container[i][j]
                if (ele == ['king','up']):
                    up_flag = False
                elif (ele == ['king','down']):
                    down_flag = False
        if (up_flag):
            return 'down'
        elif(down_flag):
            return 'up'
        return None