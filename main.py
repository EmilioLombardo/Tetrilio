import sys

import pygame
from pygame.locals import *

import constants as c


def main():
	width = 1080
	height = int(width*3/4)
	print(width, "x", height)

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
