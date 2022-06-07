""" 
    author: Chu Duc Anh
    Github: https://github.com/ChuDucAnh242002
    A game of calculate to 98 created High School Le Hong Phong in Viet Nam
"""

import pygame
import sys
import os

from button import Button

 
pygame.init()

WIDTH, HEIGHT = 1200, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("98")

CLOCK = pygame.time.Clock()
FPS = 60

# Image
bg = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'Background', 'background.jpg')), (WIDTH, HEIGHT))



def draw_bg():
    WIN.blit(bg, (0, 0))  

def main():
    run = True
    while run:
        draw_bg()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        pygame.display.update()



def lobby():
    run = True

def menu():
    run = True
    menu_button = Button(375, 312, "Click to join the server")

    while run:
        CLOCK.tick(FPS)
        draw_bg()
        menu_button.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menu_button.click(pos):
                    # try;
                    run = False
                    main()
                    break
                    # except:
                    #     print("Server Offline")

        pygame.display.update()

        
if __name__ == "__main__":
    while True:
        menu()