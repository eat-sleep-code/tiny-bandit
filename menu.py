import os

import pygame

import globals
from data import Data
from models import Button


class CreateMenu:
	def __init__(self):

		# ---------------------------------------------------------------------
		
		paddingX = 20
		paddingY = 260
		gutter = 10
		x = paddingX
		y = paddingY
		desiredColumns = 1
		iconWidth = 64
		iconHeight = 64
		cellPadding = 10
		buttonWidth = int(((globals.screenWidth - (x * 2)) / desiredColumns)) 
		buttonHeight = int(iconHeight + 10)
		textWidth = 256
		
		# ---------------------------------------------------------------------

		if globals.gameSelected == 'none':
			globals.displaySurface.fill((0,0,128))

			backgroundImage = pygame.image.load(os.path.join(globals.appRoot, 'images/menu.jpg')).convert_alpha()
			globals.displaySurface.blit(backgroundImage, (0, 0)) 	

			menuItems = Data.getGames().games
			tempButtonCollection = []
			if len(menuItems) > 0:
				if len(menuItems) > 6:
					y = y/2
				for item in menuItems:
					itemX = x
					itemY = y
					itemYAlt = 5 + y + (buttonHeight/3) 

					# Button
					gameRectangle = pygame.draw.rect(globals.displaySurface, (1, 30, 64), [itemX, itemY, buttonWidth, buttonHeight])
					button = Button()
					button.rect = gameRectangle
					button.text = item.title
					button.type = 'launcher'
					button.value = item.id
					button.icon = item.icon

					# Button Icon
					gameIcon = pygame.image.load(os.path.join(globals.appRoot, button.icon)).convert_alpha()
					gameIcon = pygame.transform.scale(gameIcon, (iconWidth, iconHeight))
					globals.displaySurface.blit(gameIcon, (itemX + 6, itemYAlt - 25))

					# Button Text
					textStart = itemX + iconWidth + cellPadding + gutter
					gameTitleText = globals.fontDefault.render(button.text, True, (255, 255, 255))
					globals.displaySurface.blit(gameTitleText, (textStart, itemYAlt))

					tempButtonCollection.append(button)
					
					if (x >= buttonWidth * (desiredColumns - 1)):	
						x = paddingX
						y = itemY + buttonHeight + gutter
					else:
						x = itemX + buttonWidth + gutter
					#print('X:', x, 'Y:', y)
					
				globals.buttonCollection.clear()
				globals.buttonCollection = tempButtonCollection
				pygame.display.flip()
