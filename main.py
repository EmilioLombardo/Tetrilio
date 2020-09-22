import sys
import random
import pygame
from pygame.locals import *

import constants as c


class Tetrimino:
	def __init__(self, typeID, spawnPos):
		self.typeID = typeID
		self.centrePos = spawnPos.copy()

		self.landed = False

		self.color = c.colors[typeID]
		self.orientations = c.allOrientations[typeID]
		self.orientationIndex = 0 # The current orientation. 0 = spawn orientation

		self.minos = [[], [], [], []] # list of coordinates for each mino

		self.updateMinos()

	# Update coords of minos according to orientation and centrePos
	def updateMinos(self):
		i = 0
		for relativeXY in self.orientations[self.orientationIndex]:
			minoCoords = [a + b for a, b in zip(relativeXY, self.centrePos)]
			self.minos[i] = minoCoords
			i += 1

	def draw(self, surface):

		for m in self.minos:
			pixelPos = gridToPixelPos(*m)

			pygame.draw.rect(
				surface, self.color,
				(pixelPos[0], pixelPos[1], c.cellSize+1, c.cellSize+1)
				)

	def fall(self, deadMinos):

		# Move all minoes down one row
		self.centrePos[1] += 1
		self.updateMinos()

		self.landed = False

		# Check for collision
		for m in self.minos:
			if m[1] + 1 > c.ROWS:
				# Move all minoes back up
				self.centrePos[1] -= 1
				self.updateMinos()
				self.landed = True
				return

			for dead in deadMinos:
				if m[:2] == dead[:2]:
					# Move all minoes back up
					print(m[:2], dead[:2])
					self.centrePos[1] -= 1
					self.updateMinos()
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
	tetrimino = Tetrimino(random.randint(0, 6), c.spawnPos)
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

		if tetrimino.landed:
			for m in tetrimino.minos:
				# (x, y, color)
				deadMinos.append([m[0], m[1], tetrimino.color])

			# Spawn new tetrimino
			del tetrimino
			tetrimino = Tetrimino(random.randint(0, 6), c.spawnPos)

		if frameCounter % c.framesPerCell[level] == 0:
			tetrimino.fall(deadMinos)

		tetrimino.draw(bg)
		for dead in deadMinos:
			pixelPos = gridToPixelPos(dead[0], dead[1])
			pygame.draw.rect(
				bg, dead[2],
				(pixelPos[0], pixelPos[1], c.cellSize+1, c.cellSize+1)
				)

		# Update screen
		screen.blit(bg, (0, 0))
		pygame.display.flip()

		frameCounter += 1
		clock.tick(FPS)

main()
