import pygame


class Monster :
    def __init__(self):
        self.isDead = false
        self.HP = 100



    # 몬스터 움직임
    def monster_move(self):


    # 몬스터 스폰 위치
    def monster_spawn(self):


    # 몬스터 사망 확인
    def monster_isDead(self, monster_hp):
        if self.HP <= 0 :
