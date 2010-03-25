# -*- coding: utf-8 -*-
import pygame, sys, os, random
from pygame.locals import *
import time
from math import *
from numpy import *

if not pygame.font: print "Warning, fonts disabled!"
if not pygame.mixer: print "Warning, sounds disabled!"

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

mod = lambda v: sqrt(v[0]*v[0] + v[1]*v[1])

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, board, vel=array([0.0,0.0]), is_white=False):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.is_white = is_white
        if self.is_white: self.image = self.board.theme.get_ball(0)
        else: self.image = self.board.theme.get_ball()
        self.rect = self.image.get_rect()
        pos = array(pos)
        self.rect.center = pos
        self.speed = vel
        self.initspeed = vel.copy()
        self.radius = int(self.rect.width / 2.0 + 1.0)
        self.pos = pos

    def draw(self):
        self.board.screen.blit(self.image, self.rect)
        pygame.display.flip()

    def set_pos(self, pos):
        self.pos = pos
        #self.rect.clamp_ip(to_int([pos[0]-self.pos[0], pos[1]-self.pos[1]]))
        #self.myrect = Rect(self.pos,(1,1))
        #self.rect.clamp_ip(self.myrect)
        self.rect.center = self.pos

    def decelerate(self, friction):
        if mod(self.speed) <= friction:
            self.speed = array([0.0,0.0])
        else:
            self.speed[0] = self.speed[0] - friction * self.speed[0] / mod(self.speed)  # friction acts in a direction
            self.speed[1] = self.speed[1] - friction * self.speed[1] / mod(self.speed)  # opposite to velocity

    def reflect(self):
        reflected = False
        if self.rect.left < 0 or self.rect.right > self.board.width:
            reflected = True
            self.speed[0] = -self.speed[0]
            if self.rect.left < 0:
                self.set_pos([self.radius, self.rect.center[1]])
            else:
                self.set_pos([self.board.width - self.radius, self.rect.center[1]])
        elif self.rect.top < 0 or self.rect.bottom > self.board.height:
            reflected = True
            self.speed[1] = -self.speed[1]
            if self.rect.top < 0:
                self.set_pos([self.rect.center[0], self.radius])
            else:
                self.set_pos([self.rect.center[0], self.board.height - self.radius])
        if reflected:
            self.board.collidecue_sound.play()

    def collide(self):
        '''
        Collides current ball with other balls of the board if possible.
        '''
        otherballs = self.board.ballsprites.sprites()[:]
        otherballs.remove(self)     # otherballs are all balls except *this* ball
        if len(otherballs) == 0:
            pass                      # no ball to collide with
        else:
            for otherball in otherballs:
                self.board.collide_ball(self, otherball)

    def go_to_holes(self):
        for hole in self.board.holerectlist:
            if hypot(*(self.rect.center-array(hole.center))) < 0.5*self.board.hole_radius:
                self.board.ballsprites.remove(self) # remove that ball from the game
                self.board.scoreboard.update(ball=self)          # update the score
                self.board.gotoholes_sound.play()


    def update(self, change=None, dest=None):
        '''
        Updates the position of current ball on the board according to the current speed and whether it reflects or collides with other balls
        (default action). If 'change' is specified, moves the ball by that change vector. If 'dest' is specified, moves the ball to the position
        specified by 'dest'.
        '''
        self.reflect()                              # reflects from board walls if possible
        self.collide()                              # collides with other balls if possible
        self.go_to_holes()                          # goes to holes if possible
        self.decelerate(self.board.friction)        # decelerates due to surface friction
        if change == None:
            change = self.speed
        if dest == None:
            self.set_pos(self.pos+change)
        else:
            self.rect.center = dest
