#This code creates a Tower Defense game. So there is only one level.
#The circles created go from left to right, but I plan to add
#a path way that will make them move throughout the board
#You should be able to select "create tower" and then click on the board
#to where you want to place the tower - you shouldn't be able to place
#a tower on the board

#http://th07.deviantart.net/fs70/PRE/i/2012/281/c/f/tileable_old_school_video_game_grass_by_hhh316-d5h58bx.jpg 
#http://4.bp.blogspot.com/-yJaHgLdGDV0/Ua5FWLqdBgI/AAAAAAABHH8/W4hCVOKVBCg/s1600/TROPHY+MAN.gif You win
import copy
import math
import random
import os
from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
class towerDefense(EventBasedAnimationClass):
    def __init__(self):
        self.canvasWidth = 1100
        self.canvasHeight = 1000
        super(towerDefense, self).__init__(self.canvasWidth, self.canvasHeight)
        self.canvasWidth1 = 800
        self.levelNumber = 1
        self.startGameCounter = 15
        self.timerForEnemies = 0
        self.numRemoved = 0  
        self.inHelpScreen = False
        self.isGameOver = False
        self.gameWon = False
        self.totalEnemiesCreated = 0
        self.newlyCreatedEnemies = []
        self.showEnemyHealth = True
        self.numRemoved = 0
        self.projectileList = []
        self.score = 0
        self.timerForEnemies1 = 0
        self.selectedTowerForBuild = 1 #Select Tower on SideBar
        self.shootCount = 0
        self.countingGolds = 0

        

    def drawTowerPlacementList(self):
        self.towerPlacementList = []
        for row in xrange(self.rows):
            self.towerPlacementList += [[None]*self.cols]
        # print self.towerPlacementList
        # print "Tower Placement List"

    def startScreen(self):
        if self.gameStarted == False:
            #It works like ~~ Magic ~~ 
            self.canvas.create_image(self.canvasWidth/2, self.canvasHeight/2, image = self.background)
            self.canvas.create_rectangle(self.canvasWidth/3 - 100, self.canvasHeight/2 - 50,self.canvasWidth/3 + 100,
            self.canvasHeight/2 + 50, outline = "black" )
            self.canvas.create_text(self.canvasWidth/3, 
                self.canvasHeight/2, text = "Play", font = "Arial 26")
            self.canvas.create_rectangle(self.canvasWidth/2 + 100, self.canvasHeight/2 - 50,self.canvasWidth/2 + 300,
            self.canvasHeight/2 + 50, outline = "black" )
            self.canvas.create_text(self.canvasWidth/2 + 200, 
                self.canvasHeight/2, text = "Help", font = "Arial 26")
            self.canvas.create_text(self.canvasWidth/2,self.canvasHeight/6, text = "Ugly Tower Defense", fill = "grey", font = "Arial 60 bold")
            self.canvas.create_text(self.canvasWidth/2,self.canvasHeight/6 + 100, text = "Created By Will Sanders", fill = "grey", font = "Arial 60 bold")

    def displayMoney(self):
        #Called in redrawAll()
        if self.gameStarted == True:
            halfMargin = 50
            # self.canvas.create_text(self.canvasWidth1+100, 200, text = " Total Lives: %i" %
            #     self.totalLives, font = "Arial 26")
            self.canvas.create_text(self.canvasWidth1 + 150, self.canvasHeight/10,
                # 9*self.canvasHeight/10, 
                text = """Money Total: %i \nLives = %i \nEnemies = %i/%i \nScore = %i""" 
                 % (self.totalGold, self.totalLives, len(self.createEnemy), self.numberOfCircles,self.score), font = "Arial 26")
            if self.startGameCounter > 0 and self.gamePaused == False:
                self.canvas.create_text((self.canvasWidth1)/2, self.canvasHeight/10,
             text = "Time Until Level Start = %i" % self.startGameCounter, font = "Arial 30 bold")
            elif self.startGameCounter <= 0 and self.gamePaused == False:
                self.canvas.create_text((self.canvasWidth1)/2, self.canvasHeight/10,
             text = "Level Started!!!", font = "Arial 30 bold") 
            elif self.gamePaused == True and self.isGameOver == False:
                self.canvas.create_text((self.canvasWidth1)/2, self.canvasHeight/10,
             text = "Game Paused", font = "Arial 30 bold") 
            if self.isGameOver == False:
                self.canvas.create_text((self.canvasWidth1)/2, self.canvasHeight/10 - 50,
             text = "Level %i" % (self.levelNumber), font = "Arial 30 bold") 

            self.canvas.create_text((self.canvasWidth1 + 150), 300, text = "Press H for Help")

    def displayTowerSelection(self):
        if self.gameStarted == True:
            cellSize = self.cellSize
            self.canvas.create_text((17*self.canvasWidth)/20, self.canvasHeight/3 + 100 , text = "Pick a Tower", 
                font = "Arial 30 bold")
            self.canvas.create_text(850, 480, text = "Square Tower", font = "Arial 14 bold")
            self.canvas.create_rectangle(825, 500, 825+self.cellSize,500 + self.cellSize, fill = "black")
            self.canvas.create_oval(825 +self.cellSize/2 + cellSize/3,
             500 +self.cellSize/2 + cellSize/4, 825+self.cellSize/2 - cellSize/4,500 + self.cellSize/2 - cellSize/3, 
             fill = "pink")
            self.canvas.create_text(825, 580, 
                    text = """
            Cost: 100
            Damage: 1
            Radius = 60
                    """, font = "arial 12")
            #This is for the Circle Tower
            self.canvas.create_text(925, 493, text = "Oval Tower", font = "Arial 14 bold")
            self.canvas.create_oval(825 + 2*cellSize, 500, 825+3*cellSize,500 + self.cellSize, fill = "black")
            xMid = (825 + 2*cellSize + 825+3*cellSize)/2
            self.canvas.create_oval(xMid + 10,
             500 +self.cellSize/2 + cellSize/4, xMid - 10,500 + self.cellSize/2 - cellSize/3, 
             fill = "yellow")
            self.canvas.create_text(920, 570, 
                    text = """
            Cost: 300
            Damage: 1
            Radius = 100
            Slows Enemy
                    """, font = "arial 12")

            #Radius Tower
            self.canvas.create_text(1000, 480, text = "Radius Tower", font = "Arial 14 bold")
            self.canvas.create_rectangle(825 + 4*cellSize, 500, 825+5*self.cellSize,500 + self.cellSize, fill = "black")
            self.canvas.create_text(825+180, 500+20, text = "R", fill = "red")
            self.canvas.create_text(1000, 580, 
                    text = """
            Cost: 400
            Damage: 1
            Radius = 150
                    """, font = "arial 12")

        #Show Currently Selected Tower
            if 20 <= self.selectedCol <= 21 and 11 <= self.selectedRow <= 13:
                self.selectedTowerForBuild = 1

            elif 22 <= self.selectedCol <= 23 and 11 <= self.selectedRow <= 13:
                self.selectedTowerForBuild = 2

            elif 24 <= self.selectedCol <= 25 and 11 <= self.selectedRow <= 13:
                self.selectedTowerForBuild = 3

            if self.selectedTowerForBuild == 1:
                #Puts Square Tower in 
                self.canvas.create_rectangle(825 + 2*cellSize, 600, 825+3*cellSize,600 + self.cellSize, fill = "black")
                xMid = (825 + 2*cellSize + 825+3*cellSize)/2
                self.canvas.create_oval(xMid + 10,
                 600 +self.cellSize/2 + cellSize/4, xMid - 10,600 + self.cellSize/2 - cellSize/3, 
                 fill = "pink")
 
            elif self.selectedTowerForBuild == 2: 
                self.canvas.create_oval(825 + 2*cellSize, 600, 825+3*cellSize,600 + self.cellSize, fill = "black")
                xMid = (825 + 2*cellSize + 825+3*cellSize)/2
                self.canvas.create_oval(xMid + 10,
                 600 +self.cellSize/2 + cellSize/4, xMid - 10,600 + self.cellSize/2 - cellSize/3, 
                 fill = "yellow")

            elif self.selectedTowerForBuild == 3: 
                self.canvas.create_rectangle(825 + 2*cellSize, 600, 825+3*cellSize,600 + self.cellSize, fill = "black")
                self.canvas.create_text(825+100, 620, text = "R", fill = "red")

            else:
                self.selectedTowerForBuild = self.selectedTowerForBuild
            # print self.selectedTowerForBuild


    def drawHelpScreen(self):
        width = self.canvasWidth
        height = self.canvasHeight
        if self.inHelpScreen == True:
            self.canvas.create_rectangle(0, 0, 
                self.canvasWidth, self.canvasHeight, fill = "purple")
            self.canvas.create_text(width/2,height/10, text = "Help Screen", font = "Arial 36")
            self.canvas.create_text(width/2, height/2, text = """
                After clicking on Start Game, the game will create a path

                You can either click where to place a tower, or move the arrow keys
                On the right side, you can click on the tower under "Build a Tower" to select a different 
                tower to build

                Press "b" to build a tower once you move to the place by the path

                Enemies spawn after the Level Starts, and you lose a life 
                when the enemy reaches the end of the board

                Press R to Restart
                Press P to Pause

                The game will end after 4 Levels

                Good Luck

                Press H to Exit this menu and continue
                """, font = "Arial 20")


    def redrawAll(self):
        #called in OnTimerFired() EventBased
        self.canvas.delete(ALL)
        if self.gameWon == True: 
            self.drawWin()
        elif self.isGameOver == True:
            self.drawGameOver()
        elif self.inHelpScreen == False: 
            self.drawGame()
            self.drawEnemies()
            self.drawTowers()
            self.startScreen()
            self.displayMoney()
            self.drawClicker()
            self.displayTowerSelection()
            self.drawProjectiles()
        else:
            self.drawHelpScreen()

    def drawProjectiles(self):
        for projectile in self.projectileList:
            projectile.draw()

    def drawGame(self):
        #draws the background canvas green
        #called in reDrawAll()
        self.canvas.create_image(self.canvasWidth/2, self.canvasHeight/2, image = self.gameBackground)
        self.canvas.create_rectangle(0,0, self.canvasWidth1, self.canvasHeight, outline = "black")
        self.canvas.create_rectangle(self.canvasWidth1, 0, self.canvasWidth, self.canvasHeight, fill = "forest green")
        self.drawBoard()
    
    def drawBoard(self):
        #go through each row and col, and then call 
        #drawCell which will make black cell, then colored
        #Called in drawGame(self):
        self.boardCounter = 0
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                self.drawCell(self.canvas, row, col, color = self.board[row][col])

    def drawCell(self, canvas, row, col, color):
        #static method - black cell, and colored
        #called in drawBoard()
        count = 0 
        x0 = col*self.cellSize
        y0 = row*self.cellSize
        x1 = (col+1)*self.cellSize
        y1 = (row+1)*self.cellSize
        if count == 0: 
            rowStart = (y0+y1)/2
        if self.board[row][col] == 'brown':
            canvas.create_rectangle(x0,y0,x1 ,y1, fill = color)
            if col == 0 and self.boardCounter == 0:
                canvas.create_text((x0+x1)/2,(y0+y1)/2, text = "Start")
                self.boardCounter += 1
                count += 1

    def drawGameOver(self):
        width = self.canvasWidth
        height = self.canvasHeight
        self.canvas.create_image(self.canvasWidth/2, self.canvasHeight/2, image = self.gameOverPicture)
        self.canvas.create_text(self.canvasWidth/2, self.canvasWidth/2, 
            text = """Game Over
            Press R to Restart
            You Score was: %i
            GREAT JOB! But You Lost!
            """ % self.score, font = "Arial 36 bold") 


    def loadTowerDefenseBoard(self):
        self.board = []
        for row in xrange(self.rows):
            self.board += [['green']*self.cols]
        self.makePath()

    def makePath(self):
        #This creates the path
        rows,cols = self.rows,self.cols
        col = 0
        row = random.randint(4,rows-1)
        self.board[row][col] = "brown"
        dirs = [(-1,0),(0,1),(1,0)]
        self.path = [(row,col)]
        self.startRow = row
        self.startCol = col
        while (col < cols-1):
            (drow,dcol) = dirs[random.randint(0,2)]
            newRow,newCol = row+drow, col+dcol
            if rows/5 <= newRow < rows - 1 and (newRow,newCol) not in self.path:
                self.board[newRow][newCol] = "brown"
                row,col = newRow, newCol
                self.path.append((row,col))
        self.path.append((row,col+1))
        self.path.append((row,col+2))

    def initAnimation(self):
        self.background = PhotoImage(file ='StartBackground_converted.gif')
        self.gameBackground = PhotoImage(file ='grassField.gif')
        self.gameOverPicture = PhotoImage(file = 'EndGamePicture.gif')
        self.youWinPicture = PhotoImage(file = 'YouWin.gif')
        #This is called once
        if self.levelNumber == 1 and self.isGameOver == False:
            self.gameStarted, self.gamePaused = False, False
            self.rows, self.cols = 20, 20
            self.cellSize = self.canvasWidth1/self.rows
            self.selectedRow = self.rows/2
            self.selectedCol = self.cols/2
            self.totalLives = 25
            self.totalGold = 700
            self.numberOfTowers = 0
        self.createTowers = []
        self.projectileList = []
        self.drawTowerPlacementList()
        self.initLevel()
        
    def initLevel(self):
        self.loadTowerDefenseBoard() 
        self.createEnemy = []
        if self.levelNumber == 1: 
            self.numberOfCircles = 40
        elif self.levelNumber > 1: 
            self.numberOfCircles = random.randint(5*self.levelNumber,10*self.levelNumber)
            self.timerForEnemies = 0
            self.newlyCreatedEnemies = []


    def drawTowers(self):
        rows = self.rows
        cols = self.cols
        # print self.towerPlacementList
        #Need to save location on the thing and assign it to tower
        # print self.towerPlacementList
        for row in xrange(rows):
            for col in xrange(cols):
                t = self.towerPlacementList[row][col]
                towerType = type(t)
                if t != None and self.board[row][col] != 'brown': 
                
                    self.drawTowerCell(self.canvas, row, col, t, towerType)

    def drawTowerCell(self, canvas, row, col, t, towerType):
        #static method - black cell, and colored
        #called in drawBoard()
        #need to figure out how to Linked this to TOwerNumber
        cellSize = self.cellSize
        x0 = col*self.cellSize
        y0 = row*self.cellSize
        x1 = (col+1)*self.cellSize
        y1 = (row+1)*self.cellSize
        middleX = (x0 + x1)/2
        middleY = (y0 + y1)/2
        if towerType == Tower:
            canvas.create_rectangle(x0, y0, x1, y1, fill = "black")
            canvas.create_oval(x0 + cellSize/3, y0 + cellSize/4, x1 - cellSize/3, y1 - cellSize/3, fill = "pink")
            canvas.create_oval(middleX + t.shootRadius, middleY + t.shootRadius, 
                middleX - t.shootRadius, middleY - t.shootRadius, outline = "purple")
        elif towerType == circleTower:
            canvas.create_oval(x0, y0, x1, y1, fill = "black")
            canvas.create_oval(x0 + cellSize/3, y0 + cellSize/4, x1 - cellSize/3, y1 - cellSize/3, fill = "yellow")
            canvas.create_oval(middleX + t.shootRadius, middleY + t.shootRadius, 
                middleX - t.shootRadius, middleY - t.shootRadius, outline = "purple")
        elif towerType == radiusTower: 
            canvas.create_rectangle(x0, y0, x1, y1, fill = "black")
            canvas.create_text(middleX, middleY, text = "R", fill = "red")
            canvas.create_oval(middleX + t.shootRadius, middleY + t.shootRadius, 
                middleX - t.shootRadius, middleY - t.shootRadius, outline = "purple")


    def drawWin(self):
        width = self.canvasWidth
        height = self.canvasHeight
        self.canvas.create_image(self.canvasWidth/2, self.canvasHeight/2, image = self.youWinPicture)
        self.canvas.create_text(width/2, height/4, text = "You Win!", font = "Arial 40 bold")

    def drawEnemies(self):
        for circle in self.createEnemy:
            if circle.isCircle == True:
                self.canvas.create_oval(circle.xStart + circle.radius, circle.yStart + circle.radius,
                    circle.xStart - circle.radius, circle.yStart - circle.radius, fill = "blue")
            elif circle.isCircle == False:
                self.canvas.create_rectangle(circle.xStart + circle.radius, circle.yStart + circle.radius,
                    circle.xStart - circle.radius, circle.yStart - circle.radius, fill = "blue")
            
    def onTimerFired(self):
        if self.gameStarted == True and self.gamePaused == False:
            if self.timerForEnemies1%10 == 0 and self.startGameCounter >= 1: 
                self.startGameCounter -= 1
            elif (self.startGameCounter == 0 and self.timerForEnemies % 5 == 0 and 
                (len(self.newlyCreatedEnemies) != self.numberOfCircles)):
                    self.creatingEnemiesRolls()
        if self.levelNumber == 5 and self.totalLives > 0:
            self.gameWon = True
        elif self.gameStarted == True and self.gamePaused == False and self.startGameCounter == 0:
            self.fireProjectiles()
            lenProjectileList = len(self.projectileList)
            numProjectilesRemoved = 0
            for pi in xrange(lenProjectileList):
                projectile = self.projectileList[pi - numProjectilesRemoved]
                if projectile.target not in self.createEnemy:
                    self.projectileList.pop(pi - numProjectilesRemoved)
                    numProjectilesRemoved += 1
            for circle in self.createEnemy:
                circle.move()
            self.shootEnemies()
            self.checkEnemyFinish()
            self.timerForEnemies += 1
            self.shootCount +=1
        if self.gamePaused == False:
            self.timerForEnemies1 += 1
        self.checkEnemiesLeft()

    def fireProjectiles(self):
        projectilesRemoved = 0
        lenProjectileList = len(self.projectileList)
        for pi in xrange(lenProjectileList):
            projectile = self.projectileList[pi - projectilesRemoved]
            projectile.move()
            l = len(self.createEnemy)
            numRemoved = 0
            for i in xrange(l):
                c = self.createEnemy[i-numRemoved]
                hit = projectile.hit(c)
                if hit: 
                    # remove from list
                    self.projectileList.pop(pi - projectilesRemoved)
                    projectilesRemoved += 1
                    c.health -= 1
                    if c.health <= 0:
                        if type(c) == Circle:
                            self.totalGold += 50
                            self.score += 50
                        elif type(c) == Square:
                            self.totalGold += 50
                            self.score += 50
                        elif type(c) == BiggerSquare:
                            self.totalGold += 500
                            self.score += 500
                        self.createEnemy.pop(i-numRemoved)
                        self.numRemoved += 1

                    break
    def creatingEnemiesRolls(self):
        #Called in OnTimerFired()
        roll = random.randint(0,1)
        bossRoll = random.randint(0,10)
        if roll == 0:
            newEnemy = Circle(len(self.newlyCreatedEnemies), self.startRow, self.startCol, self.cellSize, self.path)
        if roll == 1:
            newEnemy = Square(len(self.newlyCreatedEnemies), self.startRow, self.startCol, self.cellSize, self.path)
        if bossRoll == 5:
            newEnemy = BiggerSquare(len(self.newlyCreatedEnemies), self.startRow, self.startCol, self.cellSize, self.path)
        self.createEnemy += [newEnemy]
        self.newlyCreatedEnemies += [newEnemy]
        self.createEnemyCopy = copy.deepcopy(self.createEnemy)

    def checkEnemyFinish(self):
        #Needs to be similar to when enemy is destroyed after shooting
        l = len(self.createEnemy)
        if l > 0:
            numRemoved = 0
            self.createEnemyCopy = copy.deepcopy(self.createEnemy)
            for i in xrange(l):
                circle = self.createEnemy[i-numRemoved]
                if circle.xStart >= self.canvasWidth1:
                    self.createEnemy.pop(i-numRemoved)
                    numRemoved += 1
                    self.totalLives -= 1
                if self.totalLives <= 0:
                    print "Game Over?"
                    self.gamePaused = not self.gamePaused
                    self.isGameOver = True

    def displayGameStarted(self, canvas):
        self.canvas.create_text(self.canvasWidth/2, self.canvasHeight/2, 
            text = "LEVEL %i STARTED!" % (self.levelNumber))

    def checkEnemiesLeft(self):
        if len(self.createEnemy) == 0 and self.numberOfCircles == len(self.newlyCreatedEnemies):
            self.totalGold += 200*self.levelNumber
            self.levelNumber += 1
            self.initAnimation()
            self.startGameCounter = 15

    def shootEnemies(self):
        self.countedSlow = 0
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                t = self.towerPlacementList[row][col] 
                if t != None:
                    #If a tower is in that space, check to see if enemy near
                    self.createEnemyCopy = copy.deepcopy(self.createEnemy)
                    self.numRemoved = 0
                    for i in xrange(len(self.createEnemyCopy)):
                        c = self.createEnemy[i-self.numRemoved]
                        tx0 = col*self.cellSize
                        ty0 = row*self.cellSize
                        tx1 = (col+1)*self.cellSize
                        ty1 = (row+1)*self.cellSize
                        x1 = c.xStart #Circle x
                        y1 = c.yStart #Circle y point
                        x2 = (tx1 + tx0)/2 #Middle of Tower X
                        y2 = (ty0 + ty1)/2
                        distanceBetween = (((x1 - x2)**2)+(y1 - y2)**2)**0.5
                        if distanceBetween <= t.shootRadius and self.shootCount%5 == 0:
                            if type(t) == circleTower and self.timerForEnemies1%10:
                                c.speed = 2
                                c.health -= 0.25
                            newProjectile = Projectile(x2,y2,x1,y1,self.canvas,c)
                            self.projectileList.append(newProjectile)
                            break

    def onKeyPressed(self, event):
        if event.keysym == 's':
            self.gameStarted = True
        if self.gameStarted == True or self.inHelpScreen == True:
            if event.keysym == 'p':
                self.gamePaused = not self.gamePaused
            elif event.keysym == 'h':
                self.inHelpScreen = not self.inHelpScreen
                self.gamePaused = not self.gamePaused
            elif event.keysym == 'r':
                self.__init__()
                self.initAnimation()

            elif event.keysym == 'b':
                row = self.selectedRow
                col = self.selectedCol
                self.buildTowers()
                
            self.moveRectangle(event)


    def buildTowers(self):
        #also need a condition so it cannot be placed on the path
        if (self.towerPlacementList[self.selectedRow][self.selectedCol] == None and 
            self.totalGold >= 100 and self.selectedTowerForBuild == 1): 
            # self.towerPlacementList[row][col] != self.) :
            self.towerPlacementList[self.selectedRow][self.selectedCol] = Tower(self.numberOfTowers)
            self.totalGold -= 100
            # print self.towerPlacementList
            self.numberOfTowers += 1
            #could call a new function to build a new tower
        elif (self.towerPlacementList[self.selectedRow][self.selectedCol] == None and 
            self.totalGold >= 200 and self.selectedTowerForBuild == 2): 
            self.towerPlacementList[self.selectedRow][self.selectedCol] = circleTower(self.numberOfTowers)
            #Builds Oval Tower
            self.totalGold -= 200
            self.numberOfTowers += 1
        elif (self.towerPlacementList[self.selectedRow][self.selectedCol] == None and 
            self.totalGold >= 500 and self.selectedTowerForBuild == 3): 
            #Oval Tower
            self.towerPlacementList[self.selectedRow][self.selectedCol] = radiusTower(self.numberOfTowers)
            self.totalGold -= 500
            self.numberOfTowers += 1


    def moveRectangle(self, event):
        #This moves your guys around to build Towers
        if event.keysym == 'Left' and self.selectedCol > 0:
            self.selectedCol -= 1
        elif event.keysym == 'Right' and self.selectedCol < self.cols -1:
            self.selectedCol += 1
        elif event.keysym == 'Down' and self.selectedRow < self.rows - 1:
            self.selectedRow += 1
        elif event.keysym == 'Up' and self.selectedRow > 0:
            self.selectedRow -= 1
    
    def drawClicker(self):
        #Called in reDrawAll()
        if self.gameStarted == True and self.selectedRow <= 20 and self.selectedCol <= 19:
            reducedCell = 8
            x0 = reducedCell+self.cellSize*(self.selectedCol) 
            y0 = reducedCell+self.cellSize*(self.selectedRow) 
            x1 = self.cellSize*(self.selectedCol+1) - reducedCell
            y1 = self.cellSize*(self.selectedRow+1) - reducedCell
            self.canvas.create_rectangle(x0,y0,x1,y1, outline = "black")

    def onMousePressed(self, event):
        if self.gameStarted == False: 
            self.clickedX = event.x
            self.clickedY = event.y
            # print self.clickedX, self.clickedY
            if ((self.canvasWidth/2 + 100 <=self.clickedX <= self.canvasWidth/2 + 300) and 
                self.canvasHeight/2 - 50 <= self.clickedY <= self.canvasHeight/2 + 50):
                self.inHelpScreen = True
            elif ((self.canvasWidth/3 - 100 <= self.clickedX <= self.canvasWidth/3 + 100) and 
                self.canvasHeight/2 - 50 <= self.clickedY <= self.canvasHeight/2 +50):
                self.gameStarted = True
        elif self.gameStarted == True: 
            self.selectedCol = event.x/self.cellSize
            self.selectedRow = event.y/self.cellSize


            #Add feature that when scroll over tower, see upgrade option, sell option, stats option

class Enemies(object):
    def __init__(self, circleNumber,row,col,cellSize,path):
        self.radius = 5 
        self.health = 5
        self.xStart = int((col+0.5)*cellSize) 
        #cellSize self.canvasWidth/self.rows 500/25 = 
        self.yStart = int((row+0.5)*cellSize)
        self.reachedEnd = False
        self.circleNumber = circleNumber
        self.xVelocity = 1
        self.yVelocity = 0
        self.path = path
        self.cellSize = cellSize
        self.speed = 5
        self.isCircle = True
        self.isSquare = False

    def __repr__(self):
        #Need this 
        return 'Circle(%s)' % (self.circleNumber)

    def move(self):
        row = self.yStart/self.cellSize
        col = self.xStart/self.cellSize
        x = int((col+0.5)*self.cellSize)
        y = int((row+0.5)*self.cellSize)
        if (self.xStart == x and self.yStart == y):
            i = self.path.index((row,col))
            nextRow,nextCol = self.path[i+1]
            self.xVelocity = (nextCol - col)*self.speed
            self.yVelocity = (nextRow - row)*self.speed
        self.xStart += self.xVelocity
        self.yStart += self.yVelocity

class Square(Enemies):
    def __init__(self,circleNumber,row,col,cellSize,path):
        super(Square, self).__init__(circleNumber,row,col,cellSize,path)
        self.health = 2
        self.speed = 8
        self.isCircle = False
        self.isSquare = True
        self.isBiggerSquare = False

class BiggerSquare(Enemies):
    def __init__(self,circleNumber,row,col,cellSize,path):
        super(BiggerSquare, self).__init__(circleNumber,row,col,cellSize,path)
        self.health = 25
        self.speed = 4
        self.isCircle = False
        self.isBiggerSquare = True
        self.isSquare = True
        self.radius = 15

class Circle(Enemies):
    def __init__(self,circleNumber,row,col,cellSize,path):
        super(Circle, self).__init__(circleNumber,row,col,cellSize,path)
        self.health= 6
        self.speed = 4
        self.isCircle = True
   
class Tower(object):
    def __init__(self, towerNumber):
        self.towerSize = 20
        self.health = 10
        self.xStart = 10
        #should be on a click to place this
        self.yStart = 10
        #should be on a click to make both the x,y coordinates
        self.towerNumber = towerNumber
        self.shootRadius = 60
        self.shootFrequency = 3

    def __repr__(self):
        #Need this 
        return 'Tower(%s)' % (self.towerNumber)

class circleTower(Tower):
    def __init__(self, towerNumber):
        super(circleTower, self).__init__(towerNumber)
        self.towerRadius = 25
        self.shootRadius = 75


class radiusTower(Tower):
    def __init__(self, towerNumber):
        super(radiusTower, self).__init__(towerNumber)
        self.shootRadius = 100

class Projectile(object):
    def __init__(self, x1, y1, x2, y2, canvas, target):
        self.x = x1
        self.y = y1
        self.destX = target.xStart
        self.destY = target.yStart
        self.missleSpeed = 8
       # self.towerXStart = towerStart
        self.missleRadius = 2
        self.canvas = canvas
        self.r = 5
        self.target = target

    def move(self):
        self.destX = self.target.xStart
        self.destY = self.target.yStart
        dx = self.destX - self.x
        dy = self.destY - self.y

        distToTarget = (dx**2 + dy**2)**0.5
        if distToTarget == 0: return
        scale = float(self.missleSpeed)/distToTarget

        self.x += dx*scale
        self.y += dy*scale

    def draw(self):
        r,x,y = self.r,self.x,self.y
        self.canvas.create_oval(x-r,y-r,x+r,y+r,fill="red")

    def hit(self,circle):
        d = ((self.x - circle.xStart)**2 + (self.y - circle.yStart)**2)**0.5
        return d < (circle.radius + self.r)



t = towerDefense()

t.run()



