#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''A simple 2D billiards game
@authors: prashant agrawal, pankaj pandey
(c) 2010 the authors
'''

# changelog
# pankaj : 17 March, 2010: fixed alignment of the cue with the ball
# and made the target of the cue as the ball center instead of the mouse pos
# authors : before 17 March, 2010: did most of the setup

import pygame, sys, os, random
from pygame.locals import *
import time
from math import *
from ball import *
from numpy import *

if not pygame.font: print "Warning, fonts disabled!"
if not pygame.mixer: print "Warning, sounds disabled!"

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

mod = lambda v: sqrt(v[0] * v[0] + v[1] * v[1])

class Cue(pygame.sprite.Sprite):
    def __init__(self,hitting_ball,src,board):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.hitting_ball = hitting_ball
        self.CUE_WIDTH = 10
        self.CUE_LENGTH = 150
        self.image = pygame.image.load('data/cue.gif').convert()
        self.originalcopy = pygame.transform.scale(self.image,(self.CUE_WIDTH,self.CUE_LENGTH))
        self.image = pygame.transform.scale(self.image,(self.CUE_WIDTH,self.CUE_LENGTH))
        self.rect = self.image.get_rect()
        #self.rect.width = 1
        #self.rect.left = self.CUE_WIDTH/2.0
        self.speed = zeros((2,))
        self.radius = self.rect.centery - self.rect.top


    def update(self,src,dest,mousepressed):
        if mousepressed:
            dest_minus_src = (dest[0]-src[0],dest[1]-src[1])
            angle = atan2(dest_minus_src[0],dest_minus_src[1])
            c, s = cos(angle), sin(angle)
            angle = 180.0/pi*angle

            t = self.CUE_WIDTH/2.0
            l = self.CUE_LENGTH/2.0
            h = l*c+t*s
            w = s*(h+s*t)/c
            self.image = pygame.transform.rotate(self.originalcopy, angle)
            irect = self.image.get_rect()
            left,top = dest
            self.rect.width = irect.width
            self.rect.height = irect.height
            if 0<=angle<=90:
                top -= t*s
                left -= t*c
            elif 90<=angle<=180:
                top -= irect.height
                top += t*s
                left += t*c
            elif -90<=angle<0:
                left -= irect.width
                top += t*s
                left += t*c
            else:
                top -= irect.height
                left -= irect.width
                top -= t*s
                left -= t*c
            self.rect.topleft = left,top
        else:
            MAX_DRAG = self.board.height/8.0
            if src is not None:
                self.speed = array([-(dest[0]-src[0])*self.board.VEL_MAX/MAX_DRAG,-(dest[1]-src[1])*self.board.VEL_MAX/MAX_DRAG])
            print 'cue speed =',self.speed
            if hypot(*self.speed)<1: return
            self.board.initballspeed = [b.speed.copy() for b in self.board.ballsprites.sprites()]
            print self.board.initballspeed
            self.board.initballpos = [b.pos for b in self.board.ballsprites.sprites()]
            self.board.initcuespeed = self.speed.copy()
            self.board.inittopleft = self.rect.topleft
            self.board.initrect = self.rect
            while not self.board.collide_cue(self):
            #while not self.hitting_ball.rect.collidepoint(self.rect.center):
                time.sleep(0.01)
                self.board.cuesprite.clear(self.board.screen, self.board.background)
                self.rect.move_ip(round(self.speed[0]),round(self.speed[1]))
                self.board.draw()



class Billiards():
  def __init__(self, width=600, height=375, n_balls=7, caption='Billiards',friction=True,background='background.jpg'):
    pygame.init()
    self.ballsprites = pygame.sprite.RenderPlain()
    self.holesprites = pygame.sprite.RenderPlain()
    self.cuesprite = pygame.sprite.RenderPlain()
    self.width, self.height, self.n_balls = width, height, n_balls
    self.RUNNING, self.VEL_MAX = False, 5
    if friction==True: self.friction = 5.0*self.VEL_MAX**2/float(4*self.height)
    else: self.friction = 0.0
    self.screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption(caption)
    self.background = loadImage(background)
    self.screen.blit(self.background,(0,0))
    self.generate_balls()
    self.init_consts()
    self.draw()
    self.replaying = False
    self.wait = 0.01    # time in seconds to wait after each timestep
    pygame.mixer.init()
    self.collidecue_sound = pygame.mixer.Sound('data/collide.wav')
    self.gotoholes_sound = pygame.mixer.Sound('data/gotoholes.wav')
    self.finishmessage = pygame.mixer.Sound('data/finish_message.ogg')

  def generate_balls(self, posarr=None, speeds=None):
    n = 0
    nballs = len(posarr) if posarr is not None else self.n_balls
    while n < nballs:
      newball = Ball((0,0), self)
      self.radius = newball.radius
      vel = array((0, 0)) if speeds is None else speeds[n]
      pos = array(((random.uniform(self.radius,self.width - self.radius)), (random.uniform(self.radius,self.height - self.radius)))) if posarr is None else posarr[n]
      newball.set_pos(pos)
      newball.speed = vel
      newball.initpos[:] = newball.pos
      if n==0:
          self.ballsprites.add(newball)
          n = n + 1
      else:
          collide = False
          for oldball in self.ballsprites.sprites():
              if newball.rect.colliderect(oldball.rect):
                  collide = True
          if not collide:
              self.ballsprites.add(newball)
              n += 1

  def init_consts(self):
      rad = self.radius
      self.LEFTTOP = (rad,rad)
      self.MIDDLETOP = (int(self.width/2.0),rad)
      self.RIGHTTOP = (self.width-rad,rad)
      self.LEFTBOTTOM = (rad,self.height-rad)
      self.MIDDLEBOTTOM = (int(self.width/2.0),self.height-rad)
      self.RIGHTBOTTOM = (self.width-rad,self.height-rad)

  def draw_holes(self):
      self.hole_radius = rad = 1.2*self.radius

      lefttoprect = pygame.draw.circle(self.screen,BLACK,self.LEFTTOP,rad)
      middletoprect = pygame.draw.circle(self.screen,BLACK,self.MIDDLETOP,rad)
      righttoprect = pygame.draw.circle(self.screen,BLACK,self.RIGHTTOP,rad)
      leftbottomrect = pygame.draw.circle(self.screen,BLACK,self.LEFTBOTTOM,rad)
      middlebottomrect = pygame.draw.circle(self.screen,BLACK,self.MIDDLEBOTTOM,rad)
      rightbottomrect = pygame.draw.circle(self.screen,BLACK,self.RIGHTBOTTOM,rad)
      self.holerectlist = [lefttoprect,middletoprect,righttoprect,leftbottomrect,middlebottomrect,rightbottomrect]

  def draw(self):
      self.draw_holes()
      self.ballsprites.draw(self.screen)
      if not len(self.cuesprite.sprites())==0:
          self.cuesprite.draw(self.screen)
      pygame.display.flip()

  def after_one_timestep(self):
    self.screen.blit(self.background, (0,0))
    self.ballsprites.update()
    self.draw()
    #energy = sum([dot(i.speed,i.speed) for i in self.ballsprites.sprites()])
    #print 'Total Energy', energy
    for ball in self.ballsprites.sprites():
        if mod(ball.speed)>self.friction:
            self.runningballs = True
            return

  def collide_ball(self,ball1,ball2):
      if ball1.rect.colliderect(ball2.rect):
        r = self.radius
        r21 = array((ball1.rect.center[0] - ball2.rect.center[0],ball1.rect.center[1] - ball2.rect.center[1]))
        dist = hypot(*r21)
        if dist<2*r:
            dirx_unit, diry_unit = dir_unit = r21/dist
            #print 'dist=',dist
            next_int = lambda x: ceil(x) if x>0 else floor(x)
            ball2.rect.move_ip((next_int(0.5*r21[0]-r*dirx_unit),next_int(0.5*r21[1]-r*diry_unit)))
            ball1.rect.move_ip((next_int(-0.5*r21[0]+r*dirx_unit),next_int(-0.5*r21[1]+r*diry_unit)))
            vr1 = dot(ball1.speed,dir_unit)
            vr2 = dot(ball2.speed,dir_unit)
            dvr = vr2 - vr1
            #print 'dvr', dvr
            ball2.speed[:] = ball2.speed - dvr*dir_unit
            ball1.speed[:] = ball1.speed + dvr*dir_unit
            newdist = hypot(ball1.rect.center[0] - ball2.rect.center[0],ball1.rect.center[1] - ball2.rect.center[1])
            vr1 = dot(ball1.speed,dir_unit)
            vr2 = dot(ball2.speed,dir_unit)
            dvr = vr2 - vr1
            #print 'newdist', newdist, 'newdvr', dvr
            #self.collidecue_sound.play(maxtime=0.0001)
            return True
        else: return False
      else:
        return False

  def collide_cue(self,cue):
    r = self.radius
    irect = cue.rect
    ball = None
    headondist = 100000
    for i,b in enumerate(self.ballsprites.sprites()):
        cuespeed_unit = cue.speed/hypot(*cue.speed)
        tip = irect.center + cue.CUE_LENGTH/2.0*cuespeed_unit
        r21 = b.rect.center - tip
        r21next = b.rect.center - (tip + cue.speed)
        newheadondist = dot(cuespeed_unit,r21)
        #if dot(r21,r21next) < 0:
        if True:
	  if hypot(*(r21 - dot(cuespeed_unit,r21)*cuespeed_unit)) < r and abs(dot(cuespeed_unit,r21))<hypot(*cue.speed):
            if newheadondist < headondist:
                headondist = newheadondist
                ball = b
		
    if ball is None: return False
    tip = irect.center + cue.CUE_LENGTH/2.0*(cue.speed/hypot(*cue.speed))
    r21 = array((ball.rect.center[0] - tip[0],ball.rect.center[1] - tip[1]))
    dist = hypot(*r21)
    #print irect, ball.rect.center, r21

    ball.speed = cue.speed*0.6
    #ball.initspeed[:] = ball.speed
    #ball.initpos[:] = ball.pos
    cue.speed[:] = 0.0
    self.collidecue_sound.play(maxtime=0.0001)
    return True

  def launch_ball(self,mouse_src):
    for ball in self.ballsprites.sprites():
        if ball.rect.collidepoint(mouse_src):
            self.hitting_ball = ball
            mouse_src = ball.rect.center

            # making all other previous Cues disappear and making a new one
            if not len(self.cuesprite.sprites()) == 0: self.cuesprite.empty()
            self.cuesprite.add(Cue(self.hitting_ball,mouse_src,self))

            #init_rect = self.cuesprite.sprites()[0].rect
            mousepressed = True         # remains True till the mouse is held down
            while mousepressed:
                e = pygame.event.poll()
                if e.type==MOUSEMOTION:
                    self.cuesprite.clear(self.screen, self.background)
                    self.cuesprite.update(mouse_src,pygame.mouse.get_pos(),mousepressed)
                    self.draw()
                if e.type==MOUSEBUTTONUP:
                    print 'mouse released'
                    mousepressed = False
                    self.cuesprite.update(mouse_src,pygame.mouse.get_pos(),mousepressed)
                    self.start_game()

  def start_game(self):
    self.RUNNING = True
    self.runningballs = False
    t = time.time() #1268749892.305392
    while self.RUNNING == True:
        t2 = time.time()
        #print 'FPS :', 1/(t2-t)
        t = t2
        time.sleep(self.wait)
        self.after_one_timestep()
        for event in pygame.event.get():
            if event.type == KEYUP and event.key == K_SPACE and self.RUNNING == True:
                self.pause_game()
            if event.type == KEYDOWN and event.key == K_s:
                self.wait += 0.01            # see in slow motion
            if event.type == KEYDOWN and event.key == K_f:
                if self.wait<0.02: print "Running at normal speed. Can't speed up."
                else: self.wait -= 0.01      # see in fast motion (can't be faster than normal speed)
            if event.type == KEYDOWN and event.key == K_r:
                self.wait = 0.01        # reset to normal speed
            if event.type == KEYDOWN and event.key == K_q:
                sys.exit(0)
            if event.type == KEYDOWN and event.key == K_RETURN:
                pygame.display.toggle_fullscreen()
            if event.type == KEYDOWN and event.key == K_n:
                #print 'new game'
                self.ballsprites.empty()
                self.generate_balls()
            if event.type == MOUSEBUTTONDOWN:
                if self.replaying:
                    self.wait = 0.01
                    self.replaying = False
                mouse_src = pygame.mouse.get_pos()
                self.launch_ball(mouse_src)
            if event.type == KEYDOWN and event.key == K_e:
                self.replaying = True
                self.wait = 0.03
                self.ballsprites.empty()
                self.generate_balls(self.initballpos, self.initballspeed)
                self.cuesprite.sprites()[0].speed = self.initcuespeed
                self.cuesprite.sprites()[0].rect.topleft = self.inittopleft
                self.cuesprite.update(None,None,False)
                self.start_game()
            if event.type == QUIT:
                sys.exit(0)
	if len(self.ballsprites.sprites()) == 0:
	    if self.runningballs: 
	      if not pygame.mixer.get_busy():
		self.finishmessage.play()
		self.runningballs = False
    while self.RUNNING == False:
        event = pygame.event.poll()
        if event.type == MOUSEBUTTONDOWN:
                mouse_src = pygame.mouse.get_pos()
                self.launch_ball(mouse_src)

  def pause_game(self):
    self.RUNNING = False
    while self.RUNNING == False:
        for event in pygame.event.get():
            if event.type == KEYUP and event.key == K_SPACE:
                self.RUNNING = True
                self.start_game()
            if event.type == KEYDOWN and event.key == K_q:
                sys.exit(0)
            if event.type == MOUSEBUTTONDOWN:
                mouse_src = pygame.mouse.get_pos()
                self.launch_ball(mouse_src)

  def run(self):
    for event in pygame.event.get():
        if event.type == KEYUP and event.key == K_SPACE:
            for ball in self.ballsprites.sprites():
                ball.speed = array([-self.VEL_MAX * (2*random.random()-1), self.VEL_MAX * (2*random.random()-1)])
                #ball.speed = self.VEL_MAX * (2*random.randn(2)-1)
            self.start_game()
        elif event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN and event.key == K_q:
            sys.exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            mouse_src = pygame.mouse.get_pos()
            self.launch_ball(mouse_src)

def loadImage(name, colorKey = None):
    completeName = os.path.join('data',name) # Get a full name
    image = pygame.image.load(completeName) # load the image
    image = image.convert() # Convert the image for speed
    if colorKey != None: # colorkey (transparency) calculation
        if colorKey == -1:
            colorKey = image.get_at((0,0))
        image.set_colorkey(colorKey)
    return image

if __name__ == '__main__':
    game = Billiards(background = 'background.jpg',friction=True)
    while True:
        game.run()
    sys.exit(0)