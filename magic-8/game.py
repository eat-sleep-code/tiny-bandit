import json
import os
import random

import jmespath
import pygame
import RPi.GPIO as GPIO

import globals

# File paths
appRoot = globals.appRoot + '/magic-8/'
imageRoot = appRoot + 'images/'
audioRoot = appRoot + 'audio/'

# Positioning


class Game(object):
	def __init__(self):

		self.font = globals.fontScore

		pygame.display.set_caption('Magic 8')
		pygame.display.set_icon(pygame.image.load(os.path.join(imageRoot, 'icon.png')).convert_alpha())

		self.mask = pygame.image.load(os.path.join(imageRoot, 'mask.png')).convert_alpha()

		self.ball = pygame.image.load(os.path.join(imageRoot, 'ball.jpg')).convert_alpha()
		self.ballShaking = pygame.image.load(os.path.join(imageRoot, 'ball-shaking.jpg')).convert_alpha()
		self.ballX = 0

		self.ballWindow = pygame.image.load(os.path.join(imageRoot, 'ball-window.jpg')).convert_alpha()
		self.ballWindowShaking = pygame.image.load(os.path.join(imageRoot, 'ball-window-shaking.jpg')).convert_alpha()
		self.ballWindowX = 0

		self.audioShaking = pygame.mixer.Sound(os.path.join(audioRoot, 'shaking.wav'))
		self.audioResults = pygame.mixer.Sound(os.path.join(audioRoot, 'results.wav'))
		
		self.result = ''
		
	def playMagic8(self):
		buttonState = GPIO.input(10)
		if buttonState == GPIO.HIGH:
			self.spun = random.randint(1, 10)		
			self.shake()
			
		key = pygame.key.get_pressed()
		if globals.gameJustLaunched or key[pygame.K_UP] or key[pygame.K_DOWN]:
			if globals.gameJustLaunched == True:
				globals.gameJustLaunched = False
			self.spun = random.randint(1, 10)		
			self.shake()	
			


	def shake(self):
		
		# Shaking...
		
		ballShakes = random.randrange(7, 15)
		pygame.mixer.Sound.play(self.audioShaking, 10)
		for i in range(0, ballShakes):
			if i == ballShakes - 1:
				globals.displaySurface.blit(self.ball, (0, 0))
				globals.displaySurface.blit(self.ballWindow, (0, 0))
				#globals.displaySurface.blit(self.side + self.result, (0, 0))
			else:
				ballRandomX = random.randrange(1, 5) * 10
				ballRandomY = random.randrange(1, 5) * 10
				globals.displaySurface.blit(self.ballShaking, (ballRandomX, ballRandomY))
				globals.displaySurface.blit(self.ballWindowShaking, (ballRandomX, ballRandomY))
						
			globals.displaySurface.blit(self.mask, (0,0))
			pygame.display.update()
			
		pygame.mixer.Sound.stop(self.audioShaking)	
		pygame.mixer.Sound.play(self.audioResults)	
		
		#	for i in range(0, 20):
		#		GPIO.output(27,GPIO.HIGH)
		#		pygame.time.delay(100)
		#		GPIO.output(27,GPIO.LOW)

		pygame.display.update()
