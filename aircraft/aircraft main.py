import pygame,random
pygame.init()
screen_x = 1300
screen_y = 1000
screen = pygame.display.set_mode((screen_x,screen_y))

# 从硬盘导入图片
airforce_surface = pygame.image.load("C:/Users/zzs/OneDrive/zzs/Python zzs/Module/pygame/aircraft/airforce.png").convert_alpha()
enemy_surface = pygame.image.load("C:/Users/zzs/OneDrive/zzs/Python zzs/Module/pygame/aircraft/enemy.png").convert_alpha()
bullet_surface = pygame.image.load("C:/Users/zzs/OneDrive/zzs/Python zzs/Module/pygame/aircraft/bullet.png").convert_alpha()

# 获取图片的尺寸
airforce_size = airforce_surface.get_size()
enemy_size = enemy_surface.get_size()
bullet_size = bullet_surface.get_size()

# 把图片大小变成适合显示的大小，返回surface类型
airforce = pygame.transform.scale(airforce_surface, (int(airforce_size[0]/7), int(airforce_size[1]/7)))
enemy = pygame.transform.scale(enemy_surface, (int(enemy_size[0]/5), int(enemy_size[1]/5)))
bullet = pygame.transform.scale(bullet_surface, (int(bullet_size[0]/40), int(bullet_size[1]/20)))

# 图片旋转以符合游戏要求
enemy = pygame.transform.rotate(enemy,90) 
bullet = pygame.transform.rotate(bullet,90)

class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = airforce
        self.rect = self.image.get_rect()
        self.rect.move_ip(screen_x/2 - self.rect.width/2, screen_y - self.rect.height)

class EnemySprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy
        self.rect = self.image.get_rect()
        self.rect.move_ip(random.randint(0, screen_x - self.rect.width),random.randint(0, 50))

class EnemyBulletSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((5,10))
        self.image.fill(pygame.Color("blue"))
        self.rect = self.image.get_rect()
        self.rect.move_ip(random.randint(0, screen_x - self.rect.width),random.randint(0, 50))

class BulletSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bullet
        self.rect = self.image.get_rect()

airforce_sprite = MySprite()
enemy_sprites = []
enemy_number = 5
enemy_bullet_number = 5

my_sprites_group = pygame.sprite.Group()
my_sprites_group.add(airforce_sprite)
enemy_sprites_group = pygame.sprite.Group()
enemy_bullet_sprite_group = pygame.sprite.Group()
for i in range(len(enemy_sprites)):
    enemy_sprites_group.add(enemy_sprites[i])

myfont = pygame.font.Font("./Module/pygame/aircraft/msyhl.ttc",20)
white = 255,255,255
black_bg = 0,0,0
destroyed_enemy_number = 0

airforce_number = 5
shoot_new_bullet = True
wait_time = 0

bullet_sound = pygame.mixer.Sound("C:/Users/zzs/OneDrive/zzs/Python zzs/Module/pygame/aircraft/sound/bullet.wav")
bullet_sound.set_volume(0.02)
game_over_sound = pygame.mixer.Sound("C:/Users/zzs/OneDrive/zzs/Python zzs/Module/pygame/aircraft/sound/Game Over.wav")
game_over_sound.set_volume(0.05)
short_bomb_sound = pygame.mixer.Sound("C:/Users/zzs/OneDrive/zzs/Python zzs/Module/pygame/aircraft/sound/short_bomb.wav")
short_bomb_sound.set_volume(0.05)
start_sound = pygame.mixer.Sound("C:/Users/zzs/OneDrive/zzs/Python zzs/Module/pygame/aircraft/sound/start.wav")
start_sound.set_volume(0.2)


bullet_time = 20
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start_sound.play(fade_ms = 0)
                pygame.time.wait(300)
                running = False
    screen.fill(pygame.Color("black"))
    start_font = pygame.font.Font("./Module/pygame/aircraft/msyhl.ttc",100)
    start_image = start_font.render("开始游戏", True, white)
    screen.blit(start_image, (screen_x/2 - 200, screen_y/3 - 50))

    start_font = pygame.font.Font("./Module/pygame/aircraft/msyhl.ttc",50)
    start_image = start_font.render("上下左右:↑↓←→ 或 WSAD 控制飞机", True, white)
    screen.blit(start_image, (screen_x/2 - 380, screen_y/2))
    start_font = pygame.font.Font("./Module/pygame/aircraft/msyhl.ttc",50)
    start_image = start_font.render("按enter开始", True, white)
    screen.blit(start_image, (screen_x/2 - 130, screen_y/2 + 50))
    name_font = pygame.font.Font("./Module/pygame/aircraft/msyhl.ttc",30)
    name_image = name_font.render("by zhisuizhou", True, white)
    screen.blit(name_image, (screen_x/2 - 100, screen_y - 50))

    pygame.display.update()



enemy_speed = 1
level_difficult = 0
a = 0
running = True
while running:
    screen.fill((0, 0, 0))
    airforce_x = 0
    airforce_y = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         bullet_sprite = BulletSprite()
        #         my_sprites_group.add(bullet_sprite)
        #         bullet_sprite.rect.left = airforce_sprite.rect.left + airforce_sprite.rect.width/2 - bullet_sprite.rect.width/2 + 2
        #         bullet_sprite.rect.top = airforce_sprite.rect.top - bullet_sprite.rect.height
        
        # 键盘控制图片运动 KEYDOWN 是键盘按下的事件
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        airforce_x -= 2
        if airforce_sprite.rect.x < 2:
            airforce_x = 0
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        airforce_x += 2
        if airforce_sprite.rect.x > screen_x - airforce_sprite.rect.width - 2:
            airforce_x = 0
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        airforce_y -= 2
        if airforce_sprite.rect.y < 2:
            airforce_y = 0
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        airforce_y += 2
        if airforce_sprite.rect.y > screen_y - airforce_sprite.rect.height - 2:
            airforce_y = 0
    
    airforce_sprite.rect.move_ip(airforce_x,airforce_y)
    enemy_sprites_group.draw(screen)
    enemy_bullet_sprite_group.draw(screen)
    for i in enemy_sprites_group.sprites():
        i.rect.move_ip(0, enemy_speed)
    for i in enemy_bullet_sprite_group.sprites():
        i.rect.move_ip(0, 3)

    enemy_font = myfont.render("击落敌机:" + str(destroyed_enemy_number), True, white,black_bg)
    screen.blit(enemy_font, (0, 0))
    airforce_font = myfont.render("剩余生命数:" + str(airforce_number), True, white,black_bg)
    screen.blit(airforce_font, (0, 25))
    level = int(destroyed_enemy_number/20) + 1
    if level_difficult < 16:
        level_difficult = level
    level_font = myfont.render("等级:" + str(level), True, white,black_bg)
    screen.blit(level_font, (0, 50))

    if shoot_new_bullet == True:
        if a < 1:
            a = int(level_difficult/10)
        bullet_sound.play(maxtime = 140,fade_ms = 0)
        for i in range(-a,a+1):
            bullet_sprite = BulletSprite()
            my_sprites_group.add(bullet_sprite)
            bullet_sprite.rect.left = airforce_sprite.rect.left + airforce_sprite.rect.width/2 - bullet_sprite.rect.width/2 + 2 + i * 10
            bullet_sprite.rect.top = airforce_sprite.rect.top - bullet_sprite.rect.height
        shoot_new_bullet = False


    wait_time += 1
    if bullet_time > 11:
        bullet_time -= enemy_number + level_difficult - 1 - 5
    if wait_time % bullet_time == 0:
        shoot_new_bullet = True


    # 绘制background,airforce，enemy，mybullet
    my_sprites_group.draw(screen)
    bullet_sprites = my_sprites_group.sprites()
    for i in bullet_sprites:
        if i.image == airforce:
            pass
        else:
            i.rect.y -= level_difficult * 2 + 1
    


    enemy_number_before = len(enemy_sprites_group)
    pygame.sprite.groupcollide(my_sprites_group, enemy_sprites_group, True, True)  # kill both
    kill_air = pygame.sprite.spritecollide(airforce_sprite, enemy_bullet_sprite_group, True)  # kill
    if len(kill_air) > 0:
        airforce_sprite.kill()



    enemy_number_after = len(enemy_sprites_group)
    destroyed_enemy_number += enemy_number_before - enemy_number_after

    if enemy_number_after < enemy_number_before:
        short_bomb_sound.play(fade_ms = 0)

    airforce_bullet_sprites = my_sprites_group.sprites()

    airforce_existed = False
    for i in airforce_bullet_sprites:
        if i.image == airforce:
            airforce_existed = True
    if airforce_existed == False:
        airforce_number -= 1
        airforce_sprite = MySprite()
        my_sprites_group.add(airforce_sprite)
    
    for i in enemy_sprites_group.sprites():
        if i.rect.y > screen_y - i.rect.height:
            enemy_sprites_group.remove(i)
    for i in enemy_bullet_sprite_group.sprites():
        if i.rect.y > screen_y - i.rect.height:
            enemy_bullet_sprite_group.remove(i)
    for i in my_sprites_group.sprites():
        if i.rect.y < 0:
            my_sprites_group.remove(i)

    # 刷新
    if len (enemy_sprites_group) != (enemy_number + level_difficult - 1):
        for i in range((enemy_number + level_difficult -1) - len(enemy_sprites_group)):
            enemy_sprite = EnemySprite()
            enemy_sprites_group.add(enemy_sprite)
    if len(enemy_bullet_sprite_group) != (enemy_bullet_number + level_difficult - 1):
        for i in range(((enemy_bullet_number + level_difficult - 1) - len(enemy_bullet_sprite_group))):
                enemy_bullet_sprite = EnemyBulletSprite()
                enemy_bullet_sprite_group.add(enemy_bullet_sprite)

    pygame.display.update()
    pygame.time.wait(5)
    
    running_1 = True
    if airforce_number == 0:
        game_over_sound.play()
        while running_1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    running_1 = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running_1 = False
                        my_sprites_group.empty()
                        enemy_sprites_group.empty()
                        enemy_bullet_sprite_group.empty()
                        airforce_number = 5 + 1     #会被减一条，所以要加
                        destroyed_enemy_number = 0
                        enemy_speed = 1
                        bullet_time = 20
                        a = 0
                        running = True
            screen.fill(pygame.Color("black"))
            over_font = pygame.font.Font("./Module/pygame/aircraft/msyhl.ttc",100)
            over_image = over_font.render("Game Over", True, (255,255,255))
            screen.blit(over_image, (screen_x/2 - 250, screen_y/3 - 50))

            over_font1 = pygame.font.Font("./Module/pygame/aircraft/msyhl.ttc",50)
            over_image1 = over_font1.render("按space重来", True, (255,255,255))
            screen.blit(over_image1, (screen_x/2 - 150, screen_y/2))

            over_font1 = pygame.font.Font("./Module/pygame/aircraft/msyhl.ttc",50)
            over_image1 = over_font1.render("击落敌机:" + str(destroyed_enemy_number), True, (255,255,255))
            screen.blit(over_image1, (screen_x/2 - 150, screen_y/2 + 100))

            pygame.display.update()
    

pygame.quit()