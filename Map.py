import numpy as np
import pygame


class Map(object):
    """
    Define the map of the game

    The coordinate of the map are as following:

          x 0    1    2    3    4    5    6    7    8    9 (width)
        y
        0

        1

        2

        3

        4

        5

        6

        7

        8

        9
        (height)
    """

    def __init__(self, height = 60, width = 60):
        """
        By default, the map is 60*60
        """
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode((10*width, 10*height + 80))
        self.fruitMap = np.zeros((self.height, self.width), dtype=np.int64)
        self.time = 0


    def newFruit(self, snake_pos):
        """
        Add a fruit on the map
        """
        while 1:
            x = np.random.randint(self.width)
            y = np.random.randint(self.height)
            if [y, x] not in snake_pos:
                break

        self.fruitMap[y][x] += 1

    def render(self, env, snake, mode='Computer'):

        pyFont = pygame.font.SysFont('arial', 10)

        label = pyFont.render("You loose", 1, (255, 255, 0))

        if(mode == 'Computer'):
            if(not snake.isDead):
                self.screen.fill((0,0,0))

                for event in pygame.event.get():
                    if(event.type == pygame.QUIT):
                        pygame.quit()
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, 10*self.height, 10*self.width, 40))


                score = pyFont.render("Your score is {}".format(np.int(snake.points)), 2, (0, 0, 0))
                self.screen.blit(score, (2, 10*self.height+20))

                timeGame = pyFont.render("Time = {}".format(np.int(self.time)), 3, (255, 255, 0))
                self.screen.blit(timeGame, (2, 10*self.height + 60))

                for x in range(self.width):
                    for y in range(self.height):
                        if(self.fruitMap[y][x] >= 1):
                            pygame.draw.rect(self.screen, (230,210,0), pygame.Rect(10*x, 10*y, 10,10))
                        else:
                            pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(10*x, 10*y, 10,10))
                    for coord in snake.location:
                        pygame.draw.rect(self.screen, (110, 214, 54), pygame.Rect(10*coord[1], 10*coord[0], 10, 10))

                pygame.display.flip()
            else:
                self.screen.fill((0,0,0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        pygame.quit()

                self.screen.blit(label, (100,100))
                score = pyFont.render("Your score is {}".format(np.int(snake.points)), 2, (255, 255, 0))
                self.screen.blit(score, (100, 200))

                pygame.display.flip()
                pygame.time.wait(1000)



        elif(mode == 'Human'):
            score = pyFont.render("Your score is {}".format(np.int(snake.points)), 2, (255, 255, 0))

            while(not snake.isDead):
                self.screen.fill((0,0,0))
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, 10*self.height, 10*self.width, 40))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        snake.isDead = True
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            env.step(3)
                        if event.key == pygame.K_DOWN:
                            env.step(4)
                        if event.key == pygame.K_RIGHT:
                            env.step(2)
                        if event.key == pygame.K_LEFT:
                            env.step(1)

                for x in range(self.width):
                    for y in range(self.height):
                        if(self.fruitMap[y][x] >= 1):
                            pygame.draw.rect(self.screen, (230,210,0), pygame.Rect(10*x, 10*y, 10,10))
                        else:
                            pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(10*x, 10*y, 10,10))
                for coord in snake.location:
                    pygame.draw.rect(self.screen, (110, 214, 54), pygame.Rect(10*coord[1], 10*coord[0], 10, 10))
                score = pyFont.render("Your score is {}".format(np.int(snake.points)), 2, (0, 0, 0))
                self.screen.blit(score, (20, 10*self.height+20))
                env.step(0)

                pygame.display.flip()
                pygame.time.wait(100)

            done = False
            pygame.time.wait(100)
            while(not done):
                self.screen.fill((0,0,0))

                self.screen.blit(label, (100,100))

                self.screen.blit(score, (100, 200))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True

                pygame.display.flip()
                pygame.time.wait(1000)
            pygame.quit()
