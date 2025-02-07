import random
import copy
import pygame
import tkinter as tk
import cv2 as cv
import os
import numpy

class Tetris:
    def __init__(self):
        #window sizes
        self.margin_size = 240
        self.monitor_size = self.get_screen_height()
        self.height = 800 if self.monitor_size != 720 else 700
        self.width = 400 + (self.margin_size*2)
        self.rows = 20 if self.monitor_size != 720 else 16
        self.columns = 10

        #pygame logic
        pygame.init()
        pygame.mixer.init()
        self.font_file = 'Fonts/OpenSans-Regular.TTF'
        self.font = pygame.font.Font(self.font_file, 25)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        #dictionaries
        self.colorlist = {
            0: (0, 0, 0),
            1: (240, 160, 0),
            2: (0, 0, 240),
            3: (240, 240, 0),
            4: (0, 240, 0),
            5: (240, 0, 0),
            6: (160, 0, 240),
            7: (0, 240, 240),
            8: (0, 0, 0),
        }
        self.pointlist = {
            0: 0,
            1: 100,
            2: 300,
            3: 500,
            4: 800
        }
        self.pointsounds = {
            1: pygame.mixer.Sound('Tetris sounds/SingleSFX.mp3'),
            2: pygame.mixer.Sound('Tetris sounds/DoubleSFX.mp3'),
            3: pygame.mixer.Sound('Tetris sounds/TripleSFX.mp3'),
            4: pygame.mixer.Sound('Tetris sounds/TetrisSFX.mp3'),
        }

        #block falling speed
        self.speed = {
            0: 48,
            1: 43,
            2: 38,
            3: 33,
            4: 28,
            5: 23,
            6: 18,
            7: 13,
            8: 8,
            9: 6,
            10: 5,
            11: 5,
            12: 5,
            13: 4,
            14: 4,
            15: 4,
            16: 3,
            17: 3,
            18: 3,
            19: 2
        }

        #shapes
        self.Lshape = {
            1: [[0, 1, 0],
                [0, 1, 0],
                [0, 1, 1]],

            2: [[0, 0, 0],
                [1, 1, 1],
                [1, 0, 0]],

            3: [[1, 1, 0],
                [0, 1, 0],
                [0, 1, 0]],

            4: [[0, 0, 1],
                [1, 1, 1],
                [0, 0, 0]],
        }
        self.Reverse_Lshape = {
            1: [[0, 2, 0],
                [0, 2, 0],
                [2, 2, 0]],

            2: [[2, 0, 0],
                [2, 2, 2],
                [0, 0, 0]],

            3: [[0, 2, 2],
                [0, 2, 0],
                [0, 2, 0]],

            4: [[0, 0, 0],
                [2, 2, 2],
                [0, 0, 2]],
        }
        self.Squareshape = {
            1: [[3, 3],
                [3, 3]],
            2: [[3, 3],
                [3, 3]],
            3: [[3, 3],
                [3, 3]],
            4: [[3, 3],
                [3, 3]],
        }
        self.Sshape = {
            1: [[0, 4, 4],
                [4, 4, 0],
                [0, 0, 0]],

            2: [[0, 4, 0],
                [0, 4, 4],
                [0, 0, 4]],

            3: [[0, 0, 0],
                [0, 4, 4],
                [4, 4, 0]],

            4: [[4, 0, 0],
                [4, 4, 0],
                [0, 4, 0]],
        }
        self.Zshape = {
            1: [[5, 5, 0],
                [0, 5, 5],
                [0, 0, 0]],

            2: [[0, 0, 5],
                [0, 5, 5],
                [0, 5, 0]],

            3: [[0, 0, 0],
                [5, 5, 0],
                [0, 5, 5]],

            4: [[0, 5, 0],
                [5, 5, 0],
                [5, 0, 0]],
        }
        self.Tshape = {
            1: [[0, 6, 0],
                [6, 6, 6],
                [0, 0, 0]],

            2: [[0, 6, 0],
                [0, 6, 6],
                [0, 6, 0]],

            3: [[0, 0, 0],
                [6, 6, 6],
                [0, 6, 0]],

            4: [[0, 6, 0],
                [6, 6, 0],
                [0, 6, 0]],
        }
        self.Lineshape = {
            1: [[0, 7, 0, 0],
                [0, 7, 0, 0],
                [0, 7, 0, 0],
                [0, 7, 0, 0]],

            2: [[0, 0, 0, 0],
                [7, 7, 7, 7],
                [0, 0, 0, 0],
                [0, 0, 0, 0]],

            3: [[0, 0, 7, 0],
                [0, 0, 7, 0],
                [0, 0, 7, 0],
                [0, 0, 7, 0]],

            4: [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [7, 7, 7, 7],
                [0, 0, 0, 0]],
        }

        #variables
        self.shapelist = [self.Lshape, self.Reverse_Lshape, self.Tshape, self.Squareshape, self.Lineshape, self.Sshape, self.Zshape]
        self.TemporaryMap, self.Map, self.nextmap, self.level, self.points, self.show_cleared_rows, self.count_cleared_rows, self.currentframe, self.current_shape, self.next_shape, self.next_next_shape, self.next_next_next_shape, self.held_shape, self.shape_rotation, self.shape_pos_x, self.shape_pos_y = self.start()
        
        self.square_border_width = 1
        self.square_size = (self.width - (self.margin_size*2)) / self.columns
        self.gray = (100, 100, 100)

        self.running = True
        self.mainmenu = True
        self.gameover = False
        self.paused = False

        self.mousemode = False
        self.Rclick = 1
        self.Lclick = 3
        self.mousescrollup = 4
        self.mousescrolldown = 5

        self.stoppedbuttonsY = self.height / 2 - 150
        self.keybindY = 200
        self.Keybindbuttondistance = 50

        self.stoppedscreen = pygame.Surface((self.width, self.height))
        self.stoppedscreen.fill((50, 50, 50))
        self.stoppedscreen.set_alpha(128)

        self.paused_reset_rect = pygame.Rect(self.width/2-100, self.stoppedbuttonsY+100, 200, 40)
        self.paused_options_rect = pygame.Rect(self.width/2-100, self.stoppedbuttonsY+175, 200, 40)
        self.paused_return_rect = pygame.Rect(self.width/2-100, self.stoppedbuttonsY+250, 300, 40)
        self.paused_quit_rect = pygame.Rect(self.width/2-100, self.stoppedbuttonsY+325, 200, 40)

        self.X_rect = pygame.Rect(45, 100, 50, 50)


        self.inputdelay = 5

        self.temp_Y_holder = None

        self.FPS = 60

        self.clicked = False

        self.lockingin = False
        self.lockdelay = 30
        self.lockframe = 0

        self.harddropped = False

        self.square_border_width = 1
        self.square_size = (self.width - (self.margin_size * 2)) / self.columns
        self.gray = (100, 100, 100)

        self.temp_shape_holder = None
        self.can_switch = True

        self.optionsmenu = False

        self.KeybindsMenu = False
        self.Keybindchanging = False
        self.changedKeybind = ''

        self.error_message = False

        self.mapmouseX = 0

        self.Keybinds = {
            'down': pygame.K_s,
            'left': pygame.K_a,
            'right': pygame.K_d,
            'rotate': pygame.K_w,
            'harddrop': pygame.K_SPACE,
            'hold': pygame.K_e,
        }

        #audio variables
        pygame.mixer.music.load('Tetris sounds/BackgroundMusic.mp3')
        self.startbackgroundmusic = False

        self.GameoverSFX = pygame.mixer.Sound('Tetris sounds/GameoverSFX.mp3')
        self.PauseSFX = pygame.mixer.Sound('Tetris sounds/PauseSFX.mp3')
        self.LevelupSFX = pygame.mixer.Sound('Tetris sounds/LevelupSFX.mp3')

        self.HarddropSFX = pygame.mixer.Sound('Tetris sounds/HarddropSFX.mp3')
        self.HoldSFX = pygame.mixer.Sound('Tetris sounds/HoldSFX.mp3')
        self.LandingSFX = pygame.mixer.Sound('Tetris sounds/LandingSFX.mp3')
        self.MoveSFX = pygame.mixer.Sound('Tetris sounds/MoveSFX.mp3')
        self.RotateSFX = pygame.mixer.Sound('Tetris sounds/RotateSFX.mp3')
        self.SoftdropSFX = pygame.mixer.Sound('Tetris sounds/SoftdropSFX.mp3')

        self.Backgroundmusic_volume = 0.2
        self.SFX_volume = 0.2  
        self.previous_SFX_volume = self.SFX_volume

        pygame.mixer.music.set_volume(self.Backgroundmusic_volume)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

        self.pointsounds[1].set_volume(self.SFX_volume)
        self.pointsounds[2].set_volume(self.SFX_volume)
        self.pointsounds[3].set_volume(self.SFX_volume)
        self.pointsounds[4].set_volume(self.SFX_volume)

        self.GameoverSFX.set_volume(self.SFX_volume)
        self.PauseSFX.set_volume(self.SFX_volume)
        self.LevelupSFX.set_volume(self.SFX_volume)

        self.HarddropSFX.set_volume(self.SFX_volume)
        self.HoldSFX.set_volume(self.SFX_volume)
        self.LandingSFX.set_volume(self.SFX_volume)
        self.MoveSFX.set_volume(self.SFX_volume)
        self.RotateSFX.set_volume(self.SFX_volume)
        self.SoftdropSFX.set_volume(self.SFX_volume)

        self.audiomenu = False
        

        self.Backgroundaudio_slider = self.Slider(self,x= 65, y=340, width=200, min_value=0.0, max_value=1.0, initial_value=self.Backgroundmusic_volume, color=(255, 0, 0), background_color=(200, 200, 200))
        self.SFXaudio_slider = self.Slider(self,x= 65, y= 540, width=200, min_value=0.0, max_value=1.0, initial_value=self.Backgroundmusic_volume, color=(255, 0, 0), background_color=(200, 200, 200))

        #scoreboard
        self.scoreboard = self.Scoreboard(self)

        #customization menu
        self.customization_menu = False
        self.customization_class = self.Customize_menu(self, self.colorlist)
    
        #Ads
        self.playingAD = False
        self.ad_rect = pygame.Rect(self.width/2 - 104, self.height/2 + 100, 208, 40)
        self.Ad_path = 'Add filepath here'
        self.Ad_file_names = self.list_files_in_directory(self.Ad_path)
        self.Ad = None

        self.timer = self.CountdownTimer(initial_counter=5, x = self.width / 2, y = self.height / 2, font_size=100)
        self.start_timer = True

        #Game modes
        self.gamemodemenu = False
        self.puzzlemode_rect = pygame.Rect(55, 200, 450, 100)
        self.puzzlemode = False
        
    def get_screen_height(self):
        root = tk.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return height

    def subtract_RGB(self, color, subtract_value):
        return tuple(max(0, value - subtract_value) for value in color)

    def find_color(self, shape):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 0:
                    return shape[i][j]

    def draw(self, x, y, shape, is_ghost=False):
        if not is_ghost:
            self.Map = [row[:] for row in self.TemporaryMap]
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 0:
                    if is_ghost and self.Map[y + i][x + j] != 0:
                        continue  
                    self.Map[y + i][x + j] = 8 if is_ghost else shape[i][j]  
        return self.Map

    def drawnext(self, x, y, shape, square_size):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 0:
                    pygame.draw.rect(self.screen, self.colorlist[shape[i][j]], pygame.Rect(x + j * square_size, y + i * square_size, square_size, square_size))
                    pygame.draw.rect(self.screen, self.gray, pygame.Rect(x + j * square_size, y + i * square_size, square_size, square_size), self.square_border_width)

    def is_valid_move(self,x, y, shape):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 0:
                    if x + j < 0 or x + j >= self.columns or y + i >= self.rows:
                        return False
                    if y + i >= 0 and self.TemporaryMap[y + i][x + j] != 0:
                        return False  
        return True

    def ghostpieceY(self,x,y,shape):
        ghost_Y = y
        while self.is_valid_move(x,ghost_Y, shape):
            ghost_Y += 1
        return ghost_Y - 1

    def lockin(self,x, y, shape):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 0:
                    self.TemporaryMap[y + i][x + j] = shape[i][j]

    def check(self, row):
        return all(cell != 0 for cell in row)

    def clear(self,map):
        new_map = [row for row in map if not self.check(row)]
        cleared_rows = int(len(map) - len(new_map))
        if not self.puzzlemode:
            new_map = [[0] * self.columns for _ in range(cleared_rows)] + new_map
        else:
            new_map = map
            cleared_rows = 0
        return new_map, cleared_rows

    def start(self):
        TemporaryMap = [[0 for i in range(self.columns)] for j in range(self.rows)]
        Map = [row[:] for row in TemporaryMap]  
        nextmap = [[0 for i in range(5)] for j in range(4)]

        level = 0
        points = 0
        show_cleared_rows = 0
        count_cleared_rows = 0

        currentframe = 0

        current_shape = random.choice(self.shapelist)
        next_shape = random.choice(self.shapelist)
        next_next_shape = random.choice(self.shapelist)
        next_next_next_shape = random.choice(self.shapelist)
        held_shape = None
        shape_rotation = 1
        shape_pos_x = 3 
        shape_pos_y = 0

        return TemporaryMap, Map, nextmap, level, points, show_cleared_rows, count_cleared_rows, currentframe, current_shape, next_shape, next_next_shape, next_next_next_shape, held_shape,shape_rotation, shape_pos_x, shape_pos_y

    def list_files_in_directory(self, directory):
        files = []
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path):
                files.append(entry)
        return files

    class Scoreboard:
        def __init__(self, main, filename="Tetrisscores.txt", max_scores=5, x = 10, y = 400):
            self.main = main
            self.x = x
            self.y = y
            self.filename = filename
            self.max_scores = max_scores
            self.scores = self.load_scores()
            self.WHITE = (255, 255, 255)

        def load_scores(self):
            try:
                with open(self.filename, "r") as f:
                    scores = [int(line.strip()) for line in f]
                scores.sort(reverse=True)
                return scores[:self.max_scores]
            except FileNotFoundError:
                return [0] * self.max_scores

        def save_scores(self):
            with open(self.filename, "w") as f:
                for score in self.scores:
                    f.write(f"{score}\n")

        def update_high_scores(self, new_score):
            if new_score > self.scores[-1]:
                self.scores.append(new_score)
                self.scores.sort(reverse=True)
                self.scores = self.scores[:self.max_scores]
                self.save_scores()

        def display_high_scores(self, screen):
            y = self.y
            for i, score in enumerate(self.scores):
                score_text = self.main.font.render(f"{i+1}. {score}", True, self.WHITE)
                screen.blit(score_text, (self.x, y))
                y += 40

    class Slider:
        def __init__(self, main, x, y, width, min_value, max_value, initial_value, color, background_color):
            self.main = main
            self.rect = pygame.Rect(x, y, width, 20)
            self.color = color
            self.background_color = background_color
            self.min_value = min_value
            self.max_value = max_value
            self.value = initial_value
            self.handle_width = 20
            self.handle_x = self._value_to_x(initial_value)
            self.dragging = False

        def _value_to_x(self, value):
            range_width = self.rect.width - self.handle_width
            return int(self.rect.x + (value - self.min_value) / (self.max_value - self.min_value) * range_width)

        def _x_to_value(self, x):
            range_width = self.rect.width - self.handle_width
            return self.min_value + (x - self.rect.x) / range_width * (self.max_value - self.min_value)

        def draw(self, screen):
            pygame.draw.rect(screen, self.background_color, self.rect)
            handle_rect = pygame.Rect(self.handle_x, self.rect.y, self.handle_width, self.rect.height)
            pygame.draw.rect(screen, self.color, handle_rect)

        def update(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.collidepoint(event.pos):
                    self.dragging = True
                    self._update_handle_x(event.pos[0])
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self._update_handle_x(event.pos[0])

        def _update_handle_x(self, mouse_x):
            new_handle_x = max(self.rect.x, min(mouse_x, self.rect.right - self.handle_width))
            if new_handle_x != self.handle_x:
                self.handle_x = new_handle_x
                self.value = self._x_to_value(new_handle_x)

        def get_value(self):
            return self.value

    class Customize_menu:
        def __init__(self, main, colorlist):
            self.main = main
            self.colorlist = colorlist
            self.default = copy.deepcopy(colorlist)
            self.menu_width = 400
            self.menu_height = 580
            self.selected_index = 0
            self.menu_x = 45
            self.menu_y = 100
            self.gray = (100,100,100)

            self.button_x = self.menu_x + 40
            self.button_y = self.menu_y + 45
            self.button_move = 0
            self.button_width = 320
            self.button_height = 40
            self.button_border = 2
            self.button_distance = 20 + self.button_height
            self.button_names = {
                0: 'Empty area:',
                1: 'Lshape:',
                2: 'Reverse_Lshape:',
                3: 'Squareshape:',
                4: 'Sshape:',
                5: 'Zshape:',
                6: 'Tshape:',
                7: 'Lineshape:',
                8: 'Ghost piece:',
            }

            self.input_active = False
            self.color_input = ''

            self.default_rect = pygame.Rect(self.menu_x, self.menu_y + 50, 30,30)
        def draw(self):
            button_y = self.button_y
            pygame.draw.rect(self.main.screen, self.gray, self.default_rect)
            self.main.screen.blit(self.main.font.render('R', True, (255,255,255)) ,(self.default_rect.x+5, self.default_rect.y))
            self.main.screen.blit(self.main.font.render(f'({self.color_input})', True, (255,255,255)) ,(110, self.menu_y+5))
            for i, color in self.colorlist.items():
                color = (0,0,0) if i == 6 else color
                if button_y > self.button_height:
                    button_y = 0
                    self.button_move = self.button_width + 20
                pygame.draw.rect(self.main.screen, color, pygame.Rect(self.button_x + self.button_move, button_y , self.button_width, self.button_height), self.button_border)
                self.main.screen.blit(self.main.font.render(f'{self.button_names[i]} {self.colorlist[i]}', True, color) ,(self.button_x + 5, self.button_y + self.button_distance *i))
                button_y += self.button_y + self.button_distance *i
        def handle_event(self, event, mouse_x, mouse_y):
            if self.input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.input_active = False
                        try:
                            new_color = eval(self.color_input)
                            if isinstance(new_color, tuple) and len(new_color) == 3 and all(0 <= val <= 255 for val in new_color):
                                self.colorlist[self.selected_index] = new_color
                        except:
                            pass
                        self.color_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.color_input = self.color_input[:-1]
                    else:
                        self.color_input += event.unicode
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_y <= mouse_y <= self.menu_y + self.menu_height:
                        selected_index = (mouse_y // self.button_distance) - 2
                        if 0 <= selected_index < len(self.colorlist):
                            self.selected_index = selected_index
                            self.input_active = True

    class CountdownTimer:
        def __init__(self, initial_counter=10, font_size=100, x = 100, y = 100, radius=90, arc_width=10, color=(0, 128, 0)):
            self.initial_counter = initial_counter
            self.counter = initial_counter
            self.font = pygame.font.SysFont(None, font_size)
            self.x = x
            self.y = y
            self.position = (x,y)
            self.radius = radius
            self.arc_width = arc_width
            self.color = color
            self.timer_event = pygame.USEREVENT + 1
            pygame.time.set_timer(self.timer_event, 1000)
            self.is_running = True

        def update_timer(self, event):
            if event.type == self.timer_event and self.is_running:
                self.counter -= 1
                if self.counter == 0:
                    pygame.time.set_timer(self.timer_event, 0)
                    self.is_running = False

        def draw_timer(self, surface):
            text = self.font.render(str(self.counter), True, self.color)
            text_rect = text.get_rect(center=self.position)
            self.end_angle = (360 * self.counter) / self.initial_counter
            if self.end_angle != 0:
                pygame.draw.rect(surface, (100,100,100), pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2))
                pygame.draw.rect(surface, (0,0,0), pygame.Rect(self.x - self.radius - 8, self.y - self.radius - 8, self.radius*2 + 16, self.radius*2 + 16), 8)
                self.drawArcCv2(surface, (255, 0, 0), self.position, self.radius, self.arc_width, self.end_angle)
                surface.blit(text, text_rect)

        def drawArcCv2(self, surf, color, center, radius, width, end_angle):
            circle_image = numpy.zeros((radius * 2 + 4, radius * 2 + 4, 4), dtype=numpy.uint8)
            circle_image = cv.ellipse(circle_image, (radius + 2, radius + 2), (radius - width // 2, radius - width // 2),0, 0, end_angle, (*color, 255), width, lineType=cv.LINE_AA)
            circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius * 2 + 4, radius * 2 + 4), 'RGBA')
            surf.blit(circle_surface, circle_surface.get_rect(center=center), special_flags=pygame.BLEND_PREMULTIPLIED)

        def reset_timer(self):
            self.counter = self.initial_counter
            pygame.time.set_timer(self.timer_event, 1000)
            self.is_running = True

    def Handle_Event_Keypress(self, event):
        if event.type == pygame.KEYDOWN and ((not self.gameover and not self.mainmenu) or self.paused):
            if event.key == self.Keybinds['rotate'] and not self.mousemode:
                new_rotation = 1 if self.shape_rotation == 4 else self.shape_rotation + 1
                self.RotateSFX.play()
                if self.is_valid_move(self.shape_pos_x, self.shape_pos_y, self.current_shape[new_rotation]):
                    self.shape_rotation = new_rotation
                elif self.shape_pos_x <= self.columns / 2:
                    if self.is_valid_move(self.shape_pos_x + 1, self.shape_pos_y, self.current_shape[new_rotation]):
                        self.shape_pos_x += 1
                        self.shape_rotation = new_rotation
                else:
                    if self.is_valid_move(self.shape_pos_x - 1, self.shape_pos_y, self.current_shape[new_rotation]):
                        self.shape_pos_x -= 1
                        self.shape_rotation = new_rotation
            elif event.key == pygame.K_ESCAPE:
                self.PauseSFX.play()
                self.paused = not self.paused
            elif event.key == self.Keybinds['hold'] and self.can_switch and not self.mousemode:
                self.HoldSFX.play()
                if self.held_shape is not None:
                    temp_shape_holder = self.current_shape
                    self.current_shape = self.held_shape
                    self.held_shape = temp_shape_holder
                    self.shape_rotation = 1
                    self.shape_pos_x = 3 if not self.mousemode else int(self.mapmouseX)
                    self.shape_pos_y = 0
                    self.can_switch = False
                else:
                    self.held_shape = self.current_shape
                    self.current_shape = self.next_shape
                    self.next_shape = self.next_next_shape
                    self.next_next_shape = self.next_next_next_shape
                    self.next_next_next_shape = random.choice(self.shapelist)
                    self.shape_rotation = 1
                    self.shape_pos_x = 3 if not self.mousemode else int(self.mapmouseX)
                    self.shape_pos_y = 0
                    self.can_switch = False
            elif event.key == self.Keybinds['harddrop'] and not self.mousemode:
                self.harddropped = True
            
            if self.Keybindchanging:
                for key, value in self.Keybinds.items():
                    if value == event.key:
                        self.error_message = f'{pygame.key.name(event.key)} is already in use'
                        self.Keybindchanging = False
                        break
                else:
                    self.Keybinds[self.changedKeybind] = event.key
                    self.Keybindchanging = False

    def Handle_Event_Mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.mousemode:
                if event.button == self.Rclick:
                    self.harddropped = True
                elif event.button == self.Lclick:
                    self.HoldSFX.play()
                    if self.held_shape is not None:
                        temp_shape_holder = self.current_shape
                        self.current_shape = self.held_shape
                        self.held_shape = temp_shape_holder
                        self.shape_rotation = 1
                        self.shape_pos_x = 3 if not self.mousemode else int(self.mapmouseX) 
                        self.shape_pos_y = 0
                        self.can_switch = False
                    else:
                        self.held_shape = self.current_shape
                        self.current_shape = self.next_shape
                        self.next_shape = self.next_next_shape
                        self.next_next_shape = self.next_next_next_shape
                        self.next_next_next_shape = random.choice(self.shapelist)
                        self.shape_rotation = 1
                        self.shape_pos_x = 3 if not self.mousemode else int(self.mapmouseX)
                        self.shape_pos_y = 0
                        self.can_switch = False
                elif (event.button == self.mousescrollup) or (event.button == self.mousescrolldown):
                    self.RotateSFX.play()
                    if event.button == self.mousescrollup:
                        new_rotation = 1 if self.shape_rotation == 4 else self.shape_rotation + 1
                    elif event.button == self.mousescrolldown:
                        new_rotation = 4 if self.shape_rotation == 0 else self.shape_rotation - 1
                    if self.is_valid_move(self.shape_pos_x, self.shape_pos_y, self.current_shape[new_rotation]):
                        self.shape_rotation = new_rotation  
                    elif self.shape_pos_x <= self.columns / 2:
                        if self.is_valid_move(self.shape_pos_x + 1, self.shape_pos_y, self.current_shape[new_rotation]):
                            self.shape_pos_x += 1
                            self.shape_rotation = new_rotation
                    else:
                        if self.is_valid_move(self.shape_pos_x - 1, self.shape_pos_y, self.current_shape[new_rotation]):
                            self.shape_pos_x -= 1
                            self.shape_rotation = new_rotation
            if self.mainmenu and (not self.KeybindsMenu and not self.optionsmenu and not self.customization_menu and not self.audiomenu):
                if self.quit_rect.collidepoint(self.mouseX, self.mouseY):
                    self.running = False
                elif self.options_rect.collidepoint(self.mouseX, self.mouseY):
                    self.optionsmenu = True
                    self.clicked = True
                elif self.reset_rect.collidepoint(self.mouseX, self.mouseY):
                    self.TemporaryMap, self.Map, self.nextmap, self.level, self.points, self.show_cleared_rows, self.count_cleared_rows, self.currentframe, self.current_shape, self.next_shape, self.next_next_shape, self.next_next_next_shape, self.held_shape, self.shape_rotation, self.shape_pos_x, self.shape_pos_y = self.start()
                    self.gameover = False
                    self.paused = False
                    self.mainmenu = False
                    self.startbackgroundmusic = True
                elif self.gamemode_rect.collidepoint(self.mouseX, self.mouseY):
                    self.gamemodemenu = True
            if self.paused and (not self.KeybindsMenu and not self.optionsmenu and not self.customization_menu):
                if self.paused_quit_rect.collidepoint(self.mouseX, self.mouseY) and not self.audiomenu:
                    self.running = False
                elif self.paused_options_rect.collidepoint(self.mouseX, self.mouseY) and not self.audiomenu:
                    self.optionsmenu = True
                    self.clicked = True
                elif self.paused_reset_rect.collidepoint(self.mouseX, self.mouseY) and not self.audiomenu:
                    self.TemporaryMap, self.Map, self.nextmap, self.level, self.points, self.show_cleared_rows, self.count_cleared_rows, self.currentframe, self.current_shape, self.next_shape, self.next_next_shape, self.next_next_next_shape, self.held_shape, self.shape_rotation, self.shape_pos_x, self.shape_pos_y = self.start()
                    self.gameover = False
                    self.paused = False
                    self.mainmenu = False
                elif self.paused_return_rect.collidepoint(self.mouseX, self.mouseY):
                    self.mainmenu = True
                    self.paused = False
            if self.gameover:
                if self.ad_rect.collidepoint(self.mouseX, self.mouseY) and not self.audiomenu:
                    self.Ad = cv.VideoCapture(f'Tetris ads/{random.choice(self.Ad_file_names)}')
                    self.Ad.set(cv.CAP_PROP_POS_FRAMES, 0)
                    self.playingAD = True
            if self.optionsmenu:
                if (not self.KeybindsMenu and not self.audiomenu and not self.customization_menu):
                    if self.X_rect.collidepoint(self.mouseX, self.mouseY):
                        self.optionsmenu = False
                    elif self.keybind_rect.collidepoint(self.mouseX, self.mouseY) and not self.clicked:
                        self.KeybindsMenu = True
                        self.clickframe = None
                    elif self.mousemode_rect.collidepoint(self.mouseX, self.mouseY):
                        self.mousemode = not self.mousemode
                    elif self.audiorect.collidepoint(self.mouseX, self.mouseY):
                        self.audiomenu = True
                    elif self.customization_rect.collidepoint(self.mouseX, self.mouseY):
                        self.customization_menu = True
                if self.KeybindsMenu:
                    if self.X_rect.collidepoint(self.mouseX, self.mouseY):
                        self.KeybindsMenu = False
                    elif pygame.Rect(self.width/2-150, self.keybindY, 200, 30).collidepoint(self.mouseX, self.mouseY):
                        self.Keybindchanging = True
                        self.changedKeybind = 'down'
                    elif pygame.Rect(self.width/2-150, self.keybindY + self.Keybindbuttondistance, 200, 30).collidepoint(self.mouseX, self.mouseY):
                        self.Keybindchanging = True
                        self.changedKeybind = 'left'
                    elif pygame.Rect(self.width/2-150, self.keybindY + self.Keybindbuttondistance * 2, 200, 30).collidepoint(self.mouseX, self.mouseY):
                        self.Keybindchanging = True
                        self.changedKeybind = 'right'
                    elif pygame.Rect(self.width/2-150, self.keybindY + self.Keybindbuttondistance * 3, 200, 30).collidepoint(self.mouseX, self.mouseY):
                        self.Keybindchanging = True
                        self.changedKeybind = 'rotate'
                    elif pygame.Rect(self.width/2-150, self.keybindY + self.Keybindbuttondistance * 4, 200, 30).collidepoint(self.mouseX, self.mouseY):
                        self.Keybindchanging = True
                        self.changedKeybind = 'harddrop'
                    elif pygame.Rect(self.width/2-150, self.keybindY + self.Keybindbuttondistance * 5, 200, 30).collidepoint(self.mouseX, self.mouseY):
                        self.Keybindchanging = True
                        self.changedKeybind = 'hold'
                if self.audiomenu:
                    if self.X_rect.collidepoint(self.mouseX, self.mouseY):
                        self.audiomenu = False
                if self.customization_menu:
                    if self.X_rect.collidepoint(self.mouseX, self.mouseY):
                        self.customization_menu = False
            if self.gamemodemenu:
                if self.X_rect.collidepoint(self.mouseX, self.mouseY):
                    self.gamemodemenu = False
                elif self.puzzlemode_rect.collidepoint(self.mouseX, self.mouseY):
                    self.puzzlemode = not self.puzzlemode
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
                
    def Handle_Keypress(self):
        if self.keys[self.Keybinds['down']] and self.currentframe % self.inputdelay == 0 and not self.harddropped:
            self.SoftdropSFX.play()
            if self.is_valid_move(self.shape_pos_x, self.shape_pos_y + 1, self.current_shape[self.shape_rotation]):
                self.shape_pos_y += 1
                self.points += 1
                self.lockingin = False
            else:
                self.lockingin = True

        if self.keys[self.Keybinds['right']] and self.currentframe % self.inputdelay == 0 and not self.harddropped and not (self.paused or self.gameover or self.mousemode):
            self.MoveSFX.play()
            if self.is_valid_move(self.shape_pos_x + 1, self.shape_pos_y, self.current_shape[self.shape_rotation]):
                self.shape_pos_x += 1
        elif self.keys[self.Keybinds['left']] and self.currentframe % self.inputdelay == 0 and not self.harddropped and not (self.paused or self.gameover or self.mousemode):
            self.MoveSFX.play()
            if self.is_valid_move(self.shape_pos_x - 1, self.shape_pos_y, self.current_shape[self.shape_rotation]):
                self.shape_pos_x -= 1

    def Handle_MouseMode(self):
        if self.mousemode:
            self.mapmouseX = (self.mouseX // self.square_size) - 7
            self.mapmouseX = -1 if self.mapmouseX < -1 else self.mapmouseX
            self.mapmouseX = 8 if self.mapmouseX > 8 else self.mapmouseX

            if self.shape_pos_x < self.mapmouseX:
                if self.is_valid_move(self.shape_pos_x + 1, self.shape_pos_y, self.current_shape[self.shape_rotation]):
                    self.shape_pos_x += 1
            elif self.shape_pos_x > self.mapmouseX:
                if self.is_valid_move(self.shape_pos_x - 1, self.shape_pos_y, self.current_shape[self.shape_rotation]):
                    self.shape_pos_x -= 1

    def Handle_GameEvents(self):
        if self.currentframe % self.speed[self.level] == 0 and self.currentframe != 0 and not self.keys[self.Keybinds['down']] and not self.harddropped and not (self.paused or self.gameover or self.mainmenu or self.puzzlemode):
            if self.is_valid_move(self.shape_pos_x, self.shape_pos_y + 1, self.current_shape[self.shape_rotation]):
                self.shape_pos_y += 1
                self.lockingin = False
                self.MoveSFX.play()
            else:
                self.lockingin = True

        if self.lockingin:
            self.lockframe += 1
            if self.is_valid_move(self.shape_pos_x, self.shape_pos_y + 1, self.current_shape[self.shape_rotation]):
                self.lockingin = False
        else:
            self.lockframe = 0

        if self.harddropped:
            self.HarddropSFX.play()
            temp_Y_holder = self.shape_pos_y
            self.shape_pos_y = self.ghostpieceY(self.shape_pos_x, self.shape_pos_y, self.current_shape[self.shape_rotation])
            self.points += 2 * (self.shape_pos_y - temp_Y_holder)

        if (self.lockframe == self.lockdelay and self.lockingin) or self.harddropped:
            self.harddropped = False
            self.lockingin = False
            self.lockin(self.shape_pos_x, self.shape_pos_y, self.current_shape[self.shape_rotation])
            self.TemporaryMap, new_cleared_rows = self.clear(self.TemporaryMap)
            self.show_cleared_rows += new_cleared_rows
            self.count_cleared_rows += new_cleared_rows
            if self.count_cleared_rows >= 10:
                self.level = 19 if self.level == 19 else self.level + 1
                self.count_cleared_rows = 0
            self.points += self.pointlist[new_cleared_rows] * (1 if self.level == 0 else self.level)
            if new_cleared_rows != 0:
                self.pointsounds[new_cleared_rows].play()
            self.current_shape = self.next_shape
            self.next_shape = self.next_next_shape
            self.next_next_shape = self.next_next_next_shape
            self.next_next_next_shape = random.choice(self.shapelist)
            self.shape_rotation = 1
            self.shape_pos_x = 3 if not self.mousemode else int(self.mapmouseX)
            self.shape_pos_y = 0
            self.can_switch = True
            if not self.is_valid_move(self.shape_pos_x, self.shape_pos_y, self.current_shape[self.shape_rotation]):
                self.gameover = True
                self.start_timer = True
                self.startbackgroundmusic = False
                pygame.mixer.music.pause()
                self.scoreboard.update_high_scores(self.points)
                self.GameoverSFX.play()

    def Handle_Drawing(self):
        if not (self.gameover and self.paused and self.mainmenu):
            self.ghost_y = self.ghostpieceY(self.shape_pos_x, self.shape_pos_y, self.current_shape[self.shape_rotation])
            self.Map = self.draw(self.shape_pos_x, self.shape_pos_y, self.current_shape[self.shape_rotation])  # Draw actual piece
            self.Map = self.draw(self.shape_pos_x, self.ghost_y, self.current_shape[self.shape_rotation], is_ghost=True)  # Draw ghost piece 
        self.screen.fill((0, 0, 0))
        for w in range(self.columns):
            for h in range(self.rows):
                pygame.draw.rect(self.screen, self.subtract_RGB(self.colorlist[self.Map[h][w]], self.lockframe * 3), pygame.Rect(self.margin_size + w * self.square_size, h * self.square_size, self.square_size, self.square_size))
                if self.Map[h][w] == 8: 
                    pygame.draw.rect(self.screen, self.colorlist[self.find_color(self.current_shape[self.shape_rotation])], pygame.Rect(self.margin_size + w * self.square_size, h * self.square_size, self.square_size, self.square_size), self.square_border_width + 3)
                else:
                    pygame.draw.rect(self.screen, self.gray if self.Map[h][w] == 0 else self.subtract_RGB(self.colorlist[self.Map[h][w]], 51), pygame.Rect(self.margin_size + w * self.square_size, h * self.square_size, self.square_size, self.square_size), self.square_border_width)

        self.screen.blit(self.font.render(f'Score: {self.points}', True, (255,255,255)), (0, 240))
        self.screen.blit(self.font.render(f'Level: {self.level}', True, (255,255,255)), (0, 270))
        self.screen.blit(self.font.render(f'Lines: {self.show_cleared_rows}', True, (255,255,255)), (0, 300))

        self.drawnext(self.width - self.margin_size + 60, 50, self.next_shape[1], self.square_size)
        self.drawnext(self.width - self.margin_size + 60, 250, self.next_next_shape[1], self.square_size)
        self.drawnext(self.width - self.margin_size + 60, 450, self.next_next_next_shape[1], self.square_size)
        self.screen.blit(self.font.render('Next', True, (255,255,255)), (self.width - self.margin_size + 90, 0))
        self.screen.blit(self.font.render('Hold', True, (255,255,255)), (90, 0))
        if self.held_shape is not None:
            self.drawnext(60, 50, self.held_shape[1], self.square_size)

    def Handle_Options(self, color,  x = 45 ,y = 100, width = 790, height = 620, border_size = 10, ispaused = False):
        font = pygame.font.Font(self.font_file, 50)
        if not ispaused:
            self.screen.fill((0,0,0)) 
        if not self.KeybindsMenu and not self.audiomenu:
            pygame.draw.rect(self.screen, self.subtract_RGB(color, 50), pygame.Rect(x+border_size, y+border_size, width - border_size, height - border_size))
            pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height), border_size)
            pygame.draw.rect(self.screen, self.gray, pygame.Rect(self.X_rect.x, self.X_rect.y, self.X_rect.width, self.X_rect.height))
            self.screen.blit(font.render('X', True, (255, 255, 255)), (self.X_rect.x + 10, self.X_rect.y - 10))
            self.screen.blit(font.render('Keybinds', True, (255, 255, 255)), (self.keybind_rect.x, self.keybind_rect.y))
            self.screen.blit(font.render(f'Mouse mode: {self.mousemode}    (WIP)', True, (255, 255, 255)), (self.mousemode_rect.x, self.mousemode_rect.y))
            self.screen.blit(font.render('Audio settings', True, (255, 255, 255)), (self.audiorect.x, self.audiorect.y))
            self.screen.blit(font.render('Customization settings', True, (255, 255, 255)), (self.customization_rect.x, self.customization_rect.y))

        if self.KeybindsMenu:
            pygame.draw.rect(self.screen, self.subtract_RGB(color, 50), pygame.Rect(x+border_size, y+border_size, width - border_size, height - border_size))
            pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height), border_size)
            pygame.draw.rect(self.screen, self.gray, pygame.Rect(self.X_rect.x, self.X_rect.y, self.X_rect.width, self.X_rect.height))
            self.screen.blit(font.render('X', True, (255, 255, 255)), (self.X_rect.x + 10, self.X_rect.y - 10))
            self.screen.blit(font.render(f'Move Down: {pygame.key.name(self.Keybinds["down"])}', True, (255, 255, 255)), (self.width / 2 - 150, self.keybindY))
            self.screen.blit(font.render(f'Move Left: {pygame.key.name(self.Keybinds["left"])}', True, (255, 255, 255)), (self.width / 2 - 150, self.keybindY + self.Keybindbuttondistance))
            self.screen.blit(font.render(f'Move Right: {pygame.key.name(self.Keybinds["right"])}', True, (255, 255, 255)), (self.width / 2 - 150, self.keybindY + self.Keybindbuttondistance * 2))
            self.screen.blit(font.render(f'Rotate: {pygame.key.name(self.Keybinds["rotate"])}', True, (255, 255, 255)), (self.width / 2 - 150, self.keybindY + self.Keybindbuttondistance * 3))
            self.screen.blit(font.render(f'Harddrop: {pygame.key.name(self.Keybinds["harddrop"])}', True, (255, 255, 255)), (self.width / 2 - 150, self.keybindY + self.Keybindbuttondistance * 4))
            self.screen.blit(font.render(f'Hold: {pygame.key.name(self.Keybinds["hold"])}', True, (255, 255, 255)), (self.width / 2 - 150, self.keybindY + self.Keybindbuttondistance * 5))
            if self.error_message:
                self.screen.blit(font.render(self.error_message, True, (255, 0, 0)), (self.width / 2 - 120, 140))
        
        if self.audiomenu:
            pygame.draw.rect(self.screen, self.subtract_RGB(color, 50), pygame.Rect(x+border_size, y+border_size, width - border_size, height - border_size))
            pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height), border_size)
            pygame.draw.rect(self.screen, self.gray, pygame.Rect(self.X_rect.x, self.X_rect.y, self.X_rect.width, self.X_rect.height))
            self.screen.blit(font.render('X', True, (255, 255, 255)), (self.X_rect.x + 10, self.X_rect.y - 10))
            self.Backgroundaudio_slider.draw(self.screen)
            self.SFXaudio_slider.draw(self.screen)
            self.backgroundmusic_volume = round(self.Backgroundaudio_slider.get_value(), 1)
            self.previous_SFX_volume = round(self.SFXaudio_slider.get_value(), 1)
            self.screen.blit(font.render('Music volume', True, (255, 255, 255)), (x + 20, y + 150))
            self.screen.blit(font.render('SFX volume', True, (255, 255, 255)), (x + 20, y + 350))
            self.screen.blit(font.render(str(self.backgroundmusic_volume), True, (255, 255, 255)), (x + 240, y + 210))
            self.screen.blit(font.render(str(self.previous_SFX_volume), True, (255, 255, 255)), (x + 240, y + 410))

            pygame.mixer.music.set_volume(self.backgroundmusic_volume)

            if self.previous_SFX_volume != self.SFX_volume:
                self.SFX_volume = self.previous_SFX_volume
                self.pointsounds[1].set_volume(self.SFX_volume)
                self.pointsounds[2].set_volume(self.SFX_volume)
                self.pointsounds[3].set_volume(self.SFX_volume)
                self.pointsounds[4].set_volume(self.SFX_volume)

                self.GameoverSFX.set_volume(self.SFX_volume)
                self.PauseSFX.set_volume(self.SFX_volume)
                self.LevelupSFX.set_volume(self.SFX_volume)

                self.HarddropSFX.set_volume(self.SFX_volume)
                self.HoldSFX.set_volume(self.SFX_volume)
                self.LandingSFX.set_volume(self.SFX_volume)
                self.MoveSFX.set_volume(self.SFX_volume)
                self.RotateSFX.set_volume(self.SFX_volume)
                self.SoftdropSFX.set_volume(self.SFX_volume)
        
        if self.customization_menu:
            pygame.draw.rect(self.screen, self.subtract_RGB(color, 50), pygame.Rect(x+border_size, y+border_size, width - border_size, height - border_size))
            pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height), border_size)
            pygame.draw.rect(self.screen, self.gray, pygame.Rect(self.X_rect.x, self.X_rect.y, self.X_rect.width, self.X_rect.height))
            self.screen.blit(font.render('X', True, (255, 255, 255)), (self.X_rect.x + 10, self.X_rect.y - 10))
            self.customization_class.draw()

    def Handle_Paused(self):
        self.screen.blit(self.stoppedscreen, (0, 0))
        if self.startbackgroundmusic == False:
            pygame.mixer.music.pause()
            self.startbackgroundmusic = True

        font = pygame.font.Font(self.font_file, 50)
        self.screen.blit(font.render('GAME OVER' if self.gameover else 'PAUSED', True, (255, 255, 255)), (self.width / 2 - 150 if self.gameover else self.width / 2 - 90, self.stoppedbuttonsY))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.paused_reset_rect.x, self.paused_reset_rect.y, 200, 40))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.paused_options_rect.x, self.paused_options_rect.y, 200, 40))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.paused_quit_rect.x, self.paused_quit_rect.y, 200, 40))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.paused_return_rect.x, self.paused_return_rect.y, 200, 40))
        
        font = pygame.font.Font(self.font_file, 25)
        self.screen.blit(font.render('Restart', True, (255, 255, 255)), (self.paused_reset_rect.x + 55, self.paused_reset_rect.y))
        self.screen.blit(font.render('Options', True, (255, 255, 255)), (self.paused_options_rect.x + 50, self.paused_options_rect.y))
        self.screen.blit(font.render('Return to menu', True, (255, 255, 255)), (self.paused_return_rect.x + 5, self.paused_return_rect.y))
        self.screen.blit(font.render('Quit game', True, (255, 255, 255)), (self.paused_quit_rect.x + 40 , self.paused_quit_rect.y))

        
        if self.optionsmenu:
            self.Handle_Options(self.gray, ispaused= True)
        
    def Handle_MainMenu(self):
        self.screen.fill((0,0,0))

        x_start=45
        y_start=100
        x_end = self.width - x_start
        y_mid = y_start + 260
        y_end = self.height
        x_mid_start = x_start + 220
        x_mid_end = x_end - 220

        self.customization_rect = pygame.Rect(x_start + 10, y_start + 80, x_end-x_start, 80)
        self.audiorect = pygame.Rect(x_start + 10, y_start + 80 + 100, x_end-x_start, 80)
        self.keybind_rect  = pygame.Rect(x_start + 10, y_start + 80 + 200, x_end-x_start, 80)
        self.mousemode_rect = pygame.Rect(x_start + 10, y_start + 80 + 300, x_end-x_start, 80)

        pygame.draw.rect(self.screen, self.subtract_RGB(self.colorlist[6], 50), pygame.Rect(x_start, y_start,x_end-x_start, y_mid - y_start))
        pygame.draw.rect(self.screen, self.subtract_RGB(self.colorlist[6], 50), pygame.Rect(x_mid_start, y_mid, x_mid_end-x_mid_start, y_end - y_mid))

        pygame.draw.line(self.screen, self.colorlist[6], (x_start, y_start), (x_end, y_start), 10)
        pygame.draw.line(self.screen, self.colorlist[6], (x_start, y_start), (x_start, y_mid), 10)
        pygame.draw.line(self.screen, self.colorlist[6], (x_end, y_start), (x_end, y_mid), 10)
        pygame.draw.line(self.screen, self.colorlist[6], (x_start, y_mid), (x_mid_start, y_mid), 10)
        pygame.draw.line(self.screen, self.colorlist[6], (x_end, y_mid), (x_mid_end, y_mid), 10)
        pygame.draw.line(self.screen, self.colorlist[6], (x_mid_start, y_mid), (x_mid_start, y_end), 10)
        pygame.draw.line(self.screen, self.colorlist[6], (x_mid_end, y_mid), (x_mid_end, y_end), 10)

        font = pygame.font.Font(self.font_file, 200)
        x_offset = x_start + 50
        for i, letter in enumerate('TETRIS'):
            letter_surface = font.render(letter, True, self.colorlist[i+1] if i != 5 else self.colorlist[7])
            shadow_surface = font.render(letter, True, (0, 0, 0))
            self.screen.blit(shadow_surface, (x_offset + 5, y_start + 5 - 20))
            self.screen.blit(letter_surface, (x_offset, y_start - 20))
            x_offset += letter_surface.get_width() + 10

        buttony = y_mid + 30
        buttondistance = 70
        menu_items = ['Start Game', 'Options', 'Game Modes', 'Quit Game']
        rect_list = []
        option_rect_list = []
        font = pygame.font.Font(self.font_file, 50)

        for i, text in enumerate(menu_items):
            text_surface = font.render(text, True, (0,0,0))
            text_rect = text_surface.get_rect(center=(self.width // 2, buttony + buttondistance * i))
            
            rect = pygame.Rect(text_rect.left - 20, text_rect.top, text_rect.width + 40, text_rect.height)
            rect_list.append(rect)
            option_rect_list.append(rect)

            if rect.collidepoint(self.mouseX, self.mouseY):
                pygame.draw.rect(self.screen, self.colorlist[3], rect)
            self.screen.blit(text_surface, text_rect)
        
        self.reset_rect = rect_list[0]
        self.options_rect = rect_list[1]
        self.gamemode_rect = rect_list[2]
        self.quit_rect = rect_list[3]

        if self.optionsmenu:
            self.Handle_Options(self.colorlist[6])
        elif self.gamemodemenu:
            self.screen.fill((0,0,0)) 
            pygame.draw.rect(self.screen, self.subtract_RGB(self.colorlist[6], 50), pygame.Rect(45,100, self.width-90, self.height-100))
            pygame.draw.rect(self.screen, self.colorlist[6], pygame.Rect(55,110, self.width-70, self.height-90))
            pygame.draw.rect(self.screen, self.gray, pygame.Rect(self.X_rect.x, self.X_rect.y, self.X_rect.width, self.X_rect.height))
            self.screen.blit(font.render('X', True, (255, 255, 255)), (self.X_rect.x + 10, self.X_rect.y - 10))
            self.screen.blit(font.render(f'Puzzlemode: {self.puzzlemode}', True, (0,0,0)), (self.puzzlemode_rect.x, self.puzzlemode_rect.y))

    def Start_Game(self):
        while self.running:
            self.mouseX, self.mouseY = pygame.mouse.get_pos()
            if not self.paused and not self.gameover and not self.mainmenu:
                self.currentframe = 0 if self.currentframe > self.FPS else self.currentframe + 1  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False  

                if self.audiomenu:
                    self.Backgroundaudio_slider.update(event)
                    self.SFXaudio_slider.update(event)

                elif self.customization_menu:
                    self.customization_class.handle_event(event, self.mouseX, self.mouseY)

                self.Handle_Event_Keypress(event)
                self.Handle_Event_Mouse(event)

                if self.gameover:
                    self.timer.update_timer(event)
            
            self.keys = pygame.key.get_pressed()
            self.Handle_Drawing()

            if not (self.gameover or self.paused or self.mainmenu):
                self.Handle_Keypress()
                self.Handle_MouseMode()
                self.Handle_GameEvents()
                self.screen.blit(self.font.render('High scores:', True, (255,255,255)) ,(30, 360))
                self.scoreboard.display_high_scores(self.screen)
                if self.startbackgroundmusic:
                    pygame.mixer.music.unpause()
                    self.startbackgroundmusic = False
                
                
            elif self.mainmenu:
                self.Handle_MainMenu()
            elif self.paused:
                self.Handle_Paused()
            elif self.gameover:
                if self.start_timer:
                    self.timer.reset_timer()
                    self.start_timer = False
                self.screen.blit(self.stoppedscreen, (0, 0))
                self.timer.draw_timer(self.screen)
                pygame.draw.rect(self.screen, self.gray, self.ad_rect)
                self.screen.blit(self.font.render('Watch AD to retry', True, (255,255,255)) ,(self.ad_rect.x + 2, self.ad_rect.y + 2))
                if self.playingAD:
                    while self.playingAD:
                        IsTrue, Adframe = self.Ad.read()
                        if not IsTrue:
                            self.playingAD = False
                        try:
                            cv.imshow('Ad', Adframe)
                        except:
                            pass
                        if cv.waitKey(20) & 0xFF == ord('d'):
                            break
                    cv.destroyAllWindows()
                    self.TemporaryMap = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
                    self.Map = [row[:] for row in self.TemporaryMap]
                    self.nextmap = [[0 for _ in range(5)] for _ in range(4)]
                    self.gameover = False

                if self.timer.end_angle == 0:
                    self.gameover = False
                    self.mainmenu = True
            pygame.display.update()
            self.clock.tick(self.FPS)
        pygame.quit()

if __name__ == '__main__':
    Tetrisgame = Tetris()
    Tetrisgame.Start_Game()
