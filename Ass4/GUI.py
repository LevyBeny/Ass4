from Tkinter import *
import tkFileDialog as filedialog
import tkMessageBox as mb
import os
import os.path
##from PIL import Image, ImageTk
import Read
import PreProcess

class GUI(object):

    def __init__(self):
        self.__app=Tk()
        self.__app.title("Ass4 Data Mining")
        self.__app.geometry("720x380+290+150")

        self.__img = Image.open('miner.png')
        self.__tkimage = ImageTk.PhotoImage(self.__img)
        self.__myvar=Label(self.__app,image = self.__tkimage)
        self.__myvar.place(x=-140, y=60, relwidth=1, relheight=1)

        ## Spacing - Row Zero
        self.__app.grid_rowconfigure(0, minsize=70)
        Label(self.__app,text="Data Mining - Ass4", font=32).grid(row=0, column=1, padx=10, pady=10)

        ##  Browse Region - First Grid Row
        self.__app.grid_columnconfigure(0, minsize=180)
        self.__BrowseLabel = Label(self.__app,text="Directory Path:").grid(row=1, column=0, padx=10, pady=10, sticky=E)

        self.__browseTextEntry = Entry(self.__app, width=45 )
        self.__browseTextEntry.grid(row=1, column=1, padx=0, pady=10, sticky=W)

        self.__browseButton = Button(self.__app, text="Browse", width=10,command=self.__openBrowser).grid(row=1, column=2,padx=8, pady=10)

        ## Bins Region - Second Grid Row
        self.__app.grid_rowconfigure(2, minsize=60)
        self.__binsLabel = Label(self.__app,text="Discretization Bins:").grid(row=2, column=0, padx=10, pady=10,sticky=E)

        self.__binsTextEntry = Entry(self.__app, width=10)
        self.__binsTextEntry.grid(row=2, column=1, padx=0, pady=10, sticky=W)

        ## Build  Region - Third Grid Row
        self.__buildButton = Button(self.__app, text="Build", width=20,command = self.__bulidClick).grid(row=3, column=2, padx=12, pady=15)

        ## Classify Region = Fourth Grid Row
        self.__classifyButton = Button(self.__app, text="Classify", width=20,command = self.__classifyClick).grid(row=4, column=2, padx=10, pady=0)

        # fileds init
        self.__classifier=None # contains the classifier 
        self.__preProcess=None # contains the preProcess object
        self.__read=None # contains the read object

    # command for browser button
    def __openBrowser(self):
        self.__browseTextEntry.delete(0,END)
        result=filedialog.askdirectory()
        self.__browseTextEntry.insert(0,result)

    # command for bulid button
    def __bulidClick(self): 
        if (self.__checkInput()):
            self.__beginBuild(self.__browseTextEntry.get(),int(self.__binsTextEntry.get()))

    # command for classify button
    def __classifyClick(self):
        if (classifier==None):
            error="Make Sure To Build A Classifier Before Pressing The Classify Button!"
            mb.showinfo('Path Error',error)
            return

    # start buliding the classifier
    def __beginBuild(self,path,bins):

        # read the train
        self.__read=Read.Read(path)
        structure=self.__read.readStructure()
        train=self.__read.readTrain()
        
        if (len(train.index)<bins):
            error="Make Sure The Number Of Bins Is Smaller Then The Size Of The Train Set!"
            mb.showinfo('Bins Error',error)
            self.__read=None
            self.__preProcess=None
            return;


        # pre process
        self.__preProcess=PreProcess.PreProcess(structure)
        train=self.__preProcess.fillNA(train)
        train=self.__preProcess.discretizeTrain(bins,train)

        # update structure after pre process
        structure=self.__preProcess.getStructure()

        

    # check if the given variable is an integer
    def __isInt(self,s):
        try: 
            int(s)
            return True
        except ValueError:
            return False    
          
    # check the validlity of the given bins
    def __checkBins(self,bins):
        if (not self.__isInt(bins)):
            return False
        bins=int(bins)
        return (bins>0)

    # check the validlity of the input
    def __checkInput(self):
        path=self.__browseTextEntry.get()
        if (path==""):
            error="Make Sure You Entered A Directory Path!"
            mb.showinfo('Path Error',error)
            return False;

        bins=self.__binsTextEntry.get()
        if (bins==""):
            error="Make Sure You Entered The Number Of Bins!"
            mb.showinfo('Bins Error',error)
            return False;

        if (not self.__checkBins(bins)):
            error="Make Sure You Entered A Positive Integer In The Bins Text Box!"
            mb.showinfo('Bins Error',error)
            return False;
      
        trainExists=os.path.isfile(path+"/train.csv")
        testExists=os.path.isfile(path+"/test.csv")
        structureExists=os.path.isfile(path+"/structure.txt")
        if(trainExists and testExists and structureExists):
            trainEmpty=os.stat(path+"/train.csv").st_size==0
            testEmpty=os.stat(path+"/test.csv").st_size==0
            structureEmpty=os.stat(path+"/structure.txt").st_size==0
            if (not trainEmpty and not structureEmpty and not trainEmpty):
                return True
            else:
                error="There Are Some Empty Files In The Given Path:\n"
                if(not trainEmpty):
                    error+="train.csv is empty!\n"
                if(not testEmpty):
                    error+="test.csv is empty!\n"
                if(not structureEmpty):
                    error+="structure.txt is empty!\n"
                mb.showinfo('Files Error',error)
                return False
        else:
            error="There Are Some Missing Files In The Given Path:\n"
            if(not trainExists):
                error+="train.csv not exist!\n"
            if(not testExists):
                error+="test.csv not exist!\n"
            if(not structureExists):
                error+="structure.txt not exist!\n"
            mb.showinfo('Files Error',error)
            return False

    # starts the GUI
    def start(self):
        self.__app.mainloop()



