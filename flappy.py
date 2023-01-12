import os
import pygame
import random
import sys
from pygame.locals import *

# File paths
appRoot = os.getcwd() + '/flappy/'
imageRoot = appRoot + 'images/' 
audioRoot = appRoot + 'audio/'


class Game(object):
	def __init__(self):
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
		self.gameImages['bird'] = pygame.image.load(os.path.join(imageRoot, 'bird.png')).convert_alpha()
		self.gameImages['base'] = pygame.image.load(os.path.join(imageRoot, 'base.png')).convert_alpha()
		self.gameImages['background'] = pygame.image.load(os.path.join(imageRoot, 'background.jpg')).convert_alpha()
		self.gameImages['pipe'] = pygame.image.load(os.path.join(imageRoot, 'pipe-upper.png')).convert_alpha(), pygame.image.load(os.path.join(imageRoot, 'pipe-lower.png')).convert_alpha()



	def playFlappy(self, screen, screenX, screenY, clock):
		horizontal = int(screenX/5)
		vertical = int(screenX/2)
		elevation = screenY * 0.8
		ground = 0
	
		key = pygame.key.get_pressed()
		if key[pygame.K_UP] or key[pygame.K_DOWN]:
			print('Key pressed...')
			horizontal = int(screenX/5)
			vertical = int((screenY - self.gameImages['bird'].get_height())/2)
			ground = 0
			self.flap(screen, screenX, screenY, clock, horizontal, vertical, ground, elevation)

		else:
			screen.blit(self.gameImages['background'], (0, 0))
			screen.blit(self.gameImages['bird'], (horizontal, vertical))
			screen.blit(self.gameImages['base'], (ground, elevation))
			pygame.display.update()
			clock.tick(self.fps)



	def flap(self, surface, screenX, screenY, clock, horizontal, vertical, ground, elevation):
		currentScore = 0
		currentHeight = 100

		firstPipe = self.createPipe(screenX, screenY, self.gameImages)
		secondPipe = self.createPipe(screenX, screenY, self.gameImages)

		downPipes = [
			{'x': screenX + 300 - currentHeight, 'y': firstPipe[1]['y']},
			{'x': screenX + 300 - currentHeight + (screenX/2), 'y': secondPipe[1]['y']},
		]

		upPipes = [
			{'x': screenX + 300 - currentHeight, 'y': firstPipe[0]['y']},
			{'x': screenX + 300 - currentHeight + (screenX/2), 'y': secondPipe[0]['y']},
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
			for event in pygame.event.get():
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
					if vertical > 0:
						birdVelocityY = birdFlapVelocity
						birdFlapped = True

			gameOver = self.isGameOver(self.gameImages, elevation, horizontal, vertical, upPipes, downPipes)
			if gameOver:
				return

			# Check current score...
			playerMidPosition = horizontal + self.gameImages['bird'].get_width()/2
			for pipe in upPipes:
				pipeMidPosition = pipe['x'] + self.gameImages['pipe'][0].get_width()/2
				if pipeMidPosition <= playerMidPosition < pipeMidPosition + 4:
					currentScore += 1
					print(f"Your current score is {currentScore}")

			if birdVelocityY < birdVelocityYMax and not birdFlapped:
				birdVelocityY += birdAcceleration

			if birdFlapped:
				birdFlapped = False
			playerHeight = self.gameImages['bird'].get_height()
			vertical = vertical + min(birdVelocityY, elevation - vertical - playerHeight)

			# Move pipes...
			for upperPipe, lowerPipe in zip(upPipes, downPipes):
				upperPipe['x'] += pipeVelocityX
				lowerPipe['x'] += pipeVelocityX

			# Add a new pipe...
			if 0 < upPipes[0]['x'] < 5:
				newpipe = self.createPipe(screenX, screenY, self.gameImages)
				upPipes.append(newpipe[0])
				downPipes.append(newpipe[1])

			# Remove old pipes...
			if upPipes[0]['x'] < -self.gameImages['pipe'][0].get_width():
				upPipes.pop(0)
				downPipes.pop(0)

			# Update screen...
			surface.blit(self.gameImages['background'], (0, 0))
			for upperPipe, lowerPipe in zip(upPipes, downPipes):
				surface.blit(self.gameImages['pipe'][0], (upperPipe['x'], upperPipe['y']))
				surface.blit(self.gameImages['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

			surface.blit(self.gameImages['base'], (ground, elevation))
			surface.blit(self.gameImages['bird'], (horizontal, vertical))



			# Update score
			numbers = [int(x) for x in list(str(currentScore))]
			width = 0
			
			for num in numbers:
				width += self.gameImages['scoreimages'][num].get_width()
			offsetX = (screenX - width)/1.1

			for num in numbers:
				surface.blit(self.gameImages['scoreimages'][num], (offsetX, screenX*0.02))
				offsetX += self.gameImages['scoreimages'][num].get_width()

			pygame.display.update()
			clock.tick(self.fps)


	def isGameOver(self, gameImages, elevation, horizontal, vertical, upPipes, downPipes):
		if vertical > elevation - 25 or vertical < 0:
			return True

		for pipe in upPipes:
			pipeHeight = gameImages['pipe'][0].get_height()
			if (vertical < pipeHeight + pipe['y'] and abs(horizontal - pipe['x']) < gameImages['pipe'][0].get_width()):
				return True

		for pipe in downPipes:
			if (vertical + gameImages['bird'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < gameImages['pipe'][0].get_width():
				return True
		return False


	def createPipe(self, screenX, screenY, gameImages):
		offset = screenY/3
		pipeHeight = gameImages['pipe'][0].get_height()
		y2 = offset + random.randrange(0, int(screenY - gameImages['base'].get_height() - 1.2 * offset))
		pipeX = screenX + 10
		y1 = pipeHeight - y2 + offset
		pipe = [
			{'x': pipeX, 'y': -y1},
			{'x': pipeX, 'y': y2}
		]
		return pipe

