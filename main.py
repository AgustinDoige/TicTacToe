class Board:
	def __init__(self,window,startingPlayer,startingShape,placements=[[0,0,0],[0,0,0],[0,0,0]]):
		# Player: 1 or 2. 1 means the Human player, 2 means the Bot
		# Placements: List of lists. Matrix 3x3.
		# An element inside placement can be either: 0 Meaning EMPTY, 1 meaning an item placed by the player 1, or 2 meaning an item placed by player 2
		drawBackground(window)
		self.player = startingPlayer  #Means the player whos move is NEXT.
		self.shape = startingShape
		self.placements = placements
		self.ended = 0
		self.window = window

	def isOccupied(self,i1,i2):
		# From (0,0) to (2,2)
		if self.placements[i1][i2] == 0:
			return False
		return True

	def nextTurn(self,i1,i2):
		# i1 and i2 have to range from 0 to 2
		self.placements[i1][i2] = self.player
		drawShape(window=self.window,position=(i1+1,i2+1),shape=self.shape)

		if self.shape == 'cross':
			self.shape = 'circle'
		else:
			self.shape = 'cross'
		
		if self.player == 1:
			self.player = 2
		else:
			self.player = 1

		self.ended = hasEnded(self.placements)

def hasEnded(placements):
	# Return 0 if it hasn't, 1 if player 1 (HUMAN) won, 2 if player 2 (BOT) won, and 3 if it is a DRAW
	hasSpacesLeft = False
	e1 = set((placements[0][0],placements[1][1],placements[2][2]))
	e2 = set((placements[0][2],placements[1][1],placements[2][0]))
	for e in [e1,e2]:
		if len(e) == 1:
			if 0 not in e:
				return list(e)[0]

	for r in range(0,3):
		s1 = set()
		s2 = set()
		l = [s1,s2]
		for q in range(0,3):
			a1 = placements[r][q]
			a2 = placements[q][r]
			if a1 == 0 or a2 == 0:
				hasSpacesLeft = True
			l[0].add(a1)
			l[1].add(a2)
		for s in l:
			if len(s) == 1:
				if 0 not in s1:
					return list(s)[0]

	if not hasSpacesLeft:
		return 3
	return 0

def isPointInRectangle(point,rectangle):
	# Takes objects Point and checks if their coordenades are in rectangle. Rectangle is NOT an object, but a tuple with 2 tuples that each have the
	# x and y coord of the extreme points of the rectangle, like the way Graphics.py constructs rectangles
	xCoord = point.x
	yCoord = point.y
	edgeRestriction = 2 # A bigger number forces the player to place the mouse even more inside the rectangle and not on the edges
	if xCoord < rectangle[0][0] + edgeRestriction:
		return False
	if xCoord > rectangle[1][0] - edgeRestriction:
		return False
	if yCoord < rectangle[0][1] + edgeRestriction:
		return False
	if yCoord > rectangle[1][1] - edgeRestriction:
		return False
	return True

def boardValue(placements):
	# Returns the value of a board for the bot to chose
	state = hasEnded(placements) # state is 
	if state != 0:
		if state == 1:
			return -1
		if state == 2:
			return 1
		if state:
			return 0

	options = []
	plc = reversePlacements(placements)
	for in1 in range(0,3):
		for in2 in range(0,3):
			if plc[in1][in2] == 0:
				cpyplc = plc[:]
				cpyplc[in1][in2] = 1
				options.append(boardValue(cpyplc)*(-1))
	print(options,max(options))
	return max(options)
	# return min(options)


def chooseIndex(lis):
	# Takes a list of integers, and it chooses the index of one of the repeated max values.
	# If there are more than 1 "max" option, then this one index of those.
	# As in if options are (-1,1,0,0,1,1,-1), it will chose between  the 3 'ones', and return that index
	mx = max(lis)
	i = 0
	indexes = []
	for el in lis:
		if el == mx:
			indexes.append(i)
		i += 1
	return choice(indexes)

def reversePlacements(pl):
	ans = []
	for l in pl:
		an = []
		for el in l:
			if el == 1:
				an.append(2)
			elif el == 2:
				an.append(1)
			elif el == 0:
				an.append(0)
		ans.append(an)
	return ans

def botMove(placements,board):
	# Takes a board when it is its turn and changes it with its move
	options = []
	plcmts = reversePlacements(placements)
	# print(plcmts)
	for in1 in range(0,3):
		for in2 in range(0,3):
			if plcmts[in1][in2] == 0:
				cpyplc = deepcopy(plcmts)
				cpyplc[in1][in2] = 2 #!!!!!!!!!!!!!!!!!!!!!
				# print("AAA",plcmts,cpyplc)
				options.append(boardValue(cpyplc))
	# print("Options:",options)
	choice = chooseIndex(options)
	# print("choice",choice)
	counter = 0
	# print("plcmts",plcmts)
	# print("cpyplc",cpyplc)
	for in1 in range(0,3):
		for in2 in range(0,3):
			if plcmts[in1][in2] == 0:
				# print("Counter.choice",counter,choice)
				if counter == choice:
					# print("Adding point to position:",in1,in2)
					board.nextTurn(in1,in2)
				counter += 1

def playerMove(window,board):
	# Takes a board when it is its turn and changes it with the player move
	done = False
	while not done:
		clickPoint = window.getMouse()
		for i in range(0,3):
			for j in range(0,3):
				rect = ((xSide*i,ySide*j),(xSide*(i+1),ySide*(j+1)))
				if isPointInRectangle(clickPoint,rect):
					if not board.isOccupied(i,j):
						board.nextTurn(i,j)
						done = True


def drawShape(window,position,shape):
	# Position is a 2 item tuple with the position of one of the 9 spots on the bord. 
	# (2,2) is the center. (1,1) is the top left spot. (1,2) is the middle spot on the top row
	# shape can be 'cross' or 'circle'

	smallRatio = 9

	xSide = int(window.width / 3)
	ySide = int(window.height / 3)
	xPoint = int(xSide/2) + (xSide * (position[0]-1))
	yPoint = int(ySide/2) + (ySide * (position[1]-1))

	if shape == 'circle':
		c = Circle(Point(xPoint,yPoint),int(min(window.width,window.height)/smallRatio))
		c.setOutline(color_rgb(200,30,30))
		c.setWidth(6)
		c.draw(window)

	elif shape == 'cross':
		d = int(min(window.width,window.height)/smallRatio)
		line1 = Line(Point(xPoint-d,yPoint-d),Point(xPoint+d,yPoint+d))
		line2 = Line(Point(xPoint-d,yPoint+d),Point(xPoint+d,yPoint-d))
		line1.setOutline(color_rgb(30,30,200))
		line2.setOutline(color_rgb(30,30,200))
		line1.setWidth(6)
		line2.setWidth(6)
		line1.draw(window)
		line2.draw(window)

	else:
		while True:
			print("Shape '{}' Not Known".format(shape))
			sleep(60)

def drawBackground(window):
	window.setBackground(color_rgb(15,15,15))
	h = window.height
	w = window.width
	for d in range(1,3):
		y = ySide*d
		line1 = Line(Point(0,y),Point(w,y))
		line1.setOutline(color_rgb(230,230,230))
		line1.setWidth(4)
		line1.draw(window)

		x = xSide*d
		line2 = Line(Point(x,0),Point(x,h))
		line2.setOutline(color_rgb(230,230,230))
		line2.setWidth(4)
		line2.draw(window)

def endGame(window,status):
	if status == 1:
		txt = "Player Wins!"
	elif status == 2:
		txt = "You lose."
	else:
		txt = "It's a Draw"
	h = window.height
	w = window.width
	line = Line(Point(15,int(h/2)),Point(w-15,int(h/2)))
	line.setOutline(color_rgb(220,220,0))
	line.setWidth(50)
	line.draw(window)
	text = Text(Point(int(w/2),int(h/2)),txt) #The anchor point is on the CENTER of the text
	text.setTextColor(color_rgb(0,0,0))
	text.setSize(20)
	text.setFace('helvetica')
	text.draw(window)

def test3():
	win = GraphWin("TATETI",501,501)

	global xSide
	xSide = int(win.width / 3)
	global ySide
	ySide = int(win.height / 3)

	# b = Board(window=win,startingPlayer=1,startingShape='cross',[[0,2,0],[2,1,0],[1,0,0]])
	# print(boardValue([[0,2,0],[2,1,0],[1,0,0]]))
	print(boardValue([[1,0,0],[0,1,0],[0,0,1]]))

def main():
	win = GraphWin("TATETI",501,501)

	global xSide
	xSide = int(win.width / 3)
	global ySide
	ySide = int(win.height / 3)

	b = Board(window=win,startingPlayer=1,startingShape='cross')
	while True:
		playerMove(win,b)
		status = hasEnded(b.placements)
		# print("status1",status)
		if status > 0:
			endGame(win,status)
			break
		sleep(0.7)
		botMove(b.placements,b)
		status = hasEnded(b.placements)
		# print("status2",status)
		if status > 0:
			endGame(win,status)
			break
	win.getMouse()
	win.close()

from random import choice
from time import sleep
from copy import deepcopy
from graphics import *
main()
# test3()