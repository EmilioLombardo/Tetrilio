width = 1080
height = int(width*3/4)
print(width, "x", height)

COLS = 10
ROWS = 20
fieldWidth = 300
fieldHeight = 2 * fieldWidth
# (x, y) for top-left corner of playing field:
fieldPos = ((width // 2) - (fieldWidth // 2), (height // 2) - (fieldHeight // 2))
cellSize = fieldWidth // COLS

DAS = 16 # Auto-shift delay (in frames)
ARR = 6 # Auto repeat rate (in frames)
framesPerCell = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6,
	5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2,
	2, 2, 2, 2, 2, 2, 2, 2, 1]

spawnPos = [5, 0]

PURPLE = (180, 40, 140)
BLUE = (40, 80, 230)
GREEN = (40, 225, 20)
YELLOW = (230, 230, 0)
RED = (230, 0, 0)
ORANGE = (240, 150, 10)
CYAN = (0, 200, 230)

colors = (PURPLE, BLUE, GREEN, YELLOW, RED, ORANGE, CYAN)

orientations = (
	( # orientations[0] -- T
		((-1, 0), (0, 0), (1, 0), (0, 1)), # 02: T down (spawn)
		((0, -1), (-1, 0), (0, 0), (0, 1)),  # 03: T left
		((-1, 0), (0, 0), (1, 0), (0, -1)), # 00: T up
		((0, -1), (0, 0), (1, 0), (0, 1)) # 01: T right
		),
	( # orientations[1] -- J
		((-1, 0), (0, 0), (1, 0), (1, 1)), # 07: J down (spawn)
		((0, -1), (0, 0), (-1, 1), (0, 1)), # 04: J left
		((-1, -1), (-1, 0), (0, 0), (1, 0)), # 05: J up
		((0, -1), (1, -1), (0, 0), (0, 1)) # 06: J right
		),
	( # orientations[2] -- Z
		((-1, 0), (0, 0), (0, 1), (1, 1)), # 08: Z horizontal (spawn)
		((1, -1), (0, 0), (1, 0), (0, 1)) # 09: Z vertical
		),
	( # orientations[3] -- O
		((-1, 0), (0, 0), (-1, 1), (0, 1)) # 0A: O (spawn)
	),
	( # orientations[4] -- S
		((0, 0), (1, 0), (-1, 1), (0, 1)), # 0B: S horizontal (spawn)
		((0, -1), (0, 0), (1, 0), (1, 1)) # 0C: S vertical
		),
	( # orientations[5] -- L
		((-1, 0), (0, 0), (1, 0), (-1, 1)), # 0E: L down (spawn)
		((-1, -1), (0, -1), (0, 0), (0, 1)), # 0F: L left
		((1, -1), (-1, 0), (0, 0), (1, 0)), # 10: L up
		((0, -1), (0, 0), (0, 1), (1, 1)) # 0D: L right
		),
	( # orientations[6] -- I
		((-2, 0), (-1, 0), (0, 0), (1, 0)), # 12: I horizontal (spawn)
		((0, -2), (0, -1), (0, 0), (0, 1)) # 11: I vertical
		)
)
