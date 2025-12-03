import pygame
import sys
from Player import Player           # Player 파일의 Player 클래스 가져오기
#from Level import Level


# 설정 초기화
pygame.init()

# 게임 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snowman")

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

# Player 클래스의 player 정의
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)

#컬러
BLACK = (0, 0, 0)

# 메인 게임 루프
run = True
while run:
    # 이벤트 처리 (입력 감지)
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :       # 창 닫기 버튼을 누르면 종료  
            run = False

    # 플레이어 움직임
    player.player_move()

    # 화면 채우기, 화면 업데이트
    screen.fill(BLACK)

    # 플레이어 그리기
    player.draw(screen)

    # 화면 업데이트
    pygame.display.flip()

    # D. 프레임 속도 조절
    clock.tick(FPS)

# 게임 종료
pygame.quit()
sys.exit()