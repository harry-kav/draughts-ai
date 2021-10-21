import pygame
from .constants import BLACK, WHITE, ROWS, SQUARE_SIZE, BLUE, COLS
from .piece import Piece
class Board:
	def __init__(self):
		#board is a 2d array of 8 rows and 8 columns
		self.board = []
		#self.selected_piece = None
		self.blue_left = self.white_left = 12
		self.blue_kings = self.white_kings = 0

		self.gen_board()

	def draw_board(self, win):
		win.fill(BLACK)
		for row in range(ROWS):
			#drawing alternating squares in blue- the rest will be black
			for col in range(row % 2, ROWS, 2):
				#each square is defined by an x and y position, as well as width and height
				rect_argument = (row*SQUARE_SIZE, col* SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
				pygame.draw.rect(win, BLUE, rect_argument)


	def move(self, piece, row, col):
		self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
		piece.move(row, col)
		print("moved to row "+str(row))
		print(str(ROWS))

		if row == ROWS - 1 or row == 0:
			if piece.is_king() == False:
				piece.promote_to_king()
				if piece.colour == WHITE:
					self.white_kings += 1
				else:
					self.blue_kings +=1

	def get_piece(self, row, col):
		return self.board[row][col]

	def gen_board(self):
		for row in range(ROWS):
			self.board.append([]) #add a row to the board
			for col in range(COLS):
				if col % 2 == ((row + 1) % 2):
					if row < 3:
						self.board[row].append(Piece(row, col, WHITE))
					elif row > 4:
						self.board[row].append(Piece(row, col, BLUE))
					else:
						self.board[row].append(0)#0 represents an empty square

				else:
					self.board[row].append(0)


	def draw(self, win):
		self.draw_board(win)
		for row in range(ROWS):
			for col in range(COLS):
				piece = self.board[row][col]
				if piece !=0:
					piece.draw(win)


	def get_valid_moves(self, piece, allowed_moves = {}):
		moves = {}
		left = piece.col - 1
		right = piece.col + 1
		row = piece.row

		if piece.colour == BLUE or piece.is_king():
			moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.colour, left))
			moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.colour, right))
		if piece.colour == WHITE or piece.is_king():
			moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.colour, left))
			moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.colour, right))

		#remove moves that cannot be played- this is used to force captures
		if len(allowed_moves) > 0:
			illegal_moves = []
			for move in moves:
				if move not in allowed_moves:
					illegal_moves.append(move)
			for move in illegal_moves:
				moves.pop(move)
					
    
		print(moves)
		return moves

	def _traverse_left(self, start, stop, step, colour, left, skipped=[]):
		moves = {}
		last = []
		for r in range(start, stop, step):
			if left < 0:
				break
            
			current = self.board[r][left]
			if current == 0:
				if skipped and not last:
					break
				elif skipped:
					moves[(r, left)] = last + skipped
				else:
					moves[(r, left)] = last
		        
				if last:
					if step == -1:
						row = max(r-3, 0)
					else:
						row = min(r+3, ROWS)
					moves.update(self._traverse_left(r+step, row, step, colour, left-1,skipped=last))
					moves.update(self._traverse_right(r+step, row, step, colour, left+1,skipped=last))
				break
			elif current.colour == colour:
				break
			else:
				last = [current]

			left -= 1

		return moves

	def _traverse_right(self, start, stop, step, colour, right, skipped=[]):
		moves = {}
		last = []
		for r in range(start, stop, step):
			if right >= COLS:
				break
            
			current = self.board[r][right]
			if current == 0:
				if skipped and not last:
					break
				elif skipped:
					moves[(r,right)] = last + skipped
				else:
					moves[(r, right)] = last
                
				if last:
					if step == -1:
						row = max(r-3, 0)
					else:
						row = min(r+3, ROWS)
					moves.update(self._traverse_left(r+step, row, step, colour, right-1,skipped=last))
					moves.update(self._traverse_right(r+step, row, step, colour, right+1,skipped=last))
				break
			elif current.colour == colour:
				break
			else:
				last = [current]

			right += 1
        
		return moves

	def remove(self,pieces):
		for piece in pieces:
			self.board[piece.row][piece.col] = 0

			if piece.colour == WHITE:
				self.white_left -= 1

				if piece.is_king():
					self.white_kings -= 1
			else:
				self.blue_left -= 1

				if piece.is_king():
					self.blue_kings -= 1


	def evaluate(self):
		w1 = 1
		w2 = 0.5
		w3 = 0.3
		centre_pieces = self.find_num_centre_pieces(WHITE)
		return self.white_left - self.blue_left + w2*(self.white_kings - self.blue_kings) + w3*centre_pieces

	def find_num_centre_pieces(self, colour):
		centre_pieces = 0
		pieces = self.get_all_pieces(colour)
		for piece in pieces:
			if piece.row >2 and piece.row <6:
				centre_pieces +=1
		return centre_pieces

	def get_all_pieces(self, colour):
		pieces = []
		for row in self.board:
			for piece in row:
				if piece != 0 and piece.colour == colour:
					pieces.append(piece)
		return pieces

	def winner(self):
		if self.white_left <= 0:
			return BLUE
		elif self.blue_left <= 0:
			return WHITE

		#white_pieces = self.get_all_pieces(WHITE)
		#blue_pieces = self.get_all_pieces(BLUE)
		#white_has_moves = False
		#blue_has_moves = False
		#for piece in white_pieces:
		#	piece_moves = self.get_valid_moves(piece)

		#	if len(piece_moves) > 0:
		#		white_has_moves = True
		#		break

		#if white_has_moves == False:
		#	return BLUE

		#for piece in blue_pieces:
		#	piece_moves = self.get_valid_moves(piece)

		#	if len(piece_moves) > 0:
		#		white_has_moves = True
		#		break

		#if blue_has_moves == False:
		#	return WHITE


