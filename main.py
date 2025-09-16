import pygame as pg
import random
pg.init()
import asyncio


WIDTH = 800
HEIGHT = 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Kirby Star")
clock = pg.time.Clock()
font = pg.font.Font(None, 30)

mushrooms = []
mushroom_size = 75
mushroom_speed = 5


WHITE = (255, 255, 255)


player_size = 36
player_x = WIDTH // 2
player_y = HEIGHT - player_size
player_speed = 8
player_jump = False
player_vel_y = 0
jump_strength = 9
gravity = 0.1
lives = 5
score = 0


debris = []
debris_speed = 8
debris_size = 145


player_img = pg.image.load("./assets/images/kirby.png")
player_img = pg.transform.scale(player_img, (player_size, player_size))

debris_img = pg.image.load("./assets/images/King_dedede.png")
debris_img = pg.transform.scale(debris_img, (debris_size, debris_size))

bg_img = pg.image.load("./assets/images/Kirby_bg.jpg")
bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))

mushroom_img = pg.image.load("./assets/images/invincible_candy.webp")
mushroom_img = pg.transform.scale(mushroom_img, (mushroom_size, mushroom_size))

running = True

async def main():

    global running, player_x, player_y, player_jump, player_vel_y, lives, score

    while running:
        clock.tick(60)
        screen.blit(bg_img, (0, 0))


        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            player_x -= player_speed
        if keys[pg.K_RIGHT]:
            player_x += player_speed
        if keys[pg.K_UP] and not player_jump:
            player_jump = True
            player_vel_y = -jump_strength


        if player_jump:
            player_vel_y += gravity
            player_y += player_vel_y
            if player_y >= HEIGHT - player_size:
                player_y = HEIGHT - player_size
                player_jump = False
                player_vel_y = 0
            # screen.blit(player_img, (player_x, player_y))


        if random.random() < 0.03:
            x = random.randint(0, WIDTH - debris_size)
            debris.append([x, 0])

        for d in debris[:]:
            d[1] += debris_speed + score // 5
            screen.blit(debris_img, (d[0], d[1]))


            player_rect = pg.Rect(player_x, player_y, player_size, player_size)
            debris_rect = pg.Rect(d[0], d[1], debris_size, debris_size)
            if player_rect.colliderect(debris_rect):
                lives -= 1
                debris.remove(d)
                if lives <= 0:
                    running = False
            elif d[1] > HEIGHT:
                debris.remove(d)
                score += 1
            # screen.blit(player_img, (player_x, player_y))

        if random.random() < 0.02:
            x = random.randint(0, WIDTH - debris_size)
            mushrooms.append([x, 0])

        for m in mushrooms[:]:
            m[1] += mushroom_speed + score // 5
            screen.blit(mushroom_img, (m[0], m[1]))


            player_rect = pg.Rect(player_x, player_y, player_size, player_size)
            debris_rect = pg.Rect(m[0], m[1], mushroom_size, mushroom_size)
            if player_rect.colliderect(debris_rect):
                lives += 1
                mushrooms.remove(m)


        info = font.render(f"Score: {score}  Lives: {lives}", True, WHITE)
        screen.blit(info, (WIDTH - 200, HEIGHT - 40))
        screen.blit(player_img, (player_x, player_y))

        pg.display.flip()

        await asyncio.sleep(0)

asyncio.run(main())