import globals
import os
import pygame
import RPi.GPIO as GPIO
import sys
import threading
import time
import slots 
import flappy

# Run without Desktop
# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_MOUSEDRV', 'TSLIB')
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

#--------------------------------------------------------------------------


# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #BUTTON
GPIO.setup(27, GPIO.OUT) #LED


#--------------------------------------------------------------------------

def buttonHandler():
	while True:
		#print('Buttons: ', len(globals.buttonCollection))
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				for button in globals.buttonCollection:
					rect = button.rect
					if rect.collidepoint(event.pos):
						if button.type == 'schedule' and button.active == True:
							globals.gameInProgress = True
							globals.gameSelected = True
							globals.gameLink = button.value
				
#--------------------------------------------------------------------------

def startup():

	try:
		globals.initialize()
			
		if globals.splashDisplayed == False:
			#imageUtils.emptyCache()
			#showSplash = ShowSplash()
			#globals.splashDisplayed = True
			time.sleep(5)

		buttonHandlerThread = threading.Thread(target=buttonHandler)
		buttonHandlerThread.start()
		while True:
			if globals.gameSelected != 'none' and globals.gameInProgress == True:
				#showGame = ViewGame()
				if globals.gameSelected == 'slots':		
					slots.Game().playSlots()
				elif globals.gameSelected == 'flappy':
					flappy.Game().playFlappy()
			else:
				menu = CreateMenu()
		
	except KeyboardInterrupt:
		sys.exit(1)
		
#--------------------------------------------------------------------------

startup()

# Game Initialization
#screenX = 480 
# screenY = 800


#pygame.display.set_caption('Tiny Bandit')
#pygame.display.set_icon(pygame.image.load(os.path.join(appRoot, 'images/icon.png')))
#
#screen = pygame.display.set_mode((screenX, screenY))

#currentGame = 'none'
#running = True
#clock.tick(60)

#def playGame(requestedGame):
#	global currentGame
#	currentGame = requestedGame
#	print('Launching ' + currentGame + '...')
#	pass

#while running:
#	event = pygame.event.poll()
#	for event in pygame.event.get():
#		if event.type == pygame.QUIT:
#			currentGame = 'none'
#			running = False

	