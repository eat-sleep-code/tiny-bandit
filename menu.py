import pygame

import globals
from data import Data
from models import Button


class CreateMenu:
	def __init__(self):

		# ---------------------------------------------------------------------
		
		paddingX = 10
		paddingY = 220
		gutter = 10
		x = paddingX
		y = paddingY
		desiredColumns = 1
		iconWidth = 32
		iconHeight = 32
		cellPadding = 10
		buttonWidth = int(((globals.screenWidth - (x * 2)) / desiredColumns)) 
		buttonHeight = int(iconHeight + 10)
		textWidth = 256
		
		# ---------------------------------------------------------------------

		if globals.gameSelected == 'none':
			globals.displaySurface.fill((128,128,128))
			
			#backgroundImagePath = os.path.join(globals.appRoot, 'images/menu-background.jpg')
			#backgroundImage = pygame.image.load(backgroundImagePath)
			#globals.displaySurface.blit(backgroundImage, (0, 0)) 	

			menuItems = Data.getGames().games
			tempButtonCollection = []
			if len(menuItems) == 0:
				print('Awaiting game data...')
			else:
				if len(menuItems) > 12:
					y = y/2
				for item in menuItems:
					itemX = x
					itemY = y
					itemYAlt = y + (buttonHeight/3)
					gameRectangle = pygame.draw.rect(globals.displaySurface, (255, 255, 255), [itemX, itemY, buttonWidth, buttonHeight])
					button = Button()
					button.rect = gameRectangle
					button.text = item.title
					button.type = 'launcher'
					button.value = item.id

					columnStart = itemX + iconWidth + cellPadding + 6
					gameTitleText = globals.fontDefault.render(button.text, True, (0, 0, 0))
					globals.displaySurface.blit(gameTitleText, (columnStart, itemYAlt ))

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
