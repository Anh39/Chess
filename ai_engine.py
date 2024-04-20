import random
from board import Board
import json
import copy
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
    @classmethod
    def _read_map(self):
        result = {
            'u' : {},
            'd' : {}
        }
        with open('guide_map.json','r') as file:
            data = json.loads(file.read())
        result['u'] = copy.deepcopy(data)
        result['d'] = copy.deepcopy(data)
        for piece_name in result['u']:
            result['u'][piece_name].reverse()
        return result
    def __init__(self,depth : int = 4,ab_prune : bool = True,use_guide_map : bool = True) -> None:
        self.MAX_DEPTH = depth
        self.WIN_WEIGHT = 1000000000
        self.step = 0
        self.ab_prune = ab_prune
        self.guide_map = None
        if (use_guide_map == True):
            self.guide_map = self._read_map()
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
        other_side = 'd'
        if (input_side == 'd'):
            other_side = 'u'
        def switch_side(side):
            if (side == 'u'):
                return 'd'
            else:
                return 'u'
        def minimizer(curr_node : Node,side,depth):
            curr_node.value = -self.WIN_WEIGHT
            for child_node in curr_node.childs:
                curr_node.value = max(curr_node.value,evaluate(child_node,side,depth))
            return curr_node.value
        def maximizer(curr_node : Node,side,depth):
            curr_node.value = self.WIN_WEIGHT
            for child_node in curr_node.childs:
                curr_node.value = min(curr_node.value,evaluate(child_node,side,depth))
            return curr_node.value
        def evaluate(curr_node : Node,side,depth):
            self.step += 1
            depth += 1
            local_point,moves,captures,defenses = self.get_point(curr_node.board,input_side)
            curr_node.value = local_point
            if (depth >= self.MAX_DEPTH):
                return local_point
            if (self.ab_prune):
                parent = curr_node.parent
                if (parent != None):
                    if (side != other_side):
                        if (parent.value <= local_point):
                            return local_point
                    else:
                        if (parent.value >= local_point):
                            return local_point
                else:
                    # print('ROOT')
                    pass
            for i in range(8):
                for j in range(8):
                    capture_moves = captures[i][j]
                    if capture_moves != None and curr_node.board.sides[i][j] == side:
                        for capture_move in capture_moves:
                            new_board = curr_node.board.clone()
                            new_node = Node(new_board,curr_node)
                            curr_node.childs.append(new_node)
                            new_board._move_piece((i,j),capture_move)
            for i in range(8):
                for j in range(8):
                    move_moves = moves[i][j]
                    if move_moves != None and curr_node.board.sides[i][j] == side:
                        for move_move in move_moves:
                            new_board = curr_node.board.clone()
                            new_node = Node(new_board,curr_node)
                            curr_node.childs.append(new_node)
                            new_board._move_piece((i,j),move_move)
            if (side!=other_side):
                return minimizer(curr_node,switch_side(side),depth)
            else:
                return maximizer(curr_node,switch_side(side),depth)
        root = Node(board.clone(),None)
        depth = 0
        evaluate(root,input_side,depth)
        max_score = -self.WIN_WEIGHT
        min_board = None
        min_node = None
        for child in root.childs:
            if (child.value > max_score):
                max_score = child.value
                min_board = child.board
                min_node = child
        print(max_score)
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
            'p' : 10,
            'k' : 30,
            'b' : 30,
            'r' : 50,
            'q' : 90,
            'K' : 900,
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
                
                # for pos in p_caps[i][j]:
                #     target_type = p_types[pos[0]][pos[1]]
                #     # local_point += mapping[target_type]/4
                #     local_capture_point += mapping[target_type]/2
                
                if (self.guide_map != None):
                    local_point += self.guide_map[side][p_type][j][i]
                if (p_sides[i][j] == side):
                    ally_point += local_point
                    ally_capture_point += local_capture_point
                else:
                    enemy_point += local_point
                    enemy_capture_point += local_capture_point
        return (ally_point-enemy_point,enemy_point)
                
                
        
            