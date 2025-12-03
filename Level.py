import pygame
#from Monster import '몬스터 죽음 확인 메소드'

# 플레이어의 경험치, 레벨 클래스
class Level :
    # 생성자 실행 시 초기화
    def __init__(self) :
        self.exp_max = 100
        self.exp = 0
        self.level = 0

    # 레벨 메소드
    def Level(self, ) :

        # 몬스터 죽음 체크, 경험치 전달
        if (monster_isDead == True):
            self.exp = self.exp + 10

        # 레벨업 구현
        if (self.exp == self.exp_max):
            self.exp_max = self.exp_max + 20
            self.exp = 0
            self.level = self.level + 1
            
