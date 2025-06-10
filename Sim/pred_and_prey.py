########
# TODO #
#########################################################
#                                                       #
#   [ ] Generate the entities at the beginning          #
#   [ ] Add some sensory system to the entities         #
#   [ ] Revamp the energy system                        #
#                                                       #
#########################################################

###########
# Imports #
###########

import pygame
import random

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

#############
# Constants #
#############

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

ELEM_ENTD = 0
ELEM_PREY = 1
ELEM_PRED = 2

BACKGROUD_COLOR = 0x202020

RED_COLOR = 0xff0000
GREEN_COLOR = 0x00ff00
BLUE_COLOR = 0x0000ff

##################
# Initialization #
##################

# Init the pygame library
pygame.init()
# Set up the drawing window
window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
# Setup clock for frame rate
clock = pygame.time.Clock()
# Create custom event for adding prey
ADDPREY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPREY, 250)
# Create custom event for adding predators
ADDPRED = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPRED, 750)
# Create groups to hold sprites
preys = pygame.sprite.Group()
predators = pygame.sprite.Group()

#####################
# Geometry Function #
#####################

def eculid_distance(pointA, pointB):
    s = 0.0
    
    for i in range(len(pointA)):
        s += ((pointA[i] - pointB[i]) ** 2)
    
    return s ** 0.5

###########
# Classes #
###########

# Parent class to all the others
class Entity(pygame.sprite.Sprite):
    
    def __init__(self, position, radius, color):

        super().__init__()
        self.type = ELEM_ENTD
        self.hp = 0
        self.speed = 0
        self.direction = 0
        self.position = position
        self.radius = radius
        self.color = color

        self.collisionState = False

    def draw(self):

        pygame.draw.circle(window, self.color, self.position, self.radius)

    def updateDirection(self, entities):
        
        for entity in entities:
            if entity.position != self.position and self.checkCollision(entity):
                if self.collisionState == False:
                    self.collisionState = True
                    self.changeDirection(entity)
                    
                    # Check if we collided with a predator as a prey
                    if (entity.type == ELEM_PRED and self.type != entity.type):
                        self.hp -= 1

                    # Check if we collided with a prey as a predator
                    if (entity.type == ELEM_PREY and self.type != entity.type):
                        self.hp -= 1

                    break
                else:
                    break
        else:
            self.collisionState = False

    def changeDirection(self, entity):

        pX = self.position[0] - entity.position[0]
        pY = self.position[1] - entity.position[1]

        if abs(pX) >= abs(pY):
            self.direction = (pX/abs(pX), pY/abs(pX))
        else:
            self.direction = (pX/abs(pY), pY/abs(pY))

    def checkCollision(self, entity):
        if eculid_distance(entity.position, self.position) <= self.radius + entity.radius:
            return True
        
        return False

    def update(self, dt):

        pX = self.position[0] + self.direction[0] * self.speed * dt
        pY = self.position[1] + self.direction[1] * self.speed * dt

        self.position = (pX, pY)

        if self.position[0] <= 0 + self.radius and self.direction[0] < 0:
            self.direction = (self.direction[0] * -1, self.direction[1])
        elif self.position[0] >= SCREEN_WIDTH - self.radius and self.direction[0] > 0:
            self.direction = (self.direction[0] * -1, self.direction[1])            
        elif self.position[1] <= 0 + self.radius and self.direction[1] < 0:
            self.direction = (self.direction[0], self.direction[1] * -1)
        elif self.position[1] >= SCREEN_HEIGHT - self.radius and self.direction[1] > 0:
            self.direction = (self.direction[0], self.direction[1] * -1)
        
class Prey(Entity):
    
    def __init__(self, position, radius, color):
        super().__init__(position, radius, color)
        
        self.type = ELEM_PREY
        self.hp = random.randint(5, 15)
        self.speed = random.randint(3,6)
        self.direction = (random.randint(-1, 1), random.randint(-1, 1))
      
class Predator(Entity):
    
    def __init__(self, position, radius, color):
        super().__init__(position, radius, color)
        
        self.type = ELEM_PRED
        self.hp = random.randint(25, 50)
        self.speed = random.randint(4,8)
        self.direction = (random.randint(-1, 1), random.randint(-1, 1))

########
# Main #
########

def main():
    # Run until user quits
    running = True

    while running:
        # Delta time in seconds
        deltaTime = clock.tick(120) / 1000 * 60
        # print(deltaTime)
        
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:

                    running = False

                    print("Preys: " + str(len(preys)))
                    print("Predators: " + str(len(predators)))
            
            elif event.type == QUIT:
                
                running = False

                print("Preys: " + str(len(preys)))
                print("Predators: " + str(len(predators)))

            elif event.type == ADDPREY:
                pos = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
                radius = 10

                new_prey = Prey(pos, radius, BLUE_COLOR)
                preys.add(new_prey)

            elif event.type == ADDPRED:
                pos = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
                radius = 8
                
                new_predator = Predator(pos, radius, RED_COLOR)
                predators.add(new_predator)

        # Fill the screen with black
        window.fill((20, 20, 20))

        for prey in preys:
            prey.draw()
        for pred in predators:
            pred.draw()

        preys.update(deltaTime)
        predators.update(deltaTime)

        for prey in preys:
            prey.updateDirection(preys)
            prey.updateDirection(predators)

        for pred in predators:
            pred.updateDirection(predators)
            pred.updateDirection(preys)

        for prey in preys:
            if prey.hp == 0:
                preys.remove(prey)

        for pred in predators:
            if pred.hp == 0:
                predators.remove(pred)

        # Updates the display
        pygame.display.flip()

    pygame.quit()

if __name__  == "__main__":
    main()