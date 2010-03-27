# -*- coding: utf-8 -*-

import logging
import os
import pygame

from settings import settings

class Theme(object):
    '''A class to implement themes in pybilliards
    All other objects using any data must request it from a theme
    '''
    def __init__(self, setting=None, name=None, path=None):
        if setting is None:
            setting = settings
        self.settings = setting
        if name is None:
            name = setting.get('theme')
            if name is None:
                name = 'default'
        if path is None:
            for f in setting.get('defaultdatadir'),setting.get('systemdatadir'),setting.get('userdatadir'):
                if os.path.isdir(f) and os.path.isdir(os.path.join(f,'themes')) and name in os.listdir(os.path.join(f,'themes')):
                    path = os.path.join(f,'themes',name)
                    break
        if path is None:
            logging.warn('Theme "%s" not found: using "default"'%name)
            name = 'default'
            path = os.path.join(setting.get('defaultdatadir'),'themes',name)
        self.name = name
        self.path = path

    def get_ball(self, ballnum=-1):
        '''get the ball image for specified ball number
        if the specified ball number is not exported by a theme the default
        ball of the theme is returned
        ballnum=0 is used as a convention for the striker ball'''
        suffix = str(ballnum) if ballnum >= 0 else ''
        suffix = suffix + '.png'
        try:
            ret = pygame.image.load(os.path.join(self.path,'ball%s'%suffix))
        except:
            logging.info('Theme "%s" does not provide ball%d: using default'%(self.name,ballnum))
            ret = pygame.image.load(os.path.join(self.path,'ball.png'))
        ret.convert_alpha()
        return ret

    def get_cue(self):
        ret = pygame.image.load(os.path.join(self.path,'cue.png'))
        ret.convert_alpha()
        return ret

    def get_background(self):
        ret = pygame.image.load(os.path.join(self.path,'background.png'))
        ret.convert_alpha()
        return ret

    def get_collide_snd(self):
        return pygame.mixer.Sound(os.path.join(self.path,'collide.ogg'))

    def get_gotoholes_snd(self):
        return pygame.mixer.Sound(os.path.join(self.path,'goal.ogg'))

    def get_finish_snd(self):
        return pygame.mixer.Sound(os.path.join(self.path,'finish.ogg'))

    def get(self, name):
        '''A convenience method to get image and sound objects from a theme
        and provide extensible theme support'''
        ext = name.split(os.path.extsep)
        ext = ext[-1] if len(ext)>1 else ''
        if ext == 'png':
            ret = pygame.image.load(os.path.join(self.path,name))
            ret.convert_alpha()
        elif ext == 'ogg':
            ret = pygame.mixer.Sound(os.path.join(self.path,name))
        else:
            ret = open(os.path.join(self.path,name))
        return ret

    def __getitem__(self, name):
        return self.get(name)

def get_theme(name=None):
    if name is None:
        theme = Theme(settings, settings.get('theme'))
    else:
        try:
            theme = __import__('data.themes.%s'%name,fromlist='Theme')
            theme = theme(settings, name)
        except ImportError:
            logging.info('cannot find theme: %s'%theme)
            theme = Theme(settings)
    return theme

