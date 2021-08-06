import tkinter as tk
from tkinter.constants import DISABLED, FALSE, NORMAL
from typing import Text
import BetterShadows as bsha
import math, random
from functools import partial

#Should probably include colour constants here


class MathMatch():
    def __init__(self):

        #Main window for game to be in
        window = tk.Tk()
        window.geometry('809x500')
        window.resizable(False,False)
        window.title('Math Match')
        window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file = 'assets/icon.png'))

        #Container to hold the other frames
        self.container = tk.Frame(window)
        self.container.pack(side = "top", fill = "both", expand = True)

        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        #Variables for results screen
        self.final_score = 300
        self.final_time = 0

        ##ORIGINAL FRAME SETUP

        #Initialize the array of frames
        # self.frames = {}


        # #Iterate through frames, initialize them and put them in array
        # for F in (MainMenu, HelpScreen, GameScreen):

        #     frame = F(container, self)
        #     self.frames[F] = frame

        #     frame.grid(row = 0, column = 0, sticky ="nsew")


        # #Make Main Menu the first frame to be seen
        self.frame = MainMenu(self.container, self)
        self.show_frame(ResultsScreen)

    #Function to show the desired frame
    def show_frame(self, F):
        self.frame.destroy()
        # frame = self.frames[cont]
        # frame.tkraise()
        self.frame = F(self.container, self)
        self.frame.grid(row = 0, column = 0, sticky ="nsew")


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
        tk.Frame.__init__(self, container, bg = '#E8E8E8')
        # self.grid_columnconfigure((0,1), weight = 1)

        #Container to hold the text
        self.text_container = tk.Frame(self, bg = '#E8E8E8', width = 800, height=500)
        self.text_container.grid(column = 0, row = 0, padx = 5, pady=(30,0))
        self.text_container.grid_rowconfigure(0, weight = 1)
        self.text_container.grid_columnconfigure(0, weight = 1)
        self.text_container.grid_propagate(False)

        #Create text widget
        self.text = tk.Text(self.text_container, bg = '#E8E8E8', height = 1, bd = 0, takefocus = 0, font = ("Open Sans Semibold","18"), fg = "black")
        self.text.grid(column = 0, row = 0, sticky = 'NESW', padx = (5,0))

        #Inset text
        help_text = open("assets/help.txt","r")
        self.text.insert('end', help_text.read())
        help_text.close()
        
        #Configure Text Widget
        self.text.configure(selectbackground=self.text.cget('bg'), selectforeground=self.text.cget('fg'))
        self.text.configure(state = tk.DISABLED)

        #Back Button
        self.back_button = bsha.BetterShadow(200, 100, self, "BACK")
        self.back_button.grid(row = 0, column = 0, pady = (310,0))
        self.back_button.button.configure(command = lambda : controller.show_frame(MainMenu))


#Main gameplay screen
class GameScreen(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container, bg = '#E8E8E8')
        self.grid_columnconfigure((0,1,2,3), weight = 1)

        #Create a back button
        self.back_button = bsha.BetterShadow(90, 40, self, "BACK")
        self.back_button.grid(row = 0, column = 0, pady = (2,0), padx=(2,0), sticky = "W")
        self.back_button.button.configure(command = lambda : controller.show_frame(MainMenu))
        #Create list of equations for the buttons to display
        self.eqs = []

        self.operations = ["add", "subtract","divide","multiply"]
        for i in range(4):
            x = random.randint(1,10) #Inclusive
            for i in range(2):
                self.eqs.append(self.algebra_create(random.choice(self.operations), x) + [False])
        random.shuffle(self.eqs)

        #Tuples in self.eqs are in the form of (Equation, X Value, Answered?)

        #Initialise buttons array
        self.buttons = []

        #Create 8 buttons
        for i in range(8):
            self.buttons.append(bsha.BetterShadow(190, 120, self, self.eqs[i][0]))
            self.buttons[i].grid(row = math.floor(i/4)+2, column = i%4)
            self.buttons[i].button.configure(command = partial(self.press,i, controller))

        #Initialise whether a button is pressed or not
        self.pressed = False

        #Create container to hold the text widget
        self.text_container = tk.Frame(self, bg = 'red', width = 800, height=190)
        self.text_container.grid(column = 0, row = 1, columnspan=8, pady=(0,10))

        self.text_container.grid_rowconfigure(0, weight = 1)
        self.text_container.grid_columnconfigure(0, weight = 1)
        self.text_container.grid_propagate(False)

        #Create text widget
        self.text = tk.Text(self.text_container, bg = '#E8E8E8', height = 1, bd = 0, takefocus = 0, font = ("Open Sans Semibold","56"), fg = "black")
        self.text.grid(column = 0, row = 0, sticky = 'NESW')
        self.text.insert('end', "Time: ")
        self.text.insert('end', "0", ("Time"))
        self.text.insert('end',"\nScore: ")
        self.text.insert('end', "0", ("Score"))
        self.text.configure(selectbackground=self.text.cget('bg'), selectforeground=self.text.cget('fg'))
        self.text.configure(state = tk.DISABLED)

        self.score = 0
        self.red_buttons = []
        self.matches = 0

        self.timer(0)

    #Function to change the displayed value of the score
    def change_score(self, increment):
        self.score += increment
        self.text.configure(state = tk.NORMAL)
        self.text.insert("Score.first", str(self.score), ("New_Score"))
        self.text.delete("Score.first", "Score.last")
        self.text.tag_add("Score","New_Score.first","New_Score.last")
        self.text.configure(state = tk.DISABLED)

    #Function to change the displayed value of the time
    def change_time(self, time):
        self.text.configure(state = tk.NORMAL)
        self.text.insert("Time.first", "{:.0f}".format(time), ("New_Time"))
        self.text.delete('Time.first', "Time.last")
        self.text.tag_add("Time","New_Time.first","New_Time.last")
        self.text.configure(state = tk.DISABLED)

    #Timer to run during gameplay
    def timer(self, passed = None):
        if passed is not None:
            self.passed = passed
        self.change_time(self.passed)
        self.passed = self.passed + 1
        self.timing = self.after(1000, self.timer)


    #Function to run when a button is clicked
    def press(self, idx, controller):
        if self.eqs[idx][2] == False:
            for button in self.red_buttons:
                self.buttons[button].button.configure(bg = "white")
            self.red_buttons = []

            if self.pressed == False:
                self.buttons[idx].button.configure(bg = '#F0F0F0')
                self.pressed = True
                self.button_down = idx
            elif self.pressed == True and self.button_down != idx:
                if self.eqs[idx][1] == self.eqs[self.button_down][1]: #If buttons have the same value
                    colour = '#03fc8c'
                    self.eqs[idx][2] = True
                    self.eqs[self.button_down][2] = True
                    if self.passed < 90:
                        self.change_score(101-self.passed)
                    else:
                        self.change_score(10)
                    self.matches += 1
                    if self.matches >= len(self.eqs)/2:
                        controller.show_frame(ResultsScreen)
                        self.update_results(controller, self.score,self.passed)
                        return
                else: 
                    colour = '#e32222'
                    self.change_score(-50)
                    self.red_buttons.extend([idx,self.button_down])
                
                self.buttons[idx].button.configure(bg = colour)
                self.buttons[self.button_down].button.configure(bg = colour)
                self.pressed = False

    #Function for creating the equations on the buttons
    def algebra_create(self, operation, x):
        if operation == "subtract":
            ans = random.randint(1,20-x) #Inclusive
            return([str(ans+x)+"−X="+str(ans), x])
        elif operation == "add":
            ans = random.randint(x+1,20) #Inclusive
            return([str(ans-x)+"+X="+str(ans), x])
        elif operation == "divide":
            ans = random.choice(list(range(2,math.floor(20/x)+1)))
            return([str(ans*x)+"÷X="+str(ans), x])
        elif operation == "multiply":
            num = random.choice(list(range(2,math.floor(20/x)+1)))
            return([str(num)+"×X="+str(num*x), x])

    def update_results(self, controller, score, time):
        controller.final_score = score
        controller.final_time = time
        controller.show_frame(ResultsScreen)
        

#The results that are displayed at the end of gameplay
class ResultsScreen(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container, bg = '#E8E8E8')
        self.grid_columnconfigure((0,1,2), weight = 1)
        self.grid_rowconfigure((0), weight = 1)

        #Container to hold the text
        self.text_container = tk.Frame(self, bg = 'red', width = 450, height=190)
        self.text_container.grid(column = 0, row = 0, columnspan = 2, pady=(50,0), padx=(30,0),sticky='WN')

        self.text_container.grid_rowconfigure(0, weight = 1)
        self.text_container.grid_columnconfigure(0, weight = 1)
        self.text_container.grid_propagate(False)

        #Create text widget
        self.text = tk.Text(self.text_container, bg = '#E8E8E8', height = 1, bd = 0, takefocus = 0, font = ("Open Sans Semibold","30"), fg = "black")
        self.text.grid(column = 0, row = 0, sticky = 'NESW')
        self.text.insert('end', "Final Score: " + str(controller.final_score) + " Points\nFinal Time: " + str(controller.final_time) + " Seconds")
        self.text.configure(selectbackground=self.text.cget('bg'), selectforeground=self.text.cget('fg'))
        self.text.configure(state = tk.DISABLED)

        #Leaderboard
        self.leaderboard_container = tk.Frame(self, bg = 'white', width = 280, height=450)
        self.leaderboard_container.grid(column = 2, row = 0, rowspan=3, padx=(10,10))
     
        self.leaderboard_container.grid_rowconfigure(0, weight = 1)
        self.leaderboard_container.grid_columnconfigure(0, weight = 1)
        self.leaderboard_container.grid_propagate(False)

        self.leaderboard = tk.Text(self.leaderboard_container, bg = "white", bd = 0, takefocus = 0, font = ("Open Sans Semiobld","18"), fg = "black")
        self.leaderboard.grid(column = 0, row = 0, sticky = "NESW")
        self.leaderboard.configure(selectbackground=self.leaderboard.cget('bg'), selectforeground=self.leaderboard.cget('fg'), state = tk.DISABLED)

        #Input
        self.input_b_container = tk.Frame(self, width = 330, height = 30)
        self.input_b_container.grid(column = 0, row = 1, columnspan=2,sticky='W', padx=(30,0))
        self.input_b_container.grid_rowconfigure(0, weight = 1)
        self.input_b_container.grid_columnconfigure(0, weight = 1)
        self.input_b_container.grid_propagate(False)

        self.input_b = tk.Entry(self.input_b_container, font = ("Open Sans Semibold","16"))
        self.input_b.grid(row=0,column=0, sticky= 'NESW')
        self.input_b_container.grid_propagate(False)

        #Submit Button
        self.enter_button_container = tk.Frame(self, width=120, height=30)
        self.enter_button_container.grid(column=0,row=1,columnspan=2,sticky='W',padx=(363,0))
        self.enter_button_container.grid_columnconfigure(0,weight=1)
        self.enter_button_container.grid_rowconfigure(0,weight=1)
        self.enter_button_container.grid_propagate(False)

        self.enter_button = tk.Button(self.enter_button_container,text = "SUBMIT", bg = 'white', relief = 'flat', bd = 0, font = ("Open Sans Semibold","22"),
                                      command= lambda : self.add_to_leaderboard(controller))
        self.enter_button.grid(column=0,row=0,sticky = "NESW")

        #Create two buttons
        self.play_button = bsha.BetterShadow(200, 100, self, "PLAY AGAIN")
        self.menu_button = bsha.BetterShadow(200, 100, self, "MAIN MENU")
        
        #Put each button in the right place
        for B in ((0,self.play_button), (1,self.menu_button)):
            B[1].grid(row=2,column=B[0],padx=(20,0),pady=50)
            B[1].grid_propagate(False)
        
        #Set button commands
        self.play_button.button.configure(command = lambda : controller.show_frame(GameScreen))
        self.menu_button.button.configure(command = lambda : controller.show_frame(MainMenu))

    def add_to_leaderboard(self, controller):
        #https://stackoverflow.com/questions/34061909/how-to-write-at-a-particular-position-in-text-file-without-erasing-original-cont
        s = self.input_b.get()
        f = open("leaderboard.txt", "r")
        f.seek(0)
        for i in range(10):
            linestart = f.tell()
            line = f.readline()
            if line == "":
                f.write(s+";"+str(controller.final_score)+";"+str(controller.final_time)+";\n")
                break
            elif int(line.split(';')[1]) <= controller.final_score:
                f.seek(linestart)
                f.write(s+";"+str(controller.final_score)+";"+str(controller.final_time)+";\n")
                break
        f.close()
        self.update_leaderboard()

    def update_leaderboard(self):
        self.leaderboard.configure(state = NORMAL)
        self.leaderboard.delete("1.0",'end')
        f = open("leaderboard.txt", "r")
        for i in range(10):
            l = f.readline()
            if l == "":
                break
            l = l.split(';')
            self.leaderboard.insert("end", str(l[0] + " " + l[1] + "pts " + l[2] + "s\n")) 
        self.leaderboard.configure(state = DISABLED)


MathMatch()
tk.mainloop()