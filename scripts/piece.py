import pygame

lerp_rate = 0.2

def lerp(a, b, t, dt):
    return a + (b - a) * t * dt

class Pawn:

    def __init__(self, surf, img, color, x, y):
        self.surf = surf
        self.img = img.piece[color]["pawn"]
        self.x = x
        self.y = y
        self.last_pos = (x,y)
        self.lerp_pos = (x,y)
        self.color = color
        if color == "white":
            self.moves = [[0,-2],[0,-1],[-1,-1],[1,-1]]
        if color == "black":
            self.moves = [[0,2], [0,1],[-1,1],[1,1]]
        self.first_move = True
        self.captured = False
        self.king_in_check = False

    def check_valid_move(self, x, y, pieces):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        for move in self.moves:
            if self.x + move[0] == x and self.y + move[1] == y:
                if move[0] == 0:
                    for piece_ in pieces:
                        if piece_.x == x and piece_.y == y:
                            return False
                    return True
                else:
                    for piece_ in pieces:
                        if piece_.x == x and piece_.y == y:
                            if piece_.color != self.color:
                                return True
        return False

    def move(self, x, y, pieces):
        occupied = False
        for piece_ in pieces:
            if piece_.x == x and piece_.y == y:
                if piece_.color == self.color:
                    occupied = True
                    break
        if not occupied and self.check_valid_move(x, y, pieces):
            for piece_ in pieces:
                if piece_.x == x and piece_.y == y:
                    if piece_.color != self.color:
                        piece_.captured = True
                        break
            self.last_pos = (self.x,self.y)
            self.lerp_progress = (self.x,self.y)
            self.x = x
            self.y = y
            if self.first_move:
                self.moves.pop(0)
            self.first_move = False
            return True
        return False


    def draw(self, offset, dt):
        self.lerp_pos = (lerp(self.lerp_pos[0], self.x, lerp_rate, dt), lerp(self.lerp_pos[1], self.y, lerp_rate, dt))
        x,y = self.lerp_pos
        self.surf.blit(self.img, (x*16+offset[0], y*16+offset[1]))


class Knight:
    def __init__(self, surf, img, color, x, y):
        self.surf = surf
        self.img = img.piece[color]["knight"]
        self.color = color
        self.x = x
        self.y = y
        self.last_pos = (x,y)
        self.lerp_pos = (x,y)
        self.rect = pygame.Rect(x*16, y*16, 16, 16)
        self.moves = [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
        self.captured = False
        self.king_in_check = False

    def draw(self, offset, dt):
        self.lerp_pos = (lerp(self.lerp_pos[0], self.x, lerp_rate, dt), lerp(self.lerp_pos[1], self.y, lerp_rate, dt))
        x,y = self.lerp_pos
        self.surf.blit(self.img, (x*16+offset[0], y*16+offset[1]))

    def check_valid_move(self, x, y, pieces):
        occupied = False
        for piece_ in pieces:
            if piece_.x == x and piece_.y == y:
                if piece_.color == self.color:
                    return False
                occupied = True
                break
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        for move in self.moves:
            if self.x + move[0] == x and self.y + move[1] == y:
                return True
        return False

    def move(self, x, y, pieces):
        if self.check_valid_move(x, y, pieces):
            for piece_ in pieces:
                if piece_.x == x and piece_.y == y:
                    if piece_.color != self.color:
                        piece_.captured = True
                        break
            self.last_pos = (self.x,self.y)
            self.lerp_progress = (self.x,self.y)
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x*16, y*16, 16, 16)
            return True
        return False


class Bishop:
    def __init__(self, surf, img, color, x, y):
        self.surf = surf
        self.img = img.piece[color]["bishop"]
        self.x = x
        self.y = y
        self.last_pos = (x,y)
        self.lerp_pos = (x,y)
        self.color = color
        self.moves = []
        self.update_moves()
        self.captured = False
        self.king_in_check = False

    def draw(self, offset, dt):
        self.lerp_pos = (lerp(self.lerp_pos[0], self.x, lerp_rate, dt), lerp(self.lerp_pos[1], self.y, lerp_rate, dt))
        x,y = self.lerp_pos
        self.surf.blit(self.img, (x*16+offset[0], y*16+offset[1]))

    def update_moves(self):
        self.moves = []
        for i in range(1,8):
            self.moves.append([i, i])
            self.moves.append([-i, i])
            self.moves.append([i, -i])
            self.moves.append([-i, -i])

    def check_valid_move(self, x, y, pieces):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        dx = x - self.x
        dy = y - self.y
        if abs(dx) != abs(dy):
            return False
        x_step = dx // abs(dx)
        y_step = dy // abs(dy)
        for i in range(1, int(abs(dx))):
            for piece in pieces:
                if piece.x == self.x + x_step*i and piece.y == self.y + y_step*i:
                    return False
        for piece in pieces:
            if piece.x == x and piece.y == y:
                if piece.color != self.color:
                    return True
                if piece.color == self.color:
                    return False
        return True

    def move(self, x, y, pieces):
        if self.check_valid_move(x, y, pieces):
            for piece_ in pieces:
                if piece_.x == x and piece_.y == y:
                    if piece_.color != self.color:
                        piece_.captured = True
                        break
            self.last_pos = (self.x,self.y)
            self.lerp_progress = (self.x,self.y)
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x*16, y*16, 16, 16)
            return True
        return False


class Rook:
    def __init__(self, surf, img, color, x, y):
        self.surf = surf
        self.img = img.piece[color]["rook"]
        self.x = x
        self.y = y
        self.last_pos = (x,y)
        self.lerp_pos = (x,y)
        self.color = color
        self.moves = []
        self.update_moves()
        self.captured = False
        self.king_in_check = False

    def draw(self, offset, dt):
        self.lerp_pos = (lerp(self.lerp_pos[0], self.x, lerp_rate, dt), lerp(self.lerp_pos[1], self.y, lerp_rate, dt))
        x,y = self.lerp_pos
        self.surf.blit(self.img, (x*16+offset[0], y*16+offset[1]))

    def update_moves(self):
        self.moves = []
        for i in range(8):
            self.moves.append([i, 0])
            self.moves.append([0, i])
            self.moves.append([-i, 0])
            self.moves.append([0, -i])

    def check_valid_move(self, x, y, pieces):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        dx = x - self.x
        dy = y - self.y
        if (dx != 0 and dy != 0) or (dx == 0 and dy == 0):
            return False
        x_step = dx // abs(dx) if dx != 0 else 0
        y_step = dy // abs(dy) if dy != 0 else 0
        for i in range(1, int(max(abs(dx), abs(dy)))):
            for piece in pieces:
                if piece.x == self.x + x_step*i and piece.y == self.y + y_step*i:
                    return False
        for piece in pieces:
            if piece.x == x and piece.y == y:
                if piece.color != self.color:
                    return True
                if piece.color == self.color:
                    return False
        return True


    def move(self, x, y, pieces):
        if self.check_valid_move(x, y, pieces):
            for piece_ in pieces:
                if piece_.x == x and piece_.y == y:
                    if piece_.color != self.color:
                        piece_.captured = True
                        break
            self.last_pos = (self.x,self.y)
            self.lerp_progress = (self.x,self.y)
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x*16, y*16, 16, 16)
            return True
        return False


class Queen:
    def __init__(self, surf, img, color, x, y):
        self.surf = surf
        self.img = img.piece[color]["queen"]
        self.x = x
        self.y = y
        self.last_pos = (x,y)
        self.lerp_pos = (x,y)
        self.color = color
        self.moves = []
        self.update_moves()
        self.captured = False
        self.king_in_check = False

    def draw(self, offset, dt):
        self.lerp_pos = (lerp(self.lerp_pos[0], self.x, lerp_rate, dt), lerp(self.lerp_pos[1], self.y, lerp_rate, dt))
        x,y = self.lerp_pos
        self.surf.blit(self.img, (x*16+offset[0], y*16+offset[1]))

    def update_moves(self):
        self.moves = []
        for i in range(8):
            self.moves.append([i, 0])
            self.moves.append([0, i])
            self.moves.append([-i, 0])
            self.moves.append([0, -i])
            self.moves.append([i, i])
            self.moves.append([-i, i])
            self.moves.append([i, -i])
            self.moves.append([-i, -i])

    def check_valid_move(self, x, y, pieces):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        dx = x - self.x
        dy = y - self.y
        x_step = dx // abs(dx) if dx != 0 else 0
        y_step = dy // abs(dy) if dy != 0 else 0
        if abs(dx) == abs(dy):
            for i in range(1, int(abs(dx))):
                if any(piece.x == self.x + x_step*i and piece.y == self.y + y_step*i for piece in pieces):
                    return False
        elif dx == 0 or dy == 0:
            for i in range(1, int(max(abs(dx), abs(dy)))):
                if any(piece.x == self.x + x_step*i and piece.y == self.y + y_step*i for piece in pieces):
                    return False
        else:
            return False
        for piece in pieces:
            if piece.x == x and piece.y == y:
                if piece.color != self.color:
                    return True
                if piece.color == self.color:
                    return False
        return True

    def move(self, x, y, pieces):
        if self.check_valid_move(x, y, pieces):
            for piece_ in pieces:
                if piece_.x == x and piece_.y == y:
                    if piece_.color != self.color:
                        piece_.captured = True
                        break
            self.last_pos = (self.x,self.y)
            self.lerp_progress = (self.x,self.y)
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x*16, y*16, 16, 16)
            return True
        return False


class King:
    def __init__(self, surf, img, color, x, y):
        self.surf = surf
        self.img = img.piece[color]["king"]
        self.color = color
        self.x = x
        self.y = y
        self.last_pos = (x,y)
        self.lerp_pos = (x,y)
        self.moves = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
        self.captured = False

    def draw(self, offset, dt):
        self.lerp_pos = (lerp(self.lerp_pos[0], self.x, lerp_rate, dt), lerp(self.lerp_pos[1], self.y, lerp_rate, dt))
        x,y = self.lerp_pos
        self.surf.blit(self.img, (x*16+offset[0], y*16+offset[1]))

    def check_valid_move(self, x, y, pieces):
        if self.is_in_check(pieces, (x,y)):
            return False
        for piece_ in pieces:
            if piece_.x == x and piece_.y == y:
                if piece_.color == self.color:
                    return False
                break
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        for move in self.moves:
            if self.x + move[0] == x and self.y + move[1] == y:
                return True
        return False

    def move(self, x, y, pieces):
        if self.check_valid_move(x, y, pieces):
            for piece_ in pieces:
                if piece_.x == x and piece_.y == y:
                    if piece_.color != self.color:
                        piece_.captured = True
                        break
            self.last_pos = (self.x,self.y)
            self.lerp_progress = (self.x,self.y)
            self.x = x
            self.y = y
            return True
        return False

    def is_in_check(self, pieces, pos=None):
        if not pos:
            x,y = self.x,self.y
        else:
            x,y = pos
        for piece_ in pieces:
            if piece_.color != self.color and not isinstance(piece_, King):
                if isinstance(piece_, Pawn):
                    if piece_.color == "white":
                        if (x, y) == (piece_.x-1, piece_.y-1) or (x, y) == (piece_.x+1, piece_.y-1):
                            return True
                    if piece_.color == "black":
                        if (x, y) == (piece_.x-1, piece_.y+1) or (x, y) == (piece_.x+1, piece_.y+1):
                            return True
                else:
                    for move in piece_.moves:
                        if piece_.check_valid_move(piece_.x+move[0], piece_.y+move[1], pieces):
                            if (x, y) == (piece_.x+move[0], piece_.y+move[1]):
                                return True
        return False

    def check_mate(self,pieces):
        return
