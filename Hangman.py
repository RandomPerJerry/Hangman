# Jerry Zhang
# Main Pygame Hangman

# importing libaries
import pygame
import sys
import string
import random
import math

# setting pygamee up
pygame.init()

WIDTH, HEIGHT = 960, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HangMan")


clock = pygame.time.Clock()


class character:
    def __init__(self):
        # Pre : None
        # Post : initilizing neccacary values

        self.x = 9000
        self.y = 9000
        self.speed = 10

        self.cameraX = 8645
        self.cameraY = 8740

        self.actualpos = (self.x, self.y)
        self.blitpos = (0, 0)

        self.level = 1

        self.xp = 0
        self.xpcap = 100

        self.health = 100
        self.defense = 1
        self.attack = 1

        self.leftwalking = []
        self.rightwalking = []

        self.leftidle = []
        self.rightidle = []

        self.walking = False

        self.walkframe = 0
        self.idleframe = 0

        self.blitframe = self.idleframe

        # importing images and resizing them
        for index in range(0, 6):
            image = pygame.image.load(f'Assets/Walking/Walking{index}.png')
            self.rightwalking.append(pygame.transform.scale(image, (250, 200)))

        for image in self.rightwalking.copy():
            self.leftwalking.append(pygame.transform.flip(image, True, False))

        for index in range(0, 4):
            image = pygame.image.load(f'Assets/Idle/Idle{index}.png')
            self.rightidle.append(pygame.transform.scale(image, (255, 200)))

        for image in self.rightidle.copy():
            self.leftidle.append(pygame.transform.flip(image, True, False))

        self.inner_rect = None
        self.hitbox = None

        self.walkimage = self.rightwalking
        self.idleimage = self.rightidle

        self.blitimage = self.idleimage

        self.font = pygame.font.SysFont('times new roman', int(15))

    def animation_update(self):
        # Pre: None
        # Post: update which frame the animation is in

        if self.walking:
            self.idleframe = 0
            self.walkframe += 0.33
            self.walkframe %= 5

        else:
            self.walkframe = 0
            self.idleframe += 0.05
            self.idleframe %= 3

    def camera_position_update(self):
        # Pre: None
        # Post: update camera's position based off of the character's position
        if self.x - 200 < self.cameraX:
            self.cameraX -= self.speed

        elif self.x - (760 - self.blitimage[0].get_size()[0]) > self.cameraX:
            self.cameraX += self.speed

        if self.y - 180 < self.cameraY:
            self.cameraY -= self.speed

        elif self.y - (540 - self.blitimage[0].get_size()[1]) > self.cameraY:
            self.cameraY += self.speed

    def move(self, left, right, up, down):
        # Pre: which dirrection is the player currently moving
        # Post: update the player's position based off it's inputs

        movements = [left, right, up, down]

        if any(movements):
            self.walking = True
        else:
            self.walking = False

        if left:
            self.x -= self.speed
            self.walkimage = self.leftwalking
            self.idleimage = self.leftidle

            if up:
                self.y -= self.speed

            elif down:
                self.y += self.speed

        elif right:

            self.x += self.speed
            self.walkimage = self.rightwalking
            self.idleimage = self.rightidle

            if up:
                self.y -= self.speed

            elif down:
                self.y += self.speed

        elif up:
            self.y -= self.speed

        elif down:
            self.y += self.speed

        # Keeps the player inbound
        if self.x > 10000:
            self.x = 10000
        if self.x < -10000:
            self.x = -10000
        if self.y > 10000:
            self.y = 10000
        if self.y < -10000:
            self.y = -10000

    def hitbox_update(self):
        # Pre: None:
        # Post: updates the player's hitboxes based off it position

        self.inner_rect = pygame.Rect(
            self.x - 50, self.y - 50, WIDTH + 100, HEIGHT + 100)
        self.spawn_rect = pygame.Rect(
            self.actualpos[0] - WIDTH//2, self.actualpos[1] - HEIGHT//2, WIDTH * 1.5, HEIGHT * 1.5)

        if self.idleimage == self.rightidle:
            self.hitbox = pygame.Rect(
                self.blitpos[0] + 65, self.blitpos[1] + 40, 160, self.blitimage[0].get_size()[1] - 50)

        else:
            self.hitbox = pygame.Rect(
                self.blitpos[0] + 30, self.blitpos[1] + 40, 160, self.blitimage[0].get_size()[1] - 50)

        self.actualpos = (self.x, self.y)

    def draw(self):
        # Pre: none
        # Post: draws the player's position on screen based off the player's camera position and actual position

        if self.walking:
            self.blitimage = self.walkimage
            self.blitframe = self.walkframe
        else:
            self.blitimage = self.idleimage
            self.blitframe = self.idleframe

        self.blitpos = (self.x - self.cameraX, self.y - self.cameraY)

        screen.blit(self.blitimage[int(self.blitframe)], self.blitpos)

        cordshow = self.font.render(
            f'Cordinates: {self.actualpos}', True, (255, 255, 255))
        screen.blit(cordshow, (10, 20))

        healthshow = self.font.render(
            f'Health: {self.health}', True, (255, 255, 255))
        screen.blit(healthshow, (WIDTH - healthshow.get_width() - 10, 20))

        levelshow = self.font.render(
            f'Level: {self.level}', True, (255, 255, 255))
        screen.blit(levelshow, (WIDTH - levelshow.get_width() - 10, 50))

    def level_up_check(self):
        # Pre: None
        # Post: Check if player should level up and update the xp cap

        while self.xp >= self.xpcap:
            self.xp -= self.xpcap
            self.level += 1

            self.xpcap = self.level * 100


class enemy:
    def __init__(self):

        # Pre: None:
        # Post: importing potential images for the enemies, and initilizing values
        self.enemy1r, self.enemy2r, self.enemy3r, self.enemy4r, self.enemy5r = [], [], [], [], []
        self.enemy1l, self.enemy2l, self.enemy3l, self.enemy4l, self.enemy5l = [], [], [], [], []

        self.enemyr = [self.enemy1r, self.enemy2r,
                       self.enemy3r, self.enemy4r, self.enemy5r]
        self.enemyl = [self.enemy1l, self.enemy2l,
                       self.enemy3l, self.enemy4l, self.enemy5l]

        for index, item in enumerate(self.enemyr):
            for n in range(4):
                image = pygame.image.load(
                    f'Assets/Monsters/Monster{index+1}/enemy{n}.png')
                item.append(pygame.transform.scale(image, (167, 100)))

        for index, item in enumerate(self.enemyl):
            for image in self.enemyr[index].copy():
                item.append(pygame.transform.flip(image, True, False))

        self.tries = 0
        self.cord = []
        self.playerpos = playerpos
        for n in range(16):
            self.x, self.y = random.randrange(self.playerpos[0] - 1500, self.playerpos[0] + 2500), random.randrange(
                self.playerpos[1] - 1500, self.playerpos[1] + 2500)
            self.monsterpos = (self.x, self.y)

            self.rect = pygame.Rect(self.x, self.y, self.enemy1l[0].get_size()[
                                    0], self.enemy1l[0].get_size()[1])

            if self.unique_coordinate_checker():
                break

            self.x, self.y = (10000, 1000000)

        self.hitbox = pygame.Rect(self.x + 10, self.y + 10, 167, 100)

        self.initialmonsterpos = (self.x, self.y)

        self.level = 1
        self.chosenr = None
        self.chosenl = None
        self.blitimg = None

        self.frame = 0

        self.level_determination()

    def unique_coordinate_checker(self):
        # Pre: None
        # Post: Check if the cordinate stasify the requirement

        for image in monsterlist:
            if self.rect.colliderect(image.rect) or self.rect.colliderect(player.spawn_rect) or abs(self.x) > 10000 or abs(self.y) > 10000:
                return False
        return True

    def level_determination(self):
        # Pre: None
        # Post: Based off of the enemys location and gives its it levels

        if abs(self.x) < 1500 and abs(self.y) < 1500:
            self.level = random.choices([4, 5], [0.2, 0.8])[0]

        elif abs(self.x) < 2500 and abs(self.y) < 2500:
            self.level = random.choices([3, 4], [0.4, 0.6])[0]

        elif abs(self.x) < 4500 and abs(self.y) < 4500:
            self.level = random.choices([1, 2, 3], [0.1, 0.3, 0.6])[0]

        elif abs(self.x) < 6500 and abs(self.y) < 6500:
            self.level = random.choices([1, 2], [0.4, 0.6])[0]

        else:
            self.level = 1

        self.chosenr, self.chosenl = self.enemyr[(
            self.level - 1)], self.enemyl[(self.level - 1)]
        self.blitimg = self.chosenr

    def pos_update(self):
        # Pre: None
        # Post: updates player's position

        self.playerpos = playerpos
        self.camerapos = playercamera

    def animation_update(self):
        # Pre: None
        # Post: Determine what frame is the animation is on

        self.frame += 0.1
        self.frame %= 4

    def despawn(self, monsternum):
        # Pre: the monster's index in the monster list
        # Post: determine whether or not the monster is too far from the player and despawn them
        self.currentmonsterpos = monsterlist[monsternum].initialmonsterpos
        despawn_threshold = 3000

        if distance(playerpos[0], playerpos[1], self.currentmonsterpos[0], self.currentmonsterpos[1]) > despawn_threshold:

            del monsterlist[monsternum]

    def draw(self):
        # Pre: None
        # Post: drawing the enmies based of where the player is and where did the monster spawn

        poschange = (self.initialmonsterpos[0] - self.camerapos[0],
                     self.initialmonsterpos[1] - self.camerapos[1])
        self.actualpos = (
            self.initialmonsterpos[0] - self.playerpos[0], self.initialmonsterpos[1] - self.playerpos[1])

        image_size = self.blitimg[int(self.frame)].get_size()
        adjusted_poschange = (
            poschange[0] - image_size[0] // 2, poschange[1] - image_size[1] // 2)

        self.monsterpos = adjusted_poschange

        if playerblitpos[0] < self.monsterpos[0]:
            self.blitimg = self.chosenl
        else:
            self.blitimg = self.chosenr

        self.hitbox = pygame.Rect(
            self.monsterpos[0], self.monsterpos[1], 170, 100)

        screen.blit(self.blitimg[int(self.frame)], self.monsterpos)


def distance(x1, y1, x2, y2):
    # Pre: Cordinate of two points
    # Post: returns the distance between them
    return int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


class combat():
    def __init__(self, health, characterlevel, enemyindex):
        # Pre: How much health the player has, what level is the player, whats the player' opponent's index in the monster list
        # Post: initilizing values and setting up the fight

        self.playerHP = health

        self.playerLV = characterlevel
        self.playerIMG = character().rightidle
        self.playerframe = 0

        self.playerstat = {
            'health': health,
            'attack': 25 + characterlevel * 30,
            'defense': 20 + (characterlevel - 1) * 40  # 360
        }

        self.monsertindex = enemyindex
        self.targetmonster = monsterlist[enemyindex]

        self.enemyLV = self.targetmonster.level
        self.enemmyIMG = enemy().enemyl[self.enemyLV - 1]

        self.enemyframe = 0

        attack_data = {
            1: 25,
            2: 190,
            3: 390,
            4: 600,
            5: 790
        }

        defense_data = {
            1: 5,
            2: 135,
            3: 260,
            4: 375,
            5: 999999
        }

        health_data = {
            1: 100,
            2: 200,
            3: 500,
            4: 1000,
            5: 15
        }

        self.enemystat = {
            'health': health_data[self.enemyLV],
            'attack': attack_data[self.enemyLV],
            'defense': defense_data[self.enemyLV]
        }
        self.difficulty = self.difficulty_selection()

        self.answer = self.word_selection(self.difficulty)
        self.worddisplay = "_ "*len(self.answer)

        self.correct = None
        self.font = pygame.font.SysFont('times new roman', int(15))
        self.freezefont = pygame.font.SysFont('times new roman', int(60))
        self.titlefont = pygame.font.SysFont('times new roman', int(200))

        self.errors = 0

        self.buttons = []

        self.freeze = False
        self.freezetick = 0
        self.freezetext = None
        self.freezefunctext = None

        self.initialize_buttons()

    def difficulty_selection(self):
        # Pre: None
        # Post: Determine the word's difficulty based off the enemy's levek

        if self.enemyLV == 1 or self.enemyLV == 2:
            return 'easy'

        elif self.enemyLV == 3 or self.enemyLV == 4:
            return 'medium'

        else:
            return 'hard'

    def player_attack(self):
        # Pre: None
        # Post: calculate how much damgage the player deals to the enemy based off the players damage and the enemy's defense

        damagetaken = self.playerstat['attack'] - self.enemystat['defense']
        if damagetaken < 1:
            damagetaken = 1

        self.enemystat['health'] -= damagetaken

    def enemy_attack(self):
        # Pre: None
        # Post: calculate how much damgage the enemy deals to the player based off the enemy's damage and the player's defense

        damagetaken = self.enemystat['attack'] - self.playerstat['defense']
        if damagetaken < 1:
            damagetaken = 1

        self.playerstat['health'] -= damagetaken

    def animation_update(self):
        # Pre: None
        # Post: Determine what frame both side is on

        self.playerframe += 0.05
        self.playerframe %= 3

        self.enemyframe += 0.1
        self.enemyframe %= 4

    def word_selection(self, difficulty):
        # Pre: the difficulty
        # Post: chose a word out of the difficulty's catagory

        words = open("Dictionary.txt").read().split("\n")

        difficulty_words = {
            "easy": [word for word in words if len(word) >= 10],
            "medium": [word for word in words if 7 <= len(word) < 10],
            "hard": [word for word in words if 2 < len(word) < 7]
        }

        selected_word = random.choice(difficulty_words[difficulty])

        return selected_word

    def result_check(self):
        # Pre: None
        # Post: see if the battle should end

        if self.enemystat['health'] <= 0:
            return True

        elif self.playerstat['health'] <= 0:
            return False

        else:
            return None

    def initialize_buttons(self):
        # Pre: None
        # Post:initilizing the button's positions

        for index, letter in enumerate(string.ascii_uppercase):
            y = 600
            if index > 12:
                y = 650

            x = 155 + (index % 13) * 50

            self.buttons.append(button(letter, x, y, 20, 20))

    def correct_check(self):
        # Pre: None
        # Post:check if the player's guess is correct, gives out strikes if not

        self.correct = None

        for index, letter in enumerate(self.answer):
            if letter.upper() == self.clicked_letter:
                self.worddisplay = self.worddisplay[:index *
                                                    2] + letter + self.worddisplay[index*2+1:]
                self.correct = True
                self.errors = 0

            elif letter.upper() != self.clicked_letter and self.correct == None:
                self.correct = False

        if self.correct == False:
            self.errors += 1

            if self.errors >= 2:
                self.freeze = True
                self.freezetick = 96 * (self.errors - 1)

    def win(self, phase):
        # Pre: what phase is the win animation in
        # Post: celebrates

        if phase == 1:
            winword = self.titlefont.render("Victory!", True, (255, 255, 255))

            flash_color = (255, 255, 255) if pygame.time.get_ticks(
            ) % 1000 < 500 else (0, 0, 0)
            winword.fill(flash_color, special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(winword, ((WIDTH - winword.get_size()
                        [0])//2, (HEIGHT - winword.get_size()[1])//2))

        if phase == 2:

            player.health = self.playerstat['health'] + 30

            if player.health > 100:
                player.health = 100

            player.xp += (self.enemyLV - 1) * 500

            if self.enemyLV == 1:
                player.xp += 100

            player.level_up_check()

            del monsterlist[self.monsertindex]

    def lose(self, phase):

        # Pre: What phase is the lose anumation in
        # Post: resets

        if phase == 1:
            Loseword = self.titlefont.render(
                "Defeat...", True, (255, 255, 255))

            flash_color = (255, 255, 255) if pygame.time.get_ticks(
            ) % 1000 < 500 else (0, 0, 0)
            Loseword.fill(flash_color, special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(Loseword, ((WIDTH - Loseword.get_size()
                        [0])//2, (HEIGHT - Loseword.get_size()[1])//2))

        if phase == 2:
            player.health = 1
            player.x = 9000
            player.y = 9000

            player.cameraX = 8645
            player.cameraY = 8740

        monsterlist.clear()
        self.x = 9000
        self.y = 9000
        self.speed = 10

        self.cameraX = 8645
        self.cameraY = 8740

    def draw(self):
        # Pre: None
        # Post: Draw the neccacry elements of the battle screen

        self.freezes()

        if self.freeze == False:
            for index, button_instance in enumerate(self.buttons[:]):
                button_instance.draw()
                self.clicked_letter = button_instance.button_clicked()

                if self.clicked_letter:
                    self.correct_check()
                    del self.buttons[index]

                    if self.errors == 5:
                        self.freeze = True
                        self.freezetick = 32

        self.player_check()

        screen.blit(self.playerIMG[int(self.playerframe)], (150, 200))
        screen.blit(self.enemmyIMG[int(self.enemyframe)], (600, 300))

        self.lettershow = self.font.render(
            self.worddisplay, True, (255, 255, 255))
        screen.blit(self.lettershow,
                    ((WIDTH - self.lettershow.get_size()[0])//2, 100))

        strikecount = self.font.render(
            f'Strikes: {self.errors}', True, (255, 255, 255))
        screen.blit(strikecount, (650, 550))

        for index, stats in enumerate(self.playerstat.items()):
            screen.blit(self.font.render(
                f"{stats[0]}: {stats[1]}", True, (255, 255, 255)), (50, 200 + 100 * index))

        for index, stats in enumerate(self.enemystat.items()):
            screen.blit(self.font.render(
                f"{stats[0]}: {stats[1]}", True, (255, 255, 255)), (850, 200 + 100 * index))

    def player_check(self):
        # Pre: None
        # Post: Check if the word should reset

        if self.errors >= 5:

            self.word_reset()

        elif self.worddisplay.count('_') == 0:
            self.player_attack()

            self.word_reset()

    def word_reset(self):
        # Pre: None
        # Post: Resets the word

        self.freeze = True
        self.freezetick = 96

        self.freezes()

        self.answer = self.word_selection(self.difficulty)
        self.worddisplay = "_ "*len(self.answer)

        self.correct = None

        self.errors = 0

        self.buttons = []

        self.initialize_buttons()

    def freezetext_determination(self):
        # Pre: None
        # Post: Determine what the text on the fronzen screen should be

        if self.freezefunctext == None:

            if self.errors >= 5:
                self.freezefunctext = 'reseting (four strikes): '

            elif self.worddisplay.count('_') == 0:
                self.freezefunctext = 'reseting (word completed): '

            elif self.correct == False and self.errors >= 2:
                self.freezefunctext = 'Strike penelty: '

        return self.freezefunctext

    def freezes(self):
        # Pre: None
        # Post: Calculates how much time do we need to freeze

        time = math.ceil(self.freezetick/32)

        if self.freeze:
            self.freezetick -= 1
            blitword = self.freezefont.render(
                f'{self.freezetext_determination()}{time}', True, (255, 255, 255))
            screen.blit(blitword, ((WIDTH - blitword.get_size()[0])//2, 600))

            if self.freezetick <= 0:
                self.freeze = False
                self.freezetick = 0
                self.freezefunctext = None


class button:
    def __init__(self, text, x, y, w, h):
        # Pre: Characteristics of the text
        # Post: Initilize values

        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.mouse = False
        self.clicked = False
        self.font = pygame.font.SysFont('arial', int(h))

        self.imgpos = (x, y)
        self.letterpos = (x + 5, y - 2)

    def draw(self):
        # Pre: None
        # Post: Draws the buttons

        # Deals with mousover display
        if self.mouse:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 0)
            self.letter = self.font.render(self.text, True, (0, 0, 0))
            screen.blit(self.letter, self.letterpos)
        else:
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
            self.letter = self.font.render(self.text, True, (255, 255, 255))
            screen.blit(self.letter, self.letterpos)

    # Deals with click and returned values
    def button_clicked(self):
        # Pre: None
        # Post: Determines what state the buttons is in

        pos = pygame.mouse.get_pos()
        letter_clicked = None
        self.clicked = None
        if self.rect.collidepoint(pos):
            self.mouse = True
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                letter_clicked = self.text

        else:
            self.mouse = False

        return letter_clicked


# Setting up veriables
player = character()
monsterlist = []

levelupbutton = button('Level up', 400, 20, 100, 30)

playerblitpos = (player.x - player.cameraX, player.y - player.cameraY)
playerpos = (player.x, player.y)
playercamera = (player.cameraX, player.cameraY)


move_left, move_down, move_right, move_up = False, False, False, False

inintro, ingame, inbattle = True, True, False
battle_level = None
batlletick = 0
endingtick = 0
healtick = 0

Rungame = True
while Rungame:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rungame = False
            pygame.quit()
            sys.exit()

        if ingame:
            # Character movements
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == ord('a') or event.key == ord('A'):
                    move_left = True

                elif event.key == pygame.K_RIGHT or event.key == ord('d') or event.key == ord('D'):
                    move_right = True

                elif event.key == pygame.K_UP or event.key == ord('w') or event.key == ord('W'):
                    move_up = True

                elif event.key == pygame.K_DOWN or event.key == ord('s') or event.key == ord('S'):
                    move_down = True

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT or event.key == ord('a') or event.key == ord('A'):
                    move_left = False

                elif event.key == pygame.K_RIGHT or event.key == ord('d') or event.key == ord('D'):
                    move_right = False

                elif event.key == pygame.K_UP or event.key == ord('w') or event.key == ord('W'):
                    move_up = False

                elif event.key == pygame.K_DOWN or event.key == ord('s') or event.key == ord('S'):
                    move_down = False

    screen.fill((0, 0, 0))

    if ingame:
        # Deals with everything in the 'walking' section of the game
        playerblitpos = (player.x - player.cameraX, player.y - player.cameraY)
        playerpos = (player.x, player.y)
        playercamera = (player.cameraX, player.cameraY)
        player.move(move_left, move_right, move_up, move_down)
        player.animation_update()
        player.camera_position_update()
        player.hitbox_update()

        # make sure there is no more than 50 monster in the field at once
        if len(monsterlist) < 50:
            monsterlist.append(enemy())

        # player will heal every one second when in the 'walking section'
        if player.health != 100:
            healtick += 1

            if healtick >= 160:
                player.health += 1
                healtick = 0

        # blits the monsters
        for index, creature in enumerate(monsterlist):
            creature.pos_update()
            creature.despawn(index)

            # dont blit them if they are two far away from the screen
            if distance(creature.x, creature.y, player.x, player.y) < 1500:
                creature.animation_update()
                creature.draw()

            # check if the player collides with a monster, if yes, goes to combat
            if creature.hitbox.colliderect(player.hitbox):
                inbattle = True
                fighting = combat(player.health, player.level, index)
                ingame = False
                batlletick = 0
                endingtick = 0
                battleresult = None

        # draws the level up button for testing purpoes
        levelupbutton.draw()
        clicked_button = levelupbutton.button_clicked()

        if clicked_button:
            player.xp += player.xpcap
            player.level_up_check()

        player.draw()

    # deals with everyting in the 'combat section' of the game
    if inbattle:

        # if the battle isn't over, they will keep getting blit
        if battleresult == None:
            fighting.animation_update()
            fighting.draw()

            batlletick += 1
            if batlletick >= 480:
                fighting.enemy_attack()
                batlletick = 0

            battleresult = fighting.result_check()

        if battleresult != None:
            if battleresult:
                endingtick += 1

                if endingtick <= 180:
                    fighting.win(1)
                else:
                    fighting.win(2)
                    inbattle = False
                    ingame = True
                    move_left, move_down, move_right, move_up = False, False, False, False

            else:
                endingtick += 1
                if endingtick <= 180:
                    fighting.lose(1)
                else:
                    fighting.lose(2)
                    inbattle = False
                    ingame = True
                    move_left, move_down, move_right, move_up = False, False, False, False

    pygame.display.update()
    clock.tick(32)
