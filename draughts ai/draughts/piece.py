from .constants import BLUE, WHITE, SQUARE_SIZE, CROWN
import pygame
class Piece:
	PADDING = 10
	OUTLINE = 2

	def __init__(self, row, col, colour):
		self.row = row
		self.col = col
		self.colour = colour
		self.king = False #pieces don't start as kings
		
		#if self.colour == BLUE:
		#	self.direction = -1
		#else:
		#	self.direction = 1

		self.x = 0
		self.y = 0
		self.calc_pos()

	def calc_pos(self):
		#adding half square size at the end puts the x and y in the middle of a square
		self.x = SQUARE_SIZE * self.col + SQUARE_SIZE//2
		self.y = SQUARE_SIZE * self.row + SQUARE_SIZE//2

	def promote_to_king(self):
		print ("promoted to king")
		self.king = True

	def is_king(self):
		if self.king:
			return True
		else:
			return False

	def draw(self, win):
		xy = (self.x, self.y)
		radius = SQUARE_SIZE//2 - self.PADDING

		#pygame.draw.circle(swin, self.colour, xy, radius + self.OUTLINE)
		pygame.draw.circle(win, self.colour, xy, radius)

		if self.king == True:
			crown_pos = (self.x -CROWN.get_width()//2, self.y - CROWN.get_height()//2)
			win.blit(CROWN, crown_pos)

	def move(self, row, col):
		self.row = row
		self.col = col
		self.calc_pos()

	#representation of object
	def __repr__(self):
		return str(self.colour)