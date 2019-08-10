#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 09:53:38 2019
@author: isai
"""
import sys, random as rand, pygame as py
from pygame.locals import *

py.init()
py.mixer.quit()

class Block(py.sprite.Sprite):
    def __init__(self, width, height, x, y):
        py.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = py.Surface([width, height])
        self.color = (127, 127, 127)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.nBombs = 0
        self.r = 0
        self.c = 0
        self.is_bomb = False
        self.is_visible = False
        self.font = py.font.SysFont("Chandas", 15)
        self.text = None
        self.text_rect = None
        py.draw.rect(self.image, self.color, [0, 0, width, height])

class Game:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.isRunning = True
        self.window = py.display.set_mode([self.width, self.height])
        self.sprites = py.sprite.Group()
        self.rows = 10
        self.cols = 10
        self.x, self.y = 230, 150
        self.w, self.h = 30, 30
        self.matrix = []
        self.game_over = False
        self.bombs = 13
        py.display.set_caption("Buscaminas")
        for i in range(self.rows):
            self.matrix.append([])
            for j in range(self.cols):
                self.matrix[i].append(Block(self.w, self.h, self.x + j * (self.w + 5), self.y + i * (self.h + 5)))
                self.matrix[i][j].r = i
                self.matrix[i][j].c = j
        for i in range(self.bombs):
            x = rand.randint(0, self.rows - 1)
            y = rand.randint(0, self.cols - 1)
            self.matrix[x][y].is_bomb = True
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.matrix[i][j].is_bomb:
                    self.matrix[i][j].nBombs = self.countBombs(i, j)           
        self.sprites.add(self.matrix)
        
    def gameLoop(self):
        clock = py.time.Clock()
        while(self.isRunning):
            self.events()
            self.draw()
            clock.tick(60)
            
    def show_cells(self, row, col):
        if not self.matrix[row][col].is_visible:
            self.matrix[row][col].is_visible = True
            self.matrix[row][col].text = self.matrix[row][col].font.render(str(self.matrix[row][col].nBombs), True, (0, 0, 0))
            self.matrix[row][col].text_rect = self.matrix[row][col].text.get_rect(center = self.matrix[row][col].rect.center)
            if self.matrix[row][col].nBombs == 0:
                for i in range(row - 1, row + 2):
                    for j in range(col - 1, col + 2):
                        if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
                            continue
                        if i == row and j == col:
                            continue
                        if not self.matrix[i][j].is_bomb:
                            self.show_cells(i, j)
            
    def events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.isRunning = False
                py.quit()
                sys.exit(0)
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = py.mouse.get_pos()
                for sprite in self.sprites:
                    if sprite.rect.collidepoint(mouse_position) and not sprite.is_bomb:
                        self.show_cells(sprite.r, sprite.c)
                    elif sprite.rect.collidepoint(mouse_position) and sprite.is_bomb:
                        self.game_over = True
                        print("Boom!")
    
    def countBombs(self, row, col):
        count = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
                    continue
                if i == row and j == col:
                    continue
                elif self.matrix[i][j].is_bomb:
                    count += 1
        return count
    
    def draw(self):
        self.window.fill((255, 255, 255))
        self.sprites.draw(self.window)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j].is_visible:
                    self.window.blit(self.matrix[i][j].text, self.matrix[i][j].text_rect)
        py.display.flip()

def main():
    game = Game()
    game.gameLoop()
    
if __name__ == '__main__':
    main()



    