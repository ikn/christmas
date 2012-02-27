from os import sep

import pygame as pg

# paths
DATA_DIR = ''
IMG_DIR = DATA_DIR + 'img' + sep
SOUND_DIR = DATA_DIR + 'sound' + sep
MUSIC_DIR = DATA_DIR + 'music' + sep
FONT_DIR = DATA_DIR + 'font' + sep

# display
WINDOW_ICON = IMG_DIR + 'icon.png'
WINDOW_TITLE = 'Unintentional Christmas Tree'
MOUSE_VISIBLE = True
FLAGS = 0
FULLSCREEN = False
RESIZABLE = False
RES_W = (960, 540)
RES_F = pg.display.list_modes()[0]
MIN_RES_W = (320, 180)
ASPECT_RATIO = None

# timing
FPS = 60
FRAME = 1. / FPS

# input
KEYS_NEXT = (pg.K_RETURN, pg.K_SPACE, pg.K_KP_ENTER)
KEYS_BACK = (pg.K_ESCAPE, pg.K_BACKSPACE)
KEYS_MINIMISE = (pg.K_F10,)
KEYS_FULLSCREEN = (pg.K_F11, (pg.K_RETURN, pg.KMOD_ALT, True),
                   (pg.K_KP_ENTER, pg.KMOD_ALT, True))
KEYS_LEFT = (pg.K_LEFT, pg.K_a, pg.K_q)
KEYS_RIGHT = (pg.K_RIGHT, pg.K_d, pg.K_e, pg.K_s)
KEYS_UP = (pg.K_SPACE, pg.K_UP, pg.K_w, pg.K_z, pg.K_COMMA)
KEYS_EASY = (pg.K_1,)
KEYS_HARD = (pg.K_2,)
REPEAT_DELAY = .4
REPEAT_RATE = .15

# audio
MUSIC_VOLUME = 50
SOUND_VOLUME = 50
EVENT_ENDMUSIC = pg.USEREVENT
SOUNDS = {}
SOUND_VOLUMES = {}

# game
GROUND_POS = .95 # ratio of screen height
BLOCK_HEIGHT = (.1, .15) # ratio of screen height - (easy, hard)
COLS = 10 # must be even
BASE_SPEED = .005
INITIAL_SPEED = (1, 1.5) # (easy, hard)
UP_SPEED = 5
# (time, ID, col)
SCRIPTS = (
    ((0, 0, 1), (0, 0, 3), (0, 0, 5), (150, 1, 1), (150, 1, 3), (150, 1, 5),
     (250, 0, 3), (250, 1, 4), (250, 0, 5)),
    ((0, 0, 0), (150, 0, 9), (285, 1, 1), (405, 1, 8), (510, 0, 2),
     (605, 0, 7), (690, 1, 3), (765, 1, 6), (825, 0, 4), (875, 1, 5)),
    ((0, 0, 1), (100, 1, 1), (200, 0, 1), (300, 1, 1), (300, 0, 8),
     (450, 0, 1), (450, 1, 8), (600, 0, 1), (700, 0, 0), (700, 0, 2)),
    ((0, 0, 0), (25, 1, 1), (50, 0, 2), (75, 1, 3), (100, 0, 4), (125, 1, 5),
     (150, 0, 6), (175, 1, 7), (250, 0, 9), (275, 1, 8), (300, 0, 7),
     (325, 1, 6), (325, 1, 0), (350, 0, 5), (350, 0, 1), (375, 1, 4),
     (375, 1, 2), (450, 1, 9)),
    ((0, 1, 3), (50, 1, 4), (200, 0, 6), (250, 0, 5), (400, 0, 0),
     (450, 0, 1), (600, 1, 9), (650, 1, 8), (700, 1, 7)),
    ((0, 0, 0), (0, 1, 1), (0, 0, 2), (0, 1, 3), (0, 0, 4), (0, 1, 5),
     (0, 0, 6), (0, 1, 7), (0, 0, 8), (0, 1, 9), (100, 1, 0), (100, 0, 1),
     (100, 1, 2), (100, 0, 3), (100, 1, 4), (100, 0, 5), (100, 1, 6),
     (100, 0, 7), (100, 1, 8), (100, 0, 9), (175, 0, 0), (175, 1, 1),
     (175, 0, 2), (175, 1, 3), (175, 0, 4), (175, 1, 5), (175, 0, 6),
     (175, 1, 7), (175, 0, 8), (175, 1, 9), (250, 1, 0), (250, 0, 1),
     (250, 1, 2), (250, 0, 3), (250, 1, 4), (250, 0, 5), (250, 1, 6),
     (250, 0, 7), (250, 1, 8), (250, 0, 9), (350, 1, 0), (350, 0, 1),
     (350, 1, 2), (350, 0, 3), (350, 1, 4), (350, 0, 5), (350, 1, 6),
     (350, 0, 7), (350, 1, 8), (350, 0, 9))
)
ALT_SCRIPT_PROB = .25
# IDs match up, and we just have some (block index, new (time, ID, col) tuple)
ALT_SCRIPTS = (
    ((3, (150, 1, 2)), (4, (150, 1, 4)), (5, (150, 1, 6))),
    ((9, (875, 0, 5)),),
    ((7, (600, 1, 1)),),
    ((8, (250, 1, 9)), (9, (275, 0, 8)), (10, (300, 1, 7)), (11, (325, 0, 6)),
     (12, (325, 0, 0)), (13, (350, 1, 5)), (14, (350, 1, 1)),
     (15, (375, 0, 4)), (16, (375, 0, 2)), (17, (450, 0, 9))),
    ((8, (700, 1, 6)),),
    ((40, (350, 0, 0)), (41, (350, 1, 1)), (42, (350, 0, 2)),
     (43, (350, 1, 3)), (44, (350, 0, 4)), (45, (350, 1, 5)),
     (46, (350, 0, 6)), (47, (350, 1, 7)), (48, (350, 0, 8)),
     (49, (350, 1, 9)))
)
SCRIPT_GAP = (150, 300, 450)
SPEED_INCREASE = (1.05, 1.1, 1.15)
# score
SCORE_MULTIPLIER = 1
SCORE_SPEED_EXP = 3
SCORE_BLOCKS_EXP = 1.15
LOSE_SCORE_DECREASE = 50

# menus
LOSE_SCREEN_WAIT = 30
INSTRUCTIONS_TEXT = '''Play with space and the arrow keys.'''
INSTRUCTIONS_SIZE = .07
INSTRUCTIONS_SHADOW_OFFSET = (.0021, .0021)
INSTRUCTIONS_POS = .05 # ratio of screen height
START_TEXT = '''1: Easy
2: Hard'''
LINE_SPACING = .05
LOST_SCORE_SIZE = .2 # ratio of screen height
LOST_SCORE_SHADOW_OFFSET = (.006, .006) # screen width / height ratios
LOST_SCORE_FORMAT = ':.3f'
SCORE_DP = 2

# appearance
BG = (255, 255, 255)
COLOURS = ((200, 0, 0), (0, 200, 0))
B_COLOURS = ((100, 0, 0), (0, 100, 0))
B_SIZE = .05 # ratio of block width
FONT = 'Orbitron-Black.ttf'
SCORE_SIZE = .1 # ratio of screen height
SCORE_COLOUR = (0, 150, 0)
SCORE_SHADOW_COLOUR = (150, 0, 0)
SCORE_POS = (.05, .05) # screen width / height ratios
SCORE_SHADOW_OFFSET = (.003, .003) # screen width / height ratios
INT_SCORE = True

# debug
BLOCK_NAMES = ('red', 'green')