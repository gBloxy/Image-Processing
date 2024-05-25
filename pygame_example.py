
from sys import exit
import pygame
pygame.init()

# import the image processing library
import processing as ip


# load the image with pygame
image = pygame.image.load('image.png')

# create the pygame window
win = pygame.display.set_mode((image.get_width() * 2 + 75, image.get_height() + 50))
pygame.display.set_caption('Image Processing example with PyGame')
clock = pygame.time.Clock()

# display the original image
win.blit(image, (25, 25))

# create the shader with for example a colors inversion filter
shader = ip.Shader(ip.INVERSION)

# run the shader on the image and return the processed texture
tex = shader.run(image)

# convert the processed texture into a pygame Surface
surf = tex.toSurface()

# display the processed image
win.blit(surf, (tex.size[0] + 50, 25))


# pygame gameloop
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
    clock.tick(10)
    pygame.display.flip()
