import json
import os
import random

import jmespath
import pygame
import RPi.GPIO as GPIO

import globals

# File paths
appRoot = os.getcwd() + '/magic8/'
imageRoot = appRoot + 'images/'
audioRoot = appRoot + 'audio/'

# Positioning


class Game(object):
	def __init__(self):

		self.font = globals.fontScore

		pygame.display.set_caption('Magic 8')
		pygame.display.set_icon(pygame.image.load(os.path.join(imageRoot, 'icon.png')).convert_alpha())

		self.mask = pygame.image.load(os.path.join(imageRoot, 'mask.png')).convert_alpha()

		self.ball = pygame.image.load(os.path.join(imageRoot, '8.png')).convert_alpha()
		#self.ballShaking = pygame.image.load(os.path.join(imageRoot, 'magic-8-shaking.png')).convert_alpha()
		self.ballX = 0

		self.die = pygame.image.load(os.path.join(imageRoot, 'die.png')).convert_alpha()
		self.dieShaking = pygame.image.load(os.path.join(imageRoot, 'die-shaking.png')).convert_alpha()
		#TODO: Position die
		self.dieX = 0
		self.dieY = 0

		#self.fluid = pygame.image.load(os.path.join(imageRoot, 'fluid.png')).convert_alpha()
		#self.fluidShaking = pygame.image.load(os.path.join(imageRoot, 'fluid-shaking.png')).convert_alpha()
		#self.fluidX = 0

		self.porthole = pygame.image.load(os.path.join(imageRoot, 'porthole.png')).convert_alpha()
		self.portholeX = 0

		self.audioShaking = pygame.mixer.Sound(os.path.join(audioRoot, 'shaking.wav'))
		#self.audioResults = pygame.mixer.Sound(os.path.join(audioRoot, 'results.wav'))
		
		self.result = ''
		
	def playMagic8(self):
		globals.displaySurface.fill((0, 0, 0))
		if globals.gameJustLaunched == True: 
			globals.displaySurface.blit(self.ball, (0, 0))
			globals.displaySurface.blit(self.mask, (0, 0))
			pygame.display.update()

		buttonState = GPIO.input(10)
		if buttonState == GPIO.HIGH:
			self.spun = random.randint(1, 10)		
			self.shake()
			
		key = pygame.key.get_pressed()
		if key[pygame.K_UP] or key[pygame.K_DOWN]:
			if globals.gameJustLaunched == True:
				globals.gameJustLaunched = False
			self.spun = random.randint(1, 10)		
			self.shake()	
			


	def shake(self):
		
		# Shaking...
		
		ballShakes = random.randrange(7, 15)
		pygame.mixer.Sound.play(self.audioShaking, 10)
		for i in range(0, ballShakes):
			
			globals.displaySurface.fill((0, 0, 0))
			if i == ballShakes - 1:
				globals.displaySurface.blit(self.die, (0, 12))
				#TODO: blit the text here
				globals.displaySurface.blit(self.porthole, (0, 0))
				globals.displaySurface.blit(self.mask, (0, 0))
			else:
				dieRotation = random.randrange(1, 36) * 10
				rotatedDie = pygame.transform.rotate(self.dieShaking, dieRotation)
				rotatedDieRectangle = rotatedDie.get_rect(center = self.dieShaking.get_rect(center = (241,401)).center)
				globals.displaySurface.blit(rotatedDie, rotatedDieRectangle)
				globals.displaySurface.blit(self.porthole, (0, 0))
				globals.displaySurface.blit(self.mask, (0,0))
				
			pygame.display.update()
			
		pygame.mixer.Sound.stop(self.audioShaking)	
		
		#	for i in range(0, 20):
		#		GPIO.output(27,GPIO.HIGH)
		#		pygame.time.delay(100)
		#		GPIO.output(27,GPIO.LOW)

		pygame.display.update()
