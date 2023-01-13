# Tommyy Emo
# Finished on: January 23, 2019
# ICS3U1 - Mr. Van Rooyen

from pygame import *  #importing the needed packages
import os
import random

init()  # Initializing pygame

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d%d"%(300, 400)  #moving the window to the very top left of the screen

SIZE = 420, 700
screen = display.set_mode(SIZE)

# Basic colours used
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Reading the highscore file
myFile = open("highscore.dat", "r")
file = myFile.readline().split()

# Setting variables to the highscore, and high combo
highscore = int(file[0])
high_combo = int(file[1])

# loading tons of images.  Many names are self explanatory
# These images are used to draw the scene in the game
# Many of them were reversed to save space in the file - only 30 images are allowed at once with pygame
# In another time I would have used sprite sheets to overcome this, but it is too late now
standing_right = image.load("standing.png").convert_alpha()
standing_left = transform.flip(standing_right, True, False)

fall_right = image.load("fall.png").convert_alpha()
fall_left = transform.flip(fall_right, True, False)

jump_right = image.load("jumping_right.png").convert_alpha()
jump_left = transform.flip(jump_right, True, False)
jump_still_right = image.load("jumping_still.png").convert_alpha()
jump_still_left = transform.flip(jump_still_right, True, False)

shot_right = image.load("shot.png").convert_alpha()
shot_left = transform.flip(shot_right, True, False)

cooling_right = image.load("cooling.png").convert_alpha()
cooling_left = transform.flip(cooling_right, True, False)

run_right = image.load("move_right.png").convert_alpha()
run_left = transform.flip(run_right, True, False)

wall_img = image.load("wall.png").convert_alpha()

rust1 = image.load("rust1.png")
rust2 = image.load("rust2.png")
rust3 = image.load("rust3.png")

bullet = image.load("bullet.png").convert_alpha()

platfor = image.load("platform.png").convert_alpha()

battery_left = image.load("battery_left.png").convert_alpha()
battery_right = transform.flip(battery_left, True, False)

waiter_move_right = image.load("waiter_move_right.png").convert_alpha()
waiter_move_left = transform.flip(waiter_move_right, True, False)

waiter_sleep = image.load("waiter_sleep.png").convert_alpha()

garbage = image.load("garbage.png").convert_alpha()

floater_eyes = image.load("floater_eyes.png").convert_alpha()

floater_spam = image.load("floater_spam.png").convert_alpha()

one = image.load("one.png").convert_alpha()
zero = image.load("zero.png").convert_alpha()

hurt_right = image.load("hurt_right.png").convert_alpha()
hurt_left = transform.flip(hurt_right, True, False)

combo = image.load("combo.png").convert_alpha()
minus = image.load("minus.png").convert_alpha()
empty = image.load("empty.png").convert_alpha()

play_sel = image.load("select_play.jpg")
info_sel = image.load("select_info.jpg")
quit_sel = image.load("select_quit.jpg")

# Creating fonts that will be used to display text for the info screen, combo count, and a few other things
font_combometer = font.SysFont("Impact", 30)
font_score = font.SysFont("Arial", 20)

text1 = font_score.render("Welcome to trash stomper :)", 2, (WHITE))
text2 = font_score.render("This is an endless game about stomping ", 2, (WHITE))
text3 = font_score.render("trash and E-Waste.  You get points from", 2, (WHITE))
text4 = font_score.render(" \"cleaning\" them up", 2, (WHITE))
text5 = font_score.render("Move back an forth using the left and", 2, (WHITE))
text6 = font_score.render(" right arrow keys, and press the spacebar", 2, (WHITE))
text7 = font_score.render(" to jump.  When in the air,", 2, (WHITE))
text8 = font_score.render("you can press and hold (or tap) the spacebar", 2, WHITE)
text9 = font_score.render(" to shoot.", 2, (WHITE))
text10 = font_score.render("Keep your distance from the garbage bags, you", 2, (WHITE))
text11 = font_score.render(" are unable to stomp on these guys.  Be sure", 2, (WHITE))
text12= font_score.render("to shoot them.", 2, (WHITE))
text13 = font_score.render("Your score, current health, and current ammo", 2, (WHITE))
text14 = font_score.render("are all displayed at the top of the screen.", 2, (WHITE))
text15 = font_score.render("You can get more health by getting combos.", 2, (WHITE))
text16 = font_score.render("Get a 8 combo for 1 more bullet, and get a 15", 2, (WHITE))
text17 = font_score.render(" combo for 1 more hp.", 2, (WHITE))
text18 = font_score.render("PRESS SPACEBAR TO GO BACK TO MENU", 2, (WHITE))

# Putting these in a list so I dont have to individually scroll through them
texts = [text1, text2, text3, text4, text5, text6, text7, text8, text9, text10, text11, text12, text13, text14, text15, text16, text17, text18]

# The backbone of all of the smoothing in my game.  This function will take two numbers, and bring the first one closer to the second by a factor of 1/the smoothing value
# meaning, that if you had the first number, 0, and the second, 10, with a smoothing of 2, the value would look like this:
# 0, 5, 7.5 ...
# A very useful function my friend Borna had showed me.
def lerp(num1, num2, smooth=4):
    return num1 + (num2 - num1) / smooth

# I do not quite understand the concept of this function myself,
# Apparently you can not delete classes with a function in themselves, so I createed a global
# Function that will do it for me.
# Another way I could have done this is to have an alive boolean, and then scroll through the objects
# That are dead individually.  I think this would have taken longer than my method.
def delete(object, list):
    list.remove(object)

# This function is the backbone of every single one of my collisions.
# While it is not perfect, it was my first ever.  So some bugs are to be expected
# I wanted a way to check for collisions and have the function output what side the object had collided with, because some
# solids (such as platforms) had different ways to deal with the side collisions.
# This funciton takes a fluid - something that can move - and a solid.
# I do use this function to check for player/enemy collision.  This function will still work the same though
def collide(fluid, solid):
    if solid.y - fluid.y < 550:  # if the object is within 550 units
        if solid.x - fluid.w <= fluid.x <= solid.x + solid.w:  # checks if the object is within the solids x range
            if fluid.prevy >= solid.y + solid.h >= fluid.y:  # Checks if the object has crossed the bottom line of the solid
                return "BOTTOM"
            if fluid.prevy + fluid.h <= solid.y <= fluid.y + fluid.h:  # Checks if the object has crossed the top line of the solid
                return "TOP"
        if solid.y - fluid.h <= fluid.y <= solid.y + solid.h:  # Checks if the object is within the y range of the solid
            if fluid.prevx >= solid.x + solid.w >= fluid.x: # Checks right
                return "RIGHT"
            if fluid.prevx + fluid.w <= solid.x <= fluid.x + fluid.w: # Checks left
                return "LEFT"
        if solid.rect.colliderect(fluid.rect):  # the above statements will only return something when an object crosses a line.
            return "UNKNOWN"                    # if the object were to cross the line, and then stay, it is import that something is still returned

# Basic distance function
def dist(obj1, obj2):
    return ((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)**0.5

# The player class I will be using to represent the player
class Player:
    def __init__(self):
        self.y = -300  # initializes above the playing field
        self.prevy = self.y  # this value is used for collisions
        self.x = 210  # initializes the x value
        self.prevx = self.x  # This value is also used for collision
        self.dx = 0  # variable holding the keyboard input
        self.vx = 0  # x velocity
        self.vy = 0  # y velocity

        self.w, self.h = 22, 36   # width and height of player

        self.rect = Rect(self.x, self.y, self.w, self.h)  # A rectangle object created for the player

        self.speed = 6  # Horrizontal movement speed
        self.ysmooth = 20  # fast I want him to speed up vertically
        self.fall_speed = 15  # the max speed I want him to fall
        self.jump_height = -40  # how high I want him to jump

        self.can_jump = False  # important variable saying whenn the player can or can not jump
        self.can_shoot = True  # variable saying when the player can or can not shoot
        self.SB_pressed = False  # variable saying when the spacebar is pressed
        self.SB_end = 0  # a variable used to calculate how long the player is allowed to jump
        self.jumping = False  # variable saying when the player is jumping

        self.max_ammo = 8  # players max ammo
        self.current_ammo = 8 # players current ammo
        self.shot_cooldown = 0  # variable holding the current cooldown value  (timer)
        self.kickback = -3  # how much the player will jump every time he shoots
        self.god_mod = 0  # variable holding the invincibility value (timer)

        self.shot = False  # vairables used to draw player when he in a few different states
        self.left = False  # going left
        self.right = False  # going right
        self.still = False  # staying still

        self.max_hp = 4  # The max hp the player can get
        self.hp = 4  # current hp of the player
        self.score = 0  # current score of the player
        self.combo = 0  # current combo of the player

        self.max_combo = 0   # highest combo acheived during his playthrough

    def update(self):
        self.prevx = self.x  # saving the previous vallues
        self.prevy = self.y

        self.vx = lerp(self.vx, self.dx * self.speed)  #moving player horrizontally

        self.shot, self.cooling = False, False # resetting these to false.  Will turn into true again if they are

        if self.can_jump:  # If the player is touching the ground, reset his combo and refill his ammo
            self.combo = 0
            self.current_ammo = self.max_ammo

        if self.SB_pressed:
            if self.can_jump:  # If the player was grounded and pressed space, start jumping
                self.vy = 0
                self.jumping = True
                self.can_shoot = False
                self.can_jump = False

            if self.jumping:  # If the spacebar is still pressed and he is jumping
                if time.get_ticks() <= self.SB_end:  # if the player can still has time to jump
                    self.vy = lerp(self.vy, self.jump_height, self.ysmooth)  # continue jumping
                else:  #The player is out of time to jump
                    self.jumping = False
            else:  # Player pressed spacebar while in the air, and not jumping
                self.shot = False  # resetting, will be changed if needed
                if self.can_shoot: # if the player is able to shoot
                    if self.shot_cooldown == 0 and self.current_ammo > 0:  # if the player isnt on cooldown, and still has ammo
                        super_list.bullets.append(Bullet(self.rect.centerx, self.rect.centery))  # Spawn a bullet
                        self.vy = self.kickback  # pop him back a bit
                        self.shot_cooldown = 10  # add cooldown so he cant immediately shoot again
                        self.shot = True  # for drawing purposes
                        self.current_ammo -= 1  # he losses 1 ammo
                        if self.current_ammo == 0:  # displayers "empty" when out of ammo
                            super_list.text += [Text(self.x, self.y, "empty")]
                    else:
                        self.vy = lerp(self.vy, self.fall_speed, self.ysmooth)  # He was airborne, but unable to shoot.  just normal falling
                        self.cooling = True  #
                        self.shot = False
                else:
                    self.vy = lerp(self.vy, self.fall_speed, self.ysmooth)  # normal falling
        else:
            self.vy = lerp(self.vy, self.fall_speed, self.ysmooth)  # normal falling
            self.jumping = False  # player is no longer jumping

        self.shot_cooldown = max(self.shot_cooldown - 1, 0)  # subtracting 1 from cooldown until it reaches 0

        self.y += self.vy  # moving player's y
        self.x = min(420 - self.w, max(self.x + self.vx, 0))  # Players x movement

        if self.max_combo < self.combo:  # keeps track of players max combo
            self.max_combo = self.combo

        self.can_jump = False  #resetting variable

        for plat in super_list.platforms:
            if collide(self, plat) == "TOP":  # Platform collsions
                self.y = plat.y - self.h
                self.vy = 0
                self.can_jump = True
                self.can_shoot = False
                if self.combo >= 15:
                    self.score += 1000
                    self.hp = min(self.hp + 1, 4)
                    self.max_ammo += 1
                elif self.combo >= 8:
                    self.score += 500
                    self.max_ammo += 1
                if self.combo > 4:
                    super_list.text += [Text(self.x, self.y - 40, "combo")]
                self.current_ammo = self.max_ammo

        for block in super_list.blocks:  # Block collsions
            where = collide(self, block)
            if not where:
                continue

            if where == "TOP":
                self.can_jump = True
                self.can_shoot = False
                self.jumping = False
                self.y = block.y - self.h
                self.vy = 0
                if self.combo >= 15:
                    self.score += 1000
                    self.hp = min(self.hp + 1, 4)
                    self.max_ammo += 1
                elif self.combo >= 8:
                    self.score += 500
                    self.max_ammo += 1
                self.current_ammo = self.max_ammo
                if self.combo > 4:
                    super_list.text += [Text(self.x, self.y - 40, "combo")]

            elif where == "BOTTOM":
                self.jumping = False
                self.y = block.y + block.h
                self.vy = 0
                delete(block, super_list.blocks)
            elif where == "LEFT":
                self.vx = 0
                self.x = block.x - player.w - 1
            elif where == "RIGHT":
                self.vx = 0
                self.x = block.x + block.w + 1

        for wall in super_list.walls:  # Wall collisions
            c = collide(self, wall)
            if not c:
                continue
            if c == "TOP":
                self.can_jump = True
                self.can_shoot = False
                self.jumping = False
                self.y = wall.y - self.h
                self.vy = 0
                if self.combo >= 15:
                    self.score += 1000
                    self.hp = min(self.hp + 1, 4)
                    self.max_ammo += 1
                elif self.combo >= 8:
                    self.score += 500
                    self.max_ammo += 1
                self.current_ammo = self.max_ammo
                if self.combo > 4:
                    super_list.text += [Text(self.x, self.y - 40, "combo")]


            elif c == "BOTTOM":
                self.jumping = False
                self.y = wall.y + wall.h + 1
                self.vy = 0
            elif c == "LEFT":
                self.vx = 0
                self.x = wall.x - self.w - 1
            elif c == "RIGHT":
                self.vx = 0
                self.x = wall.x + wall.w + 1

        self.rect = Rect(self.x, self.y, self.w, self.h)  #updating player rectangle

    def paint(self):  # Command that will paint the player based on his current conditions
        if self.combo > 4:  #Draws combo count if it is 5 of greater
            text = font_combometer.render(str(self.combo), 2, (255, 0, 0))
            screen.blit(text, (player.x + 7, player.rect.centery - camera.y - 55))

        if self.god_mod > 0:
            if self.god_mod > 58:  # Will flash screen red
                screen.fill(RED)

            self.god_mod -= 1

            if self.right:
                screen.blit(hurt_right, (self.x, self.y - camera.y))
            else:
                screen.blit(hurt_left, (self.x, self.y - camera.y))
        else:
            if self.dx == 1:
                self.right = True
                self.left = False
            elif self.dx == -1:
                self.left = True
                self.right = False

            if self.jumping:
                if self.dx == 1:
                    screen.blit(jump_right, (self.x, self.y - camera.y))
                elif self.dx == -1:
                    screen.blit(jump_left, (self.x, self.y - camera.y))
                else:
                    if self.right:
                        screen.blit(jump_still_right, (self.x, self.y - camera.y))
                    else:
                        screen.blit(jump_still_left, (self.x, self.y - camera.y))
            elif 0 < self.vy:
                if self.left:
                    screen.blit(fall_left, (self.x, self.y - camera.y))
                else:
                    screen.blit(fall_right, (self.x, self.y-camera.y))
            elif self.can_jump:
                if self.dx == 1:
                    screen.blit(run_right, (self.x, self.y - camera.y))
                elif self.dx == -1:
                    screen.blit(run_left, (self.x, self.y - camera.y))
                else:
                    if self.left:
                        screen.blit(standing_left, (self.x, self.y - camera.y))
                    else:
                        screen.blit(standing_right, (self.x, self.y - camera.y))
            elif self.shot:
                if self.left:
                    screen.blit(shot_left, (self.x, self.y - camera.y))

                else:
                    screen.blit(shot_right, (self.x, self.y - camera.y))

            elif self.cooling:
                if self.left:
                    screen.blit(shot_left, (self.x, self.y - camera.y))
                else:
                    screen.blit(shot_right, (self.x, self.y - camera.y))

            else:
                if self.left:
                    screen.blit(fall_left, (self.x, self.y - camera.y))
                else:
                    screen.blit(fall_right, (self.x, self.y - camera.y))

class Camera:  # Class that moves.dat the camera around
    def __init__(self):
        self.x = 0  # unused, but can be if needed
        self.y = 0
        self.smooth = 4

    def update(self):
        # self.x = lerp(self.x, player.rect.centerx - SIZE[0] // 2, self.smooth)   # Would be used if I wanted horrizontal scrolling
        self.y = lerp(self.y, player.rect.centery - SIZE[1] // 2 + 100, 5)  # vertically scrolls the screen in relation to the player


class Platform:  # class that holds the information of platofrms
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w
        self.h = 5
        self.rect = Rect(x, y, w, 5)
        self.img = platfor

    def paint(self):
        for i in range(self.w // 10):
            screen.blit(self.img, (self.x + i * 10, self.y - camera.y))


class Block:  # Class that holds the information of destructible blocks
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 35
        self.h = self.w

        self.rect = Rect(x, y, self.w, self.h)

        self.img = random.choice([rust1, rust2, rust3])

    def paint(self):
        screen.blit(self.img, (self.x, self.y - camera.y))


class Bullet:  # Class that holds the information of bullets
    def __init__(self, x, y):

        self.x = x - 25//2
        self.prevx = self.x
        self.y = y
        self.orig_y = y
        self.prevy = y
        self.w = 25
        self.h = 45
        self.speed = 27
        self.lifespan = 300
        self.rect = Rect(x, y, 20, 35)

    def update(self):
        self.prevy = self.y
        self.y += self.speed

        self.rect.y += self.speed

    def paint(self):
        #draw.rect(screen, (255, 0, 255), (self.x, self.y - camera.y, self.w, self.h))
        screen.blit(bullet, (self.x, self.y-camera.y))


class Waste:  # Class that holds the information of the little 1's and 0's
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.w, self.h = 10, 10
        self.score = 10
        self.speed = 10
        self.img = random.choice([one, zero])
        self.rect = Rect(self.x, self.y, self.w, self.h)

    def update(self):
        if dist(self, player) < 100:

            self.y += self.vy
            self.x += self.vx

            self.vy = lerp(self.vy, ((player.rect.centery - self.rect.centery) / ((player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.y) ** 2) ** 0.5) * self.speed, 10)
            self.vx = lerp(self.vx, ((player.rect.centerx - self.rect.centerx) / ((player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.y) ** 2) ** 0.5) * self.speed, 10)

            self.rect = Rect(self.x, self.y, self.w, self.h)
        else:
            self.y += self.vy
            self.x += self.vx

            self.vy = lerp(self.vy, 0, 10)
            self.vx = lerp(self.vx, 0, 10)

            self.rect = Rect(self.x, self.y, self.w, self.h)

    def paint(self):
        screen.blit(self.img, (self.x, self.y - camera.y))

class Floater:  # Class that holds the information of the envelopes
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.prevy = y
        self.prevx = x
        self.w = 30
        self.h = 20
        self.speed = 3
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.hp = 3
        self.img = random.choice([floater_eyes, floater_spam])

    def update(self):
        if self.y - player.y < 600:

            self.prevy = self.y
            self.prevx = self.x

            self.y += self.vy
            self.x += self.vx

            self.vy = lerp(self.vy, ((player.rect.centery - self.rect.centery) / ((player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.y) ** 2) ** 0.5) * self.speed, 100)
            self.vx = lerp(self.vx, ((player.rect.centerx - self.rect.centerx) / ((player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.y) ** 2) ** 0.5) * self.speed, 100)

            self.rect = Rect(self.x, self.y, self.w, self.h)

    def paint(self):
        screen.blit(self.img, (self.x, self.y - camera.y))


class Walker:  # Class that holds the information of the batteries
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 0
        self.prevy = y
        self.prevx = x
        self.w = 40
        self.h = 10
        self.speed = 1
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.alive = True
        self.hp = 1
        self.direction = random.choice([1, -1])

    def update(self):
        self.prevy = self.y
        self.prevx = self.x

        self.y += self.vy
        self.vy = lerp(self.vy, 10)

        self.x += self.speed * self.direction

        self.rect.y = self.y
        self.rect.x = self.x

    def paint(self):
        if self.direction == 1:
            screen.blit(battery_right, (self.x, self.y - camera.y))
        else:
            screen.blit(battery_left, (self.x, self.y - camera.y))

class Waiter:  # Class that holds the information for the evil computers
    def __init__(self, x, y):
        self.x = x
        self.vx = 0
        self.y = y
        self.vy = 0
        self.w, self.h = 20, 20
        self.prevy = y
        self.prevx = x
        self.can_move = False
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.speed = 4
        self.hp = 1

    def update(self):
        if self.y - player.y < 600:
            self.prevy = self.y
            self.prevx = self.x

            self.y += self.vy
            self.x += self.vx

            self.vy = lerp(self.vy, ((player.rect.centery - self.rect.centery) / ((player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.y) ** 2) ** 0.5) * self.speed, 20)
            self.vx = lerp(self.vx, ((player.rect.centerx - self.rect.centerx) / ((player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.y) ** 2) ** 0.5) * self.speed, 20)

            self.rect = Rect(self.x, self.y, self.w, self.h)

    def paint(self):
        if self.can_move:
            if self.vx > 0:
                screen.blit(waiter_move_right, (self.x, self.y - camera.y))
            else:
                screen.blit(waiter_move_left, (self.x, self.y - camera.y))
        else:
            screen.blit(waiter_sleep, (self.x, self.y - camera.y))


class Text:  # Class for drawn text
    def __init__(self, x, y, text):
        self.x = x
        self.y = y - 100
        if text == "combo":
            self.img = combo
        elif text == "minus":
            self.img = minus
        elif text == "empty":
            self.img = empty

        self.lifespan = 80
        self.y_offset = camera.y

    def paint(self):
        screen.blit(self.img, (self.x, self.y - self.y_offset))
        self.lifespan -= 1

        if self.lifespan == 0:
            delete(self, super_list.text)


class Tracker:  # Class for the magnet garbage bags
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.prevy = y
        self.prevx = x
        self.w = 40
        self.h = 40
        self.speed = 3
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.hp = 6

    def update(self):
        if self.y - player.y < 600:

            self.prevy = self.y
            self.prevx = self.x

            self.y += self.vy
            self.x += self.vx

            self.vy = lerp(self.vy, ((player.rect.centery - self.rect.centery) / ((player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.y) ** 2) ** 0.5) * self.speed, 50)
            self.vx = lerp(self.vx, ((player.rect.centerx - self.rect.centerx) / ((player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.y) ** 2) ** 0.5) * self.speed, 50)

            self.rect = Rect(self.x, self.y, self.w, self.h)

    def paint(self):
        screen.blit(garbage, (self.x, self.y - camera.y))


class Wall:  # Class for the walls of the stages
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 35
        self.h = self.w

        self.rect = Rect(x, y, self.w, self.h)

    def paint(self):
        screen.blit(wall_img, (self.x, self.y - camera.y))


class Super:  # a strange class that I decided to use.  This has all the lists I will be using
    def __init__(self):
        self.bullets = []
        self.platforms = []
        self.floaters = []
        self.blocks = []
        self.walls = []
        self.walkers = []
        self.waiters = []
        self.waste = []
        self.trackers = []
        self.text = []
        self.super_list = [self.bullets, self.platforms, self.floaters, self.blocks, self.walls, self.walkers, self.waiters, self.waste, self.trackers, self.text]

# 6 different stage types
def stage0(offset=0):
    global super_list
    super_list.walls += [Wall(0, 200 + offset), Wall(35, 235 + offset), Wall(70, 270 + offset), Wall(105, 305 + offset), Wall(280, 305 + offset), Wall(315, 270 + offset), Wall(350, 235 + offset), Wall(385, 200 + offset)]
    for x in range(4):
        for y in range(4):
            super_list.walls += [Wall(x*35 - y*35, y*35 + 600 + offset)]
    for x in range(4):
        for y in range(4):
            super_list.walls += [Wall((420 - 2* 35) + x*35 - y*35, y*35 + 600 + offset)]

    super_list.blocks += [Block(140, 305 + offset), Block(175, 305 + offset), Block(210, 305 + offset), Block(245, 305 + offset)]
    super_list.blocks += [Block(140+x*35, 1100 + offset) for x in range(4)]
    super_list.platforms += [Platform(60, 900 + offset, 140), Platform(280, 1100 + offset, 140), Platform(0, 1100 + offset, 140)]
    super_list.floaters += [Floater(random.randint(0, 400), random.randint(500, 650) + offset) for x in range(3)]
def stage1(offset=0):
    global super_list
    super_list.walls += [Wall(0, 0 + offset), Wall(0, 35 + offset)]
    super_list.platforms += [Platform(170, 70 + offset, 100)]
    super_list.floaters += [Floater(200, 150 + offset)]
    super_list.walls += [Wall(x*35, 235 + offset) for x in range(4)]
    super_list.walls += [Wall(x*35, 270 + offset) for x in range(3)]
    super_list.walls += [Wall(x*35, 305 + offset) for x in range(2)]

    super_list.blocks += [Block(200 + x*35, 375 + offset) for x in range(3)]
def stage2(offset=0):
    global super_list
    super_list.blocks += [Block(x*35, 235 + offset) for x in range(4)]
    super_list.blocks += [Block(x*35 + 35 * 8, 235 + offset) for x in range(4)]

    super_list.waiters += [Waiter(100, 280 + offset), Waiter(320, 280 + offset)]
def stage3(offset=0):
    global super_list
    super_list.walls += [Wall(385, 0 + offset), Wall(385, 35 + offset)]
    super_list.platforms += [Platform(35, 100 + offset, 100), Platform(315, 200 + offset, 100), Platform(105, 375 + offset, 100)]
def stage4(offset=0):
    global super_list
    super_list.walls += [Wall(0, y * 35 + offset) for y in range(11)]
    super_list.walls += [Wall(385, y * 35 + offset) for y in range(11)]
    super_list.platforms += [Platform(35, 100 + offset, 100), Platform(280, 300 + offset, 100)]
    super_list.walkers += [Walker(1, offset), Walker(300, 200 + offset)]
    super_list.trackers += [Tracker(200, 300 + offset)]
def stage5(offset=0):
    global super_list
    super_list.blocks += [Block(random.randint(0, 385), random.randint(0, 100) + offset) for x in range(10)]
    super_list.floaters += [Floater(x*100, random.randint(300, 340) + offset) for x in range(4)]
def stage6(offset=0):
    global super_list
    super_list.platforms += [Platform(105, 200 + offset, 200)]
    super_list.walls += [Wall(0, y * 35 + offset) for y in range(5)]
    super_list.walls += [Wall(385, 6 * 35 + y * 35 + offset) for y in range(5)]
    super_list.waiters += [Waiter(0, 35*6 + offset)]
    super_list.walkers += [Walker(200, 180 + offset)]


# ASSIGNING VARIABLES TO CLASSES
player = Player()
camera = Camera()
super_list = Super()
clock = time.Clock()

# Basic screen state variables
running = True
menu = True
game = False
info = False
gameover = False

# variable used to hold the info of the selected item in the menu
selected = 0

while running:  # The main loop
    while game:  # The game loop
        screen.fill(BLACK)
        player.update()
        camera.update()

        for lis in super_list.super_list:  #scrolls through each list in the list
            for item in lis:  # scrolls through each item in each list
                if item.y > player.y + 600:  # Ignores loop if the item is too far away
                    continue
                item.paint()  # Paints the item onto the screen

                if item.y < player.y - 500:  # Cleans up the above section of the player, so enemies can fall, and the player can only go down
                    if type(item) is Waste:
                        delete(item, super_list.waste)
                    if type(item) is Block:
                        delete(item, super_list.blocks)
                    if type(item) is Platform:
                        delete(item, super_list.platforms)
                    if type(item) is Wall:
                        delete(item, super_list.walls)
                try:
                    if type(item) is Bullet:  # Goes through the bullet routine
                        item.update()
                        dead = False

                        # Checks for collisions.  If there is one, delete the bullet
                        for block in super_list.blocks:
                            if collide(item, block):
                                dead = True
                                delete(block, super_list.blocks)

                        for tracker in super_list.trackers:
                            if collide(item, tracker):
                                tracker.vy += 5
                                tracker.hp -= 1
                                dead = True

                        for waiter in super_list.waiters:
                            if collide(item, waiter):
                                waiter.vy += 2
                                waiter.hp -= 1
                                dead = True

                        for floater in super_list.floaters:
                            if collide(item, floater):
                                floater.vy += 1
                                floater.hp -= 1
                                dead = True

                        for wall in super_list.walls:
                            if collide(item, wall):
                                dead = True

                        if item.y > item.orig_y + 300 or dead:
                            delete(item, super_list.bullets)

                    if type(item) is Floater:  # Floater routine
                        # move the floater
                        item.update()

                        # Check to see if the player has stomped on the enemy
                        if item.x - player.w < player.x < item.x + item.w:
                            if not player.can_jump or player.jumping:
                                if player.prevy + player.h < item.y < player.y + player.h + 2:
                                    player.vy = -7
                                    player.current_ammo = player.max_ammo
                                    item.hp = 0
                                    player.current_ammo = player.max_ammo
                                else:
                                    if player.rect.colliderect(item.rect):
                                        if player.y + player.h - 5 < item.y:
                                            player.vy = -7
                                            player.current_ammo = player.max_ammo
                                            item.hp = 0

                                        elif player.god_mod == 0:
                                            player.hp -= 1
                                            player.god_mod = 60
                                            super_list.text += [Text(player.x, player.y + 40, "minus")]
                            else:
                                if player.rect.colliderect(item.rect):
                                    if player.y + player.h - 5 < item.y:
                                        player.vy = -7
                                        player.current_ammo = player.max_ammo
                                        item.hp = 0
                                    else:
                                        if player.god_mod == 0:
                                            player.hp -= 1
                                            player.god_mod = 60
                                            super_list.text += [Text(player.x, player.y + 40, "minus")]

                        # Object collisions
                        for wall in super_list.walls:
                            c = collide(item, wall)

                            if not c:
                                continue

                            if c == "TOP":
                                item.y = wall.y - item.h - 1
                                item.vy = 0
                            elif c == "BOTTOM":
                                item.y = wall.y + wall.h + 1
                                item.vy = 0
                            elif c == "LEFT":
                                item.vx = 0
                                item.x = wall.x - wall.w - 1
                            elif c == "RIGHT":
                                item.vx = 0
                                item.x = wall.x + wall.w + 1

                        for block in super_list.blocks:

                            c = collide(item, block)
                            if not c:
                                continue
                            if c == "TOP":
                                item.y = block.y - item.h - 1
                                item.vy = 0
                            elif c == "BOTTOM":
                                item.y = block.y + block.h + 1
                                item.vy = 0
                            elif c == "LEFT":
                                item.vx = 0
                                item.x = block.x - item.w - 1
                            elif c == "RIGHT":
                                item.vx = 0
                                item.x = block.x + block.w + 1

                        # If the item is dead, delete it, and spawn numbers
                        if item.hp <= 0:
                            super_list.waste += [Waste(item.rect.centerx, item.rect.centery, random.randint(-10, 10), random.randint(-10, 10)) for x in range(random.randint(3, 10))]
                            player.combo += 1
                            delete(item, super_list.floaters)

                    if type(item) is Tracker:  # the tracker routine
                        # move the tracker
                        item.update()

                        # Check for collisions
                        for wall in super_list.walls:
                            c = collide(item, wall)

                            if not c:
                                continue

                            if c == "TOP":
                                item.y = wall.y - item.h - 1
                                item.vy = -3
                            elif c == "BOTTOM":
                                item.y = wall.y + wall.h + 1
                                item.vy = 3
                            elif c == "LEFT":
                                item.vx = -3
                                item.x = wall.x - wall.w - 1
                            elif c == "RIGHT":
                                item.vx = 3
                                item.x = wall.x + wall.w + 1

                        for block in super_list.blocks:

                            c = collide(item, block)
                            if not c:
                                continue
                            if c == "TOP":
                                item.y = block.y - item.h - 1
                                item.vy = -3
                            elif c == "BOTTOM":
                                item.y = block.y + block.h + 1
                                item.vy = 3
                            elif c == "LEFT":
                                item.vx = -3
                                item.x = block.x - item.w - 1
                            elif c == "RIGHT":
                                item.vx = 3
                                item.x = block.x + block.w + 1

                        # If the player collides, he will take damage.  no stomping :P
                        if player.rect.colliderect(item.rect):
                            if player.god_mod == 0:
                                player.hp -= 1
                                player.god_mod = 60
                                super_list.text += [Text(player.x, player.y + 40, "minus")]

                        # delete and spawn numbers if dead
                        if item.hp <= 0:
                            super_list.waste += [Waste(item.rect.centerx, item.rect.centery, random.randint(-10, 10), random.randint(-10, 10)) for x in range(random.randint(10, 20))]
                            player.combo += 1
                            delete(item, super_list.trackers)

                    if type(item) is Waiter:
                        # waiters can phase through walls, so they do not need collision checks

                        if player.y + player.h - 10 > item.y:  # Player must be below the waiter before he can move
                            item.can_move = True

                        if item.can_move:  # if he can move, move
                            item.update()

                        # Checking for stomps
                        if item.x - player.w < player.x < item.x + item.w:
                            if not player.can_jump or player.jumping:
                                if player.prevy + player.h < item.y < player.y + player.h + 2:
                                    player.vy = -7
                                    player.current_ammo = player.max_ammo
                                    item.hp = 0
                                    player.current_ammo = player.max_ammo
                                else:
                                    if player.rect.colliderect(item.rect):
                                        if player.y + player.h - 5 < item.y:
                                            player.vy = -7
                                            player.current_ammo = player.max_ammo
                                            item.hp = 0

                                        elif player.god_mod == 0:
                                            player.hp -= 1
                                            player.god_mod = 60
                                            super_list.text += [Text(player.x, player.y + 40, "minus")]
                            else:
                                if player.rect.colliderect(item.rect):
                                    if player.y + player.h - 5 < item.y:
                                        player.vy = -7
                                        player.current_ammo = player.max_ammo
                                        item.hp = 0
                                    else:
                                        if player.god_mod == 0:
                                            player.hp -= 1
                                            player.god_mod = 60
                                            super_list.text += [Text(player.x, player.y + 40, "minus")]


                            for wall in super_list.walls:
                                c = collide(item, wall)

                                if not c:
                                    continue

                                if c == "TOP":
                                    item.y = wall.y - item.h - 1
                                    item.vy = 0
                                elif c == "BOTTOM":
                                    item.y = wall.y + wall.h + 1
                                    item.vy = 0
                                elif c == "LEFT":
                                    item.vx = 0
                                    item.x = wall.x - wall.w - 1
                                elif c == "RIGHT":
                                    item.vx = 0
                                    item.x = wall.x + wall.w + 1

                            for block in super_list.blocks:

                                c = collide(item, block)
                                if not c:
                                    continue
                                if c == "TOP":
                                    item.y = block.y - item.h - 1
                                    item.vy = 0
                                elif c == "BOTTOM":
                                    item.y = block.y + block.h + 1
                                    item.vy = 0
                                elif c == "LEFT":
                                    item.vx = 0
                                    item.x = block.x - item.w - 1
                                elif c == "RIGHT":
                                    item.vx = 0
                                    item.x = block.x + block.w + 1

                        # delete the item if it is dead.  Also spawn numbers of coures
                        if item.hp <= 0:
                            super_list.waste += [Waste(item.rect.centerx, item.rect.centery, random.randint(-10, 10), random.randint(-10, 10)) for x in range(random.randint(3, 10))]
                            player.combo += 1
                            delete(item, super_list.waiters)

                    if type(item) is Walker:  # The Walker routine
                        item.update()  # move the item
                        flip = False  # used for flipping his movement if he his a wall
                        if item.x - player.w < player.x < item.x + item.w:  # Checking for stomps
                            if not player.can_jump:
                                if player.prevy + player.h < item.y < player.y + player.h + 5:
                                    player.vy = -10
                                    player.current_ammo = player.max_ammo
                                    item.hp = 0
                                    player.current_ammo = player.max_ammo
                                else:
                                    if player.rect.colliderect(item.rect):
                                        if player.y + player.h - 5 < item.y:
                                            player.vy = -10
                                            player.current_ammo = player.max_ammo
                                            item.hp = 0

                                        elif player.god_mod == 0:
                                            player.hp -= 1
                                            player.god_mod = 60
                                            super_list.text += [Text(player.x, player.y + 40, "minus")]
                            else:
                                if player.rect.colliderect(item.rect):
                                    if player.y + player.h - 5 < item.y:
                                        player.vy = -10
                                        player.current_ammo = player.max_ammo
                                        item.hp = 0
                                    else:
                                        if player.god_mod == 0:
                                            player.hp -= 1
                                            player.god_mod = 60
                                            super_list.text += [Text(player.x, player.y + 40, "minus")]

                        # If dead, delete.  also numbers
                        if item.hp == 0:
                            super_list.waste += [Waste(item.rect.centerx, item.rect.centery, random.randint(-10, 10), random.randint(-10, 10)) for x in range(random.randint(1, 4))]
                            player.combo += 1
                            delete(item, super_list.walkers)

                        # collision checks
                        for wall in super_list.walls:
                            c = collide(item, wall)
                            if not c:
                                continue
                            if c == "LEFT" or c == "RIGHT":
                                flip = True
                            elif c == "TOP":
                                item.y = wall.y - item.h - 1
                                item.vy = 0

                        for block in super_list.blocks:
                            c = collide(item, block)
                            if not c:
                                continue
                            if c == "LEFT" or c == "RIGHT":
                                flip = True
                            elif c == "TOP":
                                item.y = block.y - item.h - 1
                                item.vy = 0

                        for platty in super_list.platforms:
                            if collide(item, platty) == "TOP":
                                item.y = platty.y - item.h - 1
                                item.vy = 0

                        # flipping item if needed
                        if flip or item.x > 420 - item.w or item.x < 0:
                            item.direction *= -1

                    if type(item) is Waste:  # number routine
                        item.update()  # move the numbers
                        if item.rect.colliderect(player.rect):  # if the player collects them, add score and delete item
                                player.current_ammo = min(player.max_ammo, player.current_ammo + 1)
                                player.score += item.score
                                delete(item, super_list.waste)

                except:  # If there are any issues, just continue through the loop.
                    continue

        player.paint()  # draws the player on top of everything
        # Draws the GUI on the top of the screen.  this include, hp, ammo, and score
        # player hp boxes and text
        draw.rect(screen, WHITE, (0, 0, player.hp * 200 / player.max_hp, 20))
        draw.rect(screen, (255, 50, 50), (0, 0, 200, 20), 1)
        text = font_score.render(str(player.hp) + "/" + str(player.max_hp), 2, (200, 30, 255))
        screen.blit(text, (80, -1))

        # Player score text
        text = font_score.render(str(player.score), 2, (255, 0, 0))
        screen.blit(text, (203, -1))

        # Player ammo boxes
        draw.rect(screen, GREEN, (0, 22, player.current_ammo * 420 / player.max_ammo, 10))
        for i in range(player.current_ammo + 1):
            draw.rect(screen, BLACK, (0, 22, 420 / player.max_ammo * i, 10), 1)

        # if the player is dead, end the game.
        if player.hp == 0:
            gameover = True
            game = False

        # Update the screen, we are no finished drawing everything
        display.flip()

        # Event loop
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
                game = False
            if evnt.type == KEYDOWN:
                if evnt.key == K_ESCAPE:
                    menu = True
                    game = False
                if evnt.key == K_LEFT:
                    player.dx -= 1
                if evnt.key == K_RIGHT:
                    player.dx += 1
                if evnt.key == K_SPACE:
                    player.SB_end = time.get_ticks() + 170

                    if not player.can_jump:
                        player.can_shoot = True
                    player.SB_pressed = True

            if evnt.type == KEYUP:
                if evnt.key == K_LEFT:
                    player.dx += 1
                if evnt.key == K_RIGHT:
                    player.dx -= 1
                if evnt.key == K_SPACE:
                    player.SB_pressed = False

        # 60 frames per second
        clock.tick(60)

    while gameover:  # game over loop
        # Displaying the score of the current run, and the highscores.
        screen.fill(BLACK)
        screen.blit((font_combometer.render("GAME OVER", 2, RED)), (20, 100))
        screen.blit(font_combometer.render("YOUR SCORE: " + str(player.score), 2, WHITE), (20, 300))
        screen.blit(font_combometer.render("YOUR MAX-COMBO: " + str(player.max_combo), 2, WHITE), (20, 330))
        screen.blit(font_combometer.render("HIGHSCORE: " + str(highscore), 2, WHITE), (20, 390))
        screen.blit(font_combometer.render("HIGHSCORE COMBO: " + str(high_combo), 2, WHITE), (20, 420))
        screen.blit(font_combometer.render("SPACE TO GO TO MENU", 2, GREEN), (20, 550))

        # Event loop
        for evnt in event.get():
            if evnt.type == KEYDOWN:
                if evnt.key == K_SPACE:  # When leaving, it runs through a routine that will save the new highsore if there is one
                    myFile.close()
                    if player.score > highscore:
                        newFile = open("highscore.dat", "w")

                        highscore = player.score

                        if player.max_combo > high_combo:
                            newFile.write(str(player.score) + " " + str(player.max_combo))
                            high_combo = player.max_combo
                        else:
                            newFile.write(str(player.score) + " " + str(high_combo))
                        newFile.close()
                    elif player.max_combo > high_combo:
                        high_combo = player.max_combo
                        newFile = open("highscore.dat", "w")
                        newFile.write(str(highscore) + " " + str(player.max_combo))
                        newFile.close()

                    myFile = open("highscore.dat", "r")

                    gameover = False
                    menu = True

        # Update screen, 60 fps
        display.flip()
        clock.tick(60)

    while menu:  # the menu loop
        screen.fill(BLACK)

        # deciding which image to highlight based on what the player has chosen
        if selected % 3 == 0:
            screen.blit(play_sel, (0, 100))
        elif selected % 3 == 1:
            screen.blit(info_sel, (0, 100))
        else:
            screen.blit(quit_sel, (0, 100))

        # Event loop
        for evnt in event.get():
            if evnt.type == KEYDOWN:
                if evnt.key == K_RIGHT:  # Moving the selected option
                    selected += 1
                if evnt.key == K_LEFT:
                    selected -= 1
                if evnt.key == K_SPACE:  # if the player selects something
                    if selected % 3 == 0:  # if the player selects "play"
                        menu = False  # Change loop states
                        game = True

                        # re-initialize the player, camera, and the list
                        player = Player()
                        camera = Camera()
                        super_list = Super()
                        # randomly generate the stage
                        for i in range(80):
                            x = random.randint(1, 6)

                            if x == 1:
                                stage1(i * 400)
                            if x == 2:
                                stage2(i * 400)
                            if x == 3:
                                stage3(i * 400)
                            if x == 4:
                                stage4(i * 400)
                            if x == 5:
                                stage5(i * 400)
                            if x == 6:
                                stage6(i * 400)

                    elif selected % 3 == 1:  # if player selects info, change loop state
                        info = True
                        menu = False
                    elif selected % 3 == 2:  # if player selects quit, quit the game
                        menu = False
                        running = False

        # Update the screen, 60 fps
        display.flip()
        clock.tick(60)

    while info:  # info screen loop

        screen.fill(BLACK)
        for i, tex in enumerate(texts):  # prints each of the informational texts
            screen.blit(tex, (0, 50 + i*20))

        # Displays the highscore, and max combo as well
        screen.blit(font_combometer.render("highscore: " + str(highscore), 2, GREEN), (20, 600))
        screen.blit(font_combometer.render("max combo: " + str(high_combo), 2, GREEN), (20, 630))

        # Event loop.  Only option is to press space and go back to menu
        for evnt in event.get():
            if evnt.type == KEYDOWN:
                if evnt.key == K_SPACE:
                    menu = True
                    info = False
                    
        # update screen, 60fps
        display.update()
        clock.tick(60)

# if the running loop has finished, quit
quit()
