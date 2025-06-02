
import random
import pygame

pygame.init()

WIDTH = 900
HEIGHT = 500
fps = 60
black = (0,0,0)
white = (255,255,255)
grey = (128,128,128)
red = (255,0,0)
yellow = (255,255,0)
pygame.display.set_caption('Flappy Space !')
screen = pygame.display.set_mode([WIDTH,HEIGHT])
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf',20)

#music