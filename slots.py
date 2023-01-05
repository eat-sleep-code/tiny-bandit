import pygame
import os
import random

gameTheme = 'classic'
imageRoot = os.getcwd() + '/images/' + gameTheme
audioRoot = os.getcwd() + '/audio/' + gameTheme
screenX = 320  
screenY = 480 
reelOffsetX = 10
reelOffsetY = 10
reelCount = 3
reelScoringOffset = -200 # Where is the payline relative to the top of the screen?
reelWidth = (screenX - (reelOffsetX * 2)) / reelCount
reelSequence = [500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400]

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

		self.audioSpinning = pygame.mixer.music.load(os.path.join(audioRoot, 'spinning.wav'))
		self.audioPoints = pygame.mixer.music.load(os.path.join(audioRoot, 'points.wav'))
		self.audioJackpot = pygame.mixer.music.load(os.path.join(audioRoot, 'jackpot.wav'))

		
	def handleInput(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_DOWN]:
			self.reel01Y = random.choice(reelSequence)		
			self.reel02Y = random.choice(reelSequence)	
			self.reel03Y = random.choice(reelSequence)	
			reels.draw(screen)
			

	def draw(self, surface):
		# Spinning...
		#print(self.reel01Y, self.reel02Y, self.reel03Y)
		reelSpins = random.randrange(10, 20)
		pygame.mixer.music.play(self.audioSpinning)
		for i in range(0, reelSpins):
			for y in reelSequence:
				screen.fill((255,255,255))

				if i == reelSpins - 1 and y >= self.reel01Y:
					surface.blit(self.reel01, (reelOffsetX, self.reel01Y * -1))
				else:
					surface.blit(self.reel01Spinning, (reelOffsetX, y * -1))
				
				if i == reelSpins - 1 and y >= self.reel02Y:
					surface.blit(self.reel02, (reelOffsetX + reelWidth, self.reel02Y * - 1))
				else:
					surface.blit(self.reel02Spinning, (reelOffsetX + reelWidth, y * -1.1))
				
				if i == reelSpins - 1 and y >= self.reel03Y:
					surface.blit(self.reel03, (reelOffsetX + (reelWidth * 2), self.reel03Y * -1))
				else:
					surface.blit(self.reel03Spinning, (reelOffsetX + (reelWidth * 2), y * -1.2))
				
				pygame.draw.line(screen, (255, 255, 0, 0.5), (reelOffsetX, reelOffsetY + (screenY/2)), (reelOffsetX + (reelWidth * 3), reelOffsetY + (screenY/2)), 3)
				pygame.mixer.music.fadeout(100)
				pygame.display.update()
				
				
		
		# Did we win anything?
		if (self.reel01Y == 500 and self.reel02Y == 1100 and self.reel03Y == 2400):
			print('Cherries')
		
		pygame.display.update()



pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Tiny Bandit')
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