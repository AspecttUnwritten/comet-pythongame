import sys
from logging import log
from turtle import up

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    print(f"Screen width: {SCREEN_WIDTH}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0

    # new groups
    asteroids = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, drawable, updatable)

    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y)
    field = AsteroidField()

    while True:
        log_state()

        updatable.update(dt)
        for a in asteroids:
            if player.collides_with(a) is True:
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)

        for a in asteroids:
            for b in shots:
                if a.collides_with(b):
                    log_event("asteroid_shot")
                    a.split()
                    b.kill()
        pygame.display.flip()

        dt = clock.tick(60) / 1000
        # print(dt)


if __name__ == "__main__":
    main()
