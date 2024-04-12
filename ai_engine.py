import random

class RandomEngine:
    def __init__(self) -> None:
        pass
    def calculate(self,input):
        up_pieces,down_pieces = input
        capture = []
        move = []
        reverse_mapping = {}
        for ele in up_pieces:
            move.extend(up_pieces[ele]['mov'])
            for inner_ele in up_pieces[ele]['capture']:
                capture.append(inner_ele['pos'])
                reverse_mapping[inner_ele['pos']] = up_pieces[ele]['pos']
        if (len(capture) > 0):
            target_pos = random.sample(capture,k=1)[0]
            return (reverse_mapping[target_pos],target_pos)
        while(True):
            piece = up_pieces[random.sample(sorted(up_pieces),k=1)[0]]
            if (len(piece['mov'])>0):
                return (piece['pos'],random.sample(piece['mov'],k=1)[0])
            