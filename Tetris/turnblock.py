import copy

# Wall-kick tests für I und andere Shapes (SRS Standard)
# Format: [(x offset, y offset), ...]
WALL_KICKS = {
    "I": {
        (0,1): [(0,0), (-2,0), (+1,0), (-2,-1), (+1,+2)],
        (1,0): [(0,0), (+2,0), (-1,0), (+2,+1), (-1,-2)],
        (1,2): [(0,0), (-1,0), (+2,0), (-1,+2), (+2,-1)],
        (2,1): [(0,0), (+1,0), (-2,0), (+1,-2), (-2,+1)],
        (2,3): [(0,0), (+2,0), (-1,0), (+2,+1), (-1,-2)],
        (3,2): [(0,0), (-2,0), (+1,0), (-2,-1), (+1,+2)],
        (3,0): [(0,0), (+1,0), (-2,0), (+1,-2), (-2,+1)],
        (0,3): [(0,0), (-1,0), (+2,0), (-1,+2), (+2,-1)],
    },
    "others": {
        (0,1): [(0,0), (-1,0), (-1,+1), (0,-2), (-1,-2)],
        (1,0): [(0,0), (+1,0), (+1,-1), (0,+2), (+1,+2)],
        (1,2): [(0,0), (+1,0), (+1,-1), (0,+2), (+1,+2)],
        (2,1): [(0,0), (-1,0), (-1,+1), (0,-2), (-1,-2)],
        (2,3): [(0,0), (+1,0), (+1,+1), (0,-2), (+1,-2)],
        (3,2): [(0,0), (-1,0), (-1,-1), (0,+2), (-1,+2)],
        (3,0): [(0,0), (-1,0), (-1,-1), (0,+2), (-1,+2)],
        (0,3): [(0,0), (+1,0), (+1,+1), (0,-2), (+1,-2)],
    }
}

def rotate_matrix(shape, clockwise=True):
    """Rotate a 2D shape 90° clockwise or counterclockwise."""
    if clockwise:
        return [list(row) for row in zip(*shape[::-1])]
    else:
        return [list(row) for row in zip(*shape)][::-1]

def try_rotate(piece, board, clockwise=True):
    """
    Versucht ein Piece zu rotieren.
    piece: dict mit keys shape, x, y, colors, type
    board: aktuelle Boardmatrix
    """
    piece_type = piece.get("type", "others")  # z.B. "I", "O", "others"
    if piece_type == "O":
        return piece  # O block rotiert nicht

    old_shape = piece["shape"]
    new_shape = rotate_matrix(old_shape, clockwise)
    old_rot = piece.get("rotation", 0)
    new_rot = (old_rot + (1 if clockwise else -1)) % 4

    # Wall-kick Test
    kicks = WALL_KICKS.get(piece_type, WALL_KICKS["others"])
    key = (old_rot, new_rot)
    for dx, dy in kicks.get(key, [(0,0)]):
        new_x = piece["x"] + dx
        new_y = piece["y"] + dy
        if can_place(new_shape, new_x, new_y, board):
            new_piece = copy.deepcopy(piece)
            new_piece["shape"] = new_shape
            new_piece["x"] = new_x
            new_piece["y"] = new_y
            new_piece["rotation"] = new_rot
            return new_piece

    return piece  # Rotation nicht möglich

def can_place(shape, px, py, board):
    """Check if shape can be placed at position on board."""
    rows = len(board)
    cols = len(board[0])
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                bx = px + x
                by = py + y
                if bx < 0 or bx >= cols or by >= rows:
                    return False
                if by >= 0 and board[by][bx] is not None:
                    return False
    return True
