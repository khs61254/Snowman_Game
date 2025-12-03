import pygame


class Player :
    # 게임 변수 설정
    def __init__(self, screen_width, screen_height) :

        # 플레이어 모습 사이즈, 색
        self.size = 50
        self.color = (255, 255, 255)

        # 받아온 화면 크기 저장
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 플레이어 기본 위치, 속도 설정
        self.x = screen_width // 2 - self.size // 2
        self.y = screen_height - self.size - 10
        self.speed = 5

        # 플레이어 히트박스
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)


    # 플레이어 움직임
    def player_move(self) :
        keys = pygame.key.get_pressed()     # 누른 키값을 받아오는 함수

        # 직선 이동
        if (keys[pygame.K_a]):
            self.x = self.x - self.speed      # 플레이어 속도만큼 위치값변경
            self.rect.x = self.x        # 히트박스 = 플레이어 모습과 같이 이동
        if (keys[pygame.K_d]):
            self.x = self.x + self.speed
            self.rect.x = self.x
        if (keys[pygame.K_w]):
            self.y = self.y - self.speed
            self.rect.y = self.y
        if (keys[pygame.K_s]):
            self.y = self.y + self.speed
            self.rect.y = self.y

    # 플레이어 그리기
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
