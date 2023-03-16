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


class Game:
    TICK_RATE = 60

    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        # menampilkan screen
        self.game_screen = pg.display.set_mode((width, height))
        # mengisi background saat awal permainan dengan warna putih
        self.game_screen.fill(WHITE_COLOR)
        pg.display.set_caption(title)

    def run_game_loop(self):
        is_game_over = False
        direction = 0

        # membuat instance dari class PlayerCharacter
        player_character = PlayerCharacter('asset/musuh2.png', 375, 700, 50, 50)

        while not is_game_over:
            for event in pg.event.get():
                if event.type == QUIT:
                    is_game_over = True
                # jika tombol ditekan
                elif event.type == pg.KEYDOWN:  # dictionary: type=key, pg.KEYDOWN=value
                    if event.key == pg.K_UP:  # y-position berubah ke atas
                        direction = 1
                    elif event.key == pg.K_DOWN:  # y-position berubah ke bawah
                        direction = -1
                    elif event.key == pg.K_ESCAPE:  # keluar dari game
                        is_game_over = True
                # jika tombol dilepas
                elif event.type == pg.KEYUP: # dictionary: type=key, pg.KEYUP=value
                    if event.key == pg.K_UP or event.key == pg.K_DOWN: # jika tombol atas atau bawah dilepas
                        direction = 0
                print(event)

            # me-refresh background tiap kali karakter berjalan
            self.game_screen.fill(WHITE_COLOR)
            # menambahkan nilai direction ke method move di class player_character
            player_character.move(direction)
            # menampilkan screen game | juga menggunakan method didalam class player_character
            player_character.draw(self.game_screen)

            pg.display.update()  # update layar
            clock.tick(self.TICK_RATE)


# membuat class untuk karakter
class GameObject:
    def __init__(self, image_path, x, y, width, height):
        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

        object_image = pg.image.load(image_path)  # mengambil gambar
        self.image = pg.transform.scale(object_image, (width, height))  # mengubah ukuran gambar

    # method untuk menampilkan gambar
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


class PlayerCharacter(GameObject):  # subclass

    SPEED = 10  # KECEPATAN DALAM FRAME PER SECOND

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, direction):
        # direction adalah -1 untuk ke bawah, 1 untuk ke atas
        if direction > 0:  # ke atas
            self.y_pos -= self.SPEED
        elif direction < 0:  # ke bawah
            self.y_pos += self.SPEED


pg.init()
# buat instance game
new_game = Game(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop()

# keluar dari game
pg.quit()
quit()
