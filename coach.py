import pygame

class Coach(object):

	def __init__(self, name, profPic, teamFocus):
		self.name = name
		self.profPic = pygame.image.load(profPic)
		self.teamFocus = teamFocus