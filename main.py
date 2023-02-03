import pygame, sys, time, json, math
pygame.init()

import scripts.img as img
import scripts.board as board
import scripts.background as bg
import scripts.piece as piece

window_size = (0, 0)
window = pygame.display.set_mode(window_size, pygame.FULLSCREEN)
window_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

pygame.display.set_caption("Pixel Chess")
pygame.display.set_icon(img.icon)

render_size = (320, 180)
render = pygame.Surface(render_size)

font16 = pygame.font.Font("data/m6x11.ttf", 16)
font32 = pygame.font.Font("data/m6x11.ttf", 32)
font48 = pygame.font.Font("data/m6x11.ttf", 48)

ratio = (window_size[0]/render_size[0], window_size[1]/render_size[1])

default_config = {
    "board":{
        "board-1":"board_white",
        "board-2":"board_black",
        "selected":"board_y",
        "legal-move-white":"board_g",
        "legal-move-black":"board_b",
        "move-capture":"board_r",
        "in-check":"board_o"
    },
    "fullscreen":True
}

with open("config.json", "r") as f:
    config = json.load(f)

for dat in config["board"].values():
    if dat not in img.board.keys():
        config = default_config
        print("error in config.json\nusing default config")
        break

def start():

    running = True
    last_time = time.time()
    dt = 1
    clock = pygame.time.Clock()

    start_button = pygame.Rect(8, 180-8-72-21, 44, 21)
    start_text = font16.render("START", False, (255,255,255))
    start_text_rect = start_text.get_rect(center=start_button.center)
    start_text_rect.y += 2
    
    settings_button = pygame.Rect(8, 180-8-48-21, 66, 21)
    settings_text = font16.render("SETTINGS", False, (255,255,255))
    settings_text_rect = settings_text.get_rect(center=settings_button.center)
    settings_text_rect.y += 2

    tutorial_button = pygame.Rect(8, 180-8-24-21, 84, 21)
    tutorial_text = font16.render("HOW TO PLAY", False, (255,255,255))
    tutorial_text_rect = tutorial_text.get_rect(center=tutorial_button.center)
    tutorial_text_rect.y += 2

    quit_button = pygame.Rect(8, 180-8-21, 38, 21)
    quit_text = font16.render("QUIT", False, (255,255,255))
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    quit_text_rect.y += 2

    info_button = pygame.Rect(320-8-21, 180-8-20, 20, 21)
    info_text = font16.render("i", False, (255,255,255))
    info_text_rect = info_text.get_rect(center=info_button.center)
    info_text_rect.y += 2

    while running:

        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        bg.update(render, dt)
        pygame.draw.rect(render, (255,255,255), start_button, 2, 4)
        render.blit(start_text, start_text_rect)
        pygame.draw.rect(render, (255,255,255), settings_button, 2, 4)
        render.blit(settings_text, settings_text_rect)
        pygame.draw.rect(render, (255,255,255), tutorial_button, 2, 4)
        render.blit(tutorial_text, tutorial_text_rect)
        pygame.draw.rect(render, (255,255,255), quit_button, 2, 4)
        render.blit(quit_text, quit_text_rect)
        pygame.draw.rect(render, (255,255,255), info_button, 2, 4)
        render.blit(info_text, info_text_rect)

        window.blit(pygame.transform.scale(render, window_size), (0, 0))
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                pos = (pos[0]/ratio[0], pos[1]/ratio[1])
                if start_button.collidepoint(pos):
                    game()
                if quit_button.collidepoint(pos):
                    return

        clock.tick()

def game():

    running = True
    last_time = time.time()
    dt = 1
    clock = pygame.time.Clock()
    draw_offset = 160

    quit_screen = pygame.Surface(render_size)
    quit_screen.set_alpha(170)
    quit_screen_on = False
    quit_screen_text = font32.render("Quit?", False, (255,255,255))
    quit_screen_text_rect = quit_screen_text.get_rect()
    quit_screen_text_rect.center = quit_screen.get_rect().center
    quit_screen_text2 = font16.render("'Esc' to Cancel | 'Enter' to Quit", False, (255,255,255))
    quit_screen_text2_rect = quit_screen_text2.get_rect()
    quit_screen_text2_rect.center = (quit_screen.get_rect().center[0], quit_screen.get_rect().center[1] + 24)
    quit_screen.blit(quit_screen_text, quit_screen_text_rect)
    quit_screen.blit(quit_screen_text2, quit_screen_text2_rect)

    black_win_screen = pygame.Surface(render_size)
    black_win_screen.set_alpha(170)
    black_win_screen_on = False
    black_win_screen_text = font32.render("Black Wins", False, (255,255,255))
    black_win_screen_text_rect = black_win_screen_text.get_rect()
    black_win_screen_text_rect.center = black_win_screen.get_rect().center
    black_win_screen_text2 = font16.render("'Esc' to Quit", False, (255,255,255))
    black_win_screen_text2_rect = black_win_screen_text2.get_rect()
    black_win_screen_text2_rect.center = (black_win_screen.get_rect().center[0], black_win_screen.get_rect().center[1] + 24)
    black_win_screen.blit(black_win_screen_text, black_win_screen_text_rect)
    black_win_screen.blit(black_win_screen_text2, black_win_screen_text2_rect)

    white_win_screen = pygame.Surface(render_size)
    white_win_screen.set_alpha(170)
    white_win_screen_on = False
    white_win_screen_text = font32.render("White Wins", False, (255,255,255))
    white_win_screen_text_rect = white_win_screen_text.get_rect()
    white_win_screen_text_rect.center = white_win_screen.get_rect().center
    white_win_screen_text2 = font16.render("'Esc' to Quit", False, (255,255,255))
    white_win_screen_text2_rect = white_win_screen_text2.get_rect()
    white_win_screen_text2_rect.center = (white_win_screen.get_rect().center[0], white_win_screen.get_rect().center[1] + 24)
    white_win_screen.blit(white_win_screen_text, white_win_screen_text_rect)
    white_win_screen.blit(white_win_screen_text2, white_win_screen_text2_rect)

    pos = (0,0)

    pieces = []
    selected_piece = None
    moving = "white"
    white_checked = False
    black_checked = False
    white_capture = []
    black_capture = []

    # ---- UI ----
    ui_colors = [(249,153,67),(36,159,222),(180,32,42),(20,160,46),(34,28,26),(50,43,40)]

    white_panel = pygame.Rect(188, 98, 100, 60)

    white_text_1 = font16.render("playing", False, ui_colors[0])
    white_text_1_rect = white_text_1.get_rect()
    white_text_1_rect.top = white_panel.top + 6
    white_text_1_rect.left = white_panel.left + 6
    white_text_2 = font16.render(":", False, ui_colors[1])
    white_text_2_rect = white_text_2.get_rect()
    white_text_2_rect.top = white_panel.top + 6
    white_text_2_rect.left = white_text_1_rect.right
    white_text_3 = font16.render("False", False, ui_colors[2])
    white_text_3_rect = white_text_3.get_rect()
    white_text_3_rect.top = white_panel.top + 6
    white_text_3_rect.left = white_text_2_rect.right
    white_text_4 = font16.render("True", False, ui_colors[3])
    white_text_4_rect = white_text_4.get_rect()
    white_text_4_rect.top = white_panel.top + 6
    white_text_4_rect.left = white_text_2_rect.right
    white_text_rect = pygame.Rect(white_panel.left+3, white_panel.top+3, white_panel.width-6, white_text_1_rect.height+6)

    white_text2_1 = font16.render("in_check", False, ui_colors[0])
    white_text2_1_rect = white_text2_1.get_rect()
    white_text2_1_rect.top = white_panel.top + 6 + 21
    white_text2_1_rect.left = white_panel.left + 6
    white_text2_2 = font16.render(":", False, ui_colors[1])
    white_text2_2_rect = white_text2_2.get_rect()
    white_text2_2_rect.top = white_panel.top + 6 + 21
    white_text2_2_rect.left = white_text2_1_rect.right
    white_text2_3 = font16.render("False", False, ui_colors[2])
    white_text2_3_rect = white_text2_3.get_rect()
    white_text2_3_rect.top = white_panel.top + 6 + 21
    white_text2_3_rect.left = white_text2_2_rect.right
    white_text2_4 = font16.render("True", False, ui_colors[3])
    white_text2_4_rect = white_text2_4.get_rect()
    white_text2_4_rect.top = white_panel.top + 6 + 21
    white_text2_4_rect.left = white_text2_2_rect.right
    white_text2_rect = pygame.Rect(white_panel.left+3, white_panel.top+3 + 21, white_panel.width-6, white_text_1_rect.height+3)

    black_panel = pygame.Rect(188, 22, 100, 60)

    black_text_1 = font16.render("playing", False, ui_colors[0])
    black_text_1_rect = black_text_1.get_rect()
    black_text_1_rect.top = black_panel.top + 6
    black_text_1_rect.left = black_panel.left + 6
    black_text_2 = font16.render(":", False, ui_colors[1])
    black_text_2_rect = black_text_2.get_rect()
    black_text_2_rect.top = black_panel.top + 6
    black_text_2_rect.left = black_text_1_rect.right
    black_text_3 = font16.render("False", False, ui_colors[2])
    black_text_3_rect = black_text_3.get_rect()
    black_text_3_rect.top = black_panel.top + 6
    black_text_3_rect.left = black_text_2_rect.right
    black_text_4 = font16.render("True", False, ui_colors[3])
    black_text_4_rect = black_text_4.get_rect()
    black_text_4_rect.top = black_panel.top + 6
    black_text_4_rect.left = black_text_2_rect.right
    black_text_rect = pygame.Rect(black_panel.left+3, black_panel.top+3, black_panel.width-6, black_text_1_rect.height+6)

    black_text2_1 = font16.render("in_check", False, ui_colors[0])
    black_text2_1_rect = black_text2_1.get_rect()
    black_text2_1_rect.top = black_panel.top + 6 + 21
    black_text2_1_rect.left = black_panel.left + 6
    black_text2_2 = font16.render(":", False, ui_colors[1])
    black_text2_2_rect = black_text2_2.get_rect()
    black_text2_2_rect.top = black_panel.top + 6 + 21
    black_text2_2_rect.left = black_text2_1_rect.right
    black_text2_3 = font16.render("False", False, ui_colors[2])
    black_text2_3_rect = black_text2_3.get_rect()
    black_text2_3_rect.top = black_panel.top + 6 + 21
    black_text2_3_rect.left = black_text2_2_rect.right
    black_text2_4 = font16.render("True", False, ui_colors[3])
    black_text2_4_rect = black_text2_4.get_rect()
    black_text2_4_rect.top = black_panel.top + 6 + 21
    black_text2_4_rect.left = black_text2_2_rect.right
    black_text2_rect = pygame.Rect(black_panel.left+3, black_panel.top+3 + 21, black_panel.width-6, black_text_1_rect.height+3)
    # ---- UI ----

    for i in range(8):
        pieces.append(piece.Pawn(render, img, "white", i, 6))
        pieces.append(piece.Pawn(render, img, "black", i, 1))

    pieces.append(piece.Rook(render, img, "white", 0, 7))
    pieces.append(piece.Knight(render, img, "white", 1, 7))
    pieces.append(piece.Bishop(render, img, "white", 2, 7))
    pieces.append(piece.Queen(render, img, "white", 3, 7))
    pieces.append(piece.King(render, img, "white", 4, 7))
    pieces.append(piece.Bishop(render, img, "white", 5, 7))
    pieces.append(piece.Knight(render, img, "white", 6, 7))
    pieces.append(piece.Rook(render, img, "white", 7, 7))

    pieces.append(piece.Rook(render, img, "black", 0, 0))
    pieces.append(piece.Knight(render, img, "black", 1, 0))
    pieces.append(piece.Bishop(render, img, "black", 2, 0))
    pieces.append(piece.Queen(render, img, "black", 3, 0))
    pieces.append(piece.King(render, img, "black", 4, 0))
    pieces.append(piece.Bishop(render, img, "black", 5, 0))
    pieces.append(piece.Knight(render, img, "black", 6, 0))
    pieces.append(piece.Rook(render, img, "black", 7, 0))

    while running:

        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        if draw_offset > 0:
            draw_offset -= dt * 5 * abs(math.sin(math.radians(draw_offset)))
        if draw_offset < 1:
            draw_offset = 0

        bg.update(render, dt)
        offset = board.draw(render, img.board[config["board"]["board-1"]], img.board[config["board"]["board-2"]], img.size, draw_offset, -60)

        if selected_piece != None:
            render.blit(img.board[config["board"]["selected"]], (pieces[selected_piece].x * 16 + offset[0], pieces[selected_piece].y * 16 + offset[1]))
            for move in pieces[selected_piece].moves:
                if pieces[selected_piece].check_valid_move(pieces[selected_piece].x + move[0], pieces[selected_piece].y + move[1], pieces):
                    
                    if pieces[selected_piece].color == "white":
                        render.blit(img.board[config["board"]["legal-move-white"]], ((pieces[selected_piece].x + move[0]) * 16 + offset[0], (pieces[selected_piece].y + move[1]) * 16 + offset[1]))
                    if pieces[selected_piece].color == "black":
                        render.blit(img.board[config["board"]["legal-move-black"]], ((pieces[selected_piece].x + move[0]) * 16 + offset[0], (pieces[selected_piece].y + move[1]) * 16 + offset[1]))
                    
                    for piece_ in pieces:
                        if (piece_.x, piece_.y) == (pieces[selected_piece].x + move[0], pieces[selected_piece].y + move[1]):
                            render.blit(img.board[config["board"]["move-capture"]], ((pieces[selected_piece].x + move[0]) * 16 + offset[0], (pieces[selected_piece].y + move[1]) * 16 + offset[1]))
                            break

        white_checked,black_checked = False,False

        for piece_ in pieces:
            if isinstance(piece_, piece.King):
                if piece_.color == "white":
                    if piece_.is_in_check(pieces):
                        render.blit(img.board[config["board"]["in-check"]], (piece_.x * 16 + offset[0], piece_.y * 16 + offset[1]))
                        white_checked = True
                if piece_.color == "black":
                    if piece_.is_in_check(pieces):
                        render.blit(img.board[config["board"]["in-check"]], (piece_.x * 16 + offset[0], piece_.y * 16 + offset[1]))
                        black_checked = True
            piece_.draw(offset, dt)
            if not isinstance(piece_, piece.King):
                piece_.king_in_check = False
            
        for piece_ in pieces:
            if not isinstance(piece_, piece.King):
                if piece_.color == "white":
                    if white_checked:
                        piece_.king_in_check = True
                if piece_.color == "black":
                    if black_checked:
                        piece_.king_in_check = True

        '''render.blit(font16.render("eat a dick nigga", False, (255,255,255)), (4,4))'''

        pygame.draw.rect(render, (179,185,209), white_panel, 0, 4)
        pygame.draw.rect(render, (218,224,234), white_panel, 2, 4)
        pygame.draw.rect(render, ui_colors[4], white_text_rect, 0, 2)
        pygame.draw.rect(render, ui_colors[5], white_text_rect, 1, 2)
        render.blit(white_text_1, white_text_1_rect)
        render.blit(white_text_2, white_text_2_rect)
        pygame.draw.rect(render, ui_colors[4], white_text2_rect, 0, 2)
        pygame.draw.rect(render, ui_colors[5], white_text2_rect, 1, 2)
        render.blit(white_text2_1, white_text2_1_rect)
        render.blit(white_text2_2, white_text2_2_rect)

        pygame.draw.rect(render, (74,84,98), black_panel, 0, 4)
        pygame.draw.rect(render, (51,57,65), black_panel, 2, 4)
        pygame.draw.rect(render, ui_colors[4], black_text_rect, 0, 2)
        pygame.draw.rect(render, ui_colors[5], black_text_rect, 1, 2)
        render.blit(black_text_1, black_text_1_rect)
        render.blit(black_text_2, black_text_2_rect)
        pygame.draw.rect(render, ui_colors[4], black_text2_rect, 0, 2)
        pygame.draw.rect(render, ui_colors[5], black_text2_rect, 1, 2)
        render.blit(black_text2_1, black_text2_1_rect)
        render.blit(black_text2_2, black_text2_2_rect)

        if moving == "white":
            render.blit(white_text_4, white_text_4_rect)
            render.blit(black_text_3, black_text_3_rect)
        else:
            render.blit(white_text_3, white_text_3_rect)
            render.blit(black_text_4, black_text_4_rect)

        if white_checked:
            render.blit(white_text2_4, white_text2_4_rect)
        else:
            render.blit(white_text2_3, white_text2_3_rect)

        if black_checked:
            render.blit(black_text2_4, black_text2_4_rect)
        else:
            render.blit(black_text2_3, black_text2_3_rect)

        for i, piece_ in enumerate(white_capture):
            render.blit(piece_, (white_panel.left+4+(i*4), white_text2_1_rect.bottom+2))
        for i, piece_ in enumerate(black_capture):
            render.blit(piece_, (black_panel.left+4+(i*4), black_text2_1_rect.bottom+2))
        
        if quit_screen_on:
            render.blit(quit_screen, (0,0))
        if black_win_screen_on:
            render.blit(black_win_screen, (0,0))
        if white_win_screen_on:
            render.blit(white_win_screen, (0,0))

        window.blit(pygame.transform.scale(render, window_size), (0, 0))
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if white_win_screen_on or black_win_screen_on:
                        return
                    quit_screen_on = not quit_screen_on
                if event.key == pygame.K_RETURN:
                    if quit_screen_on:
                        return

            if event.type == pygame.MOUSEBUTTONUP:

                pos = pygame.mouse.get_pos()
                pos = (pos[0]/ratio[0], pos[1]/ratio[1])

                if not quit_screen_on and not black_win_screen_on and not white_win_screen_on:
                    last_selected_piece = selected_piece

                    if selected_piece != None:
                        x = (pos[0] - offset[0]) // 16
                        y = (pos[1] - offset[1]) // 16
                        moved = pieces[selected_piece].move(x, y, pieces)
                        if moved:
                            if pieces[selected_piece].color == "white":
                                moving = "black"
                            else:
                                moving = "white"
                        selected_piece = None

                    for i, piece_ in sorted(enumerate(pieces), reverse=True):
                        rect = pygame.Rect(piece_.x*16 + offset[0], piece_.y*16 + offset[1], 16, 16)
                        if rect.collidepoint(pos):
                            if piece_.captured:
                                pieces.pop(i)
                                if piece_.color == "white":
                                    black_capture.append(piece_.img)
                                    if isinstance(piece_, piece.King):
                                        black_win_screen_on = True
                                if piece_.color == "black":
                                    white_capture.append(piece_.img)
                                    if isinstance(piece_, piece.King):
                                        white_win_screen_on = True
                                break
                            if piece_.color == moving:
                                selected_piece = i

                    if last_selected_piece == selected_piece:
                        selected_piece = None

        clock.tick()
        #pygame.display.set_caption(str(round(clock.get_fps())))

start()
pygame.quit()
sys.exit()