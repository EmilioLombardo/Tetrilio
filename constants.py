DAS = 16 # Auto-shift delay (in frames)
ARR = 6 # Auto repeat rate (in frames)
framesPerCell = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6,
	5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2,
	2, 2, 2, 2, 2, 2, 2, 2, 1]

PURPLE = (180, 40, 140)
BLUE = (40, 80, 230)
GREEN = (40, 225, 20)
YELLOW = (230, 230, 0)
RED = (230, 0, 0)
ORANGE = (240, 150, 10)
CYAN = (0, 200, 230)

Torientations = (
	((-1, 0), (0, 0), (1, 0), (0, 1)), # 02: T down (spawn)
	((0, -1), (-1, 0), (0, 0), (0, 1)),  # 03: T left
	((-1, 0), (0, 0), (1, 0), (0, -1)), # 00: T up
	((0, -1), (0, 0), (1, 0), (0, 1)) # 01: T right
	)
Jorientations = (
	((-1, 0), (0, 0), (1, 0), (1, 1)), # 07: J down (spawn)
	((0, -1), (0, 0), (-1, 1), (0, 1)), # 04: J left
	((-1, -1), (-1, 0), (0, 0), (1, 0)), # 05: J up
	((0, -1), (1, -1), (0, 0), (0, 1)) # 06: J right
	)
Zorientations = (
	((-1, 0), (0, 0), (0, 1), (1, 1)), # 08: Z horizontal (spawn)
	((1, -1), (0, 0), (1, 0), (0, 1)) # 09: Z vertical
	)
Oorientations = (
	((-1, 0), (0, 0), (-1, 1), (0, 1)) # 0A: O (spawn)
	)
Sorientations = (
	((0, 0), (1, 0), (-1, 1), (0, 1)), # 0B: S horizontal (spawn)
	((0, -1), (0, 0), (1, 0), (1, 1)) # 0C: S vertical
	)
Lorientations = (
	((-1, 0), (0, 0), (1, 0), (-1, 1)), # 0E: L down (spawn)
	((-1, -1), (0, -1), (0, 0), (0, 1)), # 0F: L left
	((1, -1), (-1, 0), (0, 0), (1, 0)), # 10: L up
	((0, -1), (0, 0), (0, 1), (1, 1)) # 0D: L right
	)
Iorientations = (
	((-2, 0), (-1, 0), (0, 0), (1, 0)), # 12: I horizontal (spawn)
	((0, -2), (0, -1), (0, 0), (0, 1)) # 11: I vertical
	)
