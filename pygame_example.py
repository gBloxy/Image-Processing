
import pygame
from sys import exit
pygame.init()

import processing as p


win = pygame.display.set_mode((1200, 400))
pygame.display.set_caption('Image Processing example with PyGame')

clock = pygame.time.Clock()


image = pygame.image.load('image.png')

win.blit(image, (40, 25))

shader = p.Shader(p.DEFAULT)

out = shader.run(image)

surf = out.toSurface()

win.blit(surf, (1200-40-out.size[0], 25))


while True:
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()
        exit()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    clock.tick(10)
    
    pygame.display.flip()
