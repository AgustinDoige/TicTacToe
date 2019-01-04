"""
0 generally represents a unfinished game
1 generally represents the Human Player.
2 generally represents the Bot Player
3 generally represents a Draw
"""
class Board:
	# placements is a list of lists that holds the matrix of the board. The matrix goes through the columns down instead of rows right
	def __init__(self,placements,shape,player):
		self.placements = placements
		self.currentShape = shape    # 'cross' OR 'circle'
		self.currentPlayer = player  # 1 OR 2 - It means the player who's turn is now.
		self.state = self.getState()

	def cloneBoard(self):
		return Board(deepcopy(self.placements),deepcopy(self.currentShape),deepcopy(self.currentPlayer))

	def getState(self):
		# 	return 0 == UNFINISHED GAME // return 1 == HUMAN WINS  //  return 2 == BOT WINS // return 3 == DRAW
		plc = self.placements
		setList = []
		#First it checks the Diagonals.
		setList.append(set((plc[0][0],plc[1][1],plc[2][2]))) #Diagonal from top left to down right
		setList.append(set((plc[0][2],plc[1][1],plc[2][0]))) #Diagonal from down left to up right
		#Then it checks the columns
		for i in range(0,3):
			setList.append(set(plc[i]))
		#Then it chekcs the rows
		for i in range(0,3):
			setList.append(set((plc[0][i],plc[1][i],plc[2][i])))
		#This checks the setList
		# print(setList)
		for st in setList:
			if len(st) == 1:
				if 0 not in st:
					return list(st)[0]
		#Now that has made sure neither 1 nor 2 have won, it needs to see if the board is a Draw (3) or Unfinished (0)
		for l in plc:
			for it in l:
				if it == 0:
					return 0
		return 3

	def value(self):
		# print("Called value about",self.placements)
		# Gives the value of the current Board. If the board is not finished, it will make every play making a tree with
		# the best choices for each player and then it will gather the value of this board
		# Degenerate case
		s = self.getState()
		if s != 0:
			return s # 1 == HUMAN WINS // 2 == BOT WINS // 3 == DRAW

		optionSet = set()
		for in1 in range(0,3):
			for in2 in range(0,3):
				if not self.occupied(in1,in2):
					subVal = self.makeMove(in1,in2).value() #Value of making the move (in1,in2)
					if subVal == self.currentPlayer:
						# If there's a move that leads to victory, the value of that board is propagated to this one
						# because we can predict that the player will make that move
						return subVal
					optionSet.add(subVal) #It adds other values that aren't victories
		if 3 in optionSet:
			# If it can't find a victory, the optimal solution is a Draw, so we propagate that result
			return 3
		else:
			# It gets to this option when all the options of moves can't lead to a victory for CurrentPlayer, nor a Draw
			return self.opponent()

	def occupied(self,i1,i2):
		# From (0,0) to (2,2)
		if self.placements[i1][i2] == 0:
			return False
		return True

	def opponent(self):
		# Returns 2 when self.currentPlayer == 1 and viceversa
		if self.currentPlayer == 1:
			return 2
		return 1

	def makeMove(self,i1,i2):
		# Returns a CLONE of board with move (i1,i2) made
		# i1 and i2 have to range from 0 to 2
		clone = self.cloneBoard()
		clone.placements[i1][i2] = self.currentPlayer
		if clone.currentShape == 'circle':
			clone.currentShape = 'cross'
		else:
			clone.currentShape = 'circle'

		if clone.currentPlayer == 1:
			clone.currentPlayer = 2
		else:
			clone.currentPlayer = 1
		clone.state = clone.getState()
		return clone

	def drawMove(self,i1,i2,window):
		# Draws move on window and returns a CLONE of board with move (i1,i2) made
		# i1 and i2 have to range from 0 to 2
		drawShape(window=window,position=(i1,i2),shape=self.currentShape)
		# print("Drawing a",self.currentShape,"in",i1,i2,)
		return self.makeMove(i1,i2)

	def drawEntireBoard(self,window):
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

def drawShape(window,position,shape):
	# Position is a 2 item tuple with the position of one of the 9 spots on the bord. 
	# (1,1) is the center. (0,0) is the top left spot. (2,0) is the top right spot
	# shape can be 'cross' or 'circle'

	smallRatio = 9

	xPoint = int(xSide/2) + (xSide * (position[0]))
	yPoint = int(ySide/2) + (ySide * (position[1]))

	if shape == 'circle':
		c = Circle(Point(xPoint,yPoint),int(min(window.width,window.height)/smallRatio))
		c.setOutline(color_rgb(200,30,30))
		c.setWidth(6)
		c.draw(window)
		drawnShapes.append(c)

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
		drawnShapes.extend([line1,line2])

	else:
		while True:
			print("Shape '{}' Not Known".format(shape))
			sleep(60)

def playerMove(window,board):
	# Takes a board when it is its turn and changes it with the player move
	# print(board,type(board))
	while True:
		clickPoint = window.getMouse()
		for i in range(0,3):
			for j in range(0,3):
				rect = ((xSide*i,ySide*j),(xSide*(i+1),ySide*(j+1)))
				if isPointInRectangle(clickPoint,rect):
					if not board.occupied(i,j):
						return board.drawMove(i,j,window)

def botMove(window,board):
	# sleep(0.5)
	optionsDictionary = {} 
	for in1 in range(0,3):
		for in2 in range(0,3):
			if not board.occupied(in1,in2):
				optionsDictionary[(in1,in2)] = board.makeMove(in1,in2).value()
	bestOptions = []
	if 2 in optionsDictionary.values():
		for key in optionsDictionary.keys():
			if optionsDictionary[key] == 2:
				bestOptions.append(key)

	elif 3 in optionsDictionary.values():
		for key in optionsDictionary.keys():
			if optionsDictionary[key] == 3:
				bestOptions.append(key)

	else:
		bestOptions = deepcopy(list(optionsDictionary.keys()))

	chosenBox = choice(bestOptions)
	return board.drawMove(chosenBox[0],chosenBox[1],window) 

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
		drawnShapes.extend([line1,line2])

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
	while True:
		click = window.getMouse()
		if startButton.wasClicked(click):
			startButton.undraw()
			text.undraw()
			text2.undraw()
			break

def winTitle(window,status):
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
	drawnShapes.extend([text,line])

def pickShape(window):
	window.setBackground(color_rgb(15,15,10))
	text = Text(Point(int(w/2),int(h/5)),"Pick your shape")
	text.setTextColor(color_rgb(230,230,80))
	text.setSize(25)
	text.setFace('helvetica')
	text.draw(window)

	crossButton = Button(window,"X",(35,40),25)
	circleButton  = Button(window,"O",(15,40),25)
	crossButton.draw()
	circleButton.draw()

	c = Circle(Point(w*15/50,h*25/50),int(min(w,h)/7))
	c.setOutline(color_rgb(200,30,30))
	c.setWidth(7)
	c.draw(window)

	d = int(min(w,h)/7)
	line1 = Line(Point(w*35/50-d,h*25/50-d),Point(w*35/50+d,h*25/50+d))
	line2 = Line(Point(w*35/50-d,h*25/50+d),Point(w*35/50+d,h*25/50-d))
	line1.setOutline(color_rgb(30,30,200))
	line2.setOutline(color_rgb(30,30,200))
	line1.setWidth(7)
	line2.setWidth(7)
	line1.draw(window)
	line2.draw(window)

	while True:
		d = False
		click = window.getMouse()
		if crossButton.wasClicked(click):
			sh = 'cross'
			d = True
		if circleButton.wasClicked(click):
			sh = 'circle'
			d = True

		if d:
			crossButton.undraw()
			circleButton.undraw()
			text.undraw()
			line1.undraw()
			line2.undraw()
			c.undraw()
			return sh

def whoStarts(window):
	window.setBackground(color_rgb(50,50,70))
	text = Text(Point(int(w/2),int(h/5)),"Do you want to go first?")
	text.setTextColor(color_rgb(230,230,80))
	text.setSize(25)
	text.setFace('helvetica')
	text.draw(window)

	yesButton = Button(window,"YES",(15,37),25)
	noButton  = Button(window,"NO ",(36,37),25)
	yesButton.draw()
	noButton.draw()
	while True:
		d = False
		click = window.getMouse()
		if yesButton.wasClicked(click):
			d = True
			starter = 1
		if noButton.wasClicked(click):
			d = True
			starter = 2
		if d:
			text.undraw()
			noButton.undraw()
			yesButton.undraw()
			return starter

def cleanWindow(window):
	for a in range(0,len(drawnShapes)):
		drawnShapes.pop(0).undraw()

def backLoop(window):
	window.getMouse()
	cleanWindow(window)
	window.setBackground(color_rgb(5,5,40))
	text = Text(Point(int(w/2),int(h/5)),"")
	text.setTextColor(color_rgb(230,230,80))
	text.setSize(25)
	text.setFace('helvetica')
	text.draw(window)

	menuButton = Button(window,"MENU",(25,15),25)
	rematchButton  = Button(window,"REMATCH ",(25,25),25)
	endButton = Button(window,"CLOSE",(25,35),25)
	menuButton.draw()
	rematchButton.draw()
	endButton.draw()
	while True:
		d = False
		click = window.getMouse()
		if menuButton.wasClicked(click):
			d = True
			action = 'restart'
		if rematchButton.wasClicked(click):
			d = True
			action = 'rematch'
		if endButton.wasClicked(click):
			d = True
			action = 'end'
		if d:
			text.undraw()
			menuButton.undraw()
			rematchButton.undraw()
			endButton.undraw()
			return action

def menu(win):
	launchScreen(win)
	global shapE
	shapE = pickShape(win)
	global startEr
	startEr = whoStarts(win)
	game(win)

def game(win):
	drawBackground(win)
	b = Board([[0,0,0],[0,0,0],[0,0,0]],shapE,startEr)
	if startEr == 1:
		while b.state == 0:
			b = playerMove(win,b)
			if b.state != 0:
				break
			b = botMove(win,b)
		winTitle(win,b.state)
	elif startEr == 2:
		while b.state == 0:
			b = botMove(win,b)
			if b.state != 0:
				break
			b = playerMove(win,b)
		winTitle(win,b.state)
	# print(drawnShapes)

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
	global drawnShapes
	drawnShapes = []

	menu(win)
	while True:
		des = backLoop(win)
		if des == 'rematch':
			game(win)
		elif des == 'restart':
			menu(win)
		else:
			win.close()
			break

from random import choice
from time import sleep
from copy import deepcopy
from graphics import *
main()