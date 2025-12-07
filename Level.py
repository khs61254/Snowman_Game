import pygame
import GameSettings

# 플레이어의 경험치, 레벨 클래스
class Level :
    # 생성자 실행 시 초기화
    def __init__(self, player) :
        self.player = player

        # 레벨 속성
        self.level = 1
        self.exp_max = 100
        self.exp = 0

        # 레벨UI를 위한 폰트 설정
        self.font = pygame.font.SysFont("malgungothic", 50, True)
        self.font_sub = pygame.font.SysFont("malgungothic", 1)


    # 경험치 획득 함수
    def gain_exp(self, amount) :
        self.exp += amount
        self.check_level_up()

    # 레벨업 함수
    def check_level_up(self):
        # 레벨업 시
        if self.exp >= self.exp_max:
            #레벨 증가, exp_max 증가
            self.level += 1
            self.exp -= self.exp_max
            self.exp_max += 20
            #maxhp 증가, 체력 모두 회복
            self.player.maxhp += 20
            self.player.hp = self.player.maxhp

            #스킬 선택

    # 레벨, 경험치 UI
    def level_draw(self, screen):
        
        # 레벨 UI
        level_text = self.font.render(f"LV. {self.level}", True, (0, 127, 255))
        screen.blit(level_text, (30, 750))

        # 총 경험치 바
        pygame.draw.rect(screen, (GameSettings.GRAY), (30, 860, 450, 30))

        # 현재 경험치 바
        ratio = self.exp / self.exp_max
        fill_width = int(450 * ratio)
        pygame.draw.rect(screen, (GameSettings.YELLOW), (30, 860, fill_width, 30))
