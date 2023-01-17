import json
import os
import random

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

		self.font = pygame.font.SysFont('Helvetica', 12, bold=False)

		pygame.display.set_caption('Magic 8')
		pygame.display.set_icon(pygame.image.load(os.path.join(imageRoot, 'icon.png')).convert_alpha())

		self.mask = pygame.image.load(os.path.join(imageRoot, 'mask.png')).convert_alpha()

		self.ball = pygame.image.load(os.path.join(imageRoot, '8.png')).convert_alpha()
		self.ballX = 0

		self.die = pygame.image.load(os.path.join(imageRoot, 'die.png')).convert_alpha()
		self.dieShaking = pygame.image.load(os.path.join(imageRoot, 'die-shaking.png')).convert_alpha()
		self.dieX = 0
		self.dieY = 12
		self.dieWidth = 75
		self.dieHeight = 75

		self.fluid = pygame.image.load(os.path.join(imageRoot, 'fluid.png')).convert_alpha()
		
		self.porthole = pygame.image.load(os.path.join(imageRoot, 'porthole.png')).convert_alpha()
		self.portholeX = 0

		self.audioShaking = pygame.mixer.Sound(os.path.join(audioRoot, 'shaking.wav'))
		
		self.outcomes = json.load(open(os.path.join(appRoot, 'outcomes.json')))
		


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
		outcomeRectangle = pygame.Rect((globals.screenWidth/2) - (self.dieWidth/2) ,(globals.screenHeight/2) - (self.dieHeight/2) + 5, self.dieWidth, self.dieHeight)
			
		pygame.mixer.Sound.play(self.audioShaking, 10)
		for i in range(0, ballShakes):
			outcome = random.choice(self.outcomes['outcomes'])
			

			globals.displaySurface.fill((0, 0, 0))
			if i == ballShakes - 1:
				globals.displaySurface.blit(self.die, (self.dieX, self.dieY))
				globals.displaySurface.blit(self.porthole, (0, 0))
				self.drawText(outcome.upper(), 'center', (255, 255, 255), outcomeRectangle)
				globals.displaySurface.blit(self.fluid, (0, 20))
				globals.displaySurface.blit(self.mask, (0, 0))
			else:
				dieRotation = random.randrange(1, 36) * 10
				rotatedDie = pygame.transform.rotate(self.dieShaking, dieRotation)
				rotatedDieRectangle = rotatedDie.get_rect(center = self.dieShaking.get_rect(center = ((globals.screenWidth/2) ,(globals.screenHeight/2))).center)				
				rotatedFluid = pygame.transform.rotate(self.fluid, dieRotation * 0.33)
				rotatedFluidRectangle = rotatedFluid.get_rect(center = self.fluid.get_rect(center = ((globals.screenWidth/2) ,(globals.screenHeight/2))).center)				
				
				globals.displaySurface.blit(rotatedDie, rotatedDieRectangle)
				globals.displaySurface.blit(self.porthole, (0, 0))
				globals.displaySurface.blit(rotatedFluid, rotatedFluidRectangle)
				globals.displaySurface.blit(self.mask, (0,0))

				dieShakeDelay = random.randrange(10, 20) * 10
				pygame.time.delay(dieShakeDelay)
				
			pygame.display.update()
			
		pygame.mixer.Sound.stop(self.audioShaking)	
		
		#	for i in range(0, 20):
		#		GPIO.output(27,GPIO.HIGH)
		#		pygame.time.delay(100)
		#		GPIO.output(27,GPIO.LOW)

		pygame.display.update()
		
		
		
	def drawText(self, text, align, color, rect):
		lineSpacing = 2
		spaceWidth, fontHeight = self.font.size(' ')[0], self.font.size('Tg')[1]

		wordList = text.split(' ')
		renderedWordList = [self.font.render(word, True, color) for word in wordList]

		
		maxLength = rect[2]
		lineLengthList = [0]
		lineList = [[]]

		for renderedWord in renderedWordList:
			width = renderedWord.get_width()
			# print('Word width:', width)
			lineLength = lineLengthList[-1] + len(lineList[-1]) * spaceWidth + width
			if len(lineList[-1]) == 0 or lineLength <= maxLength:
				lineLengthList[-1] += width
				lineList[-1].append(renderedWord)
			else:
				lineLengthList.append(width)
				lineList.append([renderedWord])

		lineBottom = rect[1]
		lastLine = 0

		#print(len(lineLengthList), lineBottom)
		if (len(lineList) == 1):
			lineBottom += (fontHeight + lineSpacing) * 2
		elif (len(lineList) == 2):
			lineBottom += (fontHeight + lineSpacing)


		for lineLength, lineRenders in zip(lineLengthList, lineList):
			lineLeft = rect[0]
			if align == 'right':
				lineLeft += + rect[2] - lineLength - spaceWidth * (len(lineRenders)-1)
			elif align == 'center':
				lineLeft += (rect[2] - lineLength - spaceWidth * (len(lineRenders)-1)) // 2
			elif align == 'block' and len(lineRenders) > 1:
				spaceWidth = (rect[2] - lineLength) // (len(lineRenders)-1)

			if lineBottom + fontHeight > rect[1] + rect[3]:
				break

			lastLine += 1

			
			for i, lineRender in enumerate(lineRenders):
				x, y = lineLeft + i*spaceWidth, lineBottom
				globals.displaySurface.blit(lineRender, (round(x), y))
				lineLeft += lineRender.get_width() 
			lineBottom += fontHeight + lineSpacing

		if lastLine < len(lineList):
			drawWords = sum([len(lineList[i]) for i in range(lastLine)])
			remainingText = ''
			for text in wordList[drawWords:]: remainingText += text + ' '
			return remainingText
		return ''


