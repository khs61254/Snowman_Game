import pygame
import GameSettings


class Bullet:
    # 초기화(생성자)
    def __init__(self, x, y, dir_x, dir_y):
        # 기본 총알 이미지 로드, 사이즈
        self.size = 40
        self.bullet_img = pygame.image.load("resource/images/bullet_default.png")
        self.bullet_img = pygame.transform.scale(self.bullet_img, (self.size, self.size))

        # 총알 속성
        self.speed = 4
        self.duration = GameSettings.FPS   # 현재 FPS설정에 따라 유동적(초당 프레임 이므로, 1초간 날아감)
        self.damage = 10

        # 총알 기본 위치, 방향 (플레이어 기준)
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        
        # 히트박스
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
    # 총알 업데이트
    def bullet_update(self):
        # 총알 방향과 속도 저장
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

        # 총알 히트박스 동기화
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # 총알 지속 시간 감소
        self.duration -= 1
    
    # 총알 그리기
    def bullet_draw(self, screen, offset_x, offset_y):
        draw_x = self.x - offset_x
        draw_y = self.y - offset_y
        
        screen.blit(self.bullet_img, (draw_x, draw_y))

