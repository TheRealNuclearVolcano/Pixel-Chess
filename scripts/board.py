import pygame

def draw(surf, white, black, size, offset, offset_x):

    x_offset = int((surf.get_size()[0] - (size * 8))/2 + offset_x)
    y_offset = int((surf.get_size()[1] - (size * 8))/2 + offset)
    board_bg_width1 = 4
    board_bg_width2 = 3
    board_bg_width3 = 1
    
    board_bg1 = pygame.Rect(x_offset - board_bg_width1, y_offset - board_bg_width1, size*8 + 2*board_bg_width1, size*8 + 2*board_bg_width1)
    board_bg2 = pygame.Rect(x_offset - board_bg_width2, y_offset - board_bg_width2, size*8 + 2*board_bg_width2, size*8 + 2*board_bg_width2)
    board_bg3 = pygame.Rect(x_offset - board_bg_width3, y_offset - board_bg_width3, size*8 + 2*board_bg_width3, size*8 + 2*board_bg_width3)

    pygame.draw.rect(surf, (74,84,98), board_bg1)
    pygame.draw.rect(surf, (179,185,209), board_bg2)
    pygame.draw.rect(surf, (74,84,98), board_bg3)

    for x in range(8):
        for y in range(8):
            
            if (x + y) % 2:
                surf.blit(black, (size*x + x_offset, size*y + y_offset))
            else:
                surf.blit(white, (size*x + x_offset, size*y + y_offset))

    return (x_offset, y_offset)
