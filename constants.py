BOARD_SIZE = 10  # changing BOARD_SIZE will require other changes, i.e. piece starting positions
SCALE = 100
TILE_COLOR = (161, 176, 194)
BORDER_COLOR = (0, 0, 0)
WALL_COLOR = (79, 75, 72)

move_color = (27, 112, 12)
shoot_color = (209, 21, 49)

SELECTION_OPACITY = .3
MOVE_COLOR = (move_color[0] * SELECTION_OPACITY + TILE_COLOR[0] * (1 - SELECTION_OPACITY),
              move_color[1] * SELECTION_OPACITY + TILE_COLOR[1] * (1 - SELECTION_OPACITY),
              move_color[2] * SELECTION_OPACITY + TILE_COLOR[2] * (1 - SELECTION_OPACITY))

SHOOT_COLOR = (shoot_color[0] * SELECTION_OPACITY + TILE_COLOR[0] * (1 - SELECTION_OPACITY),
               shoot_color[1] * SELECTION_OPACITY + TILE_COLOR[1] * (1 - SELECTION_OPACITY),
               shoot_color[2] * SELECTION_OPACITY + TILE_COLOR[2] * (1 - SELECTION_OPACITY))
