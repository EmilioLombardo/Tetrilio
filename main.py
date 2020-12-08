import sys
import random
import pygame
from pygame.locals import *
from numpy import array


import constants as c


class Tetrimino:
	def __init__(self, typeID, centrePos):
		self.typeID = typeID
		self.centrePos = centrePos.copy()

		self.landed = False
		self.hidden = False

		self.colour = c.colours[typeID]
		self.orientations = c.allOrientations[typeID]
		self.orientationIndex = 0 # The current orientation

		self.minos = [ # 2D list with of x and y coordinates for each mino
			[] for _ in range(len(self.orientations[self.orientationIndex]))
			]

		# Fill in self.minos with appropriate coords
		self.updateMinos()

	# Update coords of minos according to orientation and centrePos
	def updateMinos(self):

		i = 0
		for relativeXY in self.orientations[self.orientationIndex]:
			newCoords = [a + b for a, b in zip(relativeXY, self.centrePos)]
			self.minos[i] = newCoords
			i += 1

	def draw(self, surface):
		mPixelCoords = array([gridToPixelPos(*m) for m in self.minos])

		# Top left corner
		x1 = min(mPixelCoords[:,0])
		y1 = min(mPixelCoords[:,1]) - 2 * c.cellSize

		# Bottom right corner
		x2 = max(mPixelCoords[:,0]) + c.cellSize
		y2 = max(mPixelCoords[:,1]) + c.cellSize

		w = x2 - x1
		h = y2 - y1

		dirtyRect = pygame.Rect(x1, y1, w, h)

		if self.hidden:
			return dirtyRect

		for m in self.minos:
			pixelPos = gridToPixelPos(*m)

			pygame.draw.rect(
				surface, self.colour,
				(pixelPos[0], pixelPos[1], c.cellSize, c.cellSize)
				)

		return dirtyRect

	def fall(self, deadMinos):

		# Move all minos down one row
		self.centrePos[1] += 1
		self.updateMinos()

		self.landed = False

		# Check for collision
		for m in self.minos:
			# Collision with bottom
			if m[1] + 1 > c.ROWS:
				# Move all minos back up
				self.centrePos[1] -= 1
				self.updateMinos()
				self.landed = True
				return

			# Collision with dead minos
			for dead in deadMinos:
				if m[:2] == dead[:2]:
					# Move all minos back up
					self.centrePos[1] -= 1
					self.updateMinos()
					self.landed = True
					return

	def shift(self, direction, deadMinos):
		prevPos = self.centrePos[0]

		if direction.lower() == "left":
			self.centrePos[0] -= 1
			self.updateMinos()

		if direction.lower() == "right":
			self.centrePos[0] += 1
			self.updateMinos()

		# Check for collision
		for m in self.minos:
			# Collision with walls
			if m[0] + 1 > c.COLS or m[0] < 0:
				# Move all minos back
				self.centrePos[0] = prevPos
				self.updateMinos()
				return

			# Collision with dead minos
			for dead in deadMinos:
				if m[:2] == dead[:2]:
					# Move all minos back
					self.centrePos[0] = prevPos
					self.updateMinos()
					return

	def rotate(self, direction, deadMinos):
		prevOrientation = self.orientationIndex

		if direction.lower() == "cw":
			self.orientationIndex += 1
			self.orientationIndex %= len(self.orientations)
			self.updateMinos()

		if direction.lower() == "ccw":
			self.orientationIndex -= 1
			self.orientationIndex %= len(self.orientations)
			self.updateMinos()

		# Check for collision
		for m in self.minos:
			# Collision with walls or floor
			if (m[0] >= c.COLS) or (m[0] < 0) or (m[1] >= c.ROWS):
				# Move all minos back
				self.orientationIndex = prevOrientation
				self.updateMinos()
				return

			# Collision with dead minos
			for dead in deadMinos:
				if m[:2] == dead[:2]:
					# Move all minos back
					self.orientationIndex = prevOrientation
					self.updateMinos()
					return

# Translates grid-coords into pixel-coords
def gridToPixelPos(gridX, gridY):
	pixelX = c.cellSize * gridX + c.fieldPos[0]
	pixelY = c.cellSize * gridY + c.fieldPos[1]
	return [pixelX, pixelY]

def drawGrid(surface, colour):

	x = c.fieldPos[0]
	y = c.fieldPos[1]

	# Vertical lines
	for _ in range(c.COLS + 1):
		pygame.draw.line(surface, colour,
			(x, c.fieldPos[1]), (x, c.fieldPos[1] + c.fieldHeight))
		x += c.cellSize

	# Horisontal lines
	for _ in range(c.ROWS + 1):
		pygame.draw.line(surface, colour,
			(c.fieldPos[0], y), (c.fieldPos[0] + c.fieldWidth, y))
		y += c.cellSize

def completeRows(deadMinos):

	completeRows = []

	for rowN in range(c.ROWS):
		deadMinosInRow = [mino[:2] for mino in deadMinos if mino[1] == rowN]

		if len(deadMinosInRow) >= c.COLS:
			completeRows.append(rowN)

	# Returns a list of which rows are fillled in
	return completeRows


def main():

	# Initialise screen
	pygame.init()
	flags = pygame.DOUBLEBUF | pygame.FULLSCREEN
	screen = pygame.display.set_mode((0, 0), flags)
	# screen = pygame.display.set_mode((c.width, c.height), flags)
	pygame.display.set_caption("Tetrilio")

	# Fill background
	bg = pygame.Surface(screen.get_size())
	bg = bg.convert()
	bg.fill((0, 0, 0))

	paused = False
	gameOver = False
	startDelay = 90 # Delay before first piece starts falling (in frames)
	FPS = 60
	clock = pygame.time.Clock()
	frameCounter = 0
	DAScounter = 0 # For control of horisontal movement
	ARE = 0 # Delay after tetrimino lands (in frames)

	lines = 0
	points = 0
	startLevel = 15
	level = startLevel # Controls falling speed

	# transition is the number of lines needed before the first level increase.
	# After the transition, the level increases every 10 lines.
	# (This replicates the NES version of tetris)
	transition = min(
		startLevel * 10 + 10,
		max(100, (startLevel * 10 - 50))
		)
	# if startLevel <= 9:
	# 	transition = startLevel * 10 + 10
	# else:
	# 	transition = max(100, (startLevel * 10 - 50))

	deadMinos = []
	completeRows_ = []
	clearingLines = False

	# Fonts
	bigFont = pygame.font.Font("ARCADE_N.ttf", 20)
	smallFont = pygame.font.Font("ARCADE_N.ttf", 14)

	# Create current and next tetrimino
	nextPiece = Tetrimino(random.randint(0, 6), [13, 10])
	tetrimino = Tetrimino(random.randint(0, 6), c.spawnPos.copy())

	# Function that draws everything
	def drawAll():
		bg.fill((0, 0, 0))
		drawGrid(bg, (60, 60, 60))

		dirtyRects = []

		dirtyRects.append(nextPiece.draw(bg))

		if not paused:
			dirtyRects.append(tetrimino.draw(bg))

			# Draw all dead minos
			for dead in deadMinos:
				pixelPos = gridToPixelPos(dead[0], dead[1])
				dirtyRects.append(
					pygame.draw.rect(
						bg,
						dead[2],
						(pixelPos[0], pixelPos[1], c.cellSize, c.cellSize)
						)
					)

		# Various text
		linesText = bigFont.render(
			f"LINES {lines}", False, c.WHITE
			)
		pointsText = bigFont.render(
			f"{points}", False, c.WHITE
			)
		levelText = bigFont.render(
			f"LEVEL {level}", False, c.WHITE
			)
		pressToPauseText = smallFont.render(
			f"Press SPACE to pause and ESC to quit", False, c.GREY
			)

		dirtyRects.append(
			bg.blit(linesText, (c.fieldPos[0] - 220, c.fieldPos[1] + 10))
			)
		dirtyRects.append(
			bg.blit(pointsText,
				(c.fieldPos[0] + c.fieldWidth + 30, c.fieldPos[1] + 10))
			)
		dirtyRects.append(
			bg.blit(levelText, (c.fieldPos[0] - 220, c.fieldPos[1] + 60))
			)
		dirtyRects.append(
			bg.blit(pressToPauseText, (10, c.height - 30))
			)

		# Update screen
		screen.blit(bg, (0, 0))
		pygame.display.update(dirtyRects)
		# pygame.display.flip()

	drawAll()

	running = True
	while running: # This is the game-loop

		# Allows user to exit the screen
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			elif (event.type == pygame.KEYDOWN and
				  event.key == pygame.K_ESCAPE):
				running = False
				pygame.quit()
				sys.exit()

			# Pause game
			elif (event.type == pygame.KEYDOWN and
				  event.key in [pygame.K_SPACE, pygame.K_p, pygame.K_RETURN]):
				  paused = True if paused is False else False

		if paused:
			drawAll()
			continue

		# Shifting and rotation
		for event in events:
			if event.type == pygame.KEYDOWN:

				# Rotation:
				if event.key == pygame.K_k:
					tetrimino.rotate("cw", deadMinos)

				elif event.key == pygame.K_j:
					tetrimino.rotate("ccw", deadMinos)

				# Shifting:
				if event.key == pygame.K_a:
					prevPos = tetrimino.centrePos.copy()
					tetrimino.shift("left", deadMinos)
					currPos = tetrimino.centrePos.copy()
					DAScounter = 0 if currPos != prevPos else c.DAS-c.ARR
					# Charge DAS if tetrimino hits wall or dead mino
					# This mechanic replicates the NES version of tetris

				elif event.key == pygame.K_d:
					prevPos = tetrimino.centrePos.copy()
					tetrimino.shift("right", deadMinos)
					currPos = tetrimino.centrePos.copy()
					DAScounter = 0 if currPos != prevPos else c.DAS-c.ARR
					# Charge DAS if tetrimino hits wall or dead mino

			# If one of the shifting keys are released, reset DAS counter
			if (event.type == pygame.KEYUP and
				event.key in [pygame.K_a, pygame.K_d]):

				DAScounter = 0

		# Manage DAS:
		keys = pygame.key.get_pressed()

		if keys[pygame.K_a]: # If LEFT is held
			DAScounter += 1
			if DAScounter == c.DAS:
				tetrimino.shift("left", deadMinos)
				DAScounter = c.DAS - c.ARR

		if keys[pygame.K_d]: # If RIGHT is held
			DAScounter += 1
			if DAScounter == c.DAS:
				tetrimino.shift("right", deadMinos)
				DAScounter = c.DAS - c.ARR

		# Make tetrimino fall:
		if startDelay > 0:
			pass

		# Normal drop speed
		elif frameCounter % c.framesPerCell[level] == 0:
			tetrimino.fall(deadMinos)

		# Faster drop if holding DOWN
		elif keys[pygame.K_s] and frameCounter % 2 == 0:
			tetrimino.fall(deadMinos)
			points += 1

		# Handle tetrimino landing
		if tetrimino.landed == True:
			# Add the tetrimino's minos to deadMinos
			for m in tetrimino.minos:
				if m in [dead[:2] for dead in deadMinos]:
					gameOver = True
				deadMinos.append([m[0], m[1], tetrimino.colour])

			# Spawn new tetrimino and next piece
			tetrimino = nextPiece
			tetrimino.hidden = True
			tetrimino.centrePos = c.spawnPos.copy() # Move to top
			tetrimino.updateMinos()

			nextPiece = Tetrimino(random.randint(0, 6), [13, 10])

			# Check for complete rows
			completeRows_ = completeRows(deadMinos).copy()

			if len(completeRows_) != 0: # If there are lines to clear
				clearingLines = True
				deadMinosAbove = []

				for rowN in completeRows_:
					deadMinosAbove += [
						m for m in deadMinos
						if (m[1] < rowN and
							m[1] not in completeRows_ and
							m not in deadMinosAbove)
						]

			lines += len(completeRows_)

			# Calculate delay after tetrimino locks in place
			lockPos = min(*[m[1] for m in tetrimino.minos])
			ARE = 10 + (lockPos // 4) * 2 # Delay in frames

		# Update screen
		drawAll()

		while gameOver:
			main()
			gameOver = False

		# Advance one frame
		if ARE == 0:
			startDelay -= 1 if startDelay > 0 else 0
			frameCounter += 1
			clock.tick(FPS)

		# Delay after tetrimino locks in place
		while ARE > 0:
			if not clearingLines:
				tetrimino.hidden = False
			frameCounter += 1
			clock.tick(FPS)
			ARE -= 1

		# Clear completed lines
		if clearingLines:
			x = c.COLS // 2
			while x >= 0:
				frameCounter += 1
				clock.tick(FPS)

				if frameCounter % 4 != 0:
					continue

				for rowN in completeRows_:
					# Remove minos at position x and at COLS-x
					minosToRemove = [
						m for m in deadMinos
						if (m[0] == x or m[0] == c.COLS - x) and
							m[1] == rowN
						]

					deadMinos = [
						m for m in deadMinos
						if m not in minosToRemove
						]
				x -= 1

				# Update display
				drawAll()

			points += c.clearPoints[len(completeRows_)] * (level + 1)
			clearingLines = False

			# Move all minos above the cleared rows down
			for mino in deadMinosAbove:
				displacement = 0
				for rowN in completeRows_:
					if mino[1] < rowN: # If mino is above cleared row
						displacement += 1

				mino[1] += displacement - 1 # idk why -1 but it works

			# Move all minos above the filled row down one line
			for mino in deadMinosAbove:
				mino[1] += 1

			level = startLevel + max(0, 1 + (lines - transition) // 10)
			tetrimino.hidden = False

main()
