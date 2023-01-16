import json
import os
import random

import jmespath
import pygame
import RPi.GPIO as GPIO

import globals

# File paths
appRoot = globals.appRoot + '/lucky-day/'
imageRoot = appRoot + 'images/'
audioRoot = appRoot + 'audio/'

# Positioning


# Scoring



class Game(object):
	def __init__(self):

		self.font = globals.fontScore

		pygame.display.set_caption('Lucky Day')
		pygame.display.set_icon(pygame.image.load(os.path.join(imageRoot, 'icon.png')).convert_alpha())

		self.mask = pygame.image.load(os.path.join(imageRoot, 'mask.png')).convert_alpha()

		self.arrow = pygame.image.load(os.path.join(imageRoot, 'arrow.jpg')).convert_alpha()
		self.arrowSpinning = pygame.image.load(os.path.join(imageRoot, 'arrow-spinning.jpg')).convert_alpha()
		self.arrowRotation = 0

		self.wheel = pygame.image.load(os.path.join(imageRoot, 'wheel.jpg')).convert_alpha()
		self.wheelSpinning = pygame.image.load(os.path.join(imageRoot, 'wheel-spinning.jpg')).convert_alpha()
		self.wheelRotation = 0

		self.win = pygame.image.load(os.path.join(imageRoot, 'win.png')).convert_alpha()
		
		self.audioSpinning = pygame.mixer.Sound(os.path.join(audioRoot, 'spinning.wav'))
		self.audioPoints = pygame.mixer.Sound(os.path.join(audioRoot, 'points.wav'))
		
		self.bet = 0
		self.spun = 0
		
	def playLuckyDay(self):
		buttonState = GPIO.input(10)
		if buttonState == GPIO.HIGH:
			self.spun = random.randint(1, 10)		
			self.spin()
			
		key = pygame.key.get_pressed()
		if globals.gameJustLaunched or key[pygame.K_UP] or key[pygame.K_DOWN]:
			if globals.gameJustLaunched == True:
				globals.gameJustLaunched = False
			self.spun = random.randint(1, 10)		
			self.spin()	
			


	def spin(self):
		
		# Spinning...
		#if currentFreePlays > 0:
		#	currentFreePlays = currentFreePlays - 1;
		#else:
		#	currentPayout = int(currentPayout) - (spinCost)

		#currentFreePlaysText = self.font.render(str(currentFreePlays), True, (255, 255, 255))
		#currentPayoutText = self.font.render(str(currentPayout), True, (255, 255, 255))

		wheelSpins = random.randrange(7, 15)
		pygame.mixer.Sound.play(self.audioSpinning, 10)
		for i in range(0, wheelSpins):
			if i == wheelSpins - 1 and self.wheelRotation >= (self.spun * 36):
				globals.displaySurface.blit(self.wheel, (0, 0))
			else:
				globals.displaySurface.blit(self.wheelSpinning, (0, 0))
						
			globals.displaySurface.blit(self.mask, (0,0))
			#globals.displaySurface.blit(currentFreePlaysText, (freePlaysX, freePlaysY))
			#globals.displaySurface.blit(currentPayoutText, (payoutX, payoutY))
			pygame.display.update()
			
		pygame.mixer.Sound.stop(self.audioSpinning)		
		
		if (self.bet == self.spun):
			
			# Update the screen...
			#currentFreePlaysText = self.font.render(str(currentFreePlays), True, (255, 255, 255))
			#currentPayoutText = self.font.render(str(currentPayout), True, (255, 255, 255))
			globals.displaySurface.blit(self.mask, (0,0))
			#globals.displaySurface.blit(currentFreePlaysText, (freePlaysX, freePlaysY))
			#globals.displaySurface.blit(currentPayoutText, (payoutX, payoutY))
			
			globals.displaySurface.blit(self.win, (0,0))
			pygame.mixer.Sound.play(self.audioPoints)
			
			for i in range(0, 20):
				GPIO.output(27,GPIO.HIGH)
				pygame.time.delay(100)
				GPIO.output(27,GPIO.LOW)

		pygame.display.update()
