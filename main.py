import sys

import pygame
from pygame.locals import *

import constants as c

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

class Tetrimino:
	def __init__(self, typeID, centerPos):
		self.typeID = typeID
		self.centerPos = centerPos

		self.color = c.colors[typeID]
		self.orientations = c.orientations[typeID]

		self.minos = [] # list of coordinates for each mino

		for i in range(len(orientations)):
			orientation = orientations[i]
			self.minos.append(orientation)

	def draw(self, surface):
		pass

	def fall(self):
		pass

	def move(self):
		pass

	def rotate(self):
		pass

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


		# Update screen. This code should be ran every frame
		screen.blit(bg, (0, 0))
		pygame.display.flip()

		frameCounter += 1
		clock.tick(FPS)

main()
