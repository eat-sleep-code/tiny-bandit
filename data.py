import globals
import json
from models import Game, GameList
import os

class Data:
    
    def getGames(): 
        
        with open(os.path.join(globals.appRoot) + 'games.json') as request:
            data = json.loads(request.read())
            gameList = GameList()
            gameList.games.clear()
            dataSource = data['games']

            if len(dataSource) > 0:
                i = 0
                for gameData in dataSource:
                    i = i + 1
                    game = Game()
                    game.id = gameData['id']
                    game.title = gameData['title']
                    game.icon = gameData['icon']

                    gameList.games.append(game)

            return gameList