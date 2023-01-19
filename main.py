import pygame
import os
import sys
import random
import sqlite3


# создаём различные группы спрайтов
# группу для горизонтальных линий, которые ограничивают экран
horizontal_borders = pygame.sprite.Group()
# группу для вертикальных линий, которые ограничивают экран
vertical_borders = pygame.sprite.Group()
# группу для анимированных спрайтов
animated_sprites = pygame.sprite.Group()
# группу для остальных спрайтов
all_sprites = pygame.sprite.Group()
# указываем размеры экрана
size = width, height = 700, 700
screen = pygame.display.set_mode(size)
WIDTH = 700
HEIGHT = 700
# создаём перемененную, в которой указываем количество кадров в секунду
FPS = 50
# создаём перемененную, в которой указываем шаг героя
STEP = 25
# создаём перемененную, в которой указываем его начальные координаты
# (мы их преобразуем в стандартный вид в классе самого героя)
x0, y0 = 5, 5
clock = pygame.time.Clock()
window = pygame.display.set_mode((700, 700))
# устанавливаем название окна игры
pygame.display.set_caption('MOM_PUDGE')
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
# подключаем базу данных
con = sqlite3.connect('Game.db')
cur = con.cursor()
# инициализируем pygame
pygame.init()
# подключаем музыкальное сопровождение
pygame.mixer.music.load("data/pudge_musik.mp3")
# создаём различные вариации уровней
# первый уровень сложности
image_1 = 'frog.jpg'
quantity_1 = 5
# второй уровень сложности
image_2 = 'bee.jpg'
quantity_2 = 7
# третий уровень сложности
image_3 = 'mom.png'
quantity_3 = 10


# создаём функцию для загрузки изображений
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# функция для закрытия программы
def terminate():
    pygame.quit()
    sys.exit()


# начальный экран
def start_screen():
    # убираем с экрана мышь
    pygame.mouse.set_visible(False)
    # в переменную запишем текст, который выведем на экран
    intro_text = ["MOM_PUDGE", "",
                  "Правила игры:",
                  "Вы - персонаж с крюком.",
                  "Ваша задача увернуться от летающих",
                  "врагов. Управление: стрелочки.",
                  "Если вы коснётесь границ экрана,",
                  "то телепортируетесь в его центр."]
    # загружаем изображение, которое будем использовать в качестве фона
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# экран, который покажется в случае поражения
def lose_screen():
    # загружаем изображение, которое будем использовать в качестве фона
    fon = pygame.transform.scale(load_image('fon_2.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    animated_sprites.add(dragon_1)
    animated_sprites.add(dragon_2)
    animated_sprites.add(dragon_3)
    animated_sprites.add(dragon_4)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        animated_sprites.draw(screen)
        animated_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
        cur.execute(f"DELETE from Levels")
        con.commit()


# экран, на котором будет отображаться лучший результат
def result_screen():
    # результаты по прохождению первого уровня сложности мы ищем в базе данных sqlite3
    result_text = cur.execute("SELECT time FROM Results WHERE level = 1").fetchall()
    # затем ищем среди всех результатов лучший и переводим его в текстовый формат
    times = list()
    li = list()
    for i in result_text:
        for j in i:
            times.append(j)
    # проверка на случай, если результатов нет
    if times != li:
        best_time1 = max(times)
        if best_time1 < 60:
            best_time1 = str(best_time1)
        else:
            time_a = best_time1 // 60
            time_b = best_time1 % 60
            if time_a < 10:
                time_a = '0' + str(time_a)
            if time_b < 10:
                time_b = '0' + str(time_b)
            best_time1 = str(time_a) + ':' + str(time_b)
    else:
        best_time1 = 'уровень не пройден'
    # результаты по прохождению второго уровня сложности мы ищем в базе данных sqlite3
    result_text = cur.execute("SELECT time FROM Results WHERE level = 2").fetchall()
    # затем ищем среди всех результатов лучший и переводим его в текстовый формат
    times = list()
    li = list()
    for i in result_text:
        for j in i:
            times.append(j)
    # проверка на случай, если результатов нет
    if times != li:
        best_time2 = max(times)
        if best_time2 < 60:
            best_time2 = str(best_time2)
        else:
            time_a = best_time2 // 60
            time_b = best_time2 % 60
            if time_a < 10:
                time_a = '0' + str(time_a)
            if time_b < 10:
                time_b = '0' + str(time_b)
            best_time2 = str(time_a) + ':' + str(time_b)
    else:
        best_time2 = 'уровень не пройден'
    # результаты по прохождению третьего уровня сложности мы ищем в базе данных sqlite3
    result_text = cur.execute("SELECT time FROM Results WHERE level = 3").fetchall()
    # затем ищем среди всех результатов лучший и переводим его в текстовый формат
    times = list()
    li = list()
    for i in result_text:
        for j in i:
            times.append(j)
    # проверка на случай, если результатов нет
    if times != li:
        best_time3 = max(times)
        if best_time3 < 60:
            best_time3 = str(best_time3)
        else:
            time_a = best_time3 // 60
            time_b = best_time3 % 60
            if time_a < 10:
                time_a = '0' + str(time_a)
            if time_b < 10:
                time_b = '0' + str(time_b)
            best_time3 = str(time_a) + ':' + str(time_b)
    else:
        best_time3 = 'уровень не пройден'
    # делаем так, чтобы лучший результат по каждому уровню отображался на экране
    intro_text = ['1 уровень:', str(best_time1),
                  '2 уровень:', str(best_time2),
                  '3 уровень:', str(best_time3)]
    # загружаем изображение, которое будем использовать в качестве фона
    fon = pygame.transform.scale(load_image('momchik.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# создаём класс для создания анимации спрайтов
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

# функция, которая разрезает изображение
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


# создаём класс меню
class Menu:
    def __init__(self, punkts=[120, 140, u'Punkt', (250, 250, 30), (250, 30, 250), 0],
                 punkts_2=[120, 140, u'Punkt', (250, 250, 30), (250, 30, 250), 0]):
        self.punkts = punkts
        self.punkts_2 = punkts_2

    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], int(i[1]) - 30))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], int(i[1]) - 30))

    def render_2(self, poverhnost, font, num_punkt):
        for i in self.punkts_2:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], int(i[1]) - 30))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], int(i[1]) - 30))

    def menu(self):
        done = True
        f1 = pygame.font.get_fonts()
        f2 = pygame.font.match_font(f1[4])
        font_menu = pygame.font.Font(f2, 50)
        pygame.key.set_repeat(0, 0)
        # возвращаем мышь на экран
        pygame.mouse.set_visible(True)
        punkt = 0
        flPause = False
        while done:
            screen.fill((0, 150, 250))
            mp = pygame.mouse.get_pos()
            for i in punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cur.execute(f"DELETE from Levels")
                    con.commit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # при нажатии кнопки escape в меню, программа закроется
                    if event.key == pygame.K_ESCAPE:
                        cur.execute(f"DELETE from Levels")
                        con.commit()
                        sys.exit()
                    if event.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if event.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                    # нажатием пробела в меню можно выключить/включать музыку
                    if event.key == pygame.K_SPACE:
                        flPause = not flPause
                        if flPause:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # делаем так, чтобы при нажатии кнопки 'Play', игрок мог выбрать уровень
                    if punkt == 0:
                        self.menu_2()
                        done = False
                    # делаем так, чтобы при нажатии кнопки "Quit", игра закрывалась
                    elif punkt == 4:
                        sys.exit()
                    # делаем так, чтобы в случае возникновения бага, при открытии уровня, игрок мог его исправить
                    elif punkt == 4:
                        cur.execute(f"DELETE from Levels")
                        con.commit()
                    # делаем так, чтобы при нажатии кнопки "Delete Results", удалялись все результаты
                    elif punkt == 2:
                        cur.execute(f"DELETE from Results")
                        con.commit()
                    # делаем так, чтобы при нажатии кнопки "Best Result", открывался экран, на котором
                    # отобразится лучший результат, если он есть
                    elif punkt == 1:
                        result_screen()
            window.blit(screen, (0, 30))
            pygame.display.flip()

    def menu_2(self):
        done = True
        f1 = pygame.font.get_fonts()
        f2 = pygame.font.match_font(f1[4])
        font_menu = pygame.font.Font(f2, 50)
        pygame.key.set_repeat(0, 0)
        punkt = 0
        flPause = False
        while done:
            screen.fill((0, 150, 250))
            mp = pygame.mouse.get_pos()
            for i in punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
            self.render_2(screen, font_menu, punkt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cur.execute(f"DELETE from Levels")
                    con.commit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # при нажатии кнопки escape в меню, программа закроется
                    if event.key == pygame.K_ESCAPE:
                        cur.execute(f"DELETE from Levels")
                        con.commit()
                        sys.exit()
                    if event.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if event.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                    # нажатием пробела в меню можно выключить/включать музыку
                    if event.key == pygame.K_SPACE:
                        flPause = not flPause
                        if flPause:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # реализуем первый уровень сложности (меньше врагов)
                    if punkt == 0:
                        cur.execute(f"INSERT INTO Levels(image,quantity) VALUES('{image_1}','{quantity_1}')")
                        con.commit()
                        done = False
                    # реализуем второй уровень сложности (умеренное количество врагов)
                    elif punkt == 1:
                        cur.execute(f"INSERT INTO Levels(image,quantity) VALUES('{image_2}','{quantity_2}')")
                        con.commit()
                        done = False
                    # реализуем третий уровень сложности (много врагов)
                    elif punkt == 2:
                        cur.execute(f"INSERT INTO Levels(image,quantity) VALUES('{image_3}','{quantity_3}')")
                        con.commit()
                        done = False
            window.blit(screen, (0, 30))
            pygame.display.flip()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = enemy_image
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.collide_mask(self, pudge):
            cur.execute(f"INSERT INTO Results(time,level) VALUES({counter},{num_level})")
            con.commit()
            lose_screen()


pudge_image = load_image('pudge.png')
tile_width = tile_height = 50


# создаём класс нашего героя
class Pudge(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pudge_image
        # даём ему маску
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.mask = pygame.mask.from_surface(self.image)

    def tp(self):
        self.rect = self.image.get_rect().move(300, 300)


# создаём список значений для создания меню
punkts = [(220, 190, u'Play', (250, 250, 30), (250, 30, 250), 0),
          (220, 260, u'Best Result', (250, 250, 30), (250, 30, 250), 1),
          (220, 330, u'Delete Results', (250, 250, 30), (250, 30, 250), 2),
          (220, 400, u'Debug Button', (250, 250, 30), (250, 30, 250), 3),
          (220, 470, u'Quit', (250, 250, 30), (250, 30, 250), 4)]
# создаём список значений для создания меню с выбором уровней
punkts_2 = [(240, 210, u'Level_1', (250, 250, 30), (250, 30, 250), 0),
            (240, 280, u'Level_2', (250, 250, 30), (250, 30, 250), 1),
            (240, 350, u'Level_3', (250, 250, 30), (250, 30, 250), 2)]
game = Menu(punkts, punkts_2)
game.menu()
level = cur.execute("SELECT * FROM Levels").fetchall()[0]
# разделяем загруженные из БД данные на название изображения и количество врагов
image_main, quantity_main = level
# переводим количество врагов из текстового формата в числовой
quantity_main = int(quantity_main)
# загружаем изображение для спрайта, который будет выступать в роли врага
enemy_image = load_image(image_main)
if image_main == image_1 and quantity_main == quantity_1:
    num_level = 1
elif image_main == image_2 and quantity_main == quantity_2:
    num_level = 2
elif image_main == image_3 and quantity_main == quantity_3:
    num_level = 3
# добавляем сообщение на случай ошибки
else:
    num_level = 'произошла ошибка или вы не прошли ни одного уровня'


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    def update(self):
        if pygame.sprite.collide_mask(self, pudge):
            pudge.tp()


# создаём нашего персонажа
pudge = Pudge(x0, y0)
# создаём анимированный спрайт
dragon_1 = AnimatedSprite(load_image("dragon.png"), 8, 2, 600, 10)
dragon_2 = AnimatedSprite(load_image("dragon.png"), 8, 2, 10, 10)
dragon_3 = AnimatedSprite(load_image("dragon.png"), 8, 2, 600, 620)
dragon_4 = AnimatedSprite(load_image("dragon.png"), 8, 2, 10, 620)

if __name__ == '__main__':
    pygame.init()
    running = True
    start_screen()
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    counter, text = 0, '0'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)
    # создаём определённое количество врагов (в зависимости от уровня)
    for i in range(quantity_main):
        Enemy(20, 100, 100)
    clock = pygame.time.Clock()
    running = True
    flPause = False
    pygame.mixer.music.play(-1)
    # делаем так, чтобы во время игры драконов не было видно
    dragon_1.kill()
    dragon_2.kill()
    dragon_3.kill()
    dragon_4.kill()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cur.execute(f"DELETE from Levels")
                con.commit()
                running = False
            elif event.type == pygame.KEYDOWN:
                # настраиваем перемещение героя
                # шаг влево
                if event.key == pygame.K_LEFT:
                    pudge.rect.x -= STEP
                # шаг вправо
                if event.key == pygame.K_RIGHT:
                    pudge.rect.x += STEP
                # шаг вверх
                if event.key == pygame.K_UP:
                    pudge.rect.y -= STEP
                # шаг вниз
                if event.key == pygame.K_DOWN:
                    pudge.rect.y += STEP
                # добавляем возможность включить/выключить музыку во время игры на пробел
                if event.key == pygame.K_SPACE:
                    flPause = not flPause
                    if flPause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                # добавляем возможность выйти в меню на escape
                if event.key == pygame.K_ESCAPE:
                    game.menu()
            # добавляем таймер
            if event.type == pygame.USEREVENT:
                counter += 1
                text = str(counter).rjust(3)
        screen.fill(pygame.Color("white"))
        # загружаем изображение, которое будет фоном
        fon = pygame.transform.scale(load_image('mid.jpg'), (WIDTH, HEIGHT))
        # устанавливаем загруженное изображение в качестве фона
        screen.blit(fon, (0, 0))
        screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
        # рисуем спрайты, кроме анимированных
        player_group.draw(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    con.close()
