import pygame
import math
from Bullet import Bullet


class Monster :
    def __init__(self, x, y):
        # 몬스터 이미지 로드
        self.size = 100
        self.sangblin_img = pygame.image.load("resource/images/sangblin.png")
        self.sangblin_img = pygame.transform.scale(self.sangblin_img, (self.size, self.size))

        # 몬스터 속성
        self.hp = 30
        self.speed = 1
        self.damage = 20
        self.isDead = False
        self.exp = 20       #몬스터의 경험치량

        # 몬스터 위치
        self.x = float(x)
        self.y = float(y)

        # 몬스터 히트박스
        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    # 몬스터 움직임
    def monster_chase(self, player):
        
        # 타깃의 중심 좌표, 자신의 중심 좌표 계산
        target_x = player.x + player.size // 2
        target_y = player.y + player.size // 2
        my_center_x = self.x + self.size // 2
        my_center_y = self.y + self.size // 2

        # 벡터값 계산 (플레이어와 몬스터의 거리, 몬스터가 플레이어에게 가려면 어디로 얼마나 가야하는지)
        # AI 도움받음
        direction = pygame.math.Vector2(target_x - my_center_x, target_y - my_center_y)

        # 둘의 거리가 0보다 클 때만 이동
        if direction.length() > 0:
            # normalize = 방향 유지 but, 길이 1로 만듦
            direction = direction.normalize()

            # 방향, 속도만큼 밀기
            self.x += direction.x * self.speed
            self.y += direction.y * self.speed

        # 히트박스 동기화
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def monster_takeDamage(self, bullet_damage):
        
        self.hp -= bullet_damage

    def monster_draw(self, screen, offset_x, offset_y):
        draw_x = self.rect.x - offset_x
        draw_y = self.rect.y - offset_y

        screen.blit(self.sangblin_img, (draw_x, draw_y))
