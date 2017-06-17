from Tkinter import *
import tkFileDialog as filedialog
import tkMessageBox as mb
import os
import os.path
##from PIL import Image, ImageTk
import Read
import PreProcess

app=Tk()
app.title("Ass4 Data Mining")
app.geometry("720x380+290+150")



img = Image.open('miner.png')
tkimage = ImageTk.PhotoImage(img)
myvar=Label(app,image = tkimage)
myvar.place(x=-140, y=60, relwidth=1, relheight=1)

# command for browser button
def openBrowser():
    browseTextEntry.delete(0,END)
    result=filedialog.askdirectory()
    browseTextEntry.insert(0,result)


# command for bulid button
def bulidClick():
    path=browseTextEntry.get()
    trainExists=os.path.isfile(path+"/train.csv")
    testExists=os.path.isfile(path+"/test.csv")
    structureExists=os.path.isfile(path+"/structure.txt")
    if(trainExists and testExists and structureExists):
        trainEmpty=os.stat(path+"/train.csv").st_size==0
        testEmpty=os.stat(path+"/test.csv").st_size==0
        structureEmpty=os.stat(path+"/structure.txt").st_size==0
        if (not trainEmpty and not structureEmpty and not trainEmpty):
            beginBuild(path)
        else:
            error="There Are Some Empty Files:\n"
            if(not trainEmpty):
                error+="train.csv is empty!\n"
            if(not testEmpty):
                error+="test.csv is empty!\n"
            if(not structureEmpty):
                error+="structure.txt is empty!\n"
            mb.showinfo('Files Error',error)

    else:
        error="There Are Some Missing Files:\n"
        if(not trainExists):
            error+="train.csv not exist!\n"
        if(not testExists):
            error+="test.csv not exist!\n"
        if(not structureExists):
            error+="structure.txt not exist!\n"
        mb.showinfo('Files Error',error)

def beginBuild(path):
    read=Read.Read(path)
    structure=read.readStructure()
    train=read.readTrain()
    preProcess=PreProcess.PreProcess(structure,train)
    preProcess.fillNA()


## Spacing - Row Zero
app.grid_rowconfigure(0, minsize=70)
Label(app,text="Data Mining - Ass4", font=32).grid(row=0, column=1, padx=10, pady=10)

##  Browse Region - First Grid Row
app.grid_columnconfigure(0, minsize=180)
BrowseLabel = Label(app,text="Directory Path:").grid(row=1, column=0, padx=10, pady=10, sticky=E)


browseTextEntry = Entry(app, width=45 )
browseTextEntry.grid(row=1, column=1, padx=0, pady=10, sticky=W)

browseButton = Button(app, text="Browse", width=10,command=openBrowser).grid(row=1, column=2,padx=8, pady=10)

## Bins Region - Second Grid Row
app.grid_rowconfigure(2, minsize=60)
binsLabel = Label(app,text="Discretization Bins:").grid(row=2, column=0, padx=10, pady=10,sticky=E)

binsTextEntry = Entry(app, width=10)
binsTextEntry.grid(row=2, column=1, padx=0, pady=10, sticky=W)

## Build  Region - Third Grid Row
BuildButton = Button(app, text="Build", width=20,command = bulidClick).grid(row=3, column=1, padx=12, pady=15)

## Classify Region = Fourth Grid Row
classifyButton = Button(app, text="Classify", width=20).grid(row=4, column=1, padx=10, pady=0)

app.mainloop()
