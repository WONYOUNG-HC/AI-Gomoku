import pygame, sys
from pygame.locals import *
from rule import *
import gomoku_ai

# 색상 지정
bg_color = (161,140,127)
black = (0, 0, 0)   
blue = (0, 50, 255)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)

# 창 크기 / 보드 크기 / 돌크기
window_width = 700
window_height = 500
board_width = 500
grid_size = 30

# 상수 정의
fps = 60
fps_clock = pygame.time.Clock()

def main():
    # 아래 4줄은 pygame에서 반드시 선행되어야 하는 작업
    pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Omok game")
    surface.fill(bg_color)

    omok = Omok(surface)
    menu = Menu(surface)

    while True:
        run_game(surface, omok, menu)
        menu.is_continue(omok)

# 게임 실행부
def run_game(surface, omok, menu):
    omok.init_game()
    while True:
        if omok.turn == black_stone: # 사용자가 무조건 공격
            for event in pygame.event.get():
                if event.type == QUIT:
                    menu.terminate()
                elif event.type == MOUSEBUTTONUP and omok.turn==black_stone: # 매프레임마다 마우스 클릭 체크
                    if not omok.check_board1(event.pos): # 보드아닌곳에 클릭시,
                        if menu.check_rect(event.pos, omok): # 그게 메뉴를 클릭했으면
                            omok.init_game() # 메뉴명령 수행..
        elif omok.turn == white_stone: # AI turn
            x, y = omok.get_point(omok.coords[-1])
            y, x = omok.omok2.omok2_ai(y,x) # 사용자의 값을 넘겨주면 AI가 둔다.
            omok.check_board2(y,x)

        if omok.is_gameover:
            return

        pygame.display.update()
        fps_clock.tick(fps)

class Omok(object):
    def __init__(self, surface):
        self.board = [[0 for i in range(board_size)] for j in range(board_size)] # 오목판 만들기.
        self.menu = Menu(surface) # 메뉴 만들기
        self.rule = Rule(self.board) # 만든 보드판으로 Rule 정함.
        self.surface = surface
        self.pixel_coords = []
        self.set_coords()
        self.set_image_font()
        self.is_show = True

    def init_game(self):
        self.turn = black_stone
        self.draw_board()
        self.menu.show_msg(empty)
        self.init_board()
        self.coords = []
        self.id = 1 # 돌을 놓은 횟수..
        self.is_gameover = False
        self.omok2 = gomoku_ai.omok2()
        

    def set_image_font(self):
        black_img = pygame.image.load('image/black.png')
        white_img = pygame.image.load('image/white.png')
        self.board_img = pygame.image.load('image/board.png')
        self.font = pygame.font.Font("freesansbold.ttf", 14)
        self.black_img = pygame.transform.scale(black_img, (grid_size, grid_size))
        self.white_img = pygame.transform.scale(white_img, (grid_size, grid_size))

    def init_board(self):
        for y in range(board_size):
            for x in range(board_size):
                self.board[y][x] = 0

    # 오목판 그리기
    def draw_board(self):
        self.surface.blit(self.board_img, (0, 0))

    # (x,y)위치에 바둑돌 그리기
    def draw_image(self, img_index, x, y):
        img = [self.black_img, self.white_img]
        self.surface.blit(img[img_index], (x, y))


    def draw_stone(self, coord, stone, increase=1):
        x, y = self.get_point(coord)
        self.board[y][x] = stone # 돌 놓기

        # 돌 처음부터 다시 그리기
        for i in range(len(self.coords)):
            x, y = self.coords[i]
            self.draw_image(i % 2, x, y)


        self.id += increase # 한 수 놓을때마다 돌을 놓은 갯수인 id를 1씩 증가
        self.turn = 3 - self.turn # 턴을 바꿔준다.. turn이 1이었으면 2로, turn이 2였으면 1로


    # 위치를 정확히 지정한다. 즉, 마우스기준좌표의 대표값을 설정한다.
    def set_coords(self):
        for y in range(board_size):
            for x in range(board_size):
                self.pixel_coords.append((x * grid_size, y * grid_size)) # (30,0),(60,0),,(0,30),(30,30)

    def get_coord(self, pos):
        for coord in self.pixel_coords: 
            x, y = coord
            rect = pygame.Rect(x, y, grid_size, grid_size) # pixcel_coords의 지정된 위치값과 grid_size 30을 넣음
            if rect.collidepoint(pos): # 점이 사각형 안에 있으면 True
                return coord
        return None

    def get_point(self, coord): # 마우스 좌표를 찐좌표(board[y][x])로 변경
        x, y = coord
        x = (x) // grid_size
        y = (y) // grid_size
        return x, y

    # for user                       
    def check_board1(self, pos): # pos는 마우스 클릭된 좌표
        coord = self.get_coord(pos) # pos가 사각형내에 있다면 그놈(사각형의 대표값 pixel_coords 한개) coord을 가져옴
        if not coord: # 좌표아닌곳에 찍었다면, 그냥 함수 종료
            return False
        x, y = self.get_point(coord) # 창좌표인 coord를 grid_size로 나누어 x,y를 리턴함 ==> (0,1)과 같은 찐board좌표
        
        if self.board[y][x] != empty:
            print("occupied")
            return True

        self.coords.append(coord) # 창좌표 coord를 창좌표리스트인 coords에 append시킴.
        self.draw_stone(coord, self.turn) # 돌 그리기
        self.omok2.omok2_user(y,x)
        if self.check_gameover(coord, 3 - self.turn):
            self.is_gameover = True

        return True

    # for AI
    def check_board2(self, y, x): # pos는 마우스 클릭된 좌표
        pos = (x*30, y*30)
        coord = self.get_coord(pos) # pos가 사각형내에 있다면 그놈(사각형의 대표값 pixel_coords 한개) coord을 가져옴
        if not coord: # 좌표아닌곳에 찍었다면, 그냥 함수 종료
            return False
        x, y = self.get_point(coord) # 창좌표인 coord를 grid_size로 나누어 x,y를 리턴함 ==> (0,1)과 같은 찐board좌표
        if self.board[y][x] != empty:
            print("occupied")
            return True

        self.coords.append(coord) # 창좌표 coord를 창좌표리스트인 coords에 append시킴.
        self.draw_stone(coord, self.turn) # 돌 그리기
        if self.check_gameover(coord, 3 - self.turn):
            self.is_gameover = True

        return True

    # 돌을 놓았을 때 게임이 끝났는지를 체크
    def check_gameover(self, coord, stone):
        x, y = self.get_point(coord)
        if self.id > board_size * board_size:
            self.show_winner_msg(stone)
            return True
        elif self.rule.is_gameover(x, y, stone):
            self.show_winner_msg(stone)
            return True
        return False

    # 승리했을때 message출력
    def show_winner_msg(self, stone):
        for i in range(3):
            self.menu.show_msg(stone)
            pygame.display.update()
            pygame.time.delay(200)
            self.menu.show_msg(empty)
            pygame.display.update()
            pygame.time.delay(200)
        self.menu.show_msg(stone)

        
class Menu(object):
    def __init__(self, surface):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.surface = surface
        self.draw_menu()

    # 좌측 구석에 텍스트 적기
    def draw_menu(self):
        top, left = window_height - 30, window_width - 200
        self.new_rect = self.make_text(self.font, 'New Game', blue, None, top - 30, left)
        self.quit_rect = self.make_text(self.font, 'Quit Game', blue, None, top, left)

    # 이겼을 때 message 내용 및 위치설정하여, 화면에 뿌리기 
    def show_msg(self, msg_id): 
        msg = {
            empty : '                                    ',
            black_stone: 'Black win!!!',
            white_stone: 'White win!!!',
            tie: 'Tie',
        }
        center_x = window_width - (window_width - board_width) // 2
        self.make_text(self.font, msg[msg_id], black, bg_color, 30, center_x, 1)

    # 메뉴를 위해 text 만들어서 뿌리기
    def make_text(self, font, text, color, bgcolor, top, left, position = 0):
        surf = font.render(text, False, color, bgcolor)
        rect = surf.get_rect()
        if position:
            rect.center = (left, top)
        else:    
            rect.topleft = (left, top)
        self.surface.blit(surf, rect)
        return rect

    # 사각형안에 있는지 체크
    def check_rect(self, pos, omok):
        if self.new_rect.collidepoint(pos):
            return True
        elif self.quit_rect.collidepoint(pos):
            self.terminate()
        return False
    
    def terminate(self):
        pygame.quit()
        sys.exit()

    def is_continue(self, omok):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == MOUSEBUTTONUP:
                    if (self.check_rect(event.pos, omok)):
                        return
            pygame.display.update()
            fps_clock.tick(fps)    

if __name__ == '__main__':
    main()
