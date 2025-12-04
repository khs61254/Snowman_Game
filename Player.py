import pygame


class Player :
    # 플레이어 클래스 초기화(생성자)
    def __init__(self, map_width, map_height) :

        # 플레이어 모습 사이즈, 색
        self.size = 120

        self.snowman_img = pygame.image.load("resource/images/snowman.png")     #이미지 로드 함수
        self.snowman_img = pygame.transform.scale(self.snowman_img, (self.size, self.size)) #이미지 사이즈 조정 함수
        self.snowman_img_flipped = pygame.transform.flip(self.snowman_img, True, False)    #이미지 좌우 뒤집기 함수
        self.snowman_img_original = self.snowman_img

        # 받아온 맵 크기 저장
        self.map_width = map_width
        self.map_height = map_height

        # 플레이어 기본 위치, 속도 설정
        self.x = self.map_width // 2
        self.y = self.map_height // 2
        self.speed = 3

        # 플레이어 히트박스(사각형)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)   #사각형 생성 함수
        self.rect.topleft = (self.x, self.y)
        

    # 플레이어 움직임
    def player_move(self) :
        keys = pygame.key.get_pressed()     # 누른 키값을 받아오는 함수

        # 직선 이동
        if (keys[pygame.K_a]):
            if (self.x > 0):                  # 플레이어가 맵 밖으로 나가지 못하게 제어
                self.x = self.x - self.speed                # 플레이어 속도만큼 위치값변경
                self.snowman_img = self.snowman_img_original        
        if (keys[pygame.K_d]):
            if (self.x < self.map_width - self.size):
                self.x = self.x + self.speed
                self.snowman_img = self.snowman_img_flipped     #a, d 입력 시 이미지를 좌우반전시켜 보는 방향을 연출
        if (keys[pygame.K_w]):
            if (self.y > 0):    
                self.y = self.y - self.speed
        if (keys[pygame.K_s]):
            if (self.y < self.map_height - self.size):
                self.y = self.y + self.speed
            
    # 히트박스 = 플레이어 모습과 같이 이동하게 같은 좌표로 설정
        self.rect.x = self.x
        self.rect.y = self.y

    # 플레이어 화면에 띄우기
    def draw(self, screen, offset_x, offset_y):
        draw_x = self.x - offset_x
        draw_y = self.y - offset_y

        screen.blit(self.snowman_img, (draw_x, draw_y))
