from tkinter import messagebox

import pygame as pg
from pygame.locals import *

# mengatur ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Cross The Road"

# konstruktor untuk menetapkan frame rate
clock = pg.time.Clock()

# mengatur warna dalam RGB
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# Initialize font
pg.font.init()
font = pg.font.SysFont('comicsans', 75)


# Class untuk menampilkan layar
class Game:
    TICK_RATE = 60

    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        # make game screen
        self.game_screen = pg.display.set_mode((width, height))

        # fill screen with white color
        self.game_screen.fill(WHITE_COLOR)
        pg.display.set_caption(title)

        # add background image
        background_image = pg.image.load(image_path)
        # change size of image to fit the width and height
        self.image = pg.transform.scale(background_image, (width, height))

    def run_game_loop(self, lvl_spd):
        is_game_over = False
        is_win = False
        direction = 0

        # membuat instance dari class PlayerCharacter dan EnemyCharacter serta harta karun untuk menampilkan gambar
        # gambar, posisi koordinat x, posisi koordinat x, width karakter, height karakter
        player_character = PlayerCharacter('asset/pemain.png', 375, 700, 50, 50)
        enemy_character = EnemyCharacter('asset/musuh2.png', 225, 400, 50, 50)
        enemy_character.SPEED += lvl_spd
        one_piece = GameObject('asset/onepiece.png', 400, 50, 50, 50)
        print(enemy_character.SPEED)

        while not is_game_over:
            for event in pg.event.get():  # mengambil event dari keyboard
                if event.type == QUIT:
                    is_game_over = True
                # jika tombol ditekan
                elif event.type == pg.KEYDOWN:
                    # y-position berubah ke atas
                    if event.key == pg.K_UP:
                        direction = 1
                        # y-position berubah ke bawah
                    elif event.key == pg.K_DOWN:
                        direction = -1
                        # x-position berubah ke kiri
                    elif event.key == pg.K_LEFT:
                        direction = 2
                        # x-position berubah ke kanan
                    elif event.key == pg.K_RIGHT:
                        direction = -2
                        # keluar dari game
                    elif event.key == pg.K_ESCAPE:
                        is_game_over = True
                # jika tombol dilepas
                elif event.type == pg.KEYUP:
                    # jika tombol atas atau bawah dilepas, maka karakter berhenti
                    if event.key == pg.K_UP or event.key == pg.K_DOWN:
                        direction = 0
                    elif event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                        direction = 0
                print(event)

            # me-refresh background tiap kali karakter berjalan
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image, (0, 0))

            # menambahkan nilai direction ke method move di class player_character
            player_character.move(direction, self.height)
            # menambahkan nilai width ke method move di class enemy_character
            enemy_character.move(self.width)

            # menampilkan player, enemy, dan harta karun
            player_character.draw(self.game_screen)
            enemy_character.draw(self.game_screen)
            one_piece.draw(self.game_screen)

            # collision detection
            if player_character.detection_collision(enemy_character):
                is_game_over = True
                is_win = False
                messagebox.showinfo("You lose!", "Try Again!")
                pg.display.update()
                clock.tick(1)

            elif player_character.detection_collision(one_piece):
                is_game_over = True
                is_win = True
                messagebox.showinfo("You won!", "Congratulations, you have won the game!")
                pg.display.update()
                clock.tick(1)

            # update layar
            pg.display.update()
            clock.tick(self.TICK_RATE)

        if is_win:
            lvl_spd += 5
            self.run_game_loop(lvl_spd)


# Superclass for character
class GameObject:
    def __init__(self, image_path, x, y, width, height):
        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

        # take image from path
        object_image = pg.image.load(image_path)
        # change size of image to fit the width and height
        self.image = pg.transform.scale(object_image, (width, height))

    # method to draw object
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


# Player  Character Class
class PlayerCharacter(GameObject):

    # Define speed variable
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, direction, max_height):
        # direction = 1 is up, -1 is down, 2 is left, -2 is right
        # (0,0) of pygame is at the top left of the screen, so y_pos will decrease when moving up and vice versa
        if direction == 1:  # when up key is pressed
            self.y_pos -= self.SPEED
            if self.y_pos <= 0:  # top boundary
                self.y_pos = 0
        elif direction == -1:  # when down key is pressed
            self.y_pos += self.SPEED
            if self.y_pos >= max_height - 70:  # bottom boundary
                self.y_pos = max_height - 70
        elif direction == 2:  # when left key is pressed
            self.x_pos -= self.SPEED
            if self.x_pos <= 20:  # left boundary
                self.x_pos = 0
        elif direction == -2:  # when right key is pressed
            self.x_pos += self.SPEED
            if self.x_pos >= max_height - 70:  # right boundary
                self.x_pos = max_height - 70

    def detection_collision(self, other_body):
        # if player position in y axis + player height is less than enemy position in y axis
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        # if player position in y axis is greater than enemy position in y axis + enemy height
        elif self.y_pos + self.height < other_body.y_pos:
            return False

        # if player position in x axis + player width is less than enemy position in x axis
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        # if player position in x axis is greater than enemy position in x axis + enemy width
        elif self.x_pos + self.width < other_body.x_pos:
            return False

        # if none of the above is true, then there is a collision
        return True


# Enemy Character Class & Bounds Checking
class EnemyCharacter(GameObject):
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, max_width):  # max_width param is the width of the screen
        # if x position is less than 20 or at the left edge, 20 is the left boundary
        if self.x_pos <= 20:  # left boundary
            self.SPEED = abs(self.SPEED)  # change speed to positive value
        # if x position is greater than max_width - 70 or at the right edge, 70 is the right boundary
        elif self.x_pos >= max_width - 70:  # right boundary
            self.SPEED = -abs(self.SPEED)  # change speed to negative value

        self.x_pos += self.SPEED  # move enemy character


pg.init()
# buat instance game
new_game = Game('asset/background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
# run game loop
new_game.run_game_loop(0)

# keluar dari game
pg.quit()
quit()
