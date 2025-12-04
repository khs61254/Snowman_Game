import pygame
import sys
import GameSettings
from Player import Player           # Player 파일의 Player 클래스 가져오기
#from Level import Level


# 설정 초기화
pygame.init()

# 화면 세팅
screen = pygame.display.set_mode((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT))
pygame.display.set_caption("Snowman")

# map.png 이미지 로드
map_img = pygame.image.load("resource/images/map.png").convert()
map_img = pygame.transform.scale(map_img, (GameSettings.MAP_WIDTH, GameSettings.MAP_HEIGHT))

# 플레이어 클래스 호출
player = Player(GameSettings.MAP_WIDTH, GameSettings.MAP_HEIGHT)

# 오프셋 설정
offset_x = player.x - (GameSettings.SCREEN_WIDTH // 2)
offset_y = player.y - (GameSettings.SCREEN_HEIGHT // 2)

# 메인 게임 루프
run = True
while run:
    # 이벤트 처리 (입력 감지)
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :       # 창 닫기 버튼을 누르면 종료  
            run = False

    # 화면 채우기, 화면 업데이트
    screen.fill(GameSettings.BLACK)

    # 맵 그리기
    screen.blit(map_img, (0 - offset_x, 0 - offset_y))

    # 플레이어 움직임
    player.player_move()

    # 플레이어 그리기
    player.draw(screen)

    # 화면 업데이트
    pygame.display.flip()

    # 프레임 속도 조절
    clock = pygame.time.Clock()
    clock.tick(GameSettings.FPS)

# 게임 종료
pygame.quit()
sys.exit()