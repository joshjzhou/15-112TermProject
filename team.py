from tkinter import *
from player import Player


class Team(object):

	def __init__(self, name, logo, players):
		self.name = name
		self.logo = PhotoImage(file = logo)
		self.players = players
		#self.coach = coach


	def __repr__(self):
		returnString = self.name+"\n"
		for player in self.players:
			returnString+=repr(player)
		return returnString

