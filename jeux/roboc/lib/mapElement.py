#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pdb
import re, random

class Element():
    self.name = 'element'
    self.symbol = '?'
    self.visible = True
    self.penetrate = True

    def __init__(self,coord=(0,0)):
        self.__coordinates=coord

    def reach(self,labyrinth,robot): pass


class Wall(Element):
    self.name = 'wall'
    self.symbol = '#'
    self.visible = True
    self.penetrate = False


class Door(Element):
    self.name = 'door'
    self.symbol = '.'
    self.visible = True
    self.penetrate = True

    def __init__(self,coord=(0,0),open=True,key=None):
        self.__coordinates=coord
        self.__open=open
        self.__key = key

    def isOpen(self):
        return self.__open

    def open(self):
        if self.__key.isOpenDoor(self):
            self.__open = True
            self.symbol = '.'
    def close(self):
        if self.__key.isOpenDoor(self):
            self.__open = False
            self.symbol = '-'


class Key(Element):
    self.name = 'key'
    self.symbol = '?'
    self.visible = True
    self.penetrate = True

    def __init__(self, coord=(0, 0), door=None):
        self.__coordinates = coord
        self.__door = door

    def isOpenDoor(self,door):
        if door == self.__door: return True
        else: return False

    def reach(self, labyrinth, robot):
        robot.use['key'].append(self)

class Stair(Element):
    self.name = 'stair'
    self.symbol = '/'
    self.visible = True
    self.penetrate = True

    def __init__(self,coord=(0,0),up=None,down=None):
        self.__coordinates=coord
        self.__accessUp   = up
        self.__accessDown = down

    @property
    def accessUp(self): return self.__accessUp
    @accessUp.setter
    def accessUp(self,val):self.__accessUp=val

    @property
    def accessDown(self): return self.__accessDown
    @accessDown.setter
    def accessDown(self, val): self.__accessDown = val


class Exit(Element):
    self.name = 'exit'
    self.symbol = '='
    self.visible = True
    self.penetrate = True

    def __init__(self,coord=(0,0)):
        self.__coordinates=coord

    def reach(self,labyrinth,robot): labyrinth.done = True

class Torch(Element):
    self.name = 'torch'
    self.symbol = '?'
    self.visible = True
    self.penetrate = True

    def __init__(self,coord=(0,0),lightDist=3):
        self.__coordinates=coord
        self.__lightDist = lightDist

    @property
    def lightDist (self): return self.__lightDist
    @lightDist .setter
    def lightDist (self,val):self.__lightDist =val

    def reach(self, labyrinth, robot):
        robot.use['torch'] = self