import pygame, math, noise, random
pygame.init()

colors = [(36,159,222),(40,92,196),(20,52,100)]
detail = 80
sin_offset = 0
sin_multiplier = 20
layer_offset = 100
speed = 0.05
noise_div = 8

random.seed()
seed = random.random()*1000

sin_offset_modifier = 1

def update(surf, dt):

    global sin_offset, sin_offset_modifier
    sin_offset += dt * speed * sin_offset_modifier

    surf.fill(colors[0])

    poly1 = [[0,surf.get_size()[1]]]
    for i in range(detail+1):
        x = surf.get_size()[0] * (i/detail)
        poly1.append([x, 60 + (noise.pnoise1((i+sin_offset)/noise_div + seed)*16*math.sin(math.radians(i * sin_multiplier + sin_offset)))])
    poly1.append(surf.get_size())
    
    poly2 = [[0,surf.get_size()[1]]]
    for i in range(detail+1):
        x = surf.get_size()[0] * (i/detail)
        poly2.append([x, 120 + (noise.pnoise1((i+sin_offset)/noise_div + layer_offset + seed)*16*math.sin(math.radians(i * sin_multiplier/2 + sin_offset + layer_offset)))])
    poly2.append(surf.get_size())

    pygame.draw.polygon(surf, colors[1], poly1)
    pygame.draw.polygon(surf, colors[1], poly1, 2)
    pygame.draw.polygon(surf, colors[2], poly2)
    pygame.draw.polygon(surf, colors[2], poly2, 2)