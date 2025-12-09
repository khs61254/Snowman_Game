import pygame
import GameSettings
import random

class Skill:
    def __init__(self):
        self.name = "Skill"
        self.desc = "Description"
        self.icon_color = (100, 100, 100) # 이미지가 없을 때 쓸 색상
        self.level = 0

        self.icon_image = None
    
    def update(self, player, monsters_list, offset_x, offset_y):
        pass
    
    def draw(self, screen, offset_x, offset_y):
        pass

# 번개 이미지 관리 클래스
class Thunder :
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage

        # 번개 이미지 로드
        self.size_x = 100
        self.size_y = 300
        self.images = []
        thunder1_img = pygame.image.load("resource/images/skill_thunder1.png").convert_alpha()
        self.thunder1_img = pygame.transform.scale(thunder1_img, (self.size_x, self.size_y))
        thunder2_img = pygame.image.load("resource/images/skill_thunder2.png").convert_alpha()
        self.thunder2_img = pygame.transform.scale(thunder2_img, (self.size_x, self.size_y))

        # 번개 이미지 리스트에 추가
        self.images.append(self.thunder1_img)
        self.images.append(self.thunder2_img)

        # 이미지 인덱스 번호 변수
        self.image_index = 0
        self.current_image = self.images[0]

        # 애니메이션 딜레이
        self.animation_delay = 50

        # 마지막으로 이미지를 바꾼 시간 초기화
        self.last_update_time = pygame.time.get_ticks()

        # 번개 히트박스
        self.rect = self.current_image.get_rect()
        self.rect.midbottom = (self.x, self.y)

        # 지속 시간
        self.duration = 500
        self.spawn_time = pygame.time.get_ticks()

        # 데미지를 넣었는지 체크
        self.damaged = False
        

    # 애니메이션 (두 그림이 반복되게)
    def update(self):
        self.animation()

    def animation(self):    
        # 현재 시간 저장
        current_time = pygame.time.get_ticks()

        # 딜레이 시간이 지났다면 (마지막 이미지가 교체된 시간이 딜레이보다 더 지났다면)
        if current_time - self.last_update_time > self.animation_delay :

            # 마지막 교체 시간을 현재 시간으로 초기화
            self.last_update_time = current_time

            # 인덱스+1 (이미지 교체)
            self.image_index += 1
            
            #인덱스 번호가 2 이상이면 다시 0으로 초기화
            if self.image_index >= 2 :
                self.image_index = 0
            
            # 이미지 교체
            self.current_image = self.images[self.image_index]


    # 번개 그리기
    def draw(self, screen, offset_x, offset_y):
        draw_x = self.rect.x - offset_x
        draw_y = self.rect.y - offset_y
        screen.blit(self.current_image, (draw_x, draw_y))


class Skill_Thunder(Skill) :
    def __init__(self):
        super().__init__()
        self.name = "번개"
        self.desc = "3초마다 화면에 랜덤으로 번개가 떨어집니다"
        self.icon_color = (GameSettings.YELLOW)


        loaded_img = pygame.image.load("resource/images/skill_thunder1.png").convert_alpha()

        self.cooldown = 3000    #쿨타임
        self.last_cast_time = 0 #마지막 시전 시간 초기화
        self.damage = 50
        self.active_thunder = []


    def update(self, player, monsters_list, offset_x, offset_y):
        current_time = pygame.time.get_ticks()

        # 쿨타임 확인
        if current_time - self.last_cast_time > self.cooldown :
            # 스킬 발동 및 마지막 시간을 현재시간으로
            self.cast(player, offset_x, offset_y)
            self.last_cast_time = current_time

        for thunder in self.active_thunder[:]:
            thunder.update()

            if not thunder.damaged:
                for monster in monsters_list:
                    if thunder.rect.colliderect(monster.rect):
                        monster.monster_takeDamage(thunder.damage)
            thunder.damaged = True

            #번개 지속시간 확인 및 삭제
            if current_time - thunder.spawn_time > thunder.duration:
                self.active_thunder.remove(thunder)

    def cast(self, player, offset_x, offset_y):

        #번개 생성 좌표. 플레어의 스크린 내에서 랜덤으로 좌표를 찍고, 맵상에서 어느 좌표인지 계산
        screen_x = random.randint(50, GameSettings.SCREEN_WIDTH - 50)
        screen_y = random.randint(50, GameSettings.SCREEN_HEIGHT - 50)

        world_x = screen_x + offset_x
        world_y = screen_y + offset_y

        new_thunder = Thunder(world_x, world_y, self.damage)
        self.active_thunder.append(new_thunder)

    def draw(self, screen, offset_x, offset_y):
        for thunder in self.active_thunder:
            thunder.draw(screen, offset_x, offset_y)

# 3. 힐 스킬 (자동 회복)
class Skill_Heal(Skill):
    def __init__(self):
        super().__init__()
        self.name = "자동 회복"
        self.desc = "5초마다 체력을 10 회복합니다."
        self.icon_color = (0, 255, 0)
        
        self.heal_amount = 10
        self.cooldown = 5000
        self.last_heal_time = 0

    def update(self, player, monsters_list, offset_x, offset_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_heal_time > self.cooldown:
            if player.hp < player.max_hp:
                player.hp += self.heal_amount
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
            self.last_heal_time = current_time

# 4. 스피드 스킬 (패시브)
class Skill_Speed(Skill):
    def __init__(self):
        super().__init__()
        self.name = "속도 증가"
        self.desc = "이동 속도가 영구적으로 증가합니다."
        self.icon_color = (0, 0, 255)
        self.speed_bonus = 1
        self.applied = False # 한 번만 적용하기 위해

    def update(self, player, monsters_list, offset_x, offset_y):
        # 패시브라 한 번만 적용하면 됨 (또는 레벨업 할 때마다)
        if not self.applied:
            player.speed += self.speed_bonus
            self.applied = True