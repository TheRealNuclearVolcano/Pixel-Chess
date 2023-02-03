import pygame
pygame.init()

asset_img = pygame.image.load("data/assets.png")
size = 16

icon = asset_img.subsurface((16,16,16,16))

board = {
    "board_black":asset_img.subsurface((0,0,16,16)),
    "board_white":asset_img.subsurface((0,16,16,16)),
    "board_v":asset_img.subsurface((0,32,16,16)),
    "board_i":asset_img.subsurface((16,32,16,16)),
    "board_b":asset_img.subsurface((32,32,16,16)),
    "board_g":asset_img.subsurface((48,32,16,16)),
    "board_y":asset_img.subsurface((64,32,16,16)),
    "board_o":asset_img.subsurface((80,32,16,16)),
    "board_r":asset_img.subsurface((96,32,16,16))
}

piece = {
    "black":{
        "king":asset_img.subsurface((16,0,16,16)),
        "queen":asset_img.subsurface((32,0,16,16)),
        "bishop":asset_img.subsurface((48,0,16,16)),
        "knight":asset_img.subsurface((64,0,16,16)),
        "rook":asset_img.subsurface((80,0,16,16)),
        "pawn":asset_img.subsurface((96,0,16,16))
    },
    "white":{
        "king":asset_img.subsurface((16,16,16,16)),
        "queen":asset_img.subsurface((32,16,16,16)),
        "bishop":asset_img.subsurface((48,16,16,16)),
        "knight":asset_img.subsurface((64,16,16,16)),
        "rook":asset_img.subsurface((80,16,16,16)),
        "pawn":asset_img.subsurface((96,16,16,16))
    }
}