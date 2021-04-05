import pygame
from Modules.spriteSheet import SpriteSheet
from Enemies.spike import Spike

class Player:

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.delay = 10  # Animation
        self.currDelay = 0
        self.scale = (32,32)
        self.ecs = (-20,-12)
        self.eco = (10,0)
        self.game = None

        # Itens and Status
        self.keys = 0
        self.coins = 0
        self.health = 2
        self.maxHealth = 2
        self.lives = 3
        self.hurtTimer = 0
        self.hurtMaxTimer = 180

        # Horizontal Movement
        self.speed = 0
        self.maxSpeed = 5
        self.acc = 0.4

        # Vertical Movement
        self.maxG = 20
        self.maxGWater = 14
        self.currG = 0
        self.gAcc = 0.5
        self.gAccWater = 0.3
        self.accY = 0.0
        self.vineSpeed = 3
        self.isOnGround = False
        self.isOnVine = False
        self.isOnPlatform = False
        self.currentPlatform = None
        self.flipFlop = False

        self.jumpVel = 0
        self.jumpMax = 11

        # Player Skils
        self.canDoubleJump = False
        self.hasDoubleJumped = False
        self.isOnWater = False
        
        # Player Weapon
        self.usingWeapon = False
        self.hasDoneUsingWeapon = False
        self.weaponTime = 15
        self.weaponMaxTime = 15
        self.weapon = 'whip'
        
        # Collision Stuff
        self.last_y = y
        self.gs = 0

        # Sprites
        self.state = "IDLE_RIGHT"
        self.pastState = "RUN_RIGHT"
        self.orientation = "RIGHT"

        self.idle_state = 0
        self.idle_length = 6
        self.player_idle = SpriteSheet(pygame.image.load("./Assets/Player/player_idle.png"))
        self.idle = [self.player_idle.getimage(32*x, 0, 32, 32) for x in range(self.idle_length)]

        for x in range(len(self.idle)):
            self.idle[x] = pygame.transform.scale(self.idle[x], self.scale)

        self.run_state = 0
        self.run_length = 6
        self.player_run = SpriteSheet(pygame.image.load("./Assets/Player/player_run.png"))
        self.run = [self.player_run.getimage(32 * x, 0, 32, 32) for x in range(self.run_length)]

        for x in range(len(self.run)):
            self.run[x] = pygame.transform.scale(self.run[x], self.scale)

        self.player_jump = pygame.transform.scale(pygame.image.load("./Assets/Player/player_jump.png"), self.scale)
        self.player_fall = pygame.transform.scale(pygame.image.load("./Assets/Player/player_fall.png"), self.scale)

    def draw(self, display,camera):

        if not self.usingWeapon:
            if self.hurtTimer != 0:
                if self.hurtTimer % 5 == 0: self.flipFlop = not self.flipFlop

            if self.hurtTimer == 0 or (self.hurtTimer > 0 and self.flipFlop):
                if not self.isOnGround and self.jumpVel > self.currG:
                    if self.pastState == "RUN_RIGHT":
                        display.blit(self.player_jump, (self.x+camera.x, self.y+camera.y))
                    else:
                        display.blit(pygame.transform.flip(self.player_jump, 1, 0), (self.x+camera.x, self.y+camera.y))
                elif not self.isOnGround:
                    if self.pastState == "RUN_RIGHT":
                        display.blit(self.player_fall, (self.x+camera.x, self.y+camera.y))
                    else:
                        display.blit(pygame.transform.flip(self.player_fall, 1, 0), (self.x+camera.x, self.y+camera.y))
                elif self.state == "IDLE_RIGHT":
                    display.blit(self.idle[self.idle_state % self.idle_length], (self.x+camera.x, self.y+camera.y))
                    if self.currDelay == self.delay:
                        self.idle_state += 1
                        self.currDelay = 0
                    else:
                        self.currDelay += 1
                elif self.state == "IDLE_LEFT":
                    display.blit(pygame.transform.flip(self.idle[self.idle_state % self.idle_length], 1, 0), (self.x+camera.x, self.y+camera.y))
                    if self.currDelay == self.delay:
                        self.idle_state += 1
                        self.currDelay = 0
                    else:
                        self.currDelay += 1
                elif self.state == "RUN_RIGHT":
                    display.blit(self.run[self.run_state % self.run_length], (self.x+camera.x, self.y+camera.y))
                    if self.currDelay == self.delay:
                        self.run_state += 1
                        self.currDelay = 0
                    else:
                        self.currDelay += 1
                elif self.state == "RUN_LEFT":
                    display.blit(pygame.transform.flip(self.run[self.run_state % self.run_length], 1, 0), (self.x+camera.x, self.y+camera.y))
                    if self.currDelay == self.delay:
                        self.run_state += 1
                        self.currDelay = 0
                    else:
                        self.currDelay += 1

        # Collision Stuff
        self.last_y = self.y
        if self.gs != 0:
            self.isOnGround = True
            self.hasDoubleJumped = False
        else:
            self.isOnGround = False
        self.gs = 0

    def update(self, keys):

        if self.weapon != None and not self.usingWeapon:
            # Horizontal Movement
            stall = self.x
            if keys[pygame.K_d] and keys[pygame.K_a]:
                self.speed = 0
            else:
                if keys[pygame.K_d]:
                    if self.speed <= self.maxSpeed:
                        self.speed += self.acc
                    self.x += self.speed
                    self.state = "RUN_RIGHT"
                    self.pastState = "RUN_RIGHT"
                    self.orientation = "RIGHT"
                elif keys[pygame.K_a]:
                    if self.speed <= self.maxSpeed:
                        self.speed += self.acc
                    self.x -= self.speed
                    self.state = "RUN_LEFT"
                    self.pastState = "RUN_LEFT"
                    self.orientation = "LEFT"
                else:
                    if self.pastState == "RUN_RIGHT" or self.pastState == "JUMP_RIGHT":
                        self.state = "IDLE_RIGHT"
                    elif self.pastState == "RUN_LEFT" or self.pastState == "JUMP_LEFT":
                        self.state = "IDLE_LEFT"
            if stall == self.x:
                self.speed = 0

            if not self.isOnVine:
                # Jumping
                if self.isOnGround and (keys[pygame.K_SPACE] or keys[pygame.K_w]):
                    self.jumpVel = self.jumpMax
                    self.isOnGround = False
                if self.isOnGround:
                    self.jumpVel = 0
                if not self.isOnGround and self.jumpVel > self.currG:
                    self.state = "JUMP"
                self.y -= self.jumpVel

                if self.canDoubleJump and not self.hasDoubleJumped and self.accY < 0 and (keys[pygame.K_SPACE] or keys[pygame.K_w]):
                    self.currG = 0
                    self.hasDoubleJumped = True

            else:
                # Vine Movement
                if keys[pygame.K_w]:
                    self.y -= self.vineSpeed
                elif keys[pygame.K_s]:
                    self.y += self.vineSpeed

            # Gravity, only apply if
            # player is not on vine
            if not self.isOnVine:
                if not self.isOnGround:
                    if self.isOnWater:
                        if self.currG <= self.maxGWater:
                            self.currG += self.gAccWater
                        self.y += self.currG
                    else:
                        if self.currG <= self.maxG:
                            self.currG += self.gAcc
                        self.y += self.currG         
                else:
                    self.currG = 0
            
            # Reset Back isOnVine
            self.isOnVine = False
            # Reset is on Water
            self.isOnWater = False

        # Weapon
        if (keys[pygame.K_q]) and self.weaponTime == 0:
            self.weaponTime = self.weaponMaxTime
            self.usingWeapon = True
            self.useWeapon()
            self.hasDoneUsingWeapon = True        

        self.accY = self.last_y-self.y
        
        self.hurtTimer -= 1
        self.weaponTime -= 1
        if self.hurtTimer <= 0 : self.hurtTimer = 0
        if self.weaponTime <= 0 :
            self.usingWeapon = False
            if self.hasDoneUsingWeapon:
                self.doneWeapon()
            self.hasDoneUsingWeapon = False
            self.weaponTime = 0
        
    def hurt(self, enemy,game):
        if self.hurtTimer == 0:
            self.health -= enemy.hurtAmount
            self.game.audioSystem.playSFX('player_hurt')
            if self.health == 0 and self.lives > 0:
                self.health = self.maxHealth
                self.lives -= 1
                game.saveSystem.loadCheckpoint(game)

            if self.lives == 0 and self.health == 0:
                game.saveSystem.loadGame(game)

            self.hurtTimer = self.hurtMaxTimer
        if self.health < 0 : self.health = 0

    def enemyContact(self, enemy, game):
        if self.accY < 0:
            enemy.hurt()
        else:
            if hasattr(enemy,'state') and enemy.state != 'KILL':
                self.hurt(enemy,game)
            elif isinstance(enemy, Spike):
                self.hurt(enemy,game)

    def useWeapon(self):
        if self.game != None and self.weapon != None:
            print('Use Weapon')
                    
    def doneWeapon(self):
        if self.game != None and self.weapon != None:
            print('Done use weapon')
