import os
import sys

import pygame


def initialize():
	pygame.init()
	pygame.mixer.pre_init(16000, -16, 2, 1024)
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
	fontDefault = pygame.font.SysFont('Helvetica', 20, bold=False)

	global fontScore
	fontScore = pygame.font.SysFont('Helvetica', 32, bold=False)

	global appRoot
	appRoot = '/home/pi/tiny-bandit/'
	if os.path.exists(appRoot) == False:
		appRoot = os.getcwd() + '/'
	os.chdir(appRoot)

	global title
	title = 'Tiny Bandit'

	global iconDefault 
	iconDefault = os.path.join(appRoot, 'images/icon.png')

	global audioAmbience
	audioAmbience = pygame.mixer.Sound(os.path.join(appRoot, 'audio/ambience.wav'))
	
	global gameSelected
	gameSelected = 'none'

	global gameJustLaunched
	gameJustLaunched = False

	global gameInProgress
	gameInProgress = False

	global buttonCollection
	buttonCollection = []
	

def restart():
	os.execv(sys.executable, ['python'] + sys.argv)