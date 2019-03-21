import pygame
import pygame.locals as locals
import math
import random
import sys
from pygame.locals import *

pygame.mixer.init()
# 加载欢快的背景音乐
a = pygame.mixer.Sound("source/背景音乐/蘑菇城/蘑菇城.wav")
a.play()


# 计时类
# 背景类
class Background(object):
    def __init__(self):
        self.img = pygame.image.load \
            ('source/场景/刀塔传奇地图原画-bbg 春天龙骨(bbg_spring_d_爱给网_aigei_com.jpg')

    def display(self):
        screen.blit(self.img, (0, 0))
        # global gameTime
        # gameTime = GameTime()
        # gameTime.display()


# 游戏基本事物类
class GameObject(object):
    def __init__(self):
        self.is_alive = True

    def isCrash(self, other):
        if self.x - self.width / 2 < other.x + other.width / 2 \
                and self.x + self.width / 2 > other.x - other.width / 2 \
                and self.y + self.height / 2 > other.y - other.height / 2 \
                and self.y - self.height / 2 < other.y + other.height / 2:
            return True
        return False


# 游戏时间类
class GameTime(GameObject):
    def __init__(self):
        super().__init__()
        self.backgroudColor = (255, 0, 0)
        self.fontColor = (0, 0, 0)

    def display(self):
        fontObj = pygame.font.Font(None, 30)  # 通过字体文件获得字体对象
        global finalTime
        # finalTime=t
        finalTime = str(int(time / 60000)) + ":" + str(int((time) / 1000 % 60))
        # if youwin() or gameover():
        #     t = 90000
        # textSurfaceObj = fontObj.render(str(int((90000 - t) / 60000)) +
        #                                 ":" + str(int((90000 - t) / 1000 % 60)),
        #                                 True, self.fontColor, self.backgroudColor)  # 配置要显示的文字
        textSurfaceObj = fontObj.render(
            "Rank:" + str(player.rank) + "  " + "Skill consumption:15" + "  " + "Anxiety:" + str(
                anxiety_count) + "  " + "Alive time:" + str(int(time / 60000)) +
            ":" + str(int((time) / 1000 % 60)),
            True, self.fontColor, self.backgroudColor)  # 配置要显示的文字
        textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
        # textRectObj.center = (self.posx, self.posy)  # 设置显示对象的坐标
        textRectObj.center = (SCREEN_WIDTH - 300, 50)  # 设置显示对象的坐标
        screen.blit(textSurfaceObj, textRectObj)  # 绘制字


# 玩家类
class Player(GameObject):
    def __init__(self):
        super().__init__()
        self.width = 90
        self.height = 123
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.life = 3000
        self.rank = 1
        self.atk = 0

        # self.rect =rect

        self.imgs_left = []
        self.imgs_left.append(pygame.image.load("source/角色/瓜皮兔/瓜皮兔1.png"))
        self.imgs_left.append(pygame.image.load("source/角色/瓜皮兔/瓜皮兔2.png"))
        self.imgs_left.append(pygame.image.load("source/角色/瓜皮兔/瓜皮兔3.png"))
        self.imgs_left.append(pygame.image.load("source/角色/瓜皮兔/瓜皮兔4.png"))
        self.imgs_left.append(pygame.image.load("source/角色/瓜皮兔/瓜皮兔5.png"))
        self.imgs_left.append(pygame.image.load("source/角色/瓜皮兔/瓜皮兔6.png"))

        self.imgs_right = []
        self.imgs_right.append(pygame.image.load("source/角色/镜像瓜皮兔/瓜皮兔1.png"))
        self.imgs_right.append(pygame.image.load("source/角色/镜像瓜皮兔/瓜皮兔2.png"))
        self.imgs_right.append(pygame.image.load("source/角色/镜像瓜皮兔/瓜皮兔3.png"))
        self.imgs_right.append(pygame.image.load("source/角色/镜像瓜皮兔/瓜皮兔4.png"))
        self.imgs_right.append(pygame.image.load("source/角色/镜像瓜皮兔/瓜皮兔5.png"))
        self.imgs_right.append(pygame.image.load("source/角色/镜像瓜皮兔/瓜皮兔6.png"))

        self.index = 0
        self.count = 0
        self.img = self.imgs_left[0]
        # 主角死亡图
        self.boom_imgs = []
        self.boom_imgs.append(pygame.image.load("source/角色/主角死亡/8.png"))
        self.boom_imgs.append(pygame.image.load("source/角色/主角死亡/7.png"))
        self.boom_imgs.append(pygame.image.load("source/角色/主角死亡/6.png"))
        self.boom_imgs.append(pygame.image.load("source/角色/主角死亡/5.png"))
        self.boom_imgs.append(pygame.image.load("source/角色/主角死亡/4.png"))
        self.boom_imgs.append(pygame.image.load("source/角色/主角死亡/3.png"))
        self.boom_imgs.append(pygame.image.load("source/角色/主角死亡/2.png"))
        self.boom_imgs.append(pygame.image.load("source/角色/主角死亡/1.png"))
        self.boom_index = 0
        self.boom_time = 10

        self.move_x = -1
        self.move_y = -1
        self.speed = 4
        self.life = 100
        self.need_move = True

    def update(self, press_keys):
        if self.life > 0:

            if press_keys[K_a]:
                self.x -= self.speed
            if press_keys[K_d]:
                self.x += self.speed
            if press_keys[K_w]:
                self.y -= self.speed
            if press_keys[K_s]:
                self.y += self.speed

            # 到一定时间(RECOVERY_CD)自我恢复血量
            if time_count % RECOVERY_CD == 0:
                self.life += 10

            # 存活足够久就升级
            if time_count % LVUP_NEED_TIME == 0:
                self.rank += 1
                self.life += 200
                # self.atk+=1

        global game_over
        self.count += 1
        # if x<self.x:#鼠标坐标<玩家坐标时，播放向左走图片
        if mouse_x - self.x < 0:  #####早上写到此
            self.img = self.imgs_left[self.index]
        elif mouse_x - self.x >= 0:
            self.img = self.imgs_right[self.index]
        if self.count % 5 == 0:
            self.count = 0
            self.index += 1
        if self.index >= len(self.imgs_left):
            self.index = 0

            # if self.need_move:
            # #if self.is_alive:
            #
            #     len_x = self.move_x - self.x
            #     len_y = self.move_y - self.y
            #     s = math.sqrt(len_x ** 2 + len_y ** 2)
            #     times = int(s / self.speed)
            #     if times >= 1:
            #         x_speed = len_x / times
            #         y_speed = len_y / times
            #         self.x += x_speed
            #         self.y += y_speed
            #     else:
            #         self.x = self.move_x
            #         self.y = self.move_y
        if self.y < 200:
            self.y = 200
        # 如果血量<0死亡
        if self.life <= 0:
            if self.boom_index >= len(self.boom_imgs):  # 判断爆炸图片的下标是否越界

                self.is_alive = False  # 主角死亡
                self.img = self.boom_imgs[-1]
                # if time_count % 50 == 0:
                game_over = True
            else:
                self.img = self.boom_imgs[self.boom_index]  # 每次将要绘制的图片，替换为对应的爆炸图片

            if time_count % self.boom_time == 0:  # 判断是否达到循环次数，替换为下一张爆炸图片
                self.boom_index += 1
            # if self.boom_index >= len(self.boom_img):  # 判断爆炸图片的下标是否越界
            #     self.is_alive = False  # 如果成立，代表越界，爆炸轮播完，敌机不需存活
            #     # return  # 因为越界，后续代码不能执行
            #
            # print("1111111111111111111111111")
            # self.img = self.boom_img[self.boom_index]  # 每次将要绘制的图片，替换为对应的爆炸图片
            # if time_count % self.boom_time == 0:  # 判断是否达到循环次数，替换为下一张爆炸图片
            #     self.boom_index += 1
            # # self.is_alive = False
            # if time_count % 400 == 0:
            #     game_over = True

    def display(self):
        # if self.life > 0:
        width = self.width * self.life / 100
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.x - self.width / 2, self.y - self.height / 2 - 4, width, 2), 0)
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))

    def move(self, x, y):
        if self.life > 0:
            if self.y >= 200:
                self.move_x = x
                self.move_y = y
        # if self.y<=200:
        #     self.need_move=False
        # elif self.y>200:
        #     self.need_move=True
        # if self.need_move:
        #     self.move_x = x
        #     self.move_y = y

    def attack(self):
        if self.life > 0:
            bullet = PlayerBullet(self.x, self.y)
            player_bullets.append(bullet)

    def attack_2(self):
        if self.life > 0:
            bullet = PlayerBullet_2(self.x, self.y)
            player_bullets.append(bullet)


# 玩家子弹类
class PlayerBullet(GameObject):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.atk = 1  # 攻击力点数
        # self.y = y - player.height / 3

        # self.width = 32
        # self.height = 32
        self.width = 40
        self.height = 40
        self.speed = 15
        # self.img = pygame.image.load("source/角色子弹/普攻/火球_001.png")
        self.img = pygame.image.load("source/角色子弹/普攻/火球_002.png")
        len_x = press_mouse_x - self.x
        len_y = press_mouse_y - self.y
        s = math.sqrt(len_x ** 2 + len_y ** 2)
        times = int(s / self.speed)
        if times > 0:
            self.x_speed = len_x / times
            self.y_speed = len_y / times
        else:
            self.is_alive = False

    def update(self):
        if time_count % LVUP_NEED_TIME == 0:
            self.atk += 1
        self.x += self.x_speed
        self.y += self.y_speed

        if self.y + self.height / 2 < 0 or self.y - self.height > 615 or \
                self.x + self.width / 2 < 0 or self.x - self.width / 2 > 1024:
            self.is_alive = False

    def display(self):
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))


# 玩家小技能
class PlayerBullet_2(GameObject):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y - player.height / 2
        # self.width=220
        # self.height=256
        # self.width = 32
        # self.height = 32
        self.width = 40
        self.height = 40
        self.atk = 4
        self.speed = 9
        self.imgs = []
        self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/螺旋丸手里剑/螺旋丸手里剑0.png"))
        self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/螺旋丸手里剑/螺旋丸手里剑1.png"))
        self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/螺旋丸手里剑/螺旋丸手里剑2.png"))
        self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/螺旋丸手里剑/螺旋丸手里剑3.png"))
        self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/螺旋丸手里剑/螺旋丸手里剑4.png"))
        self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/螺旋丸手里剑/螺旋丸手里剑5.png"))
        self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/螺旋丸手里剑/螺旋丸手里剑6.png"))
        self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/螺旋丸手里剑/螺旋丸手里剑7.png"))
        self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/螺旋丸手里剑/螺旋丸手里剑8.png"))
        self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/螺旋丸手里剑/螺旋丸手里剑9.png"))
        self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/螺旋丸手里剑/螺旋丸手里剑10.png"))
        # self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/火焰喷射/火焰喷射5.png"))
        # self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/火焰喷射/火焰喷射6.png"))
        # self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/火焰喷射/火焰喷射7.png"))
        # self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/火焰喷射/火焰喷射8.png"))
        # self.imgs.append(pygame.image.load("source/角色子弹/特殊子弹/火焰喷射/火焰喷射9.png"))
        self.img = self.imgs[0]
        # print(self.img)
        self.index = 0

        # self.img = pygame.image.load("source/角色子弹/普攻/火球_002.png")
        len_x = press_mouse_x - self.x
        len_y = press_mouse_y - self.y
        s = math.sqrt(len_x ** 2 + len_y ** 2)
        times = int(s / self.speed)
        if times > 0:
            self.x_speed = len_x / times
            self.y_speed = len_y / times
        else:
            self.is_alive = False

    def update(self):
        # self.count += 1
        self.x += self.x_speed
        self.y += self.y_speed

        # if self.y + self.height / 2 < 0 or self.y - self.height > 615 or \
        #         self.x + self.width / 2 < 0 or self.x - self.width / 2 > 1024:
        #     self.is_alive = False
        # if self.is_alive:
        # if self.life <= 0:  # 敌人血量<=0,死亡
        #     if self.boom_index >= len(self.boom_img):  # 判断爆炸图片的下标是否越界
        #         self.is_alive = False  # 如果成立，代表越界，爆炸轮播完，敌机不需存活
        #         self.img = self.boom_img[-1]
        #     else:
        #         self.img = self.boom_img[self.boom_index]  # 每次将要绘制的图片，替换为对应的爆炸图片
        #     if time_count % self.boom_time == 0:  # 判断是否达到循环次数，替换为下一张爆炸图片
        #         self.boom_index += 1
        if self.is_alive:
            if self.index >= len(self.imgs):  # 判断爆炸图片的下标是否越界
                self.is_alive = False  # 如果成立，代表越界，爆炸轮播完，敌机不需存活
                self.img = self.imgs[-1]
            else:
                self.img = self.imgs[self.index]  # 每次将要绘制的图片，替换为对应的爆炸图片
            if time_count % 5 == 0:  # 判断是否达到循环次数，替换为下一张爆炸图片
                self.index += 1

        # if  True:
        #     self.count+=1
        #     if self.index >= len(self.imgs):  # 判断爆炸图片的下标是否越界
        #         self.is_alive = False  # 子弹消亡
        #         self.img = self.imgs[-1]
        #
        #         print("====="+type(self.img))
        #     else:
        #         self.img = self.img[self.index]  # 每次将要绘制的图片，替换为对应图片
        #     if time_count % 5 == 0:  # 判断是否达到循环次数，替换为下一张爆炸图片
        #         self.index += 1

    def display(self):
        # print("111111111111111")
        # print(type(self.img))
        # print(type(self.imgs[0]))
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))


# 敌人类
class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, 1) * SCREEN_WIDTH  #
        self.y = SEA_HEIGHT + random.randint(1, 3) * (LAND_HEIGHT / 3)
        self.rank = 1
        self.atk = 1
        self.preTimeCount = 0  # 攻击准备计时，当此数大于等于敌人攻击准备所需准备时间且玩家进入敌人射程时允许敌人攻击
        # self.life = 10 * self.rank
        self.imgs_right = []
        self.imgs_left = []
        self.boom_img = []
        self.boom_img.append(pygame.image.load("source/爆炸/boom_1.png"))
        self.boom_img.append(pygame.image.load("source/爆炸/boom_2.png"))
        self.boom_img.append(pygame.image.load("source/爆炸/boom_3.png"))
        self.boom_img.append(pygame.image.load("source/爆炸/boom_4.png"))
        self.boom_img.append(pygame.image.load("source/爆炸/boom_5.png"))
        self.boom_img.append(pygame.image.load("source/爆炸/boom_6.png"))
        self.boom_index = 0
        self.boom_time = 5
        # self.img=self.imgs_left[0]
        # self.img=self.imgs_left[len(self.imgs_left)-1]
        # self.imgs_index = 0

    def attack_5(self):
        bullet = EnemyBullet_5(self.x, self.y)
        enemy_bullets.append(bullet)

    def attack_4(self):
        bullet = EnemyBullet_4(self.x, self.y)
        enemy_bullets.append(bullet)

    def attack_3(self):
        bullet = EnemyBullet_3(self.x, self.y)
        enemy_bullets.append(bullet)

    def attack_2(self):
        bullet = EnemyBullet_2(self.x, self.y)
        enemy_bullets.append(bullet)

    def attack(self):
        bullet = EnemyBullet(self.x, self.y)
        enemy_bullets.append(bullet)

    def update(self):

        if time_count % (LVUP_NEED_TIME - 50) == 0:  # 敌人的升级时间要略少于玩家的，营造紧张感:
            self.life += 20
            self.atk += 1

        if self.life <= 0:  # 敌人血量<=0,死亡
            if self.boom_index >= len(self.boom_img):  # 判断爆炸图片的下标是否越界
                self.is_alive = False  # 如果成立，代表越界，爆炸轮播完，敌机不需存活
                self.img = self.boom_img[-1]
            else:
                self.img = self.boom_img[self.boom_index]  # 每次将要绘制的图片，替换为对应的爆炸图片
            if time_count % self.boom_time == 0:  # 判断是否达到循环次数，替换为下一张爆炸图片
                self.boom_index += 1

    def display(self):
        pass


# 敌人子弹类（发散火球）
class EnemyBullet(GameObject):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 5
        self.atk = 2
        self.img = pygame.image.load("source/角色子弹/普攻/发散火球.png")
        len_x = player.x - self.x
        len_y = player.y - self.y
        s = math.sqrt(len_x ** 2 + len_y ** 2)
        times = s / self.speed
        self.x_speed = len_x / times
        self.y_speed = len_y / times

    def update(self):
        print("麒麟atk:" + str(self.atk))
        self.x += self.x_speed
        self.y += self.y_speed
        if time_count % (LVUP_NEED_TIME - 50) == 0:
            self.atk += 1

    def display(self):
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))


# 敌人子弹类2（蓝弹）
class EnemyBullet_2(GameObject):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 5
        self.atk = 1
        self.img = pygame.image.load("source/角色子弹/普攻/蓝火球_001.png")
        len_x = player.x - self.x
        len_y = player.y - self.y
        s = math.sqrt(len_x ** 2 + len_y ** 2)
        times = s / self.speed
        self.x_speed = len_x / times
        self.y_speed = len_y / times

    def update(self):
        print("sk_atk:" + str(self.atk))
        self.x += self.x_speed
        self.y += self.y_speed
        if time_count % (LVUP_NEED_TIME - 50) == 0:
            self.atk += 1

    def display(self):
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))


# 敌人子弹类3（魔法黑弹）
class EnemyBullet_3(GameObject):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 5
        self.atk = 5
        self.img = pygame.image.load("source/boss技能/魔法黑弹/魔法黑弹.png")
        len_x = player.x - self.x
        len_y = player.y - self.y
        s = math.sqrt(len_x ** 2 + len_y ** 2)
        times = s / self.speed
        self.x_speed = len_x / times
        self.y_speed = len_y / times

    def update(self):
        print("boss魔法黑弹_atk:" + str(self.atk))
        self.x += self.x_speed
        self.y += self.y_speed
        if time_count % (LVUP_NEED_TIME - 50) == 0:
            self.atk += 1

    def display(self):
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))


# 敌人子弹类4（闪电球）
class EnemyBullet_4(GameObject):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 5
        self.atk = 4
        self.img = pygame.image.load("source/角色子弹/普攻/闪电球 .png")
        len_x = player.x - self.x
        len_y = player.y - self.y
        s = math.sqrt(len_x ** 2 + len_y ** 2)
        times = s / self.speed
        self.x_speed = len_x / times
        self.y_speed = len_y / times

    def update(self):
        print("蓝龙_atk:" + str(self.atk))
        self.x += self.x_speed
        self.y += self.y_speed
        if time_count % (LVUP_NEED_TIME - 50) == 0:
            self.atk += 1

    def display(self):
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))


# 敌人子弹类5（大火球）
class EnemyBullet_5(GameObject):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 5
        self.atk = 7
        self.img = pygame.image.load("source/角色子弹/特殊子弹/大火球/大火球0.png")
        len_x = player.x - self.x
        len_y = player.y - self.y
        s = math.sqrt(len_x ** 2 + len_y ** 2)
        times = s / self.speed
        self.x_speed = len_x / times
        self.y_speed = len_y / times

    def update(self):
        print("boss大火球atk:" + str(self.atk))
        self.x += self.x_speed
        self.y += self.y_speed
        if time_count % (LVUP_NEED_TIME - 50) == 0:
            self.atk += 1

    def display(self):
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))


# 敌人：骷髅兵
class Skeleton(Enemy):
    def __init__(self):
        super().__init__()
        self.width = 100
        self.height = 100
        self.life = 20
        self.atk = 1
        self.speed = 3
        self.shootDistance = 160
        self.attackPreTime = 50
        # self.y = random.randint(0, 5) * (LAND_HEIGHT / 5) + self.height / 2
        if random.randint(1, 2) == 1:
            self.x = random.randint(0, 1) * SCREEN_WIDTH  # 左右上下随机出现怪物
            self.y = SEA_HEIGHT + random.randint(1, 5) * (LAND_HEIGHT / 5)
        else:
            self.x = random.randint(0, 7) * SCREEN_WIDTH / 7  # 左右上下随机出现怪物
            self.y = SCREEN_HEIGHT

        self.imgs_left = []
        self.imgs_left.append(pygame.image.load("source/怪物/窟窿战士/骷髅战士01.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/窟窿战士/骷髅战士02.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/窟窿战士/骷髅战士03.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/窟窿战士/骷髅战士04.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/骷髅小兵挥刀动图/骷髅战士左1.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/骷髅小兵挥刀动图/骷髅战士左2.png"))
        self.imgs_right = []
        self.imgs_right.append(pygame.image.load("source/怪物/窟窿战士/骷髅战士11.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/窟窿战士/骷髅战士22.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/窟窿战士/骷髅战士33.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/窟窿战士/骷髅战士44.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/骷髅小兵挥刀动图/骷髅战士右1.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/骷髅小兵挥刀动图/骷髅战士右2.png"))
        self.index = 0
        self.count = 0
        self.img = self.imgs_left[0]

        self.move_x = -1
        self.move_y = -1
        self.need_move = True

    def update(self):

        self.count += 1
        # if x<self.x:#敌人坐标>玩家坐标时，播放向左走图片
        # if mouse_x - self.x < 0:
        if self.x > player.x:
            self.img = self.imgs_left[self.index]
        # elif mouse_x - self.x >= 0:
        elif self.x < player.x:
            self.img = self.imgs_right[self.index]
        if self.count % 5 == 0:
            self.count = 0
            self.index += 1
        if self.index >= len(self.imgs_left):
            self.index = 0

        if self.need_move:
            # len_x = self.move_x - self.x
            # len_y = self.move_y - self.y
            len_x = player.x - self.x
            len_y = player.y - self.y
            s = math.sqrt(len_x ** 2 + len_y ** 2)
            times = int(s / self.speed)
            if s >= self.shootDistance:
                if times >= 1:
                    x_speed = len_x / times
                    y_speed = len_y / times
                    self.x += x_speed
                    self.y += y_speed
            # else:
            #     self.x = self.move_x
            #     self.y = self.move_y

            # 进入射程且攻击准备计时到
            # self.preTimeCount += 1
            # if self.preTimeCount >= self.attackPretime and:
            #     self.preTimeCount = 0
        super().update()
        if s <= self.shootDistance:
            if time_count % self.attackPreTime == 0:
                self.attack_2()

    def display(self):
        # screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))


# 敌人：麒麟
class Unicorn(Enemy):
    def __init__(self):
        super().__init__()
        self.width = 170
        self.height = 123
        self.life = 50  # 麒麟生命值
        self.speed = 4  # 麒麟速度
        self.shootDistance = 400  # 射程距离
        self.attackPreTime = 100  # 攻击准备时间
        self.y = random.randint(0, 5) * (LAND_HEIGHT / 5) + self.height / 2
        self.x = random.randint(0, 1) * SCREEN_WIDTH  # 左右随机出现怪物
        self.imgs_left = []
        self.imgs_left.append(pygame.image.load("source/怪物/龙麒麟/龙麒麟01.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙麒麟/龙麒麟02.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙麒麟/龙麒麟03.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙麒麟/龙麒麟04.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙麒麟/龙麒麟05.png"))

        self.imgs_right = []
        self.imgs_right.append(pygame.image.load("source/怪物/龙麒麟/龙麒麟11.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙麒麟/龙麒麟22.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙麒麟/龙麒麟33.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙麒麟/龙麒麟44.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙麒麟/龙麒麟55.png"))
        self.index = 0
        self.count = 0
        self.img = self.imgs_left[0]

        self.move_x = -1
        self.move_y = -1

        self.need_move = True

    def update(self):
        self.count += 1
        # if x<self.x:#敌人坐标>玩家坐标时，播放向左走图片
        # if mouse_x - self.x < 0:
        if self.x > player.x:
            self.img = self.imgs_left[self.index]
        # elif mouse_x - self.x >= 0:
        elif self.x < player.x:
            self.img = self.imgs_right[self.index]
        if self.count % 5 == 0:
            self.count = 0
            self.index += 1
        if self.index >= len(self.imgs_left):
            self.index = 0

        # if self.need_move:
        if True:
            # len_x = self.move_x - self.x
            # len_y = self.move_y - self.y
            len_x = player.x - self.x
            len_y = player.y - self.y
            s = math.sqrt(len_x ** 2 + len_y ** 2)
            times = int(s / self.speed)
            if s >= self.shootDistance:
                if times >= 1:
                    x_speed = len_x / times
                    y_speed = len_y / times
                    self.x += x_speed
                    self.y += y_speed
            # else:
            #     self.x = self.move_x
            #     self.y = self.move_y
        super().update()
        if s <= self.shootDistance:
            if time_count % self.attackPreTime == 0:
                self.attack()

    def display(self):
        # screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))


# 龙
class Dragon(Enemy):
    def __init__(self):
        super().__init__()
        self.width = 167
        self.height = 158
        self.speed = 2  # 龙的速度
        self.life = 70  # 龙的生命值
        self.shootDistance = 350
        self.attackPreTime = 100
        self.y = random.randint(0, 5) * (LAND_HEIGHT / 5) + self.height / 2
        self.x = random.randint(0, 1) * SCREEN_WIDTH  # 左右随机出现怪物

        self.imgs_left = []
        self.imgs_left.append(pygame.image.load("source/怪物/龙/小龙/蓝龙/蓝1.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙/小龙/蓝龙/蓝2.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙/小龙/蓝龙/蓝3.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙/小龙/蓝龙/蓝4.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙/小龙/蓝龙/蓝5.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙/小龙/蓝龙/蓝6.png"))

        self.imgs_right = []
        self.imgs_right.append(pygame.image.load("source/怪物/龙/小龙/蓝龙镜像/蓝1反.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙/小龙/蓝龙镜像/蓝2反.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙/小龙/蓝龙镜像/蓝3反.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙/小龙/蓝龙镜像/蓝4反.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙/小龙/蓝龙镜像/蓝5反.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙/小龙/蓝龙镜像/蓝6反.png"))
        self.index = 0
        self.count = 0
        self.img = self.imgs_left[0]

        self.move_x = -1
        self.move_y = -1

        self.need_move = True

    def update(self):
        self.count += 1
        # if x<self.x:#敌人坐标>玩家坐标时，播放向左走图片
        # if mouse_x - self.x < 0:
        if self.x > player.x:
            self.img = self.imgs_left[self.index]
        # elif mouse_x - self.x >= 0:
        elif self.x < player.x:
            self.img = self.imgs_right[self.index]
        if self.count % 5 == 0:
            self.count = 0
            self.index += 1
        if self.index >= len(self.imgs_left):
            self.index = 0

        # if self.need_move:
        if True:
            # len_x = self.move_x - self.x
            # len_y = self.move_y - self.y
            len_x = player.x - self.x
            len_y = player.y - self.y
            s = math.sqrt(len_x ** 2 + len_y ** 2)
            times = int(s / self.speed)
            if s >= self.shootDistance:
                if times >= 1:
                    x_speed = len_x / times
                    y_speed = len_y / times
                    self.x += x_speed
                    self.y += y_speed
            super().update()
            if s <= self.shootDistance:
                if time_count % self.attackPreTime == 0:
                    self.attack_4()

    def display(self):
        # screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))

    # def attack(self):
    #     preTime = 20
    #     count = 0  # 计时器
    #     count += 1
    #     if count >= preTime:  # 攻击准备时间到
    #         if self.s <= self.shootDistance:
    #             pass
    # super().update()
    # if s <= self.shootDistance:
    #     if time_count % self.attackPreTime == 0:
    #         self.attack()


# BOSS
class Boss(Enemy):
    def __init__(self):
        super().__init__()
        self.width = 190
        self.height = 180
        self.life = 1000  # boss的生命值
        self.speed = 1  # boss的速度
        self.shootDistance = 450
        self.attackPreTime = 50
        self.y = random.randint(0, 5) * (LAND_HEIGHT / 5) + self.height / 2
        self.x = random.randint(0, 1) * SCREEN_WIDTH  # 左右随机出现怪物

        self.imgs_left = []
        self.imgs_left.append(pygame.image.load("source/怪物/龙/大龙/黑龙/黑龙1.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙/大龙/黑龙/黑龙2.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙/大龙/黑龙/黑龙3.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙/大龙/黑龙/黑龙4.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙/大龙/黑龙/黑龙5.png"))
        self.imgs_left.append(pygame.image.load("source/怪物/龙/大龙/黑龙/黑龙6.png"))

        self.imgs_right = []
        self.imgs_right.append(pygame.image.load("source/怪物/龙/大龙/黑龙镜像/黑龙1反.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙/大龙/黑龙镜像/黑龙2反.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙/大龙/黑龙镜像/黑龙3反.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙/大龙/黑龙镜像/黑龙4反.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙/大龙/黑龙镜像/黑龙5反.png"))
        self.imgs_right.append(pygame.image.load("source/怪物/龙/大龙/黑龙镜像/黑龙6反.png"))
        self.index = 0
        self.count = 0
        self.img = self.imgs_left[0]

        self.move_x = -1
        self.move_y = -1

        self.need_move = True

    def update(self):
        self.count += 1
        # if x<self.x:#敌人坐标>玩家坐标时，播放向左走图片
        # if mouse_x - self.x < 0:
        if self.x > player.x:
            self.img = self.imgs_left[self.index]
        # elif mouse_x - self.x >= 0:
        elif self.x < player.x:
            self.img = self.imgs_right[self.index]
        if self.count % 5 == 0:
            self.count = 0
            self.index += 1
        if self.index >= len(self.imgs_left):
            self.index = 0

        # if self.need_move:
        if True:
            # len_x = self.move_x - self.x
            # len_y = self.move_y - self.y
            len_x = player.x - self.x
            len_y = player.y - self.y
            s = math.sqrt(len_x ** 2 + len_y ** 2)
            times = int(s / self.speed)
            if s >= self.shootDistance:
                if times >= 1:
                    x_speed = len_x / times
                    y_speed = len_y / times
                    self.x += x_speed
                    self.y += y_speed
            super().update()
            if s <= self.shootDistance:
                if time_count % self.attackPreTime == 0:

                    # boss三种攻击方式
                    r = random.randint(1, 3)
                    if r == 1:
                        self.attack_3()
                    if r == 2:
                        self.attack_4()
                    elif r == 3:
                        self.attack_5()

    def display(self):
        # screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))

        # def attack(self):
        preTime = 20
        # count = 0  # 计时器
        # count += 1
        # if count >= preTime:  # 攻击准备时间到
        #     if self.s <= self.shootDistance:
        #         pass


# ========================大更新方法=================================
def update():
    global time_count
    time_count += 1
    if time_count == 100000:
        time_count = 0
    # 更新玩家
    player.update(press_keys)  # ==================================出問題
    # sk.update()#单个骷髅兵测试
    playerbullet_crash_enemy()
    enemybullet_crash_player()
    for player_b in player_bullets:
        if not player_b.is_alive:  # 判断子弹是否存活
            player_bullets.remove(player_b)  # 移除子弹
        else:
            player_b.update()
    for enemy_b in enemy_bullets:
        if not enemy_b.is_alive:  # 判断子弹是否存活
            enemy_bullets.remove(enemy_b)  # 移除子弹
        else:
            enemy_b.update()
    # 敌人死亡，消失
    for enemy in enemies:
        if not enemy.is_alive:
            enemies.remove(enemy)
        else:
            enemy.update()
    # ================创建敌人===================
    create_skeleton()  # 骷髅创建
    create_unicorn()  # 麒麟创建
    create_dragon()  # 龙创建
    create_boss()  # boss创建
    # # 更新麒麟
    # for unicorn in unicorns:
    #     if not unicorn.is_alive:
    #         unicorns.remove(unicorn)
    #     else:
    #         unicorn.update()
    # create_unicorn()


# =======================================大显示方法======================
def display():
    if start_Flag:
        background.display()  # 显示背景
        gameTime.display()
        # 显示玩家子弹
        for player_b in player_bullets:
            player_b.display()
        for b in enemy_bullets:
            b.display()
        # sk.display()
        # 显示骷髅兵
        for enemy in enemies:
            enemy.display()
        # 显示玩家

        player.display()
        # print("----1------")
        # for unicorn in unicorns:
        #     unicorn.display()
        #     print("----2------")
    if not start_Flag:
        # start_img = pygame.image.load("source/场景/开始界面.png")
        start_img = pygame.image.load('source/场景/刀塔传奇地图原画-bbg 春天龙骨(bbg_spring_d_爱给网_aigei_com.jpg')




        screen.blit(start_img, (0, 0))


# 处理用户事件
def eventControl():
    for event in pygame.event.get():
        if event.type == locals.QUIT:
            exit()
        if event.type == locals.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()  # 获取鼠标的位置
            global mouse_x, mouse_y
            mouse_x = x
            mouse_y = y
            player.move(x, y)  # player向指定坐标移动
        if event.type == locals.MOUSEBUTTONDOWN:
            pressed_array = pygame.mouse.get_pressed()
            left, wheel, right = pressed_array
            if left == 1:  # 点击左键
                global anxiety_count
                anxiety_count += 1
                # 加载子弹音效
                sound = pygame.mixer.Sound("source/子弹音效/02.wav")
                sound.play()
                # player.attack()
                global press_mouse_x, press_mouse_y
                press_mouse_x, press_mouse_y = pygame.mouse.get_pos()
                player.attack()
                global start_Flag,timesa
                if not start_Flag:
                    time = 0
                    start_Flag = True
            global right_press_Flag
            if anxiety_count >= anxiety_need:
                if right == 1:
                    player.attack_2()
                    anxiety_count -= 15
            #     right_press_Flag=True
            # elif right==0:
            #     right_press_Flag=False

            # global CD_count
            # CD_count += 1


def create_player():
    player = Player()
    players.append(player)


# 创建骷髅兵方法
def create_skeleton():
    global time_count, enemyRefresh_time
    # 随机生成骷髅兵
    # enemyRefresh_time = 200
    if time_count % enemyRefresh_time == 0:
        # enemyRefresh_time = random.randint(10, 15) * 10  # 重新设置一个随机的刷新时间
        enemyRefresh_time = random.randint(10, 15) * 6  # 重新设置一个随机的刷新时间
        # enemyRefresh_time = 20
        skeleton = Skeleton()  # 创建一个骷髅兵
        enemies.append(skeleton)  # 让骷髅兵加入骷髅群列表


# 创建麒麟方法
def create_unicorn():
    global time_count, enemyRefresh_time
    # 随机生成麒麟

    if time_count % enemyRefresh_time == 0:
        enemyRefresh_time = random.randint(10, 21) * 10  # 重新设置一个随机的刷新时间
        # enemyRefresh_time = 20
        unicorn = Unicorn()  # 创建一个麒麟
        enemies.append(unicorn)  # 让麒麟加入敌人列表


# 创建龙方法
def create_dragon():
    # global time_count, enemyRefresh_time_2

    enemyRefresh_time = 500
    # enemyRefresh_time = 100  # 龙的刷新时间
    if time_count % enemyRefresh_time == 0:
        # enemyRefresh_time = random.randint(3, 15) * 10  # 重新设置一个随机的刷新时间
        # enemyRefresh_time = 20
        dragon = Dragon()  # 创建一个龙
        enemies.append(dragon)  # 让龙加入enemys列表


# 创建BOSS方法
def create_boss():
    # global time_count, enemyRefresh_time_2
    # 随机生成BOSS
    # enemyRefresh_time = 200
    # enemyRefresh_time = 2200  # BOSS 的刷新时间
    enemyRefresh_time = 1500  # BOSS 的刷新时间
    if time_count % enemyRefresh_time == 0:
        boss = Boss()  # 创建一个BOSS
        enemies.append(boss)  # 让BOSS加入enemies列表
        # 加载龙吼音效
        sound = pygame.mixer.Sound("source/角色音效/boss吼叫音效/吼声05.wav")
        sound.play()
        a.stop()
        s = pygame.mixer.Sound("source/背景音乐/无限火力/01.wav")  # boss出场特殊bgm
        s.play()


# 玩家子弹碰撞敌人方法
def playerbullet_crash_enemy():
    # 玩家子弹和敌机碰撞的逻辑处理
    for bullet in player_bullets:
        for enemy in enemies:
            if bullet.isCrash(enemy) and enemy.life > 0:
                bullet.is_alive = False
                enemy.life -= 10 * bullet.atk


# 敌人子弹碰撞玩家方法
def enemybullet_crash_player():
    for bullet in enemy_bullets:
        if bullet.isCrash(player) and player.life > 0:
            bullet.is_alive = False
            player.life -= 10 * bullet.atk


# 初始化方法
def init():
    global screen, background, player, gameTime
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = Background()
    gameTime = GameTime()
    player = Player()
    pygame.font.init()
    # gameTime=GameTime()#+++++++++++++
    # sk = Skeleton()  # 测试骷髅兵
    # create_player()
    # create_skeleton()
    # create_unicorn()


# 主函数
def main():
    global time
    init()
    while True:
        eventControl()
        # 捕获按键
        global press_keys
        press_keys = pygame.key.get_pressed()
        if not game_over:
            update()
            display()
        else:
            over = pygame.image.load \
                ('source/场景/结束界面.png')
            screen.blit(over, (0, 0))
            # 显示存活时间======
            fontObj = pygame.font.Font(None, 80)  # 通过字体文件获得字体对象
            textSurfaceObj = fontObj.render("Rank:" + str(player.rank) + " " + "Alive time:" + str(finalTime),
                                            True, (0, 0, 0), (255, 0, 0))  # 配置要显示的文字
            textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
            # textRectObj.center = (self.posx, self.posy)  # 设置显示对象的坐标
            textRectObj.center = (SCREEN_WIDTH - 512, 100)  # 设置显示对象的坐标
            screen.blit(textSurfaceObj, textRectObj)  # 绘制字
        # 每（1000/FPS）ms更新一次，即一秒钟更新FPS次
        time += clock.tick(FPS)
        pygame.display.update()
        # 检查音乐流播放，有返回True，没有返回False
        # 如果没有音乐流则选择播放
        # if pygame.mixer.music.get_busy() == False:  # 背景音乐程序a
        # pygame.mixer.music.play()  # 背景音乐程序


# 各种参数
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 615
LAND_HEIGHT = 400
SEA_HEIGHT = 200
FPS = 50
RECOVERY_CD = 100
LVUP_NEED_TIME = 2200
anxiety_count = 0
anxiety_need = 15
CD_count = 0
clock = pygame.time.Clock()
players = []
player_bullets = []
enemy_bullets = []
enemies = []
time_count = 0
game_over = False
start_Flag = False
right_press_Flag = False
screen = None
enemyRefresh_time = random.randint(3, 15) * 20
gameTime = None
time = 0
finalTime = None

if __name__ == '__main__':
    main()
