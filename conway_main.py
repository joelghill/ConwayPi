from conway import *
from tkinter import *
from tkinter import messagebox
from threading import *
import time

width = 120
height = 80
conway = Conway(width, height)
running = False
waitTime = 5
cells = []
generation = 0

def on_closing():
	global running
	running = False
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
		root.destroy()
	else:
		running = True

def initializeCanvas(canvas, width, height):
	global conway
	global bitmap
	cellWidth = 600/width
	cellHeight = 400/height
	for j in range(height):
		for i in range(width):
			cells.append(canvas.create_rectangle(i*cellWidth+3, j*cellHeight+3, 
			(i+1)*cellWidth+3, (j+1)*cellHeight+3,
			fill='white',
			width = 0,
			activefill='lightblue'))
	
def refreshCanvas(con, canvas):
	global waitTime
	global running
	for index in range(len(con.changedCells)):
                changeIndex = con.changedCells[index]
                if(con.isCellAlive(changeIndex)):
                    if(canvas.itemcget(changeIndex+1, 'fill') != 'black'):
                        canvas.itemconfig(changeIndex+1, fill = 'black')
                else:
                    if(canvas.itemcget(changeIndex+1, 'fill') != 'white'):
                        canvas.itemconfig(changeIndex+1, fill = 'white')

	"""
	for index in range(len(con.data)):
		if(con.isCellAlive(index)):
			if(canvas.itemcget(index+1, 'fill') != 'black'):
				canvas.itemconfig(index+1, fill = 'black')
		else:
			if(canvas.itemcget(index+1, 'fill') != 'white'):
				canvas.itemconfig(index+1, fill = 'white')
	"""		
def clickCallback(event):
	global conway
	canvas = event.widget
	x = canvas.canvasx(event.x)
	y = canvas.canvasy(event.y)
	cell = canvas.find_closest(x, y)
	cellClick(canvas, cell[0])
	return
	
def cellClick(canvas, index):
	global conway
	if(conway.isCellAlive(index-1)):
		canvas.itemconfig(index, fill='white')
		conway.killCell(index-1)
	else:
		canvas.itemconfig(index, fill='black')
		conway.reviveCell(index-1)
		
def updateConway(conway, canvas):
	global running
	global waitTime
	if(running):
		conway.newGeneration()
		refreshCanvas(conway, canvas)
	root.after(waitTime, updateConway, conway, canvas)

def nextGeneration(conway, canvas):
	conway.newGeneration()
	refreshCanvas(conway, canvas)
	
def startButtonClick():
	global running
	if(running):
		running = False
		startButton['text'] = 'Start'
		nextButton['state'] = NORMAL
	else:
		running = True
		startButton['text'] = 'Stop'
		nextButton['state'] = DISABLED
		
root = Tk()
root.minsize(640,480)
main = Frame(root)

main.pack()

title = Label(main, text="Conway's Game of Life", font=("Helvetica", 16))
title.pack(side = TOP)

w = Canvas(main, width=600, height=400, bg='black')
initializeCanvas(w, width, height)
w.bind("<Button-1>", clickCallback)
w.pack(side=TOP)

controls = Frame(root)
controls.pack( side = BOTTOM )

startButton = Button(controls, text="Start", fg="black")
startButton['command'] = startButtonClick
startButton['state'] = NORMAL
startButton.pack( side = LEFT)

nextButton = Button(controls, text="Next")
nextButton['command'] =  lambda: nextGeneration(conway, w)
nextButton.pack(side = RIGHT)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.after(waitTime, updateConway, conway, w)
root.mainloop()
