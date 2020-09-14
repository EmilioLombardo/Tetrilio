import sys

import pygame
from pygame.locals import *

import constants as c


class Tetrimino:
	def __init__(self, typeID, centrePos):
		self.typeID = typeID
		self.centrePos = centrePos

		self.color = c.colors[typeID]
		self.orientations = c.orientations[typeID]

		self.minos = [] # list of coordinates for each mino

		for i in range(len(self.orientations[0])):
			coords = self.orientations[0][i]
			self.minos.append(coords)

	def draw(self, surface):
		for m in self.minos:
			gridPos = [
				m[i] + self.centrePos[i] for i in range(2)
				]
			pixelPos = gridToPixelPos(*gridPos)

			pygame.draw.rect(
				surface, self.color,
				(pixelPos[0], pixelPos[1], cellSize+1, cellSize+1)
				)

	def fall(self):
		pass

	def move(self):
		pass

	def rotate(self):
		pass


def gridToPixelPos(gridX, gridY):
	pixelX = cellSize * gridX + fieldPos[0]
	pixelY = cellSize * gridY + fieldPos[1]
	return [pixelX, pixelY]

def drawGrid(surface, color):

	x = fieldPos[0]
	y = fieldPos[1]

	for i in range(COLS+1):
		pygame.draw.line(surface, color,
			(x, fieldPos[1]), (x, fieldPos[1] + fieldHeight))
		x += cellSize

	for l in range(ROWS+1):
		pygame.draw.line(surface, color,
			(fieldPos[0], y), (fieldPos[0] + fieldWidth, y))
		y += cellSize

def main():

	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Tetrilio")

	# Fill background
	bg = pygame.Surface(screen.get_size())
	bg = bg.convert()
	bg.fill((0, 0, 0))

	# Blit everything to the screen
	screen.blit(bg, (0, 0))
	pygame.display.flip()

	FPS = 60
	clock = pygame.time.Clock()
	frameCounter = 0

	drawGrid(bg, (100, 100, 100))

	while True: # This is the game-loop

		#allows user to exit the screen
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		tetrimino = Tetrimino(6, c.spawnPos)
		tetrimino.draw(bg)

		# Update screen. This code should be ran every frame
		screen.blit(bg, (0, 0))
		pygame.display.flip()

		frameCounter += 1
		clock.tick(FPS)

main()
