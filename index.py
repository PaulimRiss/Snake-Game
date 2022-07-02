import random
import pygame as pg
from sys import exit

pg.init()

bg_music = pg.mixer.music.load("assets/audio/bgcat.mp3")
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.1)
collision_sound = pg.mixer.Sound("assets/audio/smw_coin.wav")

screen = [640, 480]

screen_set = pg.display.set_mode((screen[0], screen[1]))
pg.display.set_caption("First Game Ever")
clock = pg.time.Clock()
font = pg.font.SysFont("Arial", 30, True)

snake_size = [20, 20]
snake_pos = [int(screen[0] / 2 - snake_size[0]), int(screen[1] / 2 - snake_size[1])]
velocity = 10
direction = [1, 0]
score = 0
trail = []

apple_pos = [random.randint(200, 200), random.randint(200, 200)]
apple_size = [20, 20]


def drawSnake(trail):
    for i in range(len(trail)):
        pg.draw.rect(
            screen_set,
            (0, 255, 0),
            (trail[i][0], trail[i][1], snake_size[0], snake_size[1]),
        )
    for i in range(len(trail)):
        if len(trail) > score + 1:
            trail.pop(0)

    return trail


def changeDirection(key):
    return (
        [0, -1] * (key == pg.K_UP and direction != [0, 1])
        + [0, 1] * (key == pg.K_DOWN and direction != [0, -1])
        + [-1, 0] * (key == pg.K_LEFT and direction != [1, 0])
        + [1, 0] * (key == pg.K_RIGHT and direction != [-1, 0])
        + direction
        * (
            key not in (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT)
            or key == pg.K_UP
            and direction == [0, 1]
            or key == pg.K_DOWN
            and direction == [0, -1]
            or key == pg.K_LEFT
            and direction == [1, 0]
            or key == pg.K_RIGHT
            and direction == [-1, 0]
        )
    )


while True:
    clock.tick(30)
    text = "score: " + str(score)
    rendered_text = font.render(text, True, (0, 0, 0))
    screen_set.fill((255, 255, 255))
    event_count = 0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN and not event_count:
            direction = changeDirection(event.key)
            event_count += 1

    snake_pos = [
        snake_pos[0] + direction[0] * velocity,
        snake_pos[1] + direction[1] * velocity,
    ]

    trail.append(snake_pos)
    drawSnake(trail)

    snake = pg.draw.rect(
        screen_set,
        (0, 200, 0),
        (snake_pos[0], snake_pos[1], snake_size[0], snake_size[1]),
    )
    apple = pg.draw.rect(
        screen_set,
        (255, 0, 0),
        (apple_pos[0], apple_pos[1], apple_size[0], apple_size[1]),
    )

    if snake.colliderect(apple):
        apple_pos = [
            random.randint(0, 640 - apple_size[0]),
            random.randrange(0, 480 - apple_size[1]),
        ]
        score += 1
        collision_sound.play()

    screen_set.blit(rendered_text, (10, 10))

    pg.display.update()
