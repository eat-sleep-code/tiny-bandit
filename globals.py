import os
import pygame

def initialize():
	pygame.init()
	pygame.mixer.init()

	global clock
	clock = pygame.time.Clock()

	global title
	title = 'Tiny Bandit'

	global screenWidth
	screenWidth = 480

	global screenHeight
	screenHeight = 800

	global displaySurface
	displaySurface = pygame.display.set_mode((screenWidth, screenHeight), pygame.HWSURFACE | pygame.DOUBLEBUF)

	#--------------------------------------------------------------------------
		
	global homePath
	homePath = os.getcwd()
	os.chdir(homePath)

	global splashDisplayed
	splashDisplayed = False
	
	global gameSelected
	gameSelected = 'none'

	global gameInProgress
	gameInProgress = False

	global buttonCollection
	buttonCollection = []
	