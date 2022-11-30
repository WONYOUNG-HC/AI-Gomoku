board_size = 15
empty = 0
black_stone = 1
white_stone = 2
last_b_stone = 3
last_a_stont = 4
tie = 100

class Rule(object):
    def __init__(self, board):
        self.board = board

    def is_invalid(self, x, y):
        return (x < 0 or x >= board_size or y < 0 or y >= board_size)

    def set_stone(self, x, y, stone):
        self.board[y][x] = stone

    def get_xy(self, direction):
        list_dx = [-1, 1, -1, 1, 0, 0, 1, -1]
        list_dy = [0, 0, -1, 1, -1, 1, -1, 1]
        return list_dx[direction], list_dy[direction]

    def get_stone_count(self, x, y, stone, direction): # (x,y)는 현재 pos이고, direction은 0,1,2,3호출할 것임.
        origin_x, origin_y = x, y
        cnt = 1 # 함수호출시마다 카운트 1로 set
        for i in range(2): # 반대방향까지 확인(i=0,1)
            dx, dy = self.get_xy(direction * 2 + i) # 0~7까지 지정하기 위한 트릭(0,1 / 2,3 / 4,5 / 6,7)
            x, y = origin_x, origin_y
            while True: # 한쪽방향으로 계속 체크해나감
                x, y = x + dx, y + dy
                if self.is_invalid(x, y) or self.board[y][x] != stone: # 보드크기를 넘어서는 pos인지 혹은 이미 돌이 놓아져있는 순간 break
                    break;
                else:
                    cnt += 1 # 연속적일때까지 계속 카운트 1씩 증가
        return cnt
    
    # 현재 돌을 놓았을 때, 그 순간 5목이 되었는지 체크
    def is_gameover(self, x, y, stone):
        for i in range(4): # 각 i는 양방향을 의미..
            cnt = self.get_stone_count(x, y, stone, i)
            if cnt >= 5:
                return True
        return False


