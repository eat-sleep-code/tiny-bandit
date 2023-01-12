import os
import pygame
import RPi.GPIO as GPIO
import slots 
import flappy

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #BUTTON
GPIO.setup(27, GPIO.OUT) #LED

# Game Initialization
appRoot = os.getcwd()
screenX = 480 
screenY = 800

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Tiny Bandit')
pygame.display.set_icon(pygame.image.load(os.path.join(appRoot, 'images/icon.png')))
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenX, screenY))

running = True
clock.tick(60)

while running:
	event = pygame.event.poll()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		#slots.Game().playSlots(screen, screenX, screenY, clock)
		flappy.Game().playFlappy(screen, screenX, screenY, clock)