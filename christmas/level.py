from random import random, randrange, triangular

import pygame as pg

from ext import evthandler as eh
import conf

ir = lambda x: int(round(x))

def border (surface, rect, data):
    """Fill with a border.

Takes (border_width, border_colour, inner_colour).  If inner_colour is omitted
or width is 0, border colour is used for the whole tile.

"""
    if len(data) == 2:
        border = data[1]
        width = 0
    else:
        width, border, inner = data
    surface.fill(border, rect)
    if width != 0:
        width *= 2
        surface.fill(inner, pg.Rect(rect).inflate(-width, -width))

class Block:
    def __init__ (self, ID, col, size):
        self.ID = ID
        self.colour = conf.COLOURS[ID]
        self.b_colour = conf.B_COLOURS[ID]
        self.b_size = ir(conf.B_SIZE * size[1])
        self.size = tuple(size)
        self.col = col
        self.x = col * size[0]
        self.y = -self.size[1]
        self.dirn = 1

    def __str__ (self):
        return '<{0}>'.format(conf.BLOCK_NAMES[self.ID])

    __repr__ = __str__

    def update (self, speed):
        v = self.dirn * speed
        self.y += v
        self.rect = (self.x, int(self.y)) + self.size
        if self.dirn < 0 and self.y < -self.size[1]:
            # OoB
            dead = True
        else:
            dead = False
        return (v, dead)

    def draw (self, screen):
        border(screen, self.rect, (self.b_size, self.b_colour, self.colour))
        #screen.fill(self.colour, self.rect)
        #pg.draw.rect(screen, self.b_colour, self.rect, self.b_size)

class Level:
    def __init__ (self, game, event_handler, hard):
        self.game = game
        self.event_handler = event_handler
        self.frame = conf.FRAME
        repeat = (eh.MODE_ONDOWN_REPEAT, ir(conf.REPEAT_DELAY * conf.FPS), ir(conf.REPEAT_RATE * conf.FPS))
        event_handler.add_key_handlers([
            (conf.KEYS_LEFT, [(self.move, (-1,))]) + repeat,
            (conf.KEYS_RIGHT, [(self.move, (1,))]) + repeat,
            (conf.KEYS_UP, self.push, eh.MODE_ONDOWN),
            (conf.KEYS_BACK, self.toggle_paused, eh.MODE_ONDOWN)
        ])
        self.init(conf.COLS, hard)

    def init (self, cols, hard):
        self.cols = cols
        self.hard = hard
        self.first_col = 0
        self.blocks = []
        self.ground = [0 for x in xrange(cols)]
        self.col_blocks = [[] for x in xrange(cols)]
        self.gd_pos = ir(conf.GROUND_POS * self.game.res[1])
        self.block_size = (ir(float(self.game.res[0]) / cols), ir(self.gd_pos * conf.BLOCK_HEIGHT[self.hard]))
        self.base_speed = self.game.res[1] * conf.BASE_SPEED
        self.speed = conf.INITIAL_SPEED[self.hard]
        # scripting
        self.script = None
        self.t = 0
        self.script_start_t = 0
        self.script_invert_colour = randrange(2)
        # other stuff
        self.score_pos = [ir(x * s) for x, s in zip(conf.SCORE_POS, self.game.res)]
        self.score_shadow_offset = tuple(ir(x * s) for x, s in zip(conf.SCORE_SHADOW_OFFSET, self.game.res))
        self.set_score(0)
        self.paused = False

    def toggle_paused (self, *args):
        self.paused = not self.paused

    def move (self, key, evt, mods, dirn):
        self.first_col = (self.first_col + dirn) % 2
        # move grounded blocks
        col_blocks = self.col_blocks
        ground = self.ground
        cols = self.cols
        w, h = self.block_size
        for b in self.blocks:
            if b.dirn == 0:
                b.x = (b.x + w * dirn) % (cols * w)
                old = b.col
                b.col = new = (old + dirn) % cols
                col_blocks[old].remove(b)
                col_blocks[new].append(b)
                ground[old] -= 1
                ground[new] += 1
        # move falling/ascending blocks if pushed
        gd = self.gd_pos
        for b in self.blocks:
            if b.dirn != 0:
                old = b.col
                top = gd - h * ground[old]
                if b.y + h > top:
                    b.x = (b.x + w * dirn) % (cols * w)
                    b.col = new = (old + dirn) % cols
                    col_blocks[old].remove(b)
                    col_blocks[new].append(b)

    def push (self, *args):
        n = 0
        for b in self.blocks:
            if b.dirn == 0:
                b.dirn = -conf.UP_SPEED
                self.ground[b.col] -= 1
                n += 1
        if n > 0:
            speed = conf.SCORE_SPEED_EXP ** self.speed
            blocks = conf.SCORE_BLOCKS_EXP ** n
            self.set_score(self.score + conf.SCORE_MULTIPLIER * speed * blocks)

    def add_block (self, ID, col):
        block = Block(ID, col, self.block_size)
        self.blocks.append(block)
        self.col_blocks[col].append(block)

    def update (self):
        if self.paused:
            return
        # add blocks
        script = self.script
        current_t = self.t
        if script is None:
            if self.script_start_t <= current_t:
                # start new script
                script_i = randrange(len(conf.SCRIPTS))
                script = list(conf.SCRIPTS[script_i])
                if self.hard and random() < conf.ALT_SCRIPT_PROB:
                    # alternative script
                    for i, new in conf.ALT_SCRIPTS[script_i]:
                        script[i] = new
                # adjust times
                s = self.speed
                self.script = script = [(ir(float(t) / s), i, c) for t, i, c in script]
                self.t = current_t = 0
        if script is not None:
            # continue script
            done = False
            while script and script[0][0] <= current_t:
                t, ID, col = script.pop(0)
                ID = (ID + self.script_invert_colour) % 2
                self.add_block(ID, col)
            if not script:
                # finished
                self.script = None
                self.t = 0
                self.script_start_t = triangular(*(ir(float(t) / self.speed) for t in conf.SCRIPT_GAP))
                self.script_invert_colour = randrange(2)
                # increase speed
                self.speed *= triangular(*conf.SPEED_INCREASE)
        self.t += 1
        # update blocks
        rm = []
        h = self.block_size[1]
        gd = self.gd_pos
        for c, bs in enumerate(self.col_blocks):
            top = gd - h * self.ground[c]
            for b in bs:
                v, dead = b.update(self.speed * self.base_speed)
                if dead:
                    rm.append(b)
                elif v > 0 and b.y + h > top:
                    # landed
                    b.dirn = 0
                    b.y = top - h
                    self.ground[c] += 1
                    if (c - self.first_col) % 2 != b.ID:
                        # lost
                        if self.hard:
                            self.game.quit_backend(no_quit = True)
                            self.game.start_backend(LoseScreen, self.score)
                        else:
                            self.set_score(self.score - conf.LOSE_SCORE_DECREASE * self.speed)
            # if any block going up is now higher than one going down, they've collided
            ymax_up = min([gd] + [b.y - h for b in bs if b.dirn < 0])
            down = [b for b in bs if b.dirn > 0]
            ymin_down = max([0] + [b.y for b in down])
            dy = 0
            if ymax_up < ymin_down:
                for b in down:
                    this_dy = b.y - ymax_up
                    if this_dy > 0:
                        dy = max(dy, this_dy)
                        b.y -= dy
                        b.dirn = -conf.UP_SPEED
        for b in rm:
            assert b.dirn != 0
            self.blocks.remove(b)
            self.col_blocks[b.col].remove(b)

    def set_score (self, score):
        self.score = score
        if conf.INT_SCORE:
            score = ir(score)
        font = (conf.FONT, ir(conf.SCORE_SIZE * self.game.res[1]), False)
        shadow = (conf.SCORE_SHADOW_COLOUR, self.score_shadow_offset)
        font_args = (font, 'Score: {0}'.format(score), conf.SCORE_COLOUR, shadow)
        self.score_sfc = self.game.img(font_args)[0]

    def draw (self, screen):
        if self.paused:
            return
        # BG
        screen.fill(conf.BG)
        # floor
        w = self.block_size[0]
        c = self.first_col
        for i in xrange(self.cols):
            r = (i * w, self.gd_pos, w, self.game.res[0] - self.gd_pos)
            screen.fill(conf.COLOURS[c], r)
            c = (c + 1) % 2
        # blocks
        for b in self.blocks:
            b.draw(screen)
        # score
        screen.blit(self.score_sfc, self.score_pos)
        return True

class LoseScreen:
    def __init__ (self, game, event_handler, score):
        self.game = game
        self.event_handler = event_handler
        self.frame = conf.FRAME
        self.score = score
        self.t = 0
        self.waiting = True

    def finish (self, *args):
        self.game.quit_backend(no_quit = True)
        self.game.start_backend(StartScreen)

    def update (self):
        if self.waiting:
            self.t += 1
            if self.t == conf.LOSE_SCREEN_WAIT:
                keys = conf.KEYS_EASY + conf.KEYS_HARD + conf.KEYS_NEXT + conf.KEYS_BACK
                self.event_handler.add_key_handlers([
                    (keys, self.finish, eh.MODE_ONDOWN)
                ])
                self.waiting = False

    def draw (self, screen):
        if self.dirty:
            # BG
            screen.fill(conf.BG)
            # score
            w, h = self.game.res
            font = (conf.FONT, ir(conf.LOST_SCORE_SIZE * h), False)
            o = tuple(ir(x * s) for x, s in zip(conf.LOST_SCORE_SHADOW_OFFSET, (w, h)))
            shadow = (conf.SCORE_SHADOW_COLOUR, o)
            text = ('Score:\n{0' + conf.LOST_SCORE_FORMAT + '}').format(self.score)
            spacing = ir(conf.LINE_SPACING * h)
            font_args = (font, text, conf.SCORE_COLOUR, shadow, None, 1, False, spacing)
            sfc = self.game.img(font_args)[0]
            sw, sh = sfc.get_size()
            screen.blit(sfc, (ir(float(w - sw) / 2), ir(float(h - sh) / 2)))
            self.dirty = False
            return True
        else:
            return False

class StartScreen:
    def __init__ (self, game, event_handler):
        self.game = game
        self.event_handler = event_handler
        self.frame = conf.FRAME
        event_handler.add_key_handlers([
            (conf.KEYS_EASY, [(self.start, (False,))], eh.MODE_ONDOWN),
            (conf.KEYS_HARD, [(self.start, (True,))], eh.MODE_ONDOWN)
        ])

    def start (self, key, evt, mode, hard):
        self.game.quit_backend(no_quit = True)
        self.game.start_backend(Level, hard)

    def update (self):
        pass

    def draw (self, screen):
        if self.dirty:
            # BG
            screen.fill(conf.BG)
            # instructions
            w, h = self.game.res
            font = (conf.FONT, ir(conf.INSTRUCTIONS_SIZE * h), False)
            o = tuple(ir(x * s) for x, s in zip(conf.INSTRUCTIONS_SHADOW_OFFSET, (w, h)))
            shadow = (conf.SCORE_SHADOW_COLOUR, o)
            font_args = (font, conf.INSTRUCTIONS_TEXT, conf.SCORE_COLOUR, shadow)
            sfc = self.game.img(font_args)[0]
            sw, sh = sfc.get_size()
            screen.blit(sfc, (ir(float(w - sw) / 2), ir(h * conf.INSTRUCTIONS_POS)))
            # options
            font = (conf.FONT, ir(conf.LOST_SCORE_SIZE * h), False)
            o = tuple(ir(x * s) for x, s in zip(conf.LOST_SCORE_SHADOW_OFFSET, (w, h)))
            shadow = (conf.SCORE_SHADOW_COLOUR, o)
            spacing = ir(conf.LINE_SPACING * h)
            font_args = (font, conf.START_TEXT, conf.SCORE_COLOUR, shadow, None, 0, False, spacing)
            sfc = self.game.img(font_args)[0]
            sw, sh = sfc.get_size()
            screen.blit(sfc, (ir(float(w - sw) / 2), ir(float(h - sh) / 2)))
            self.dirty = False
            return True
        else:
            return False