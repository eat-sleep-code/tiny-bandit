import os
import random

import pygame
from pygame.locals import *

import globals
import gpio



class Game(object):
	def __init__(self):
		appRoot = globals.appRoot + 'flappy/'
		imageRoot = appRoot + 'images/' 
		audioRoot = appRoot + 'audio/'

		pygame.display.set_caption('FlappyBird')
		pygame.display.set_icon(pygame.image.load(os.path.join(imageRoot, 'icon.png')).convert_alpha())

		self.fps = 32
		
		self.gameImages = {}
		self.gameImages['scoreimages'] = (
			pygame.image.load(os.path.join(imageRoot, '0.png')).convert_alpha(),
			pygame.image.load(os.path.join(imageRoot, '1.png')).convert_alpha(),
			pygame.image.load(os.path.join(imageRoot, '2.png')).convert_alpha(),
			pygame.image.load(os.path.join(imageRoot, '3.png')).convert_alpha(),
			pygame.image.load(os.path.join(imageRoot, '4.png')).convert_alpha(),
			pygame.image.load(os.path.join(imageRoot, '5.png')).convert_alpha(),
			pygame.image.load(os.path.join(imageRoot, '6.png')).convert_alpha(),
			pygame.image.load(os.path.join(imageRoot, '7.png')).convert_alpha(),
			pygame.image.load(os.path.join(imageRoot, '8.png')).convert_alpha(),
			pygame.image.load(os.path.join(imageRoot, '9.png')).convert_alpha()
		)
		self.gameImages['splash'] = pygame.image.load(os.path.join(imageRoot, 'splash.png')).convert_alpha()
		self.gameImages['bird'] = pygame.image.load(os.path.join(imageRoot, 'bird.png')).convert_alpha()
		self.gameImages['base'] = pygame.image.load(os.path.join(imageRoot, 'base.png')).convert_alpha()
		self.gameImages['background'] = pygame.image.load(os.path.join(imageRoot, 'background.jpg')).convert_alpha()
		self.gameImages['pipe'] = pygame.image.load(os.path.join(imageRoot, 'pipe-upper.png')).convert_alpha(), pygame.image.load(os.path.join(imageRoot, 'pipe-lower.png')).convert_alpha()
		self.gameImages['gameOver'] = pygame.image.load(os.path.join(imageRoot, 'game-over.png')).convert_alpha()

		self.audioDie = pygame.mixer.Sound(os.path.join(audioRoot, 'die.wav'))
		self.audioHit = pygame.mixer.Sound(os.path.join(audioRoot, 'hit.wav'))
		self.audioPoint = pygame.mixer.Sound(os.path.join(audioRoot, 'point.wav'))
		self.audioSwoosh = pygame.mixer.Sound(os.path.join(audioRoot, 'swoosh.wav'))
		self.audioWing = pygame.mixer.Sound(os.path.join(audioRoot, 'wing.wav'))



	def playFlappy(self):
		horizontal = int(globals.screenWidth/5)
		vertical = int(globals.screenWidth/2)
		elevation = globals.screenHeight * 0.8
		ground = 0

		if globals.gameJustLaunched == True:
			globals.gameJustLaunched = False

		key = pygame.key.get_pressed()
		if key[pygame.K_UP] or key[pygame.K_DOWN] or gpio.isButtonPressed("left"):
			horizontal = int(globals.screenWidth/5)
			vertical = int((globals.screenHeight - self.gameImages['bird'].get_height())/2)
			ground = 0
			self.flap(horizontal, vertical, ground, elevation)

		else:
			globals.displaySurface.blit(self.gameImages['background'], (0, 0))
			globals.displaySurface.blit(self.gameImages['bird'], (horizontal, vertical))
			globals.displaySurface.blit(self.gameImages['base'], (ground, elevation))
			pygame.display.update()
			globals.clock.tick(self.fps)



	def flap(self, horizontal, vertical, ground, elevation):
		pygame.mixer.Sound.play(self.audioWing)

		currentScore = 0
		currentHeight = 100

		firstPipe = self.createPipe(self.gameImages)
		secondPipe = self.createPipe(self.gameImages)

		downPipes = [
			{'x': globals.screenWidth + 300 - currentHeight, 'y': firstPipe[1]['y']},
			{'x': globals.screenWidth + 300 - currentHeight + (globals.screenWidth/2), 'y': secondPipe[1]['y']},
		]

		upPipes = [
			{'x': globals.screenWidth + 300 - currentHeight, 'y': firstPipe[0]['y']},
			{'x': globals.screenWidth + 300 - currentHeight + (globals.screenWidth/2), 'y': secondPipe[0]['y']},
		]

		# Velocity
		pipeVelocityX = -4
		birdVelocityY = -9
		birdVelocityYMax = 10
		birdVelocityYMin = -8
		birdAcceleration = 1
		birdFlapVelocity = -8
		birdFlapped = False


		while True:
			key = pygame.key.get_pressed()
			if key[pygame.K_UP] or key[pygame.K_DOWN] or gpio.isButtonPressed("left"):
				
				if vertical > 0:
					pygame.mixer.Sound.play(self.audioWing)
					birdVelocityY = birdFlapVelocity
					birdFlapped = True

			gameOver = self.isGameOver(self.gameImages, elevation, horizontal, vertical, upPipes, downPipes)
			if gameOver:
				pygame.time.delay(500)
				pygame.mixer.Sound.stop(self.audioWing)
				pygame.mixer.Sound.stop(self.audioSwoosh)
				pygame.mixer.Sound.play(self.audioDie)
				globals.displaySurface.blit(self.gameImages['gameOver'], (0, 0))
				pygame.display.update()
				pygame.time.delay(4000)
				return

			# Check current score...
			playerMidPosition = horizontal + self.gameImages['bird'].get_width()/2
			for pipe in upPipes:
				pipeMidPosition = pipe['x'] + self.gameImages['pipe'][0].get_width()/2
				if pipeMidPosition <= playerMidPosition < pipeMidPosition + 4:
					currentScore += 1
					pygame.mixer.Sound.stop(self.audioWing)
					pygame.mixer.Sound.stop(self.audioSwoosh)
					pygame.mixer.Sound.play(self.audioPoint)
					print(f"Your current score is {currentScore}")

			if birdVelocityY < birdVelocityYMax and not birdFlapped:
				birdVelocityY += birdAcceleration

			if birdFlapped:
				pygame.mixer.Sound.play(self.audioSwoosh)
				birdFlapped = False
			playerHeight = self.gameImages['bird'].get_height()
			vertical = vertical + min(birdVelocityY, elevation - vertical - playerHeight)

			# Move pipes...
			for upperPipe, lowerPipe in zip(upPipes, downPipes):
				upperPipe['x'] += pipeVelocityX
				lowerPipe['x'] += pipeVelocityX

			# Add a new pipe...
			if 0 < upPipes[0]['x'] < 5:
				newpipe = self.createPipe(self.gameImages)
				upPipes.append(newpipe[0])
				downPipes.append(newpipe[1])

			# Remove old pipes...
			if upPipes[0]['x'] < -self.gameImages['pipe'][0].get_width():
				upPipes.pop(0)
				downPipes.pop(0)

			# Update globals.displaySurface...
			globals.displaySurface.blit(self.gameImages['background'], (0, 0))
			for upperPipe, lowerPipe in zip(upPipes, downPipes):
				globals.displaySurface.blit(self.gameImages['pipe'][0], (upperPipe['x'], upperPipe['y']))
				globals.displaySurface.blit(self.gameImages['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

			globals.displaySurface.blit(self.gameImages['base'], (ground, elevation))
			globals.displaySurface.blit(self.gameImages['bird'], (horizontal, vertical))



			# Update score
			numbers = [int(x) for x in list(str(currentScore))]
			width = 0
			
			for num in numbers:
				width += self.gameImages['scoreimages'][num].get_width()
			offsetX = (globals.screenWidth - width)/1.1

			for num in numbers:
				globals.displaySurface.blit(self.gameImages['scoreimages'][num], (offsetX, globals.screenWidth*0.02))
				offsetX += self.gameImages['scoreimages'][num].get_width()

			pygame.display.update()
			

			globals.clock.tick(self.fps)
			pygame.event.pump()


	def isGameOver(self, gameImages, elevation, horizontal, vertical, upPipes, downPipes):
		if vertical > elevation - 25 or vertical < 0:
			return True

		for pipe in upPipes:
			pipeHeight = gameImages['pipe'][0].get_height()
			if (vertical < pipeHeight + pipe['y'] and abs(horizontal - pipe['x']) < gameImages['pipe'][0].get_width()):
				pygame.mixer.Sound.play(self.audioHit)
				return True

		for pipe in downPipes:
			
			if (vertical + gameImages['bird'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < gameImages['pipe'][0].get_width():
				pygame.mixer.Sound.play(self.audioHit)
				return True
		return False


	def createPipe(self, gameImages):
		offset = globals.screenHeight/3
		pipeHeight = gameImages['pipe'][0].get_height()
		y2 = offset + random.randrange(0, int(globals.screenHeight - gameImages['base'].get_height() - 1.2 * offset))
		pipeX = globals.screenWidth + 10
		y1 = pipeHeight - y2 + offset
		pipe = [
			{'x': pipeX, 'y': -y1},
			{'x': pipeX, 'y': y2}
		]
		return pipe

