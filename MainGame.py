import pygame
import sys
import random
import math
import GameSettings
from Player import Player           # Player 파일의 Player 클래스 가져오기
from Monster import Monster
from Level import Level

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

# 레벨 객체 생성
level = Level(player)

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

# 폰트
game_font = pygame.font.SysFont("consolas", 60, True)
sub_font = pygame.font.SysFont("malgungothic", 30)
timer_font = pygame.font.SysFont("malgungothic", 50, True)

# 생존 시간 타이머 변수
start_time = pygame.time.get_ticks()
final_time = ""

# 난이도 조절 변수
difficult_trigger = False

#게임 오버 확인
game_over = False

# 메인 게임 루프
run = True
while run:
    # 이벤트 처리 (입력 감지)
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :       # 창 닫기 버튼을 누르면 종료  
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            run = False

    # 맵 그리기
    screen.fill(GameSettings.BLACK)
    screen.blit(map_img, (0 - offset_x, 0 - offset_y))

    # 게임 진행중
    if not game_over:
        # 현재 시간 저장
        current_time = pygame.time.get_ticks()

        # 생존 시간 타이머(흐른 시간 저장)
        elapsed_time = pygame.time.get_ticks() - start_time
        elapsed_seconds = (elapsed_time // 1000) % 60
        elapsed_minutes = (elapsed_time // 1000) // 60
        
        # 문자열 포맷 02d - 두 자리 숫자로 채우기
        timer_text = f"{elapsed_minutes:02d}:{elapsed_seconds:02d}"

        # 2분 뒤 몬스터가 강해지게 설정
        if elapsed_time >= 120000 and not difficult_trigger:
            difficult_trigger = True

            # 클래스 속성 자체를 변화(앞으로 나오는 몬스터 전부 적용)
            Monster.default_hp = 50
            Monster.default_speed = 1.5
            Monster.default_damage = 30
            Monster.default_exp = 30
            monster_spawn_delay = 2500

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
        
        # 플레이어 그리기
        player.player_draw(screen, offset_x, offset_y)

        # 레벨 UI 그리기
        level.level_draw(screen)

        # 플레이어 체력 UI 그리기
        player.player_hp_draw(screen)

        # 게임 진행 중 타이머 그리기
        display_text = timer_font.render(timer_text, True, (GameSettings.BLACK))
        timer_rect = display_text.get_rect(center=(GameSettings.SCREEN_WIDTH // 2, 50))
        screen.blit(display_text, timer_rect)

        # 몬스터 스폰 로직
        if current_time - monster_spawn_timer > monster_spawn_delay:    # 몬스터 스폰 딜레이가 끝났다면
            spawn_x, spawn_y = get_spawn_position(player, GameSettings.MAP_WIDTH, GameSettings.MAP_HEIGHT)
            monsters_list.append(Monster(spawn_x, spawn_y)) #스폰 포지션 값을 받아와서, 몬스터 리스트에 추가
            monster_spawn_timer = current_time  #그 후 스폰타이머를 현재시간으로 초기화

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

                    # 몬스터의 사망 확인, 경험치
                    if monster.hp <= 0 :
                        level.gain_exp(monster.exp)
                        monsters_list.remove(monster)
                        break
        # 플레이어 사망 체크
        if player.hp <= 0:
            if not game_over:   # 게임 오버 상태가 되기 전에
                final_time = timer_text # 마지막 시간을 체크
                game_over = True


    # 게임 오버(플레이어 사망시)
    if game_over:

        # 반투명 검은색 배경 덮기
        overlay = pygame.Surface((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT))
        overlay.set_alpha(180) # 투명도
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # 텍스트 생성
        text_big = game_font.render("GAME OVER", True, (GameSettings.WHITE))
        text_small = sub_font.render("아무 곳이나 클릭해서 종료", True, (120, 120, 120))
        display_text = timer_font.render(f"생존 시간: {final_time}", True, (GameSettings.RED))

        # 텍스트 위치
        rect_big = text_big.get_rect(center=(GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT // 2 - 40))
        rect_small = text_small.get_rect(center=(GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT // 2 + 40))
        timer_rect = display_text.get_rect(center=(GameSettings.SCREEN_WIDTH // 2, 50))

        # 화면에 글자 그리기
        screen.blit(text_big, rect_big)
        screen.blit(text_small, rect_small)
        screen.blit(display_text, timer_rect)

    # 화면 업데이트
    pygame.display.flip()

    # FPS 설정
    clock.tick(GameSettings.FPS)

# 게임 종료
pygame.quit()
sys.exit()
