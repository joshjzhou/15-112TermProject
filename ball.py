from tkinter import *
import time
class Ball(object):

	def __init__(self, cx, cy):
		self.cx = cx
		self.cy = cy
		self.dx = 0
		self.dy = 0
		self.image = PhotoImage(file = "bigball.png")
		self.rad = 40

	def collide(self, data):
		if(self.cx< 0 ):
			self.dx *= -1
			data.bounces += 1
		if(self.cy>data.height):
			print("heree")
			self.dy *= -1
			data.bounces += 1

		if(self.cx > data.width):
			data.bounces = 3 


		#all collisions with any part of the hoop
		if(840 <= (self.cx + self.rad) <= 900 and (120 <= (self.cy + self.rad) <= 180)):
			if(self.dx < 0):
				self.dy *= -0.9
			else:
				self.dx *= -0.7
			data.bounces += 1
		
		if(1000 <= self.cx + self.rad<= 1100 and 0 <= self.cy + self.rad<= 250):
			self.dx *= -0.6
			self.cx -= 20
			data.bounces += 1
		elif(1030 <= self.cx+ self.rad<= 1100 and self.cy + self.rad> 250):
			self.dx *= -1
			data.bounces += 1
		if(900 <= self.cx + self.rad<= 1000 and 120 <= self.cy + self.rad<= 160):

			self.dy = 0
			self.dx = 0
			data.accel = 5

			#data.wentIn = True


	def draw(self, canvas, data):
		canvas.create_image(self.cx, self.cy, anchor = NW, image = self.image)

		#for debugging hitboxes on hoop
		# canvas.create_rectangle(840, 120, 900, 180)
		# canvas.create_rectangle(1000, 0, 1100, 250)
		# canvas.create_rectangle(1030,250,1100,data.height)
		# canvas.create_rectangle(900, 120, 1000, 160)


	def move(self, data):
		self.cx += self.dx
		self.cy += self.dy
		

