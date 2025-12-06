import pygame
import sys
import GameSettings
from Player import Player           # Player 파일의 Player 클래스 가져오기


# 설정 초기화
pygame.init()

# 화면 세팅
screen = pygame.display.set_mode((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT))
pygame.display.set_caption("Snowman")

# map.png 이미지 로드
map_img = pygame.image.load("resource/images/map.png").convert()
map_img = pygame.transform.scale(map_img, (GameSettings.MAP_WIDTH, GameSettings.MAP_HEIGHT))

# 플레이어 객체 생성
player = Player(GameSettings.MAP_WIDTH, GameSettings.MAP_HEIGHT)

# 오프셋(시작위치) 초기화
offset_x = 0
offset_y = 0

# 클락 함수 호출(움직이는것처럼 보이기 위해)
clock = pygame.time.Clock()

# 총알 리스트 생성
bullets_list = []

# 메인 게임 루프
run = True
while run:
    # 이벤트 처리 (입력 감지)
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :       # 창 닫기 버튼을 누르면 종료  
            run = False

    # 플레이어 움직임
    player.player_move()

    player.player_shooting(bullets_list)

    # 플레이어 시점 고정(중앙 고정)
    center_x = player.x + (player.size // 2)
    center_y = player.y + (player.size // 2)
    offset_x = center_x - (GameSettings.SCREEN_WIDTH // 2)
    offset_y = center_y - (GameSettings.SCREEN_HEIGHT // 2)

    # 맵 그리기()
    screen.fill(GameSettings.BLACK)
    screen.blit(map_img, (0 - offset_x, 0 - offset_y))

    # 총알 업데이트, 그리기
    for bullet in bullets_list[:]:
        bullet.bullet_update()

        if bullet.duration <= 0:
            bullets_list.remove(bullet)
        else:
            bullet.bullet_draw(screen, offset_x, offset_y)

    # 플레이어 그리기
    player.player_draw(screen, offset_x, offset_y)

    # 화면 업데이트
    pygame.display.flip()

    # FPS 설정
    clock.tick(GameSettings.FPS)

# 게임 종료
pygame.quit()
sys.exit()
