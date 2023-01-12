import os

import pygame


def initialize():
	pygame.init()
	pygame.mixer.init()

	global clock
	clock = pygame.time.Clock()

	global screenWidth
	screenWidth = 480

	global screenHeight
	screenHeight = 800

	global displaySurface
	displaySurface = pygame.display.set_mode((screenWidth, screenHeight), pygame.HWSURFACE | pygame.DOUBLEBUF)

	global fontDefault
	fontDefault = pygame.font.SysFont('Helvetica', 16, bold=False)

	global fontScore
	fontScore = pygame.font.SysFont('Helvetica', 32, bold=False)

	global appRoot
	appRoot = os.getcwd() + '/'
	os.chdir(appRoot)

	global title
	title = 'Tiny Bandit'

	global iconDefault 
	iconDefault = os.path.join(appRoot, 'images/icon.png')
	
	global gameSelected
	gameSelected = 'none'

	global gameJustLaunched
	gameJustLaunched = False

	global gameInProgress
	gameInProgress = False

	global buttonCollection
	buttonCollection = []
	