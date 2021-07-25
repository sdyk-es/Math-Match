import tkinter as tk


class BetterShadow(tk.Frame):
    def __init__(self, width, height, parent, text):
        tk.Frame.__init__(self, parent, width = width+5, height = height+5, bg = "RED", borderwidth=0)

        #Prepare images 
        self.bottom = tk.PhotoImage(file="assets/Shadows/Shadow2.gif")
        self.side = tk.PhotoImage(file="assets/Shadows/SideShadow2.gif")
        self.sidetop = tk.PhotoImage(file="assets/Shadows/SideShadowTop2B.gif")
        self.bottomedge = tk.PhotoImage(file="assets/Shadows/ShadowEdge2B.gif")
        self.corner = tk.PhotoImage(file="assets/Shadows/ShadowCorner2.gif")


        #Set Up Main Inner Frame
        inframe = tk.Frame(self, width = width, height = height, bg = "WHITE", borderwidth=0)
        inframe.grid(row = 0, column = 0, sticky = "", rowspan = int(height/5), columnspan = int(width/5))
        inframe.grid_propagate(False)

        inframe.grid_rowconfigure(0, weight = 1)
        inframe.grid_columnconfigure(0, weight = 1)

        #Put Shadow Images In Outer Frame
        tk.Label(self, image = self.bottomedge, width = 5, height = 5, bd = 0).grid(row = int(height/5+1), column = 0)
        for i in range(int(width/5-1)):
            tk.Label(self, image = self.bottom, width = 5, height = 5, bd = 0).grid(row = int(height/5+1), column = i+1)

        tk.Label(self, image = self.sidetop, width = 5, height = 5, bd = 0).grid(row = 0, column = int(width/5+1))
        for i in range(int(height/5)-1):
            tk.Label(self, image = self.side, width = 5, height = 5, bd = 0).grid(row = i+1, column = int(width/5+1))

        tk.Label(self, image = self.corner, width = 5, height = 5, bd = 0).grid(row = int(height/5+1), column = int(width/5+1))

        #Add Text To Frame
        self.button = tk.Button(inframe, text = text, bg ='white', font = ("Open Sans Semibold","24"), borderwidth=0)
        self.button.grid(row = 0, column = 0, sticky = 'nesw')
        self.button.grid_propagate(False)