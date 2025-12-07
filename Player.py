import pygame
import GameSettings
from Bullet import Bullet


class Player :

    default_speed = 1.5
    default_hp = 100
    default_maxhp = 100

    # 플레이어 클래스 초기화(생성자)
    def __init__(self, map_width, map_height) :

        # 플레이어 이미지로드, 사이즈
        self.size = 120
        self.snowman_img = pygame.image.load("resource/images/snowman.png")     #이미지 로드 함수
        self.snowman_img = pygame.transform.scale(self.snowman_img, (self.size, self.size)) #이미지 사이즈 조정 함수
        self.snowman_img_flipped = pygame.transform.flip(self.snowman_img, True, False)    #이미지 좌우 뒤집기 함수
        self.snowman_img_original = self.snowman_img

        # 받아온 맵 크기 저장
        self.map_width = map_width
        self.map_height = map_height

        # 플레이어 속성
        self.speed = Player.default_speed
        self.hp = Player.default_hp
        self.maxhp = Player.default_maxhp

        # 플레이어 무적
        self.isInv = False  #무적 상태 확인
        self.inv_start_time = 0  #무적 시작 시간
        self.inv_duration = 1000  #무적 지속 시간

        # 플레이어 기본 위치
        self.x = self.map_width // 2
        self.y = self.map_height // 2

        # 플레이어 히트박스(사각형)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)   #사각형 생성 함수
        self.rect.topleft = (self.x, self.y)
        
        # 총알 쿨다운 설정
        self.last_shot_time = 0
        self.shoot_cooldown = 800

        # 폰트
        self.font = pygame.font.SysFont("malgungothic", 1, True)


    # 플레이어 움직임
    def player_move(self) :
        keys = pygame.key.get_pressed()     # 누른 키값을 받아오는 함수

        # 직선 이동
        if (keys[pygame.K_a]):
            if (self.x > 0):                  # 플레이어가 맵 밖으로 나가지 못하게 제어
                self.x -= self.speed                # 플레이어 속도만큼 위치값변경
                self.snowman_img = self.snowman_img_original        
        if (keys[pygame.K_d]):
            if (self.x < self.map_width - self.size):
                self.x += self.speed
                self.snowman_img = self.snowman_img_flipped     #a, d 입력 시 이미지를 좌우반전시켜 보는 방향을 연출
        if (keys[pygame.K_w]):
            if (self.y > 0):    
                self.y -= self.speed
        if (keys[pygame.K_s]):
            if (self.y < self.map_height - self.size):
                self.y += self.speed
            
    # 히트박스 = 플레이어 모습과 같이 이동하게 같은 좌표로 설정
        self.rect.x = self.x
        self.rect.y = self.y

    # 플레이어 그리기
    def player_draw(self, screen, offset_x, offset_y):

        # 무적 상태에서 깜빡임
        if self.isInv == True:
            if (pygame.time.get_ticks() % 200) < 100:
                return

        draw_x = self.x - offset_x
        draw_y = self.y - offset_y
        screen.blit(self.snowman_img, (draw_x, draw_y))
        

    # 플레이어 총알 발사
    def player_shooting(self, bullets_list):

        current_time = pygame.time.get_ticks()  # 현재시간을 ms단위로 가져오는 함수
        
        # 쿨다운 시간을 넘었다면
        if current_time - self.last_shot_time > self.shoot_cooldown:
            
            # 초기화
            keys = pygame.key.get_pressed() # 누르고 있는 키값을 받아오는 함수
            direction_x = 0         # 초기값 0은 쏘지 않는 상태
            direction_y = 0
            isShooting = False

            # 방향키로 발사 방향 설정 (-1, 0, 1)
            if keys[pygame.K_LEFT]:
                direction_x = -1
                isShooting = True
            if keys[pygame.K_RIGHT]:
                direction_x = 1
                isShooting = True
            if keys[pygame.K_UP]:
                direction_y = -1
                isShooting = True
            if keys[pygame.K_DOWN]:
                direction_y = 1
                isShooting = True

            # 쐈을 경우(방향키를 눌렀다면)
            if isShooting == True:
                
                # 총알 시작 위치는 플레이어의 중앙
                start_x = self.x + self.size // 2
                start_y = self.y + self.size // 2

                # 총알 객체 생성
                bullet = Bullet(start_x, start_y, direction_x, direction_y) # 총알의 시작 위치, 방향 인수값 전달
                bullets_list.append(bullet)      # bullets_list 리스트에 추가

                # 총알 발사 시간을 현재 시간에 맞춤(현재시간으로 초기화)
                self.last_shot_time = current_time
    
    # 데미지를 받을 때
    def take_damage(self, monster_damage):
        current_time = pygame.time.get_ticks()

        if not self.isInv :
            self.hp -= monster_damage

            self.isInv = True           # 데미지를 받은 후 무적 활성화
            self.inv_start_time = current_time  # 무적 시작 시간을 현재시간으로 지정


    # 플레이어 상태를 무적으로 업데이트
    def update_status(self):
        
        if self.isInv == True:
            current_time = pygame.time.get_ticks()

            if current_time - self.inv_start_time > self.inv_duration:
                self.isInv = False

    # 체력바 UI
    def player_hp_draw(self, screen):

        # 총 체력 바
        pygame.draw.rect(screen, (100, 100, 100), (30, 820, 450, 30))

        # 현재 체력 바
        ratio = self.hp / self.maxhp
        fill_width = int(450 * ratio)
        pygame.draw.rect(screen, (GameSettings.RED), (30, 820, fill_width, 30))
