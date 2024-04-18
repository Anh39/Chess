import random
from board import Board

class Node:
    def __init__(self,board : Board,parent = None,childs : list = None) -> None:
        self.parent = parent
        self.childs = [] if childs is None else childs
        self.board = board
        self.value = None
class Engine:
    def caculate(self,board : Board,input_side : str = 'u') -> Board:
        return None
            
class MinimaxEngine(Engine):
    def __init__(self) -> None:
        self.MAX_DEPTH = 4
        self.WIN_WEIGHT = 1000000000
        self.step = 0
    def get_moves(self,board : Board):
        moves = [[None for i in range(8)] for j in range(8)]
        captures = [[None for i in range(8)] for j in range(8)]
        defenses = [[None for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in range(8):
                piece = board.get_piece((i,j))
                if (piece != None):
                    type,side = piece
                    moves[i][j],captures[i][j],defenses[i][j] = board.get_moves((i,j))
        return (moves,captures,defenses)
    def caculate(self,board : Board,input_side : str = 'u') -> Board:
        def evaluate(side,curr_node : Node,depth):
            self.step += 1
            # print(f'Depth : {depth}')
            depth += 1
            local_point,moves,captures,defenses = self.get_point(curr_node.board,side)
            # print(f'Point : {local_point}')
            # print(curr_node.board.to_string())
            if (depth >= self.MAX_DEPTH):
                curr_node.value = local_point
            else:
                if (side == 'u'):
                    next_side = 'd'
                else:
                    next_side = 'u'
                for i in range(8):
                    for j in range(8):
                        capture_moves = captures[i][j]
                        if capture_moves != None and curr_node.board.sides[i][j] == side:
                            for capture_move in capture_moves:
                                new_board = curr_node.board.clone()
                                new_node = Node(new_board,curr_node)
                                curr_node.childs.append(new_node)
                                new_board._move_piece((i,j),capture_move)
                                evaluate(next_side,new_node,depth)
                for i in range(8):
                    for j in range(8):
                        move_moves = moves[i][j]
                        if move_moves != None and curr_node.board.sides[i][j] == side:
                            for move_move in move_moves:
                                new_board = curr_node.board.clone()
                                new_node = Node(new_board,curr_node)
                                curr_node.childs.append(new_node)
                                new_board._move_piece((i,j),move_move)
                                evaluate(next_side,new_node,depth)
                if (side == 'u'):
                    max_score = -self.WIN_WEIGHT
                    for child_node in curr_node.childs:
                        if (child_node.value > max_score):
                            max_score = child_node.value
                    curr_node.value = max_score
                elif (side == 'd'):
                    min_score = self.WIN_WEIGHT
                    for child_node in curr_node.childs:
                        if (child_node.value < min_score):
                            min_score = child_node.value
                    curr_node.value = min_score
        root = Node(board.clone(),None)
        depth = 0
        evaluate(input_side,root,depth)
        min_score = self.WIN_WEIGHT
        min_board = None
        min_node = None
        for child in root.childs:
            if (child.value < min_score):
                min_score = child.value
                min_board = child.board
                min_node = child
        # for i in range(len(self.container)):
        #     for j in range(len(self.container[i])):
        #         if (min_state[i][j] != self.container[i][j]):
        #             self.tick_in([i,j])
        # curr_node = min_node
        # print(f'Min Point : {min_score}')
        # print(min_board.to_string())
        print(min_score)
        print(f'Count : {self.step}')
        return min_board
    def get_point(self,board : Board,side : str):
        sides = board.sides
        types = board.types
        moves,captures,defenses = self.get_moves(board)
        ally_point,enemy_point = self._get_point(sides,types,moves,captures,defenses,side)
        return (ally_point,moves,captures,defenses)
    def _get_point(self,p_sides,p_types,p_moves,p_caps,p_defs,side):
        mapping = {
            'p' : 1,
            'k' : 3,
            'b' : 3,
            'r' : 5,
            'q' : 10,
            'K' : 1000,
        }
        move_multi = {
            'p' : 0.25,
            'k' : 0.25,
            'b' : 0.25,
            'r' : 0.25,
            'q' : 0.25,
            'K' : 1
        }
        capture_multi = {
            'p' : 0.1,
            'k' : 0.15,
            'b' : 0.15,
            'r' : 0.15,
            'q' : 0.25,
            'K' : 0
        }
        defense_multi = {
            'p' : 0.3,
            'k' : 0.3,
            'b' : 0.3,
            'r' : 0.3,
            'q' : 0.3,
            'K' : 0
        }
        ally_point = 0
        enemy_point = 0
        ally_capture_point = 0
        enemy_capture_point = 0
        for i in range(8):
            for j in range(8):
                local_point = 0
                p_type = p_types[i][j]
                if (p_type == None):
                    continue
                # if (p_type != 'K'):
                #     local_point += mapping[p_type]*move_multi[p_type]*len(p_moves[i][j])
                # else:
                local_point += mapping[p_type]
                # for pos in p_defs[i][j]:
                #     target_type = p_types[pos[0]][pos[1]]
                #     local_point += mapping[p_type]*defense_multi[target_type]
                local_capture_point = 0
                for pos in p_caps[i][j]:
                    target_type = p_types[pos[0]][pos[1]]
                    local_point += mapping[target_type]/4
                    local_capture_point += mapping[target_type]/2
                if (p_sides[i][j] == side):
                    ally_point += local_point
                    ally_capture_point += local_capture_point
                else:
                    enemy_point += local_point
                    enemy_capture_point += local_capture_point
        return (ally_capture_point-enemy_capture_point/2,enemy_point)
                
                
        
            