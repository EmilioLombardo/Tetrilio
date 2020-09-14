import sys
import pygame
from pygame.locals import *

import constants as c


class Tetrimino:
	def __init__(self, typeID, centrePos):
		self.typeID = typeID
		self.centrePos = centrePos

		self.landed = False

		self.color = c.colors[typeID]
		self.orientations = c.orientations[typeID]

		self.minos = [] # list of coordinates for each mino

		for i in range(len(self.orientations[0])):
			relativeCoords = self.orientations[0][i]
			self.minos.append(relativeCoords)

	def draw(self, surface):

		for m in self.minos:
			gridPos = [m[i] + self.centrePos[i] for i in range(2)]
			pixelPos = gridToPixelPos(*gridPos)

			pygame.draw.rect(
				surface, self.color,
				(pixelPos[0], pixelPos[1], c.cellSize+1, c.cellSize+1)
				)

	def fall(self, deadMinos):

		# Move all minoes down one row
		self.minos = [[m[0], m[1] + 1] for m in self.minos]

		# Check for collision
		for m in self.minos:
			if m[1] + 1 > c.ROWS:
				# Move all minoes back up
				self.minos = [[m[0], m[1] - 1] for m in self.minos]
				self.landed = True
				return
			for dead in deadMinos:
				if m[1] + 1 > dead[1]:
					# Move all minoes back up
					self.minos = [[m[0], m[1] - 1] for m in self.minos]
					self.landed = True
					return

	def move(self):
		pass

	def rotate(self):
		pass

# Translates grid-coords into pixel-coords
def gridToPixelPos(gridX, gridY):
	pixelX = c.cellSize * gridX + c.fieldPos[0]
	pixelY = c.cellSize * gridY + c.fieldPos[1]
	return [pixelX, pixelY]

def drawGrid(surface, color):

	x = c.fieldPos[0]
	y = c.fieldPos[1]

	for i in range(c.COLS+1):
		pygame.draw.line(surface, color,
			(x, c.fieldPos[1]), (x, c.fieldPos[1] + c.fieldHeight))
		x += c.cellSize

	for l in range(c.ROWS+1):
		pygame.draw.line(surface, color,
			(c.fieldPos[0], y), (c.fieldPos[0] + c.fieldWidth, y))
		y += c.cellSize

def main():

	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	pygame.display.set_caption("Tetrilio")

	# Fill background
	bg = pygame.Surface(screen.get_size())
	bg = bg.convert()
	bg.fill((0, 0, 0))

	FPS = 60
	clock = pygame.time.Clock()
	frameCounter = 0
	level = 9
	deadMinos = []

	drawGrid(bg, (100, 100, 100))
	tetrimino = Tetrimino(0, c.spawnPos)
	tetrimino.draw(bg)

	# Blit everything to the screen
	screen.blit(bg, (0, 0))
	pygame.display.flip()

	running = True
	while running: # This is the game-loop

		#allows user to exit the screen
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
					pygame.quit()
					sys.exit()

		bg.fill((0, 0, 0))
		drawGrid(bg, (100,100,100))

		if frameCounter % c.framesPerCell[level] == 0:
			tetrimino.fall(deadMinos)

		if tetrimino.landed:
			for m in tetrimino.minos:
				minoX = m[0] + tetrimino.centrePos[0]
				minoY = m[1] + tetrimino.centrePos[1]

				deadMinos.append((minoX, minoY, tetrimino.color))
			del tetrimino
			tetrimino = Tetrimino(0, c.spawnPos) # Spawn new tetrimino

		tetrimino.draw(bg)
		for mino in deadMinos:
			if mino is not None:
				pixelPos = gridToPixelPos(mino[0], mino[1])
				pygame.draw.rect(
					bg, mino[2],
					(pixelPos[0], pixelPos[1], c.cellSize+1, c.cellSize+1)
					)

		# Update screen
		screen.blit(bg, (0, 0))
		pygame.display.flip()

		frameCounter += 1
		clock.tick(FPS)

main()
