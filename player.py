from tkinter import *

class Player(object):

	def __init__(self, attr):
		self.name = attr[0]
		self.pic =  PhotoImage(file = attr[1])
		self.threePt = int(attr[2])
		self.midRange = int(attr[3])
		self.inside = int(attr[4])
		self.onBallD = int(attr[5])
		self.steal = int(attr[6])
		self.offBallD = int(attr[7])
		self.passingAcc = int(attr[8])
		self.stamina = 100
		self.x = 0
		self.y = 0
		self.scored = 0


		self.gamePic = PhotoImage(file = attr[10])
		self.hasBall = False




	def passBall(self, other):
		other.hasBall = True
		self.hasBall = False


	def __repr__(self):
		return self.name + "\n" + "3pt:"+str(self.threePt)+"\n"+"Mid:"+str(self.midRange)+"\n"

