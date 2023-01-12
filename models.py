class Button(object):
	def __init__(self):
		self.rect = None
		self.text = ''
		self.type = ''
		self.value = ''
		self.icon = ''


# ---------------------------------------------------------------------

class Game(object):
	def __init__(self):
		self.id = ''
		self.title = ''
		self.icon = ''

# ---------------------------------------------------------------------

class GameList(object):
	def __init__(self):
		self.games = [Game()]
