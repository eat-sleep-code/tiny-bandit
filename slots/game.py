import json
import os
import random

import jmespath
import pygame

import globals
import gpio

# Positioning
reelOffsetX = 45
reelOffsetY = 10
reelGutter = 45
reelCount = 3
reelScoringOffset = 400 # Where is the payline relative to the top of the screen?
reelSequence = [500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400]
payoutX = 45
payoutY = 750
freePlaysX = 295
freePlaysY = 750

# Scoring
spinCost = 10
currentPayout = 0
currentFreePlays = 20
wildPayout = 10
wildFreePlays = 3


class Game(object):
	def __init__(self):
		gameTheme = 'classic'
		appRoot = globals.appRoot + 'slots/'
		imageRoot = appRoot + 'images/' + gameTheme
		audioRoot = appRoot + 'audio/' + gameTheme

		self.font = globals.fontScore

		pygame.display.set_caption('Slots')
		pygame.display.set_icon(pygame.image.load(os.path.join(imageRoot, 'icon.png')).convert_alpha())

		self.mask = pygame.image.load(os.path.join(imageRoot, 'mask.png')).convert_alpha()

		self.reel01 = pygame.image.load(os.path.join(imageRoot, 'reel-01.jpg')).convert_alpha()
		self.reel01Spinning = pygame.image.load(os.path.join(imageRoot, 'reel-01-spinning.jpg')).convert_alpha()
		self.reel01Y = reelOffsetY

		self.reel02 = pygame.image.load(os.path.join(imageRoot, 'reel-02.jpg')).convert_alpha()
		self.reel02Spinning = pygame.image.load(os.path.join(imageRoot, 'reel-01-spinning.jpg')).convert_alpha()
		self.reel02Y = reelOffsetY

		self.reel03 = pygame.image.load(os.path.join(imageRoot, 'reel-03.jpg')).convert_alpha()
		self.reel03Spinning = pygame.image.load(os.path.join(imageRoot, 'reel-03-spinning.jpg')).convert_alpha()
		self.reel03Y = reelOffsetY

		self.winningsJackpot = pygame.image.load(os.path.join(imageRoot, 'jackpot.png')).convert_alpha()
		self.winningsWild = pygame.image.load(os.path.join(imageRoot, 'wild.png')).convert_alpha()

		self.audioSpinning = pygame.mixer.Sound(os.path.join(audioRoot, 'spinning.wav'))
		self.audioPoints = pygame.mixer.Sound(os.path.join(audioRoot, 'points.wav'))
		self.audioJackpot = pygame.mixer.Sound(os.path.join(audioRoot, 'jackpot.wav'))

		self.symbolMapping = json.load(open(os.path.join(appRoot, 'symbol-mapping.json')))


		
	def playSlots(self):
		global currentFreePlays
		key = pygame.key.get_pressed()
		if globals.gameJustLaunched or key[pygame.K_UP] or key[pygame.K_DOWN] or gpio.isButtonPressed("left"):
			if globals.gameJustLaunched == True:
				currentFreePlays = currentFreePlays + 1
				globals.gameJustLaunched = False
			self.reel01Y = random.choice(reelSequence)		
			self.reel02Y = random.choice(reelSequence)	
			self.reel03Y = random.choice(reelSequence)	
			self.spin()
			


	def spin(self):
		global currentFreePlays
		global currentPayout
		reelWidth = (globals.screenWidth - (reelOffsetX * 2) - ((reelCount -1) * reelGutter)) / reelCount

		# Spinning...
		if currentFreePlays > 0:
			currentFreePlays = currentFreePlays - 1;
		else:
			currentPayout = int(currentPayout) - (spinCost)

		currentFreePlaysText = self.font.render(str(currentFreePlays), True, (255, 255, 255))
		currentPayoutText = self.font.render(str(currentPayout), True, (255, 255, 255))

		reelSpins = random.randrange(7, 15)
		pygame.mixer.Sound.play(self.audioSpinning, 10)
		for i in range(0, reelSpins):
			for y in reelSequence:
				globals.displaySurface.fill((255,255,255))
				
				if i == reelSpins - 1 and y >= self.reel01Y:
					globals.displaySurface.blit(self.reel01, (reelOffsetX, self.reel01Y * -1))
				else:
					globals.displaySurface.blit(self.reel01Spinning, (reelOffsetX, y * -1))
				
				if i == reelSpins - 1 and y >= self.reel02Y:
					globals.displaySurface.blit(self.reel02, (reelOffsetX + reelWidth + reelGutter, self.reel02Y * - 1))
				else:
					globals.displaySurface.blit(self.reel02Spinning, (reelOffsetX + reelWidth + reelGutter, y * -1.1))
				
				if i == reelSpins - 1 and y >= self.reel03Y:
					globals.displaySurface.blit(self.reel03, (reelOffsetX + (reelWidth * 2) + (reelGutter * 2), self.reel03Y * -1))
				else:
					globals.displaySurface.blit(self.reel03Spinning, (reelOffsetX + (reelWidth * 2) + (reelGutter * 2), y * -1.2))
				
				globals.displaySurface.blit(self.mask, (0,0))
				globals.displaySurface.blit(currentFreePlaysText, (freePlaysX, freePlaysY))
				globals.displaySurface.blit(currentPayoutText, (payoutX, payoutY))
				pygame.display.update()
				
		pygame.mixer.Sound.stop(self.audioSpinning)		
		
		reel01payline = self.reel01Y + reelScoringOffset
		reel02payline = self.reel02Y + reelScoringOffset
		reel03payline = self.reel03Y + reelScoringOffset
		#print(reel01payline, reel02payline, reel03payline)
		
		winnings = self.checkWinnings(reel01payline, reel02payline, reel03payline)
		if (winnings[0] != "none"):
			currentPayout = int(currentPayout) + int(winnings[1])
			currentFreePlays = int(currentFreePlays) + int(winnings[2])

			# Update the screen...
			currentFreePlaysText = self.font.render(str(currentFreePlays), True, (255, 255, 255))
			currentPayoutText = self.font.render(str(currentPayout), True, (255, 255, 255))
			globals.displaySurface.blit(self.mask, (0,0))
			globals.displaySurface.blit(currentFreePlaysText, (freePlaysX, freePlaysY))
			globals.displaySurface.blit(currentPayoutText, (payoutX, payoutY))
			
			if (winnings[0] == "wildPartial"):
				# Wilds
				globals.displaySurface.blit(self.winningsWild, (0,0))
				pygame.mixer.Sound.play(self.audioPoints)
			else:
				# Jackpot
				globals.displaySurface.blit(self.winningsJackpot, (0,0))
				pygame.mixer.Sound.play(self.audioJackpot)

			pygame.display.update()
			
			

		pygame.display.update()



	def checkWinnings(self, reel01, reel02, reel03):
		
		# Get the wild positions...
		wild = jmespath.search("symbols[?name == 'wild'].positions | [0]", self.symbolMapping)
		wildCount = 0
		# Check each reel for a non-wild symbol, if exists adjust match expressions 
		matchExpression01 = "(positions[0] >= `0`)"
		if (reel01 != wild[0]):
			matchExpression01 = "(positions[0] == `" + str(reel01) + "`) "
		else:
			wildCount = wildCount + 1

		matchExpression02 = "(positions[1] >= `0`)"
		if (reel02 != wild[1]):
			matchExpression02 = "(positions[1] == `" + str(reel02) + "`) "
		else: 
			wildCount = wildCount + 1

		matchExpression03 = "(positions[2] >= `0`)"
		if (reel03 != wild[2]):
			matchExpression03 = "(positions[2] == `" + str(reel03) + "`) "
		else: 
			wildCount = wildCount + 1

		# Search for matches...
		matches = jmespath.search("symbols[?" + matchExpression01 + "&&" + matchExpression02 + "&&" + matchExpression03 + "]", self.symbolMapping)
		if matches and (wildCount == 0 or wildCount == 3):
			print("Jackpot!", matches[0])
			winningMatch = json.loads(json.dumps(matches[0]))
			return winningMatch["name"], winningMatch["payout"], winningMatch["freePlays"]
		elif wildCount > 0: 
			print("You got " + str(wildCount) + " wild slots!")
			return "wildPartial", wildPayout * wildCount, wildFreePlays * wildCount 
		else:
			#print("You got nothin'", matches)
			return "none", 0, 0	
