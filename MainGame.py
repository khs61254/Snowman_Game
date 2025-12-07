import pygame
import sys
import random
import math
import GameSettings
from Player import Player           # Player 파일의 Player 클래스 가져오기
from Monster import Monster

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

# 몬스터 리스트
monsters_list = []

# 몬스터 스폰 타이머
monster_spawn_timer = 0
monster_spawn_delay = 5000

# 플레이어로부터 일정 거리 밖에서의 랜덤 좌표 계산 함수
def get_spawn_position(player, map_width, map_height):
    safe_radius = 700   # 안전 거리

    while True:
        # 몬스터 랜덤 스폰 위치(+ 맵 밖에 스폰 방지)
        x = random.randint(0, map_width - 100)
        y = random.randint(0, map_height - 100)

        # 플레이어와 거리 계산
        dist_x = x - player.x
        dist_y = y - player.y
        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

        # 안전 거리보다 멀다면 좌표값 리턴
        if distance > safe_radius:
            return x, y

# 메인 게임 루프
run = True
while run:
    # 이벤트 처리 (입력 감지)
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :       # 창 닫기 버튼을 누르면 종료  
            run = False

    # 현재 시간 저장
    current_time = pygame.time.get_ticks()

    # 플레이어 움직임 함수 호출
    player.player_move()

    # 플레이어 상태(무적 시간) 함수 호출
    player.update_status()

    # 플레이어 슈팅 함수 호출
    player.player_shooting(bullets_list)

    # 플레이어 시점 고정(중앙 고정)
    center_x = player.x + (player.size // 2)
    center_y = player.y + (player.size // 2)
    offset_x = center_x - (GameSettings.SCREEN_WIDTH // 2)
    offset_y = center_y - (GameSettings.SCREEN_HEIGHT // 2)

    # 몬스터 스폰 로직
    if current_time - monster_spawn_timer > monster_spawn_delay:    # 몬스터 스폰 딜레이가 끝났다면
        spawn_x, spawn_y = get_spawn_position(player, GameSettings.MAP_WIDTH, GameSettings.MAP_HEIGHT)
        monsters_list.append(Monster(spawn_x, spawn_y)) #스폰 포지션 값을 받아와서, 몬스터 리스트에 추가
        monster_spawn_timer = current_time  #그 후 스폰타이머를 현재시간으로 초기화

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

    # 몬스터 업데이트, 그리기, 몬스터/플레이어 충돌
    for monster in monsters_list[:]:
        monster.monster_chase(player)
        monster.monster_draw(screen, offset_x, offset_y)

        # 몬스터의 히트박스가 플레이어와 닿았다면 데미지
        if player.rect.colliderect(monster.rect):   # 사각형(히트 박스)의 충돌 감지 함수
            player.take_damage(monster.damage)

        #몬스터, 플레이어 충돌과 몬스터, 총알 충돌을 같이 하기 위해 이중 for문 사용 (AI도움)
        for bullet in bullets_list[:]:
            # bullet 히트박스가 몬스터와 닿았다면 몬스터에게 데미지, 닿은 총알은 삭제
            if monster.rect.colliderect(bullet.rect):
                monster.monster_takeDamage(bullet.damage)
                bullets_list.remove(bullet)

                # 몬스터의 체력이 0이 되면 몬스터 리스트에서 삭제 후 빠져나감(아니면 몬스터 유지)
                if monster.hp <= 0 :
                    monsters_list.remove(monster)   
                    break
        
    if player.hp <= 0 :     # 플레이어 체력이 0이 되면 게임 오버
        run = False



    # 플레이어 그리기
    player.player_draw(screen, offset_x, offset_y)

    # 화면 업데이트
    pygame.display.flip()

    # FPS 설정
    clock.tick(GameSettings.FPS)

# 게임 종료
pygame.quit()
sys.exit()
