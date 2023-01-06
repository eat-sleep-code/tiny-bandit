import pygame
import os
import json
import jmespath
import random

gameTheme = 'classic'
appRoot = os.getcwd()
imageRoot = appRoot + '/images/' + gameTheme
audioRoot = appRoot + '/audio/' + gameTheme
screenX = 480 
screenY = 800 
reelOffsetX = 45
reelOffsetY = 10
reelGutter = 45
reelCount = 3
reelScoringOffset = 400 # Where is the payline relative to the top of the screen?
reelWidth = (screenX - (reelOffsetX * 2) - ((reelCount -1) * reelGutter)) / reelCount
reelSequence = [500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400]



class Slots(object):
	def __init__(self):
		self.mask = pygame.image.load(os.path.join(imageRoot, 'mask.png'))

		self.reel01 = pygame.image.load(os.path.join(imageRoot, 'reel-01.jpg'))
		self.reel01Spinning = pygame.image.load(os.path.join(imageRoot, 'reel-01-spinning.jpg'))
		self.reel01Y = reelOffsetY

		self.reel02 = pygame.image.load(os.path.join(imageRoot, 'reel-02.jpg'))
		self.reel02Spinning = pygame.image.load(os.path.join(imageRoot, 'reel-01-spinning.jpg'))
		self.reel02Y = reelOffsetY

		self.reel03 = pygame.image.load(os.path.join(imageRoot, 'reel-03.jpg'))
		self.reel03Spinning = pygame.image.load(os.path.join(imageRoot, 'reel-03-spinning.jpg'))
		self.reel03Y = reelOffsetY

		self.audioSpinning = pygame.mixer.Sound(os.path.join(audioRoot, 'spinning.wav'))
		self.audioPoints = pygame.mixer.Sound(os.path.join(audioRoot, 'points.wav'))
		self.audioJackpot = pygame.mixer.Sound(os.path.join(audioRoot, 'jackpot.wav'))

		self.symbolMapping = json.load(open(os.path.join(appRoot, 'symbol-mapping.json')))


		
	def handleSpins(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_DOWN]:
			self.reel01Y = random.choice(reelSequence)		
			self.reel02Y = random.choice(reelSequence)	
			self.reel03Y = random.choice(reelSequence)	
			slots.spin(screen)
			


	def spin(self, surface):
		# Spinning...
		reelSpins = random.randrange(7, 15)
		pygame.mixer.Sound.play(self.audioSpinning)
		for i in range(0, reelSpins):
			for y in reelSequence:
				screen.fill((255,255,255))
				
				if i == reelSpins - 1 and y >= self.reel01Y:
					surface.blit(self.reel01, (reelOffsetX, self.reel01Y * -1))
				else:
					surface.blit(self.reel01Spinning, (reelOffsetX, y * -1))
				
				if i == reelSpins - 1 and y >= self.reel02Y:
					surface.blit(self.reel02, (reelOffsetX + reelWidth + reelGutter, self.reel02Y * - 1))
				else:
					surface.blit(self.reel02Spinning, (reelOffsetX + reelWidth + reelGutter, y * -1.1))
				
				if i == reelSpins - 1 and y >= self.reel03Y:
					surface.blit(self.reel03, (reelOffsetX + (reelWidth * 2) + (reelGutter * 2), self.reel03Y * -1))
				else:
					surface.blit(self.reel03Spinning, (reelOffsetX + (reelWidth * 2) + (reelGutter * 2), y * -1.2))
				
				surface.blit(self.mask, (0,0))
				pygame.display.update()
				
		pygame.mixer.Sound.stop(self.audioSpinning)		
		
		reel01payline = self.reel01Y + reelScoringOffset
		reel02payline = self.reel02Y + reelScoringOffset
		reel03payline = self.reel03Y + reelScoringOffset
		#print(reel01payline, reel02payline, reel03payline)
		
		winnings = slots.checkWinnings(reel01payline, reel02payline, reel03payline)
		if (winnings[0] != "none"):
			pygame.mixer.Sound.play(self.audioJackpot)


		pygame.display.update()



	def checkWinnings(self, reel01, reel02, reel03):
		
		# Get the wild positions...
		wild = jmespath.search("symbols[?name == 'wild'].positions | [0]", self.symbolMapping);
		
		# Check each reel for a non-wild symbol, if exists adjust match expressions 
		matchExpression01 = "(positions[0] >= `0`)"
		if (reel01 != wild[0]):
			matchExpression01 = "(positions[0] == `" + str(reel01) + "`) "

		matchExpression02 = "(positions[1] >= `0`)"
		if (reel02 != wild[1]):
			matchExpression02 = "(positions[1] == `" + str(reel02) + "`) "

		matchExpression03 = "(positions[2] >= `0`)"
		if (reel03 != wild[2]):
			matchExpression03 = "(positions[2] == `" + str(reel03) + "`) "

		# Search for matches...
		matches = jmespath.search("symbols[?" + matchExpression01 + "&&" + matchExpression02 + "&&" + matchExpression03 + "]", self.symbolMapping)
		if matches:
			print("You win!", matches)
			winningMatch = json.loads(json.dumps(matches[0]))
			return winningMatch["name"], winningMatch["payout"], winningMatch["freePlays"]
		else:
			print("You lose", matches)
			return "none", 0, 0	
	



pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Tiny Bandit')
pygame.display.set_icon(pygame.image.load(os.path.join(imageRoot, 'icon.png')))
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenX, screenY))
slots = Slots()

running = True
while running:
	event = pygame.event.poll()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		slots.handleSpins()
		clock.tick(30)