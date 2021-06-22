import tkinter as tk
import BetterShadows as bsha
import math
from functools import partial

class MathMatch():
    def __init__(self):

        #Main window for game to be in
        window = tk.Tk()
        window.geometry('809x500')
        window.resizable(False,False)
        window.title('Math Match')

        #Container to hold the other frames
        container = tk.Frame(window)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)


        #Initialize the array of frames
        self.frames = {}


        #Iterate through frames, initialize them and put them in array
        for F in (MainMenu, HelpScreen, GameScreen):

            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")


        #Make Main Menu the first frame to be seen
        self.show_frame(MainMenu)


    #Function to show the desired frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


#Main menu and the frame the game starts up with
class MainMenu(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container, bg='#E8E8E8') #F8F8F8 #E1E1E1 ##E8E8E8

        #Configure columns
        self.grid_columnconfigure((0,1,2), weight = 1)

        #Create three buttons
        self.play_button = bsha.BetterShadow(200, 100, self, "PLAY")
        self.help_button = bsha.BetterShadow(200, 100, self, "HELP")
        self.quit_button = bsha.BetterShadow(200, 100, self, "QUIT")
        
        #Put each button in the right place
        for B in ((0,self.play_button), (1,self.help_button), (2,self.quit_button)):
            B[1].grid(row=1,column=B[0],padx=10,pady=50)
            B[1].grid_propagate(False)
        
        #Set button commands
        self.play_button.button.configure(command = lambda : controller.show_frame(GameScreen))
        self.help_button.button.configure(command = lambda : controller.show_frame(HelpScreen))
        self.quit_button.button.configure(command = quit)

        #Create title object
        self.titleimage = tk.PhotoImage(file = 'assets/Titles/Title-Montserrat-Blue.png')
        self.title = tk.Label(self, image = self.titleimage, width = 800, height = 100, bg = '#E8E8E8')
        self.title.grid(row = 0, column = 0, columnspan=3, pady=50)


#Help menu frame, currently only here for testing
class HelpScreen(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container, bg = 'green')


#Main gameplay screen
class GameScreen(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container, bg = '#E8E8E8')
        
        self.buttons = []

        for i in range(8):
            self.buttons.append(bsha.BetterShadow(100, 100, self, str(i)))
            self.buttons[i].grid(row = math.floor(i/4), column = i%4)
            self.buttons[i].button.configure(command = partial(self.colour,i))

        


    def colour(self, index):
        self.buttons[index].button.configure(bg = 'green')
        



MathMatch()
tk.mainloop()