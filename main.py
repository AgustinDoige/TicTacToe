class Board:
	def __init__(self,window,startingPlayer,startingShape,placements=[[0,0,0],[0,0,0],[0,0,0]]):
		# Player: 1 or 2. 1 means the Human player, 2 means the Bot
		# Placements: List of lists. Matrix 3x3.
		# An element inside placement can be either: 0 Meaning EMPTY, 1 meaning an item placed by the player 1, or 2 meaning an item placed by player 2
		drawBackground(window)
		self.player = startingPlayer  #Means the player whos move is NEXT.
		self.shape = startingShape
		self.placements = placements
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

	def drawIt(self):
		tDic = {1:'cross',2:'circle'}
		i = 0
		for l in self.placements:
			j = 0
			for it in l:

				if it != 0:
					drawShape(self.window,position=(i+1,j+1),shape=tDic[it])
				j+=1
			i += 1



class Button:
	def __init__(self,window,text,relativeCoord,size):
		# Relative Coord is the relative position if the screen would be a 50x50 pixel window
		self.txt = text
		self.window = window
		pos1 = int((w/50)*relativeCoord[0]) - size*len(self.txt)
		pos2 = int((h/50)*relativeCoord[1]) - size
		pos3 = int((w/50)*relativeCoord[0]) + size*len(self.txt)
		pos4 = int((h/50)*relativeCoord[1]) + size
		self.pos1 = pos1
		self.pos2 = pos2
		self.pos3 = pos3
		self.pos4 = pos4
		self.rectangle = Rectangle(Point(pos1,pos2),Point(pos3,pos4))
		self.rectangle.setOutline(color_rgb(100,100,0))
		self.rectangle.setFill(color_rgb(200,200,0))
		self.rectangle.setWidth(3)
		
		self.text = Text(Point(int((w/50)*relativeCoord[0]),int((h/50)*relativeCoord[1])),self.txt)
		self.text.setTextColor(color_rgb(20,20,100))
		self.text.setSize(size)
		self.text.setFace('arial')

	def draw(self):
		self.rectangle.draw(self.window)
		self.text.draw(self.window)

	def wasClicked(self,click):
		# click is a Point Object generally obtained from a .getMouse() call
		return isPointInRectangle(click,((self.pos1,self.pos2),(self.pos3,self.pos4)))

	def undraw(self):
		self.rectangle.undraw()
		self.text.undraw()

def hasEnded(placements):
	"""
	return 0 == UNFINISHED GAME
	return 1 == HUMAN WINS
	return 2 == BOT WINS
	return 3 == DRAW
	return 4 == BOTH WIN

	placements coord are (x,y) with origin on the top left going larger "right-down"
	So a value on the top right is a [[0,0,0],[0,0,0],[1,0,0]] (x=2,y=0)
	"""

	hW = False
	bW = False
	# First it checks the diagonals
	d1 = set((placements[0][0],placements[1][1],placements[2][2]))
	d2 = set((placements[0][2],placements[1][1],placements[2][0]))
	for d in [d1,d2]:
		if len(d) == 1:
			if 0 not in d:
				if 1 in d:
					hW = True
				else:
					bW = True

	# Then checks the columns
	for l in placements:
		r = set(l)
		if len(r) == 1:
			if 0 not in r:
				if 1 in r:
					hW = True
				else:
					bW = True

	# Then it checks the rows
	for i in range(0,3):
		c = set((placements[i][0],placements[i][1],placements[i][2]))
		if len(c) == 1:
			if 0 not in c:
				if 1 in c:
					hW = True
				else:
					bW = True

	# Finally checks for a draw
	for l in placements:
		for item in l:
			if item == 0:
				return 0

	if hW and bW:
		return 4
	if hW:
		return 1
	if bW:
		return 2
	return 3

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

def boardValue(placements,turn=2):
	# Returns the value of a board for the bot to chose
	# turn = 1 means it's the players turn, turn = 2 means it's the  bot's turn
	state = hasEnded(placements) # 1 = Human Wins, 2 = Bot wins, 3 = Draw, 0 = Non Finished
	if state != 0:
		if state == 1:
			return -1
			# global humanWins
			# humanWins += 1
		if state == 2:
			# global botWins
			# botWins  += 1
			return 1
		elif state == 3:
			# global draws
			# draws += 1
			return 0
		else:
			print("Error! with boardValue()",placements,turn)

	if turn == 2:
		mx = -2
		for in1 in range(0,3):
			for in2 in range(0,3):
				if placements[in1][in2] == 0:
					plCopy = deepcopy(placements)
					plCopy[in1][in2] = 2
					val = boardValue(plCopy,1)
					if val > mx:
						mx = deepcopy(val)
		# print(placements,mx)	
		return mx

	elif turn == 1:
		mn = 2
		for in1 in range(0,3):
			for in2 in range(0,3):
				if placements[in1][in2] == 0:
					plCopy = deepcopy(placements)
					plCopy[in1][in2] = 1
					val = boardValue(plCopy,2)
					if val < mn:
						mn = deepcopy(val)

		# print(placements,mn)
		return mn

	else:
		print("Problem:",placements,turn)

def botMove(board):
	plc = board.placements

	moveDic = {}
	for in1 in range(0,3):
		for in2 in range(0,3):
			if plc[in1][in2] == 0:
				cpyplc = deepcopy(plc)
				cpyplc[in1][in2] = 2
				moveDic[(in1,in2)] = boardValue(cpyplc,1)
	mx = max(moveDic.values())
	options = []
	for key in moveDic.keys():
		if moveDic[key] == mx:
			options.append(key)
	print(mx,moveDic,options,board.placements)
	chosenMove = choice(options)
	board.nextTurn(chosenMove[0],chosenMove[1])

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
	line = Line(Point(15,int(h/2)),Point(w-15,int(h/2)))
	line.setOutline(color_rgb(220,220,0))
	line.setWidth(50)
	line.draw(window)
	text = Text(Point(int(w/2),int(h/2)),txt) #The anchor point is on the CENTER of the text
	text.setTextColor(color_rgb(0,0,0))
	text.setSize(20)
	text.setFace('helvetica')
	text.draw(window)

def whoStarts(window):
	# Returns the variable startingPlayer
	pass

def playerShape(window,startingPlayer):
	# Returns the variable startingShape
	pass

def launchScreen(window):
	window.setBackground(color_rgb(10,10,70))
	text = Text(Point(int(w/2),int(h/5)),"Ta Te Ti")
	text.setTextColor(color_rgb(230,230,80))
	text.setSize(25)
	text.setFace('helvetica')
	text.draw(window)
	text2 = Text(Point(int(w/2),int(h*1.5/5)),"Agustin Dominguez")
	text2.setTextColor(color_rgb(230,230,80))
	text2.setSize(10)
	text2.setFace('helvetica')
	text2.draw(window)

	startButton = Button(window,"START",(25,37),25)
	startButton.draw()
	# (self,window,text,relativeCoord,size):
#########################
	while True:
		click = window.getMouse()
		if startButton.wasClicked(click):
			startButton.undraw()
			text.undraw()
			text2.undraw()
			break

def testA():
	# print(boardValue([[1,0,1],[0,1,2],[2,0,2]],1))
	# print(boardValue([[1,1,1],[0,1,2],[2,0,2]],2))
	# print(boardValue([[0,0,2],[0,1,0],[0,0,0]],1))
	# print(boardValue([[2,0,0],[0,1,0],[0,0,0]],1))


	global botWins
	global humanWins
	global draws 
	botWins = 0
	humanWins = 0
	draws = 0
	boardValue([[0,0,0],[0,0,0],[0,0,0]],1)
	print("botWins:",botWins,". humanWins:",humanWins,". draws",draws)
	humanWins = 0
	botWins = 0
	draws = 0
	boardValue([[0,0,0],[0,0,0],[0,0,0]],2)
	print("botWins:",botWins,". humanWins:",humanWins,". draws",draws)

def testB():
	import itertools
	a = (0,1,2)
	gen = itertools.product(a,repeat=9)
	botW = 0
	humW = 0
	draw = 0
	both = 0
	incl = 0
	for it in gen:
		l = list((list(it[0:3]),list(it[3:6]),list(it[6:])))

		st = hasEnded(l)
		if st != 0:
			if st == 1:
				humW += 1
				print(st,l)
			elif st == 2:
				botW += 1
			elif st == 3:
				draw += 1
			else:
				both += 1
		else:
			incl += 1
	print("botWins:",botW,". humanWins:",humW,". draws:",draw,". both:",both,". incomplete:",incl)
	print(botW+humW+draw+both+incl)

	win = GraphWin("TATETI",501,501)
	global h
	h = win.height
	global w
	w = win.width
	global xSide
	xSide = int(w/3)
	global ySide
	ySide = int(h/3)
	plac = [[1, 1, 2], [1, 2, 2], [2, 2, 1]]
	# window,startingPlayer,startingShape,placements=[[0,0,0],[0,0,0],[0,0,0]]
	brd = Board(win,1,'cross',plac)
	brd.drawIt()
	win.getMouse()
	win.close()

def main():
	win = GraphWin("TATETI",501,501)

	global h
	h = win.height
	global w
	w = win.width
	global xSide
	xSide = int(w/3)
	global ySide
	ySide = int(h/3)

	launchScreen(win)

	b = Board(window=win,startingPlayer=1,startingShape='cross')
	while True:
		playerMove(win,b)
		status = hasEnded(b.placements)
		if status > 0:
			endGame(win,status)
			break
		botMove(b)
		status = hasEnded(b.placements)
		if status > 0:
			endGame(win,status)
			break
	win.getMouse()
	win.close()

from random import choice
from time import sleep
from copy import deepcopy
from copy import copy
from graphics import *
# main()
# testA()
testB()


###
"""
RESULTS:
- Checking all posible board combinations:
botWins: 178 . humanWins: 178 . draws: 114 . both: 42 . incomplete: 19171		  TOTAL; 19683
"""
###