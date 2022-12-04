import heapq
# p : positive, n : negative or new
N = 15  # 판 크기
BLACK, WHITE = 1, 2  # 흑돌과 백돌
INF = 100000  # 가중치 계산을 위한 최대값

# 보드판 탐색을 위한 리스트. 코드내 첫번째 인덱스(방향) 변수는 k로 사용
direction = [[[-1, 0], [1, 0]],  # 북 남
             [[0, -1], [0, 1]],  # 서 동
             [[-1, -1], [1, 1]],  # 북서 남동
             [[-1, 1], [1, -1]]]  # 북동 남서


# 좌표가 오목판 범위 내에 있는지 검사
def check_range(a, b):
    if 0 <= a < N and 0 <= b < N:
        return True
    return False


# 오목판을 위한 클래스
class Board:
    # 오목판 생성
    def __init__(self):
        self.board = [[0] * N for _ in range(N)]

    # 인자로 받은 보드판을 해당 클래스의 가중치판으로 복사
    def copy_board(self, new_board):
        for y in range(N):
            for x in range(N):
                self.board[y][x] = new_board[y][x]

    # 승리 판정 함수
    def is_win(self, color):
        for y in range(N):
            for x in range(N):
                # 자신의 돌이 승리 하였을 경우 INF 리턴
                if self.board[y][x] == color:
                    for k in range(4):
                        cnt = 1
                        py, px = y + direction[k][0][0], x + direction[k][0][1]
                        while check_range(py, px) and self.board[py][px] == color:
                            cnt += 1
                            if cnt > 5:
                                break
                            py += direction[k][0][0]
                            px += direction[k][0][1]

                        ny, nx = y + direction[k][1][0], x + direction[k][1][1]
                        while check_range(ny, nx) and self.board[ny][nx] == color:
                            cnt += 1
                            if cnt > 5:
                                break
                            ny += direction[k][1][0]
                            nx += direction[k][1][1]

                        # 5목 일때만 승리 판정 (장목은 인정하지 않는다)
                        if cnt == 5:
                            return True

        # 승리가 결정되지 않았을 때는 None을 리턴
        return None

    # 오목판에 빈공간이 없는지 판별하는 함수
    def is_full(self):
        for y in range(N):
            for x in range(N):
                if self.board[y][x] == 0:
                    return False
        return True

    # 콘솔에서 오목판 출력
    def draw(self):
        print(end='   ')
        for i in range(N):
            print(i, end=' ')
        print()
        for y in range(N):
            print(y, end=' ')
            if y < 10:
                print(end=' ')
            for x in range(N):
                print(self.board[y][x], end=' ')
            print()
        print()


# 가중치판을 위한 클래스
class Weight:
    # 가중치판 및 방문판 생성
    def __init__(self):
        # 0 -> BLACK, 1 -> WHITE
        # class 내에서 첫번째 인덱스는 turn-1로 사용
        self.board = [[[0] * N for _ in range(N)] for _ in range(2)]  # 가중치판
        self.visited = [[[True] * N for _ in range(N)] for _ in range(2)]  # 탐색을 위한 방문판

    # 인자로 받은 가중치판을 해당 클래스의 가중치판으로 복사
    def copy_board(self, new_board):
        for i in range(2):
            for y in range(N):
                for x in range(N):
                    self.board[i][y][x] = new_board[i][y][x]

    # 콘솔에서 가중치판 출력
    def draw(self):
        print('weight for 1(BLACK)')
        for u in range(N):
            for v in range(N):
                print(self.board[0][u][v], end='  ')
            print()
        print()
        print('weight for 2(WHITE)')
        for u in range(N):
            for v in range(N):
                print(self.board[1][u][v], end='  ')
            print()
        print()

    # 가중치판에 상대편 수가 있는지 검사
    def check(self, a, b, turn, after):
        if self.board[turn-1][a][b] == -after:
            return False
        return True

    # 가중치판 탐색 후 Figure 클래스 리턴, 오목이 불가능 한 경우 None 리턴
    def search(self, turn, y, x, k):
        self.visited[turn-1][y][x] = True  # 방문판의 해당 좌표에 방문 처리
        figure = Figure(y, x, k)  # 해당 위치에서 연결되는 수를 저장하기 윈한 Figure 클래스 생성
        cnt_line = 1  # 현재 연결된(라인) 수를 count
        py_dir, px_dir = direction[k][0]
        ny_dir, nx_dir = direction[k][1]
        py, px = y + py_dir, x + px_dir  # positive 방향
        ny, nx = y + ny_dir, x + nx_dir  # neagtive 방향

        cnt_p_blank = 0  # positive 방향으로 공백의 수를 count
        # positive 방향의 위치가 오목판 범위내에 있고, 공백의 수가 5 미만(이후로는 5목 생성이 불가)일 경우.
        while check_range(py, px) and cnt_p_blank < 5:
            if turn == BLACK and self.board[turn-1][py][px] == -BLACK:
                figure.line.append((py, px))
                self.visited[turn-1][py][px] = True  # 해당 위치가 수에 포함되었으면 방문 처리
                figure.p_blank.clear()  # 연결된 수의 바깥쪽 공백만 저장 하기 때문에 자신의 돌을 발견하면 초기화 진행
                cnt_p_blank = 0
                cnt_line += 1
            elif turn == WHITE and self.board[turn-1][py][px] == -WHITE:
                figure.line.append((py, px))
                self.visited[turn-1][py][px] = True
                figure.p_blank.clear()
                cnt_p_blank = 0
                cnt_line += 1
            elif self.board[turn-1][py][px] >= 0:
                figure.p_blank.append((py, px))
                cnt_p_blank += 1
            else:
                # 적의 돌을 발견한 경우
                break
            py += direction[k][0][0]
            px += direction[k][0][1]

        cnt_n_blank = 0  # negative 방향으로 공백의 수를 count
        while check_range(ny, nx) and cnt_n_blank < 5:
            if turn == BLACK and self.board[turn - 1][ny][nx] == -BLACK:
                figure.line.append((ny, nx))
                self.visited[turn-1][ny][nx] = True
                figure.n_blank.clear()
                cnt_n_blank = 0
                cnt_line += 1
            elif turn == WHITE and self.board[turn - 1][ny][nx] == -WHITE:
                figure.line.append((ny, nx))
                self.visited[turn-1][ny][nx] = True
                figure.n_blank.clear()
                cnt_n_blank = 0
                cnt_line += 1
            elif self.board[turn-1][ny][nx] >= 0:
                figure.n_blank.append((ny, nx))
                cnt_n_blank += 1
            else:
                # 적의 돌을 발견한 경우
                break
            ny += direction[k][1][0]
            nx += direction[k][1][1]

        # 내부 공백을 계산
        ny, nx = min(figure.line)  # 수(라인)의 시작점
        end_y, end_x = max(figure.line)  # 수(라인)의 끝점
        cnt_in_blank = 0  # 내부 공백의 수를 count
        # 해당 위치가 end 위치에 접근하지 않을때까지 내부 공백을 생성
        while ny != end_y or nx != end_x:
            ny, nx = ny + ny_dir, nx + nx_dir
            if (ny, nx) not in figure.line:
                figure.in_blank.append((ny, nx))
                cnt_in_blank += 1

        # 수가 적수로 막혀 5목이 불가하거나, 6목 이상의 장목이 되는경우 None을 리턴
        if cnt_line + cnt_p_blank + cnt_n_blank + cnt_in_blank < 5 or cnt_line > 5:
            return None
        else:
            return figure

    # 1목 가중치 계산
    def weight_line1(self, figure, turn):
        # 가중치 설정 순서 : 유일한 오목의 위치 -> 돌의 인접한 위치 -> 나머지 오목이 가능한 위치
        # 양쪽이 막혀 5목이 가능한 유일한 수일때 가중치 설정후 함수 종료
        # 양방향 blank와 돌의 합이 5일 경우
        if len(figure.p_blank) + 1 + len(figure.n_blank) == 5:
            for y, x in figure.p_blank:
                self.board[turn-1][y][x] += 5
            for y, x in figure.n_blank:
                self.board[turn-1][y][x] += 5
            return

        # 돌의 근접한 위치에 대하여 가중치 설정
        # 근접한 위치를 얻는 과정에서 해당 방향 blank가 비어있는 경우를 대비해 예외처리 진행
        try:
            y, x = figure.p_blank[0]
            # 양 방향으로 장애물과 인접하지 않은 경우
            if len(figure.p_blank) > 1 and figure.n_blank:
                self.board[turn-1][y][x] += 13
            else:
                self.board[turn-1][y][x] += 7
        except IndexError:
            pass

        try:
            y, x = figure.n_blank[0]
            if len(figure.n_blank) > 1 and figure.p_blank:
                self.board[turn-1][y][x] += 13
            else:
                self.board[turn-1][y][x] += 7
        except IndexError:
            pass

        # 돌이 5목이 가능한 위치에 장애물이 존재 할 경우 가중치 설정
        # blank의 길이가 5 미만일 경우 해당 방향으로 장애물이 존재
        if 1 < len(figure.p_blank) < 5:
            y, x = figure.p_blank[-1]
            self.board[turn-1][y][x] += 5
        # 해당방향으로 장애물이 존재하는 경우 위에서 설정한 위치 이전까지 가중치 설정
        # 해당방향으로 장애물이 없을경우 자신의 돌을 포함해 5목이 가능한 위치에 가중치 설정
        for y, x in figure.p_blank[1:-1]:
            self.board[turn-1][y][x] += 10

        if 1 < len(figure.n_blank) < 5:
            y, x = figure.n_blank[-1]
            self.board[turn-1][y][x] += 5
        for y, x in figure.n_blank[1:-1]:
            self.board[turn-1][y][x] += 10

    # 2목 가중치 계산
    def weight_line2(self, figure, turn):
        # 양쪽이 막혀 5목이 가능한 유일한 수일때 가중치 설정후 함수 종료
        if len(figure.p_blank) + 2 + len(figure.in_blank) + len(figure.n_blank) == 5:
            for y, x in figure.p_blank:
                self.board[turn - 1][y][x] += 30
            for y, x in figure.n_blank:
                self.board[turn - 1][y][x] += 30
            for y, x in figure.in_blank:
                self.board[turn - 1][y][x] += 30
            return

        # 돌이 연속적을 연결되어있는 경우
        # 가중치 설정 순서 : 돌의 인접한 위치 -> 나머지 오목이 가능한 위치
        if not figure.in_blank:
            # 원할한 리스트 인덱싱을 위해 blank리스트 최적화
            p_blank, n_blank = figure.p_blank[:4], figure.n_blank[:4]

            # 돌의 인접한 위치에 가중치 설정
            try:
                y, x = p_blank[0]
                if len(p_blank) > 1 and n_blank:
                    self.board[turn-1][y][x] += 55
                else:
                    self.board[turn-1][y][x] += 35
            except IndexError:
                pass

            try:
                y, x = n_blank[0]
                if len(n_blank) > 1 and p_blank:
                    self.board[turn-1][y][x] += 55
                else:
                    self.board[turn-1][y][x] += 35
            except IndexError:
                pass

            # 해당 방향으로 장애물이 존재 할 경우
            if 1 < len(p_blank) < 4:
                y, x = p_blank[-1]
                self.board[turn-1][y][x] += 30
            # 나머지 부분에 대하여 가중치 설정
            for y, x in p_blank[1:-1]:
                self.board[turn-1][y][x] += 50

            if 1 < len(n_blank) < 4:
                y, x = n_blank[-1]
                self.board[turn-1][y][x] += 30
            for y, x in n_blank[1:-1]:
                self.board[turn-1][y][x] += 50

        # 돌의 중앙이 한곳이 비어있는 경우
        # 가중치 설정 순서 : 돌의 인접한 위치와 내부 공백 -> 나머지 오목이 가능한 위치
        elif len(figure.in_blank) == 1:
            # 원할한 리스트 인덱싱을 위해 blank리스트 최적화
            p_blank, n_blank = figure.p_blank[:3], figure.n_blank[:3]

            # 돌의 인접한 위치와 내부 공백에 대하여 가중치 설정
            try:
                y, x = p_blank[0]
                if len(p_blank) > 1:
                    self.board[turn-1][y][x] += 55
                else:
                    self.board[turn-1][y][x] += 35
            # 한 방향이라도 인접한 위치에 장애물이 위치한 경우 내부 공백위치에 대하여 가중치 설정
            except IndexError:
                y, x = figure.in_blank[0]
                self.board[turn-1][y][x] = 35

            try:
                y, x = n_blank[0]
                if len(n_blank) > 1:
                    self.board[turn-1][y][x] += 55
                else:
                    self.board[turn-1][y][x] += 35
            except IndexError:
                y, x = figure.in_blank[0]
                self.board[turn-1][y][x] = 35

            # 돌 양방향으로 인접한 위치에 장애물이 없는 경우에 대하여 가중치 설정
            if p_blank and n_blank:
                y, x = figure.in_blank[0]
                self.board[turn-1][y][x] += 55

            # 해당 방향으로 장애물이 존재 할 경우
            if 1 < len(p_blank) < 3:
                y, x = p_blank[-1]
                self.board[turn-1][y][x] += 30
            # 나머지 부분에 대하여 가중치 설정
            for y, x in p_blank[1:-1]:
                self.board[turn-1][y][x] += 50

            if 1 < len(n_blank) < 3:
                y, x = n_blank[-1]
                self.board[turn-1][y][x] += 30
            for y, x in n_blank[1:-1]:
                self.board[turn-1][y][x] += 50

        # 돌의 중앙 두곳이 비어있는 경우
        # 가중치 설정 순서 : 돌의 인접한 위치와 내부 공백 -> 나머지 오목이 가능한 위치
        elif len(figure.in_blank) == 2:
            # 원할한 리스트 인덱싱을 위해 blank리스트 최적화
            p_blank, n_blank = figure.p_blank[:2], figure.n_blank[:2]

            # 돌의 인접한 위치와 내부 공백에 대하여 가중치 설정
            try:
                y, x = p_blank[0]
                if len(p_blank) > 1:
                    self.board[turn-1][y][x] += 55
                else:
                    self.board[turn-1][y][x] += 35
            # 해당 방향으로 장애물이 존재 할 경우 내부 공백에 대하여 가중치 설정
            # in_blank는 오름차순으로 정렬되어 있으므로 0번 인덱스는 positive, 1번 인덱스는 negative
            except IndexError:
                y, x = figure.in_blank[0]
                self.board[turn-1][y][x] += 35
                y, x = figure.in_blank[1]
                self.board[turn-1][y][x] += 55

            try:
                y, x = n_blank[0]
                if len(n_blank) > 1:
                    self.board[turn-1][y][x] += 55
                else:
                    self.board[turn-1][y][x] += 35
            except IndexError:
                y, x = figure.in_blank[1]
                self.board[turn-1][y][x] += 35
                y, x = figure.in_blank[0]
                self.board[turn-1][y][x] += 55

            # 돌 양방향으로 인접한 위치에 장애물이 없는 경우에 대하여 가중치 설정
            if p_blank and n_blank:
                for y, x in figure.in_blank:
                    self.board[turn-1][y][x] += 55

        # 돌의 중앙 세곳이 비어있는 경우
        # 가중치 설정 순서 : 돌과 인접한 내부 공백 -> 나머지 내부 공백
        elif len(figure.in_blank) == 3:
            # 돌과 인접한 위치에 있는 내부 공백에 대하여 가중치 설정
            y, x = figure.in_blank[0]
            if figure.p_blank:
                self.board[turn-1][y][x] += 55
            else:
                self.board[turn-1][y][x] += 35

            y, x = figure.in_blank[2]
            if figure.n_blank:
                self.board[turn-1][y][x] += 55
            else:
                self.board[turn-1][y][x] += 35

            # 나머지 내부 공백 위치에 대하여 가중치 설정
            y, x = figure.in_blank[1]
            self.board[turn-1][y][x] += 55

    # 3목 가중치 계산
    def weight_line3(self, figure, turn):
        # 양쪽이 막혀 5목이 가능한 유일한 수일때 가중치 설정후 함수 종료
        if len(figure.p_blank) + 3 + len(figure.in_blank) + len(figure.n_blank) == 5:
            for y, x in figure.p_blank:
                self.board[turn-1][y][x] += 57
            for y, x in figure.n_blank:
                self.board[turn-1][y][x] += 57
            for y, x in figure.in_blank:
                self.board[turn-1][y][x] += 57
            return

        # 돌이 연속적을 연결되어있는 경우
        # 가중치 설정 순서 : 돌과 인접한 위치에 장애물이 있을때 -> 돌의 근접한 위치 -> 나머지 오목이 가능한 위치
        if not figure.in_blank:
            # 원할한 리스트 인덱싱을 위해 blank리스트 최적화
            p_blank, n_blank = figure.p_blank[:3], figure.n_blank[:3]

            # 돌과 인접한 위치에 장애물이 존재 할 경우 반대 방향에 대하여 가중치 설정후 함수 종료
            if not n_blank:
                for y, x in p_blank[:2]:
                    self.board[turn-1][y][x] += 57
                return

            if not p_blank:
                for y, x in n_blank[:2]:
                    self.board[turn-1][y][x] += 57
                return

            # 돌과 인접한 위치에 대하여 가중치 설정
            y, x = p_blank[0]
            if len(p_blank) > 1:
                self.board[turn-1][y][x] += 600
            else:
                self.board[turn-1][y][x] += 57

            y, x = n_blank[0]
            if len(n_blank) > 1:
                self.board[turn-1][y][x] += 600
            else:
                self.board[turn-1][y][x] += 57

            # 해당 방향으로 장애물이 존재 할 경우
            if 1 < len(p_blank) < 3:
                y, x = p_blank[-1]
                self.board[turn-1][y][x] += 57
            # 나머지 부분에 대하여 가중치 설정
            for y, x in p_blank[1:-1]:
                self.board[turn-1][y][x] += 500

            if 1 < len(n_blank) < 3:
                y, x = n_blank[-1]
                self.board[turn-1][y][x] += 57
            for y, x in n_blank[1:-1]:
                self.board[turn-1][y][x] += 500

        # 돌의 중앙이 한곳이 비어있는 경우
        # 가중치 설정 순서 : 돌과 인접한 위치에 장애물이 있을때 -> 나머지 오목이 가능한 위치
        elif len(figure.in_blank) == 1:
            # 원할한 리스트 인덱싱을 위해 blank리스트 최적화
            p_blank, n_blank = figure.p_blank[:2], figure.n_blank[:2]

            # 돌과 인접한 위치에 장애물이 존재 할 경우 반대 방향과 내부 공백에 대하여 가중치 설정후 함수 종료
            if not n_blank:
                y, x = figure.in_blank[0]
                self.board[turn-1][y][x] += 57
                y, x = figure.p_blank[0]
                self.board[turn-1][y][x] += 57
                return

            if not p_blank:
                y, x = figure.in_blank[0]
                self.board[turn-1][y][x] += 57
                y, x = figure.n_blank[0]
                self.board[turn-1][y][x] += 57
                return

            # 내부 공백에 대하여 가중치 설정
            y, x = figure.in_blank[0]
            self.board[turn-1][y][x] += 600

            # 돌과 인접한 위치에 대하여 가중치 설정
            y, x = p_blank[0]
            if len(p_blank) == 2:
                self.board[turn-1][y][x] += 600
            else:
                self.board[turn-1][y][x] += 57

            y, x = n_blank[0]
            if len(n_blank) == 2:
                self.board[turn-1][y][x] += 600
            else:
                self.board[turn-1][y][x] += 57

        # 돌의 중앙 두곳이 비어있는 경우
        # 가중치 설정 순서 : 돌과 인접한 위치에 장애물이 있을때 -> 돌과 인접한 위치에 장애물이 없을때
        elif len(figure.in_blank) == 2:
            if not figure.n_blank:
                for y, x in figure.in_blank:
                    self.board[turn-1][y][x] += 57
                return

            if not figure.p_blank:
                for y, x in figure.in_blank:
                    self.board[turn-1][y][x] += 57
                return

            for y, x in figure.in_blank:
                self.board[turn-1][y][x] += 600

    # 4목 가중치 계산
    def weight_line4(self, figure, turn):
        # 5목이 가능한 모든 위치에 가중치 설정
        # 돌이 연속적으로 연결되어 있는 경우
        if not figure.in_blank:
            # 돌과 인접한 위치에 가중치 설정
            try:
                y, x = figure.p_blank[0]
                self.board[turn-1][y][x] += 5000
            except IndexError:
                pass

            try:
                y, x = figure.n_blank[0]
                self.board[turn-1][y][x] += 5000
            except IndexError:
                pass

        # 내부 공백이 있는 경우
        else:
            # 내부 공백에 가중치 설정
            y, x = figure.in_blank[0]
            self.board[turn-1][y][x] += 5000

    # 가중치 계산
    def calc_weight(self, turn):
        # 가중치판, 방문판 초기화
        for u in range(N):
            for v in range(N):
                # 오목판에 돌이 착수되어 있을때 해당 위치의 visited판에 False 설정
                if turn == BLACK and self.board[turn-1][u][v] == -BLACK:
                    self.visited[turn-1][u][v] = False
                elif turn == WHITE and self.board[turn-1][u][v] == -WHITE:
                    self.visited[turn-1][u][v] = False
                elif self.board[turn-1][u][v] > 0:
                    self.board[turn-1][u][v] = 0

        for u in range(N):
            for v in range(N):
                # visited판에 False를 만났을때 -> 해당 위치에 돌이 있는 경우
                if not self.visited[turn-1][u][v]:
                    y, x = u, v

                    for k in range(4):
                        figure = self.search(turn, y, x, k)
                        # figure class가 생성 되어 5목이 가능한 경우의 수
                        if figure:
                            if len(figure.line) == 1:  # 1목
                                self.weight_line1(figure, turn)
                            elif len(figure.line) == 2:  # 2목
                                self.weight_line2(figure, turn)
                            elif len(figure.line) == 3:  # 3목
                                self.weight_line3(figure, turn)
                            elif len(figure.line) == 4:  # 4목
                                self.weight_line4(figure, turn)


# 해당 좌표의 k 방향으로 연결되어 있는 수들을 위한 class
class Figure:
    def __init__(self, y, x, k):
        self.line = [(y, x)]  # 연결되는 수를 저장
        self.p_blank = []  # 수의 바깥쪽에 위치한 positve 공백 저장
        self.n_blank = []  # 수의 바깥쪼겡 위차한 negative 공백 저장
        self.in_blank = []  # 수의 내부 공백 저장
        self.direction = k  # direction 리스트를 사용하기 위한 방향 저장


# ai의 착수를 계산하는 클래스
# board 클래스의 함수를 사용하기 위해 상속
class Ai (Board):
    # 가중치판에서 가장 큰 가중치를 찾는 함수
    @staticmethod
    def find_max(weight_board, turn):
        cost = 0
        position = (-1, -1)
        for y in range(N):
            for x in range(N):
                if weight_board[turn-1][y][x] > cost:
                    cost = weight_board[turn-1][y][x]
                    position = (y, x)
        return cost, position

    # 가중치판에서 가중치의 값이 설정되어 있는 위치를 리턴하는 함수
    @staticmethod
    def find_possible(weight_board):
        heap = []  # 가중치값이 양수인 위치들을 가중치값과 저장
        high = []  # 가중치값이 100이상인 위치들을 가중치값과 저장
        for y in range(N):
            for x in range(N):
                cost = max(weight_board[BLACK-1][y][x], weight_board[WHITE-1][y][x])
                # 100 이상의 가중치가 존재하는 경우 100 이상의 가중치값이 있는 위치들만 리턴하고, 그 이외의 위치에서는 무시
                if cost >= 100:
                    high.append((cost, y, x))
                # 100 이상의 가중치가 존재하지 않을때 heap에 위치와 가중치값을 저장
                # 최대힙 사용을 위해 cost값은 음수를 붙여 최소힙에서 최대힙 사용
                elif not high and cost > 0:
                    heapq.heappush(heap, (-cost, y, x))

        # 100 이상의 가중치값이 있으면 high리스트를 리턴
        if high:
            return high

        # 100 이상의 가중치가 없는 경우 heap에 있던 위치들중 가중치값 기준으로 상위 15개의 위치들에 대하서 리턴
        possible = []
        for _ in range(15):
            try:
                possible.append(heapq.heappop(heap))
            except IndexError:
                break
        # 상위 15개의 가중치값이 중복되 있는 경우 해당 가중치값까지 리턴하도록 해줌
        if heap and possible[0][0] == heap[0][0]:
            while possible[0][0] != heap[0][0]:
                possible.append(heapq.heappop(heap))
        return possible

    # minimax 알고리즘
    def minimax(self, board_board, weight_board, depth, turn, after, alpha, beta):
        self.copy_board(board_board)  # 보드판 복사
        win = self.is_win(after)  # turn의 이전 차례인 after의 착수가 승리하였는지 판정

        # 재귀함수의 탈출 조건
        if depth == 0 or win is not None or self.is_full():
            turn_cost, _ = self.find_max(weight_board, turn)
            after_cost, _ = self.find_max(weight_board, after)
            if win is None:
                if turn == WHITE:
                    return (turn_cost, after_cost), None
                else:
                    return (after_cost, turn_cost), None
            else:
                if turn == WHITE:
                    return (turn_cost, INF), None
                else:
                    return (INF, after_cost), None

        # 위치, 가중치값, 보드판, 가중치판 초기화
        position = (-1, -1)
        value_tuple = (0, 0)
        new_board, new_weight = Board(), Weight()
        new_board.copy_board(board_board)
        new_weight.copy_board(weight_board)
        # WHITE는 AI의 turn이므로 max값을 선택
        if turn == WHITE:
            value = -INF
            # find_possible을 통해 착수 가능한 후보군 위치에 대하여 착수후 가중치 계산
            for _, y, x in self.find_possible(new_weight.board):
                new_board.board[y][x] = turn
                new_weight.board[turn-1][y][x] = -turn
                new_weight.board[after-1][y][x] = -turn
                new_weight.calc_weight(turn)
                new_weight.calc_weight(after)

                # minimax 알고리즘을 통하여 이전 노드들의 가중치값 추출
                cost_tuple, _ = self.minimax(new_board.board, new_weight.board, depth-1, after, turn, alpha, beta)
                cost = cost_tuple[0] - cost_tuple[1]
                if cost > value:
                    value = cost
                    value_tuple = (cost_tuple[0], cost_tuple[1])
                    position = (y, x)
                    alpha = max(alpha, value)
                # 알파베타 가지치기
                if value >= beta:
                    return value_tuple, position

                # 다음 반복문에서 new클래스를 다시 사용하기 위해 해당 위치 초기화
                new_board.board[y][x] = 0
                new_weight.board[turn-1][y][x] = 0
                new_weight.board[after-1][y][x] = 0
        # PLAYER의 turn이므로 min값을 선택
        else:
            value = INF
            for _, y, x in self.find_possible(new_weight.board):
                new_board.board[y][x] = turn
                new_weight.board[turn-1][y][x] = -turn
                new_weight.board[after-1][y][x] = -turn
                new_weight.calc_weight(turn)
                new_weight.calc_weight(after)

                cost_tuple, _ = self.minimax(new_board.board, new_weight.board, depth-1, after, turn, alpha, beta)
                cost = cost_tuple[0] - cost_tuple[1]
                if cost < value:
                    value = cost
                    value_tuple = (cost_tuple[0], cost_tuple[1])
                    position = (y, x)
                    beta = min(beta, value)
                # 알파베타 가지치기
                if value <= alpha:
                    return value_tuple, position

                new_board.board[y][x] = 0
                new_weight.board[turn-1][y][x] = 0
                new_weight.board[after-1][y][x] = 0

        return value_tuple, position


class omok2:
    def __init__(self):
        # 게임에 쓰일 오목판, 가중치판, ai 생성
        self.board = Board()
        self.weight = Weight()
        self.ai = Ai()

    def omok2_user(self, y, x):
        turn = BLACK
        after = WHITE
        self.board.board[y][x] = turn

        self.weight.board[turn-1][y][x] = -turn
        self.weight.board[after-1][y][x] = -turn

        self.weight.calc_weight(turn)
        self.weight.calc_weight(after)

    def omok2_ai(self, y, x):
        position = (-1,-1)
        turn = WHITE
        after = BLACK

        if turn==WHITE:
            _, position = self.ai.minimax(self.board.board, self.weight.board, 4, turn, after, -INF, INF)
        y,x = position
        self.board.board[y][x] = turn

        self.weight.board[turn-1][y][x] = -turn
        self.weight.board[after-1][y][x] = -turn

        self.weight.calc_weight(turn)
        self.weight.calc_weight(after)

        return y,x






