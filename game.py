from tkinter import *
from team import Team
from player import Player
import time
import random
import math
from ball import Ball
	#got from classNotes
def readFile(path):
	with open(path, "rt") as f:
	     return f.read()

def loadTeams(path):
	teams = readFile(path).splitlines()
	players = []
	lisTeams = []
	teamName = ""
	logoUrl = ""
	for j in range(len(teams)//7):
		for i in range(7):
			if(i%7 == 0):
				teamName = teams[j*7+i]
			elif(i%7 == 1):
				logoUrl = teams[j*7+i]
			else:
				players.append(Player(returnPlayers(teams[j*7+i])))
		lisTeams.append(Team(teamName,logoUrl,players))
		players = []
	return lisTeams

def returnPlayers(playerInfo):
	pInfo = playerInfo.split(",")
	name = pInfo[0]
	pic = pInfo[1]
	three = pInfo[2]
	mid = pInfo[3]
	inside = pInfo[4]
	onball = pInfo[5]
	steal = pInfo[6]
	offball = pInfo[7]
	passing = pInfo[8]
	stamina = pInfo[9]
	gamePic = pInfo[10]
	return name, pic, three, mid, inside, onball, steal, offball, passing, stamina, gamePic

def getTeam(data, name):
	for team in data.teams:
		if(team.name == name):
			return team
	return None

def getDistance(x1, y1, x2, y2):
	#print(abs(x1-x2), abs(y1 - y2))
	if(abs(x1-x2) == abs(y1 - y2)):
		return abs(x1 - x2)
	return int(((x1-x2)**2 + (y1-y2)**2)**0.5)

# Basic Animation Framework


####################################
# customize these functions
####################################

def init(data):
    data.logok = PhotoImage(file = "2k.png")

    # load data.xyz as appropriate
    data.teams = loadTeams("teamInfo.txt")
    
    data.teamName = []
    data.score = {}
    for team in data.teams:
    	data.teamName.append(team.name)
    
    data.mode = "homeScreen"
    data.selected = data.teamName[0]
    data.players = []
    data.playerTurn = 0
    data.cellDim = 75
    data.moveSelect = None
    data.passSelect = None
    data.firstInstance = True
    data.highlightedCell = None
    data.ball = PhotoImage(file = "bball.png")
    data.gameMode = 0 #either moveplayer or pass ball
    data.moves = []
    data.maxPass = 5
    data.moveChances = []
    data.maxTurn = 10
    data.maxShots = [2,2]
    data.realShot = 0
    data.timer = 0
    
    data.bounces = 0
    data.wentIn = False
    #PVC

    data.compOn = False
    data.compTeam = None
    data.offenseType = ""
    data.defenseType = ""
    
    pass

def mousePressed(event, data):
    # use event.x and event.y
    if(data.mode == "homeScreen"):
    	homeScreenMousePressed(event, data)
    elif(data.mode == "selectMode"):
    	selectModeMousePressed(event, data)
    elif(data.mode == "controls"):
    	controlsMousePressed(event, data)
    elif(data.mode == "playGame"):
    	playGameMousePressed(event, data)
	
    pass

def keyPressed(event, data):
    if(event.char == "r"):
	    init(data)
    # use event.char and event.keysym
    if(data.mode == "teamSelect"):
    	teamSelectKeyPressed(event, data)
   
    elif(data.mode == "playGame"):
    	playGameKeyPressed(event, data)
    elif(data.mode == "ballGame"):
    	ballKeyPressed(event, data)
    pass

def timerFired(data):
	if(data.mode == "ballGame"):
		ballTimerFired(data)


def redrawAll(canvas, data):
    # draw in canvas
    if(data.mode == "homeScreen"):
        homeScreenRedrawAll(canvas, data)
    elif(data.mode == "selectMode"):
    	selectModeRedrawAll(canvas, data)
    elif(data.mode == "teamSelect"):
        teamSelectRedrawAll(canvas, data)
    elif(data.mode == "playGame"):
       
        playGameRedrawAll(canvas, data)
    elif(data.mode == "gameOver"):
    	gameOverRedrawAll(canvas, data)
    elif(data.mode == "ballGame"):
    	ballRedrawAll(canvas, data)
    elif(data.mode == "controls"):
    	controlsRedrawAll(canvas, data)

    pass







def homeScreenMousePressed(event, data):
	data.mode = "selectMode"
	pass

def homeScreenRedrawAll(canvas, data):

	canvas.create_image(data.width//2.5, data.height//2-30, image=data.logok)
	canvas.create_text(data.width//1.8  + 10, data.height//2 - 40, text="-112",fill="#cf112a", font=("Times", 100, "bold"))
	canvas.create_text(data.width//2, data.height//2 +70, text="The Boardgame",fill="#cf112a", font=("Times", 70, "bold"))
	canvas.create_text(data.width//2, 5 * data.height//6, text="Click anywhere to start", font=("Comic Sans MS", 30, "bold"))


def selectModeRedrawAll(canvas, data):
	canvas.create_text(data.width//2, data.height//6, text="Select Mode", font=("Times", 50, "bold"))
	
	canvas.create_rectangle(data.width//2 - 120 , data.height//2 - 60 - 40, data.width//2 + 120 , data.height//2 + 60 - 40, fill="#787878", activefill="#CACACA")
	canvas.create_text(data.width//2, data.height//2 - 40, text="PvP", font=("Times", 30,"bold"))


	canvas.create_rectangle(data.width//2 - 120, 3 * data.height//4 - 60 - 40, data.width//2 + 120, 3 * data.height//4 + 60 - 40, fill="#787878", activefill="#CACACA")
	canvas.create_text(data.width//2, 3 * data.height//4 - 40, text="PvC", font=("Times", 30,"bold"))

	canvas.create_rectangle(data.width//2 - 120, 8 * data.height//9 - 40, data.width//2 + 120, 8 * data.height//9 + 40, fill="#787878", activefill="#CACACA")
	canvas.create_text(data.width//2, 8 * data.height//9, text="Controls", font=("Times", 30,"bold"))

	

def selectModeMousePressed(event, data):
	if(data.width//2 - 120 <= event.x <= data.width//2 + 120):
		if(data.height//2 - 60 - 40<= event.y <= data.height//2 + 60 - 40):
			data.mode = "teamSelect"
		elif(3 * data.height//4 - 60 -40<= event.y <= 3 * data.height//4 + 60-40):
			data.compOn = True
			data.mode = "teamSelect"
		elif(8 * data.height//9 -40<= event.y <= 8 * data.height//9 + 40):
			data.mode = "controls"
	



def controlsRedrawAll(canvas, data):
	padding = 40
	canvas.create_text(data.width//2, data.height//6, text="Controls", font=("Times", 50, "bold"))

	canvas.create_text(data.width//2, 3 *padding + data.height//6, text="Press r to reset the game at anytime", font=("Times", 20, "bold"))
	canvas.create_text(data.width//2, 4 * padding + data.height//6, text="Press t during your offense phase to toggle real shot", font=("Times", 20, "bold"))
	canvas.create_text(data.width//2, 5 * padding + data.height//6, text="Use the L/R arrows in real shot mode to inc/dec the velocity of the shot", font=("Times", 20, "bold"))
	canvas.create_text(data.width//2, 6 * padding + data.height//6, text="Use the Up/Down arrows in real shot mode to inc/dec the angle of launch", font=("Times", 20, "bold"))
	canvas.create_text(data.width//2, 7 * padding + data.height//6, text="Use the L/R arrows in team select to cycle through teams", font=("Times", 20, "bold"))
	canvas.create_text(data.width//2, 8 * padding + data.height//6, text="Press space in team select to select the team", font=("Times", 20, "bold"))
	canvas.create_rectangle(data.width//2 - 120, 8 * data.height//9 - 40, data.width//2 + 120, 8 * data.height//9 + 40, fill="#787878", activefill="#CACACA")
	canvas.create_text(data.width//2, 8 * data.height//9, text="Back", font=("Times", 30,"bold"))


def controlsMousePressed(event, data):
	if(data.width//2 - 120 <= event.x <= data.width//2 + 120):
		if(8 * data.height//9 -40<= event.y <= 8 * data.height//9 + 40):
			data.mode = "selectMode"
	

def determineOffenseType(data):
	if(data.score[data.players[1].name] > data.score[data.players[0].name] and (data.score[data.players[1].name] - data.score[data.players[0].name])//data.maxTurn <= 3 and data.maxTurn <3 ):
		data.offenseType = "threePt"
	else:
		data.offenseType = "normal"

def determineDefenseType(data):
	if(data.score[data.players[1].name] < data.score[data.players[0].name] and (data.score[data.players[0].name] - data.score[data.players[1].name])//data.maxTurn <= 3 and data.maxTurn <3 ):
		data.defenseType = "threePt"
	else:
		data.defenseType = "normal"



def runOffense(data):
	if(data.offenseType == "threePt"):
		zone1 = [[0],[0,4]]
		zone2 = [[0,2],[5,7]]
		zone3 = [[3,5],[7]]
		zone4 = [[6,8],[5,7]]
		zone5 = [[8],[0,4]]
		zones = [zone1, zone2, zone3, zone4, zone5]
		bestStaThreeAvg = 0
		bestPlayer = None
		for i in range(len(data.players[0].players)):
			player = data.players[0].players[i]
			if(len(zones[i][0]) == 1):
				player.x = zones[i][0][0]
			else:
				player.x = random.randint(zones[i][0][0],zones[i][0][1])
			if(len(zones[i][1]) == 1):
				player.y = zones[i][1][0]
			else:
				player.y = random.randint(zones[i][1][0],zones[i][1][1])

			curAvg = (player.threePt + player.stamina)/2
			if(curAvg > bestStaThreeAvg):
				bestStaThreeAvg = curAvg
				bestPlayer = player
		if(bestPlayer.name != getPlayerWithBall(data).name):
			data.moves.append(("Pass", getPlayerWithBall(data), bestPlayer))
			getPlayerWithBall(data).passBall(bestPlayer)
			data.moves.append(("Shoot", bestPlayer))
		else:
			data.moves.append(("Shoot", bestPlayer))
	else:
		zone1 = [[0,2],[0,3]]
		zone2 = [[0,4],[4,7]]
		zone3 = [[5,8],[4,7]]
		zone4 = [[6,8],[0,3]]
		zone5 = [[3,5],[0,3]]
		zones = [zone1, zone2, zone3, zone4, zone5]
		bestStaThreeAvg = 0
		bestPlayer = None
		for i in range(len(data.players[0].players)):
			player = data.players[0].players[i]
			
			player.x = random.randint(zones[i][0][0],zones[i][0][1])
			
			player.y = random.randint(zones[i][1][0],zones[i][1][1])

			curAvg = (player.threePt + player.midRange + player.inside + player.stamina)/4
			if(curAvg > bestStaThreeAvg):
				bestStaThreeAvg = curAvg
				bestPlayer = player
		if(bestPlayer.name != getPlayerWithBall(data).name):
			data.moves.append(("Pass", getPlayerWithBall(data), bestPlayer))
			getPlayerWithBall(data).passBall(bestPlayer)
			data.moves.append(("Shoot", bestPlayer))
		else:
			data.moves.append(("Shoot", bestPlayer))





def placePlayer(player, zones, data, i = 1):
	dirs = [(0, -1),(1, -1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
	
	if(i == 5):
		return

	locs = []
	x = random.randint(zones[i][0][0],zones[i][0][1])
	y = random.randint(zones[i][1][0],zones[i][1][1])
	locs.append((x,y))
	while(not returnOverlapArea(player, i, x, y, data) and len(locs) < (abs(zones[i][0][0]- zones[i][0][1])+1) * (abs(zones[i][1][0]-zones[i][1][1])+1)):

		x = random.randint(zones[i][0][0],zones[i][0][1])
		y = random.randint(zones[i][1][0],zones[i][1][1])
		if((x,y) not in locs):
			locs.append((x,y))

	player.x = x
	player.y = y
	if(i == 4):
		placePlayer(data.players[1].players[i], zones, data, i+1)
	else:
		placePlayer(data.players[1].players[i+1], zones, data, i+1)




def returnOverlapArea(player, i, x, y, data):
	dirs = [(0, -1),(1, -1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
	overlap = 0

	for tups in dirs:
		for k in range(0, 4):
			if(checkPrevious(x + k * tups[0], y + k * tups[1], i, data)):
				return False	
	return True

def checkPrevious(x, y, i, data):
	dirs = [(0, -1),(1, -1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
	for j in range(0, i):
		player = data.players[1].players[j]
		if(x == player.x and y == player.y):
			return True
	return False


def runDefense(data):
	dirs = [(0, -1),(1, -1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
	


	if(data.defenseType == "threePt"):
		zone1 = [[1,2],[1,3]]
		zone2 = [[1,2],[4,6]]
		zone3 = [[3,5],[4,6]]
		zone4 = [[6,7],[4,6]]
		zone5 = [[6,7],[1,3]]
		zones = [zone1, zone2, zone3, zone4, zone5]
		player = data.players[1].players[0]
		player.x = random.randint(zones[0][0][0],zones[0][0][1])
		player.y = random.randint(zones[0][1][0],zones[0][1][1])
		placePlayer(data.players[1].players[1], zones, data)
	else:
		#normal defense
		zone1 = [[1,3],[0,3]]
		zone2 = [[1,3],[4,6]]
		zone3 = [[5,7],[4,6]]
		zone4 = [[5,7],[0,3]]
		zone5 = [[3,5],[0,3]]
		zones = [zone1, zone2, zone3, zone4, zone5]
		player = data.players[1].players[0]
		player.x = random.randint(zones[0][0][0],zones[0][0][1])
		player.y = random.randint(zones[0][1][0],zones[0][1][1])
		
		placePlayer(data.players[1].players[1], zones, data)
	

			
def checkAllDirs(x, y, data):
	dirs = [(0, -1),(1, -1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
	for move in dirs:
		if(isOnPlayer((x+move[0],y+move[1]), data)):
			return False
	return True


def teamSelectRedrawAll(canvas, data):
	paddingTop = 20
	colWidth = data.width//6
	rowHeight = data.height//3
	tenDown = 40
	team = getTeam(data, data.selected)
	for j in range(6):
		if(j == 0):
			
			if(len(data.players) == 1):
				canvas.create_image(colWidth*(j), 0, anchor = NW, image =data.players[0].logo)
				canvas.create_text(colWidth*(j+.35), rowHeight, text="Player 1", font = ('Comic Sans MS', 15, 'italic'))
				canvas.create_image(colWidth*(j), 1.5* rowHeight, anchor = NW, image =team.logo)
				if(not data.compOn):
					canvas.create_text(colWidth*(j+.35), 2.5 * rowHeight, text="Player 2", font = ('Comic Sans MS', 15, 'italic'))
				else:
					canvas.create_text(colWidth*(j+.35), 2.5 * rowHeight, text="Computer", font = ('Comic Sans MS', 15, 'italic'))
			elif(len(data.players) == 0):
				canvas.create_image(colWidth*(j), 0, anchor = NW, image =team.logo)
				canvas.create_text(colWidth*(j+.35), rowHeight, text="Player 1", font = ('Comic Sans MS', 15, 'italic'))

		else:
			if(len(data.players) == 1):
				newRowHeight = rowHeight * 2.5
				drawTeam(canvas, data, rowHeight, j, data.players[0])
				drawTeam(canvas, data, newRowHeight, j, team)
				
			else:
				drawTeam(canvas, data, rowHeight, j, team)

def drawTeam(canvas, data, rowHeight, j, team):
			paddingTop = 20
			colWidth = data.width//6
			tenDown = 40
			player = team.players[j-1]
			canvas.create_image(colWidth*(j),0 + data.height//3 * ((rowHeight/(data.height//3))-1), anchor = NW, image = player.pic)
			canvas.create_text(colWidth*(j+.5), rowHeight+paddingTop//2, text=player.name, font = ('Comic Sans MS', 15, 'italic'))
			canvas.create_text(colWidth*(j), rowHeight+paddingTop//2 + tenDown, text="Offense", font = ('Comic Sans MS', 8, 'italic'))
			offensiveAvg = ((player.threePt + player.midRange + player.inside + player.passingAcc)/4)/100
			canvas.create_rectangle(colWidth*j+paddingTop*1.5, rowHeight+paddingTop//2 + tenDown, j* colWidth+ (colWidth-20) * offensiveAvg, rowHeight+paddingTop//2 + tenDown+3, fill="green")			
			canvas.create_text(colWidth*(j), rowHeight+paddingTop//2 + 2 * tenDown, text="Defense", font = ('Comic Sans MS', 8, 'italic'))
			defensiveAvg = ((player.onBallD + player.offBallD + player.steal)/3)/100
			canvas.create_rectangle(colWidth*j+paddingTop*1.5, rowHeight+paddingTop//2 + 2* tenDown, j* colWidth+ (colWidth-20) * defensiveAvg, rowHeight+paddingTop//2 +2*tenDown+3, fill="red")			

def teamSelectKeyPressed(event, data):
	if(event.keysym == "Right"):
		data.selected = data.teamName[(data.teamName.index(data.selected)+1)%len(data.teamName)]
	elif(event.keysym == "Left"):
		data.selected = data.teamName[(data.teamName.index(data.selected)-1)%len(data.teamName)]
	elif(event.keysym == "space"):
		if(len(data.players)==0):
			data.players.append(getTeam(data, data.selected))
			data.teamName.remove(data.selected)
			data.selected = data.teamName[0]
		else:
			data.players.append(getTeam(data, data.selected))
			data.teamName.remove(data.selected)
			for team in data.players:
				data.score[team.name] = 0
			data.selected = data.teamName[0]
			if(data.compOn):
				data.compTeam = data.players[-1]
			data.mode = "playGame"


def playGameMousePressed(event, data):
	data.highlightedCell = getXY(event, data)
	if(getXY(event, data) == None):
		if(975 - 40 <= event.x <= 975 + 40 and data.playerTurn == 0):
			if(130 <= event.y <= 170):
				data.gameMode += 1
				if(data.realShot == 1):
					data.gameMode = 0
				data.gameMode %= 2
		if(975 - 50 <= event.x <= 975 + 40):
			if(575 - 20 <= event.y<=575 + 20):
				if(data.playerTurn == 0):
					data.moves.append(("Shoot", getPlayerWithBall(data)))
				if(data.playerTurn == 1):
					for player in data.players[0].players:
						movePlayerOverlap(data, player)
				data.playerTurn += 1
				data.firstInstance = True
				data.gameMode = 0
				if(data.compOn and data.playerTurn < 2 and data.players[data.playerTurn].name == data.compTeam.name):
					if(data.playerTurn == 0):
						determineOffenseType(data)
						runOffense(data)
						data.playerTurn += 1
					elif(data.playerTurn == 1):
						determineDefenseType(data)
						runDefense(data)
						data.playerTurn += 1
				if(data.playerTurn == 2 and not bool(data.realShot)):
					for move in range(len(data.moves)):
						data.moveChances.append(evalLikelihood(calculatePercentage(data.moves[move], data)))
					if(data.moveChances[-1] and False not in data.moveChances):
						if(getShotType(data) == "inside" or getShotType(data) == "midRange"):
							data.score[data.players[0].name] += 2
							play = getPlayerWithBall(data)
							play.scored += 2
						else:
							data.score[data.players[0].name] += 3
							play = getPlayerWithBall(data)
							play.scored += 3
				elif(data.playerTurn == 2 and bool(data.realShot)):
					data.mode = "ballGame"
					ballInit(data)
					
				if(data.playerTurn == 3):
					if((False not in data.moveChances[:-1] and len(data.moveChances) != -1) or
						len(data.moveChances) == 1):
						if(getShotType(data) == "inside" or getShotType(data) == "midRange"):
							
							play = getPlayerWithBall(data)
							if(data.compOn and data.players[0].name == data.compTeam.name):
								play.stamina -= 8
							play.stamina -= 8
						else:
							
							play = getPlayerWithBall(data)
							if(data.compOn and data.players[0].name == data.compTeam.name):
								play.stamina -= 8
							play.stamina -= 12
						if(play.stamina <= 0):
							play.stamina = 0
					for player in data.players[0].players:
						if player.name != getPlayerWithBall(data).name:
							if(player.stamina+3<=100):
								player.stamina += 4
					data.playerTurn %= 3
					data.players = data.players[::-1]
					resetHasBall(data)
					data.moves = []
					data.moveChances = []
					data.maxPass = 5
					data.maxTurn -= 1
					data.maxShots = data.maxShots[::-1]
					data.bounces = 0
					data.wentIn = False
					data.realShot = 0
					data.timer = 0
					if(data.maxTurn == 0):
						data.mode = "gameOver"
					if(data.compOn and data.playerTurn < 2 and data.players[data.playerTurn].name == data.compTeam.name):
						if(data.playerTurn == 0):
							data.players[data.playerTurn].players[0].hasBall = True
							determineOffenseType(data)
							runOffense(data)
							data.playerTurn += 1
						elif(data.playerTurn == 1):
							determineDefenseType(data)
							runDefense(data)
							data.playerTurn += 1
	elif(getXY(event, data) != None and data.playerTurn != 2):
		if(data.gameMode == 0):
			if(data.moveSelect == None):
				for player in data.players[data.playerTurn].players:
					if(getXY(event, data) == (player.x, player.y)):
						data.moveSelect = player
			elif(data.moveSelect != None and not isOnPlayer(getXY(event, data), data)):
				final = getXY(event, data)
				if(data.moveSelect.name == getPlayerWithBall(data).name):
					data.moveSelect.stamina -= 2 * getDistance(data.moveSelect.x, data.moveSelect.y, final[0], final[1])
					
				data.moveSelect.x = final[0]
				data.moveSelect.y = final[1]
				data.moveSelect = None
				data.highlightedCell = None
			else:
				data.moveSelect = None
				data.highlightedCell = None
		else:
			if(data.passSelect == None):
				for player in data.players[data.playerTurn].players:
					if(player.hasBall):
						data.passSelect = player
			elif(data.passSelect != None and isOnPlayer(getXY(event, data), data) and not getPlayer(getXY(event, data), data).hasBall and data.maxPass > 0):
				data.passSelect.passBall(getPlayer(getXY(event, data), data))
				data.moves.append(("Pass", data.passSelect, getPlayer(getXY(event, data), data)))
				data.maxPass -= 1
				data.passSelect = None
				data.highlightedCell = None
			else:
				data.passSelect = None
				data.highlightedCell = None
			pass


	
def evalLikelihood(percent):
	chance = int(100 * percent)
	rand = random.randint(1,100)
	if(rand<=chance):
		return True
	return False


def playGameKeyPressed(event, data):
	if(event.char == "u"):
		if(len(data.moves) != 0):
			pair = data.moves.pop()
			pair[2].passBall(pair[1])
			data.maxPass+=1
	if(event.char == "t"):
		if(data.maxShots[0] != 0):
			data.realShot += 1
			data.realShot %= 2
			if(data.realShot == 1):
				data.moves = []
				data.gameMode = 0

def getShotType(data):
	x,y = getPlayerWithBall(data).x, getPlayerWithBall(data).y

	if(3 <= x <= 5 and 0 <= y <= 3):
		return "inside"
	elif((1 <= x <= 7 and 0 <= y <= 5 ) or (2 <= x <= 6 and 2 <= y <= 6)):
		return "midRange"
	else:
		return "threePt"


def isOnPlayer(tup, data):
	if(data.playerTurn == 2):
		for player in data.players[1].players:
			if(player.x == tup[0] and player.y == tup[1]):
				return True
		
	else:
		for player in data.players[data.playerTurn].players:
			if(player.x == tup[0] and player.y == tup[1]):
				return True
	return False

def getPlayer(tup, data):
	if(data.playerTurn == 2):
		for player in data.players[0].players:
			if(player.x == tup[0] and player.y == tup[1]):
				return player

	else:
		for player in data.players[data.playerTurn].players:
			if(player.x == tup[0] and player.y == tup[1]):
				return player
	return None

def getPlayerWithBall(data):
	for player in data.players[0].players:
		if(player.hasBall):
			return player
	return None

def playGameRedrawAll(canvas, data):
	
	drawCourt(canvas, data)
	drawSideMenu(canvas, data)

	pass



def drawSideMenu(canvas, data):
	modes = ["Move Players", "Pass Ball"]
	playType = ["Offense", "Defense"]
	realShot = ["Off", "On"]
	canvas.create_text(925, 20, text=("%d - %d" %(data.score[data.players[0].name], data.score[data.players[1].name])), font = ('Comic Sans MS', 15, 'italic'))
	canvas.create_text(1025, 20, text=("Turns Left: %d" %data.maxTurn), font = ('Comic Sans MS', 12, 'italic'))
	if(data.playerTurn == 0):
		canvas.create_text(975 , 100, text = ("Current Play Mode: %s" %(modes[data.gameMode])), font = ('Comic Sans MS', 12, 'italic'))
		canvas.create_rectangle(975 - 40, 150 - 20, 975 + 40, 150 + 20, fill = "grey")

		canvas.create_text(975, 150, text="Toggle", font = ('Comic Sans MS', 15, 'italic'))



		canvas.create_text(850, 200, text=("Passes Left: %d" %(data.maxPass)), font = ('Comic Sans MS', 15, 'italic'))
		canvas.create_text(1100, 200, text=("Real Shots Left: %d" %(data.maxShots[0])), font = ('Comic Sans MS', 15, 'italic'))
		canvas.create_text(975, 225, text=("Real Shot: %s" %(realShot[data.realShot])), font = ('Comic Sans MS', 12, 'italic'))
		canvas.create_rectangle(975-200, 250, 975+200, 550, fill="grey")

		for i in range(len(data.moves)):
			if(data.moves[i][0] == "Pass"):
				canvas.create_text(975, 30 * (i+1)+ 250, text = ("%s %ses to %s" %(data.moves[i][1].name, data.moves[i][0], data.moves[i][2].name)), font = ('Comic Sans MS', 10, 'italic'))
			else:
				canvas.create_text(975, 30 * (i+1)+ 250, text = ("%s %ss a %s" %(data.moves[i][1].name, data.moves[i][0], getShotType(data))), font = ('Comic Sans MS', 10, 'italic'))
	
	if(data.playerTurn != 2):
		canvas.create_text(975,60, text = ("%s are on %s" %(data.players[data.playerTurn].name, playType[data.playerTurn])), font = ('Comic Sans MS', 12, 'bold italic'))
	
	if(data.playerTurn == 2):
		
		canvas.create_rectangle(975-200, 250, 975+200, 550, fill="grey")

		for i in range(len(data.moves)):
			if(data.moves[i][0] == "Pass"):
				if(not data.moveChances[i]):
					
					canvas.create_text(975, 30 * (i+1)+ 250, text = ("Pass is stolen:%f success" %(calculatePercentage(data.moves[i], data))), font = ('Comic Sans MS', 10, 'italic'))
					break
				else:
					canvas.create_text(975, 30 * (i+1)+ 250, text = ("%s %ses to %s:%f success" %(data.moves[i][1].name, data.moves[i][0], data.moves[i][2].name,calculatePercentage(data.moves[i], data))), font = ('Comic Sans MS', 10, 'italic'))

			else:
				wIn = ["missed", "made"]
				if(not bool(data.realShot) and not data.moveChances[i]):
					
					canvas.create_text(975, 30 * (i+1)+ 250, text = ("Shot Missed:%f success" %(calculatePercentage(data.moves[i], data))), font = ('Comic Sans MS', 10, 'italic'))
				elif(bool(data.realShot)):
					canvas.create_text(975, 30 * (i+1)+ 250, text = ("Shot %s" %(wIn[int(data.wentIn)])), font = ('Comic Sans MS', 10, 'italic'))
				else:
					canvas.create_text(975, 30 * (i+1)+ 250, text = ("%s makes a %s:%f success" %(data.moves[i][1].name, getShotType(data),calculatePercentage(data.moves[i], data))), font = ('Comic Sans MS', 10, 'italic'))

				
	


	canvas.create_rectangle(975-50, 575 - 20, 975 + 50, 575 + 20, fill="green")
	canvas.create_text(975, 575, text="Finish", font = ('Comic Sans MS', 10, 'italic'))


def drawCourt(canvas, data):
	for i in range(9):
		canvas.create_line(75 * (i+1), 0 , 75 * (i+1), data.height - 50)
	for i in range(8):
		canvas.create_line(0 , 75 * (i+1),  data.width//2 + 75, 75 * (i+1))

	canvas.create_line(75, 0, 75, 75*5, width= 5)
	canvas.create_line(600 , 0, 600 , 75*5, width= 5)

	curvePoints = [(75, 75*5),(150, 75*7), (75 * 7, 75 * 7),(600 , 75 * 5)]
	canvas.create_line(curvePoints, smooth = True, width = 5)

	canvas.create_line(75 * 3, 0, 75 * 3, 75*4, width= 5)
	canvas.create_line(450 , 0, 450 , 75*4, width= 5)
	canvas.create_line(75 * 3, 75 * 4, 450, 75 * 4, width = 5)

	curvePts = [(75 * 3, 75 * 4),(75 * 4.5, 75 * 6),(450, 75 * 4)]
	canvas.create_line(curvePts, smooth = True, width = 5)
	if(data.highlightedCell != None):
		canvas.create_rectangle(data.highlightedCell[0] * data.cellDim, (data.highlightedCell[1]) * data.cellDim, (data.highlightedCell[0]+1) * data.cellDim, (data.highlightedCell[1]+1) * data.cellDim, fill = "yellow")
	loadPlayersOnCourt(canvas, data)

def loadPlayersOnCourt(canvas, data):
	
	
	if(data.playerTurn != 2):
		if(data.firstInstance):
			for i in range(len(data.players[data.playerTurn].players)):

				player = data.players[data.playerTurn].players[i]
				
				canvas.create_image(5 + data.cellDim * i, data.cellDim * 7, anchor = NW, image = player.gamePic)
				if(i == 0 and data.playerTurn == 0):
					player.hasBall = True
					canvas.create_image(5 + data.cellDim * i, data.cellDim * 7, anchor = NW, image = data.ball)
					drawStaminaBar(canvas, data, player)
				player.x = i
				player.y = 7
			data.firstInstance = False
		else:
			for player in data.players[data.playerTurn].players:
				canvas.create_image(5 + data.cellDim * player.x, data.cellDim * player.y, anchor = NW, image = player.gamePic)
				drawStaminaBar(canvas, data, player)
				if(player.hasBall and data.playerTurn == 0):
					canvas.create_image(data.cellDim * player.x, data.cellDim * player.y, anchor = NW, image = data.ball)
	else:
		for i in range(len(data.players)):
			for player in data.players[i].players:
				if(i == 1):
					canvas.create_rectangle(data.cellDim * player.x, data.cellDim * player.y, data.cellDim * (player.x + 1), data.cellDim * (player.y+ 1), fill = "blue")
				
				canvas.create_image(5 + data.cellDim * player.x, data.cellDim * player.y, anchor = NW, image = player.gamePic)
				if(player.hasBall):
					canvas.create_image(data.cellDim * player.x, data.cellDim * player.y, anchor = NW, image = data.ball)
				drawStaminaBar(canvas, data, player)
def drawStaminaBar(canvas, data, player):
	if(player.stamina >= 0):
		canvas.create_rectangle(data.cellDim * player.x + 5, data.cellDim * (player.y+1) - 10, data.cellDim * player.x + data.cellDim*player.stamina/100 - 5, data.cellDim * (player.y+1 )-5, fill = "red")

def gameOverRedrawAll(canvas, data):
	winner = 0
	for key in data.score:
		if(data.score[key] >= winner):
			winner = data.score[key]

	
	winningTeam = ""
	for key in data.score:
		if(data.score[key] == winner):
			winningTeam = key
	
	if(data.score[data.players[0].name] == data.score[data.players[1].name]):
		canvas.create_text(600, 100, text=("Tie Game!"), font = ('Comic Sans MS', 15, 'italic'))
	else:
		canvas.create_text(600, 100, text=("%s won the game!" %winningTeam), font = ('Comic Sans MS', 15, 'italic'))
	canvas.create_text(600, 200, text=("%d - %d" %(data.score[data.players[0].name], data.score[data.players[1].name])), font = ('Comic Sans MS', 15, 'italic'))
	canvas.create_text(300, 270, text=("Player"), font = ('Comic Sans MS', 10, 'italic'))
	canvas.create_text(350, 240, text=("%s" %data.players[0].name), font = ('Comic Sans MS', 10, 'italic'))
	canvas.create_text(400, 270, text=("Points Scored"), font = ('Comic Sans MS', 10, 'italic'))
	canvas.create_text(800, 270, text=("Player"), font = ('Comic Sans MS', 10, 'italic'))
	canvas.create_text(850, 240, text=("%s" %data.players[1].name), font = ('Comic Sans MS', 10, 'italic'))
	canvas.create_text(900, 270, text=("Points Scored"), font = ('Comic Sans MS', 10, 'italic'))
	
	for i in range(len(data.players[0].players)):
		canvas.create_text(300, (i+1)*30 + 300, text=("%s" %(data.players[0].players[i].name)), font = ('Comic Sans MS', 10, 'italic'))
		canvas.create_text(400, (i+1)*30 + 300, text=("%d" %(data.players[0].players[i].scored)), font = ('Comic Sans MS', 10, 'italic'))
	for i in range(len(data.players[1].players)):
		canvas.create_text(800, (i+1)*30 + 300, text=("%s" %(data.players[1].players[i].name)), font = ('Comic Sans MS', 10, 'italic'))
		canvas.create_text(900, (i+1)*30 + 300, text=("%d" %(data.players[1].players[i].scored)), font = ('Comic Sans MS', 10, 'italic'))

	canvas.create_text(600, 500, text=("Press r to restart" ), font = ('Comic Sans MS', 20, 'italic'))


def movePlayerOverlap(data, p1):

	dirs = [(0, -1),(1, -1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
	for i in range(0, 5):
		for tups in dirs:
			if(not isOnPlayer((p1.x+i*tups[0],p1.y + i*tups[1]), data)
			and not isOnTeammate((p1.x+i*tups[0],p1.y + i*tups[1], p1), data)
			 and 0 <= p1.x+i*tups[0] < 9 and 0 <= p1.y + i*tups[1] < 8):

				p1.x += i * tups[0]
				p1.y += i * tups[1]

				return
def isOnTeammate(tup, data):
	for player in data.players[0].players:
			if(player.x == tup[0] and player.y == tup[1] and tup[2].name != player.name):
				return True
	return False

def resetHasBall(data):
	for i in range(2):
		for player in data.players[i].players:
			player.hasBall = False

def getXY(event, data):
	if(0 <= event.x <= 675):
		if(0 <= event.y <= 600):
			return event.x // data.cellDim, event.y // data.cellDim
	return None
	pass


def calculatePercentage(tup, data):
	typeP = tup[0]
	player1 = tup[1]
	player2 = None
	if(len(tup) == 3):
		player2 = tup[2]
	if(typeP == "Shoot"):
		shotType = getShotType(data)
		if(shotType == "inside"):
			if(findClosestPlayer(player1, data) != None):
				p2, dist = findClosestPlayer(player1, data)
				offBallPlayers = offBallEffect(player1, p2, data)
				offBalleffect = 0
				if(offBallPlayers != None):
					for i in offBallPlayers:
						offBalleffect += .15/i[1] * i[0].offBallD
				chance = (player1.stamina/100 * player1.inside - .55/dist * (p2.onBallD) - offBalleffect)/100
				if(chance < 0):
					chance = 0.01
				return chance
			else:
				return player1.stamina/100 * player1.inside/100
		elif(shotType == "midRange"):
			if(findClosestPlayer(player1, data) != None):
				p2, dist = findClosestPlayer(player1, data)
				offBallPlayers = offBallEffect(player1, p2, data)

				offBalleffect = 0
				if(offBallPlayers != None):
					for i in offBallPlayers:
						offBalleffect += .15/i[1] * i[0].offBallD

				chance = (player1.stamina/100 * player1.midRange - .55/dist * (p2.onBallD) - offBalleffect)/100
				if(chance < 0):
					chance = 0.01
				return chance
			else:
				return player1.stamina/100 * player1.midRange/100
		else:
			if(findClosestPlayer(player1, data) != None):
				p2, dist = findClosestPlayer(player1, data)
				offBallPlayers = offBallEffect(player1, p2, data)

				offBalleffect = 0
				if(offBallPlayers != None):
					for i in offBallPlayers:
						offBalleffect += .1/i[1] * i[0].offBallD

				chance = (player1.stamina/100 * player1.threePt - .6/dist * (p2.onBallD) - offBalleffect)/100
				if(chance < 0):
					chance = 0.01
				return chance
			else:
				return player1.stamina/100 * player1.threePt/100
	else:
		dirs = [(0, -1),(1, -1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
		path = getPassPath(player1, player2, data)
		playerEffect = []
		for player in data.players[1].players:
			for i in range(1,3):
				for tup in dirs:
					if((player.x + i * tup[0], player.y + i * tup[1]) in path):
						playerEffect.append((player, i))
		totalEff = 0
		if(playerEffect != []):
			for tup in playerEffect:
				totalEff += .05/tup[1] * tup[0].steal
			return (player1.passingAcc - totalEff)/100
		else:
			return player1.passingAcc/100
		pass
		#
	

def getPassPath(p1, p2, data):
	top = (p2.y - p1.y)
	bottom = (p2.x - p1.x)
	move2 = max(abs(top),abs(bottom))
	startX = p1.x
	startY = p1.y
	path = []
	move = math.gcd(abs(top), abs(bottom))
	top1 = abs(top)// move
	bottom1 = abs(bottom) // move
	if(top <= 0 and bottom >= 0):
		for i in range(move):
			#print(top1, bottom1)
			for i in range(abs(bottom1)):
				startX += 1
				path.append((startX, startY))
			for i in range(abs(top1)):
				startY -= 1
				path.append((startX, startY))
	elif(top >= 0 and bottom >= 0):
		for i in range(move):
			for i in range(abs(bottom1)):
				startX += 1
				path.append((startX, startY))
			for i in range(abs(top1)):
				startY += 1
				path.append((startX, startY))
	elif(top <= 0 and bottom < 0):
		for i in range(move):
			for i in range(abs(bottom1)):
				startX -= 1
				path.append((startX, startY))
			for i in range(abs(top1)):
				startY -= 1
				path.append((startX, startY))
	else:
		for i in range(move):
			for i in range(abs(bottom1)):
				startX -= 1
				path.append((startX, startY))
			for i in range(abs(top1)):
				startY += 1
				path.append((startX, startY))
	return path
		




def findClosestPlayer(p1, data):
	dirs = [(0, -1),(1, -1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
	bestPlayer = None
	bestI = 5
	for player in data.players[1].players:
		for i in range(1,3):
			for tup in dirs:
				if(player.x + i * tup[0] == p1.x and player.y + i * tup[1] == p1.y):
					if(i < bestI):
						bestI = i
						bestPlayer = player
	if(bestPlayer == None):
		return None
	return bestPlayer, bestI

def offBallEffect(p1, p2, data):
	dirs = [(0, -1),(1, -1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
	effects = []
	for player in data.players[1].players:
		for i in range(1,4):
			for tup in dirs:
				if(player.x + i * tup[0] == p1.x and player.y + i * tup[1] == p1.y 
					and (player.x != p2.x or player.y != p2.y)):
					
					effects.append((player, i))
	return effects







#ball stuff, live action

def ballInit(data):
    # load data.xyz as appropriate
    player = getPlayerWithBall(data)
    dist = getDistance(player.x, player.y, 4, 0)
    far = data.width - 300 - 125 * dist
    if(far < 0):
    	far = 10
    data.bball = Ball(far , 500)
    data.startX = data.bball.cx + 20
    data.startY = data.bball.cy
    data.len = 150
    data.angle = math.radians(45)
    data.start = False
    data.accel = 5
    pass

def ballMousePressed(event, data):
    # use event.x and event.y
    
    

    pass

def ballKeyPressed(event, data):
    # use event.char and event.keysym
    if(event.char == "r"):
    	init(data)
    if(event.keysym == "Up"):
    	data.angle -= math.radians(5)
    if(event.keysym == "Down"):
    	data.angle += math.radians(5)
    if(event.keysym == "Left"):
    	data.len -= 5
    	if(data.len<0):
    		data.len = 0
    if(event.keysym == "Right"):
    	data.len += 5

    if(event.keysym == "space"):
    	data.bball.dx = data.len/4 * math.sin(data.angle)
    	data.bball.dy = -data.len/3 * math.cos(data.angle)

    	data.start = True


    pass

def ballTimerFired(data):
	data.bball.move(data)
	data.bball.collide(data)
	if(data.start):
		data.bball.dy += data.accel


	if(data.bball.dx == 0 and data.bball.dy != 0):
		data.timer += 1


	if(data.timer == 20):
		data.wentIn = True

	if(data.wentIn):
		if(getShotType(data) == "inside" or getShotType(data) == "midRange"):
			data.score[data.players[0].name] += 2
			play = getPlayerWithBall(data)
			play.scored += 2
		else:
			data.score[data.players[0].name] += 3
			play = getPlayerWithBall(data)
			play.scored += 3
		data.mode = "playGame"
		data.maxShots[0] -=1
	elif(data.bounces == 3 and not data.wentIn):
		data.mode = "playGame"
		data.maxShots[0] -=1

	



def ballRedrawAll(canvas, data):
    # draw in canvas
    data.bball.draw(canvas, data)
    drawBallCourt(canvas, data)
    if(not data.start):
    	drawArrow(canvas, data)
    pass


def drawBallCourt(canvas, data):
	canvas.create_line(1100, 200, 1110, data.height, fill="orange", width = 10)
	canvas.create_line(1000, 20, 1100, 200, width = 10, fill="orange")
	canvas.create_line(1000, 200, 1100, 200, width = 10, fill="orange")
	canvas.create_line(1000, 20, 1000, 200, width = 10, fill="orange")
	canvas.create_line(875,150,1000,150, width = 10, fill="orange")
	canvas.create_line(900,150,990,150,width=10, fill="black")


def drawArrow(canvas, data):
	canvas.create_line(data.startX+40, data.startY,40+ data.startX + math.sin(data.angle) * data.len, data.startY - math.cos(data.angle) * data.len, width = 10)









####################################
# use the run function as-is
# got it from course notes, graphics demo
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1200, 650)



		

