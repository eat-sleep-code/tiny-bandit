import pygame
import os
import random

imageRoot = os.getcwd() + '/images'
screenX = 640
screenY = 640
reelOffsetX = 10
reelOffsetY = 10
reelCount = 3
reelWidth = (screenX - (reelOffsetX * 2)) / reelCount
reelSequence = [40,80,160,320,500]

class Reels(object):
	def __init__(self):
		self.reel01 = pygame.image.load(os.path.join(imageRoot, 'reel-01.jpg'))
		self.reel01Spinning = pygame.image.load(os.path.join(imageRoot, 'reel-01-spinning.jpg'))
		self.reel01Y = reelOffsetY

		self.reel02 = pygame.image.load(os.path.join(imageRoot, 'reel-02.jpg'))
		self.reel02Spinning = pygame.image.load(os.path.join(imageRoot, 'reel-01-spinning.jpg'))
		self.reel02Y = reelOffsetY

		self.reel03 = pygame.image.load(os.path.join(imageRoot, 'reel-03.jpg'))
		self.reel03Spinning = pygame.image.load(os.path.join(imageRoot, 'reel-03-spinning.jpg'))
		self.reel03Y = reelOffsetY

		
	def handleInput(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_DOWN]:
			print('Trying...')
			self.reel01Y = random.choice(reelSequence)			
			self.reel02Y = random.choice(reelSequence)	
			self.reel03Y = random.choice(reelSequence)	
			reels.draw(screen)
			

	def draw(self, surface):
		# Spinning...
		reelSpins = random.randrange(10, 20)
		for i in range(0, reelSpins):
			for y in reelSequence:
				screen.fill((255,255,255))

					
				if i == reelSpins - 1 and y >= self.reel01Y:
					surface.blit(self.reel01, (reelOffsetX, self.reel01Y))
				else:
					surface.blit(self.reel01Spinning, (reelOffsetX, y))
				
				if i == reelSpins - 1 and y >= self.reel02Y:
					surface.blit(self.reel02, (reelOffsetX + reelWidth, self.reel02Y))
				else:
					surface.blit(self.reel02Spinning, (reelOffsetX + reelWidth, y * 1.1))
				
				if i == reelSpins - 1 and y >= self.reel03Y:
					surface.blit(self.reel03, (reelOffsetX + (reelWidth * 2), self.reel03Y))
				else:
					surface.blit(self.reel03Spinning, (reelOffsetX + (reelWidth * 2), y * 1.2))
				pygame.display.update()
				
				
		
		# Did we win anything?
		if (self.reel01Y == self.reel02Y == self.reel03Y):
			print('Jackpot!')
		pygame.display.update()



pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenX, screenY))
reels = Reels()

running = True
while running:
	event = pygame.event.poll()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		reels.handleInput()
		clock.tick(30)