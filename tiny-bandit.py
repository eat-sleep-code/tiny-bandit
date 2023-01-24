import sys
import threading

import pygame
import RPi.GPIO as GPIO

import globals
from menu import CreateMenu

from flappy.game import Game as Flappy
from luckyDay.game import Game as LuckyDay
from magic8.game import Game as Magic8
from slots.game import Game as Slots

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
		for event in pygame.event.get():
			if globals.gameInProgress == False:
				if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
					for button in globals.buttonCollection:
						rect = button.rect
						if rect.collidepoint(event.pos):
							pygame.mixer.Sound.stop(globals.audioAmbience)
							globals.gameJustLaunched = True
							globals.gameInProgress = True
							globals.gameSelected = button.value
				
#--------------------------------------------------------------------------


def startup():

	try:
		globals.initialize()
		pygame.mixer.Sound.play(globals.audioAmbience, 5)
		
		buttonHandlerThread = threading.Thread(target=buttonHandler)
		buttonHandlerThread.start()

		globals.clock.tick(60)
		
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					globals.gameSelected == 'none'
					globals.gameInProgress == False
					globals.gameJustLaunched == False
					running = False
					pygame.display.quit()
					pygame.quit()
					sys.exit()


			if globals.gameSelected != 'none':
				if globals.gameSelected == 'slots':		
					Slots().playSlots()
				elif globals.gameSelected == 'flappy':
					Flappy().playFlappy()
				elif globals.gameSelected == 'lucky-day':
					LuckyDay().playLuckyDay()
				elif globals.gameSelected == 'magic-8':
					Magic8().playMagic8()
				
			else:
				pygame.display.set_caption(globals.title)
				pygame.display.set_icon(pygame.image.load(globals.iconDefault))
				CreateMenu()
				
		
	except KeyboardInterrupt:
		sys.exit(1)
		

#--------------------------------------------------------------------------


startup()
