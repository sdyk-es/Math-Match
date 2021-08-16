import tkinter as tk
import tkinter.messagebox
import BetterShadows as bsha
from tkinter.constants import DISABLED, FALSE, NORMAL
from functools import partial
import math
import random
import csv
import pyglet

# Colour Constants
BG_GREY = '#E8E8E8'
BUTTON_PRESSED = '#F0F0F0'
BUTTON_GREEN = '#03FC8C'
BUTTON_RED = '#E32222'

# Load Fonts
for font in ["OpenSans-SemiBold","OxygenMono-Regular"]:
    pyglet.font.add_file("assets/fonts/"+font+".ttf")

# Main Program Class
class MathMatch():
    def __init__(self):

        # Main window for game to be in
        window = tk.Tk()
        window.geometry('809x500')
        window.resizable(False, False)
        window.title('Math Match')
        window.tk.call('wm', 'iconphoto', window._w,
                       tk.PhotoImage(file='assets/icon.png'))

        # Container to hold the other frames
        self.container = tk.Frame(window)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Variables for results screen
        self.final_score = 0
        self.final_time = 0

        # Make Main Menu the first frame to be seen
        self.frame = MainMenu(self.container, self)
        self.show_frame(MainMenu)

    # Function to show the desired frame
    def show_frame(self, F):
        self.frame.destroy()
        self.frame = F(self.container, self)
        self.frame.grid(row=0, column=0, sticky="nsew")


# Main Menu
class MainMenu(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container, bg=BG_GREY)

        # Configure columns
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # Create three buttons
        self.play_button = bsha.BetterShadow(200, 100, self, "PLAY")
        self.help_button = bsha.BetterShadow(200, 100, self, "HELP")
        self.quit_button = bsha.BetterShadow(200, 100, self, "QUIT")

        # Put each button in the right place
        for B in ((0, self.play_button), (1, self.help_button),
                  (2, self.quit_button)):
            B[1].grid(row=1, column=B[0], padx=10, pady=50)
            B[1].grid_propagate(False)

        # Set button commands
        self.play_button.button.configure(command=lambda:
                                          controller.show_frame(GameScreen))
        self.help_button.button.configure(command=lambda:
                                          controller.show_frame(HelpScreen))
        self.quit_button.button.configure(command=quit)

        # Create title object
        title_location = 'assets/Titles/Title-Montserrat-Blue.png'
        self.titleimage = tk.PhotoImage(file=title_location)
        self.title = tk.Label(self, image=self.titleimage,
                              width=800, height=100, bg=BG_GREY)
        self.title.grid(row=0, column=0, columnspan=3, pady=50)


# Help Screen
class HelpScreen(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container, bg=BG_GREY)

        # Container to hold the text
        self.text_container = tk.Frame(self, bg=BG_GREY, width=800, height=500)
        self.text_container.grid(column=0, row=0, padx=5, pady=(30, 0))
        self.text_container.grid_rowconfigure(0, weight=1)
        self.text_container.grid_columnconfigure(0, weight=1)
        self.text_container.grid_propagate(False)

        # Create text widget
        self.text = tk.Text(self.text_container, bg=BG_GREY,
                            height=1, bd=0, takefocus=0,
                            font=("Open Sans Semibold", "18"), fg="black")
        self.text.grid(column=0, row=0, sticky='NESW', padx=(5, 0))

        # Insert text
        help_text = open("assets/help.txt", "r")
        self.text.insert('end', help_text.read())
        help_text.close()

        # Configure Text Widget
        self.text.configure(selectbackground=self.text.cget('bg'),
                            selectforeground=self.text.cget('fg'))
        self.text.configure(state=tk.DISABLED)

        # Back Button
        self.back_button = bsha.BetterShadow(200, 100, self, "BACK")
        self.back_button.grid(row=0, column=0, pady=(310, 0))
        self.back_button.button.configure(command=lambda:
                                          controller.show_frame(MainMenu))


# Main Gameplay Screen
class GameScreen(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container, bg=BG_GREY)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Create a back button
        self.back_button = bsha.BetterShadow(90, 40, self, "BACK")
        self.back_button.grid(row=0, column=0, pady=(2, 0), padx=(2, 0),
                              sticky="W")
        self.back_button.button.configure(command=lambda:
                                          controller.show_frame(MainMenu))

        # Create list of equations for the buttons to display
        self.eqs = []

        self.operations = ["add", "subtract", "divide", "multiply"]
        for i in range(4):
            x = random.randint(1, 10)  # Inclusive
            for i in range(2):
                op = random.choice(self.operations)
                self.eqs.append(self.algebra_create(op, x) + [False])
        random.shuffle(self.eqs)
        # Tuples in self.eqs are in the form of (Equation, X Value, Answered?)

        # Initialise buttons array
        self.buttons = []

        # Create 8 buttons
        for i in range(8):
            button = bsha.BetterShadow(190, 120, self, self.eqs[i][0])
            self.buttons.append(button)
            self.buttons[i].grid(row=math.floor(i/4)+2, column=i % 4)
            self.buttons[i].button.configure(command=partial(self.press, i,
                                                             controller))

        # Initialise variable to store whether any button is currently pressed
        self.pressed = False

        # Create container to hold the text widget
        self.text_container = tk.Frame(self, bg='white', width=800, height=190)
        self.text_container.grid(column=0, row=1, columnspan=8, pady=(0, 10))

        self.text_container.grid_rowconfigure(0, weight=1)
        self.text_container.grid_columnconfigure(0, weight=1)
        self.text_container.grid_propagate(False)

        # Create text widget
        self.text = tk.Text(self.text_container, bg=BG_GREY, height=1, bd=0,
                            takefocus=0, font=("Open Sans Semibold", "56"),
                            fg="black")
        self.text.grid(column=0, row=0, sticky='NESW')
        self.text.insert('end', "Time: ")
        self.text.insert('end', "0", ("Time"))
        self.text.insert('end', "\nScore: ")
        self.text.insert('end', "0", ("Score"))
        self.text.configure(selectbackground=self.text.cget('bg'),
                            selectforeground=self.text.cget('fg'))
        self.text.configure(state=tk.DISABLED)

        # Initialise miscellaneous variables
        self.score = 0
        self.red_buttons = []
        self.matches = 0

        # Begin timer
        self.timer(0)

    # Function to change the displayed value of the score
    def change_score(self, increment):
        self.score += increment
        self.text.configure(state=tk.NORMAL)
        self.text.insert("Score.first", str(self.score), ("New_Score"))
        self.text.delete("Score.first", "Score.last")
        self.text.tag_add("Score", "New_Score.first", "New_Score.last")
        self.text.configure(state=tk.DISABLED)

    # Function to change the displayed value of the time
    def change_time(self, time):
        self.text.configure(state=tk.NORMAL)
        self.text.insert("Time.first", "{:.0f}".format(time), ("New_Time"))
        self.text.delete('Time.first', "Time.last")
        self.text.tag_add("Time", "New_Time.first", "New_Time.last")
        self.text.configure(state=tk.DISABLED)

    # Timer to run during gameplay
    def timer(self, passed=None):
        if passed is not None:
            self.passed = passed
        self.change_time(self.passed)
        self.passed = self.passed + 1
        self.timing = self.after(1000, self.timer)

    # Function to run when a button is clicked
    def press(self, idx, controller):
        if self.eqs[idx][2] is False:
            for button in self.red_buttons:
                self.buttons[button].button.configure(bg="white")
            self.red_buttons = []

            if self.pressed is False:
                self.buttons[idx].button.configure(bg=BUTTON_PRESSED)
                self.pressed = True
                self.button_down = idx
            elif self.pressed is True and self.button_down != idx:
                # If buttons have the same value
                if self.eqs[idx][1] == self.eqs[self.button_down][1]:
                    colour = BUTTON_GREEN
                    self.eqs[idx][2] = True
                    self.eqs[self.button_down][2] = True
                    if self.passed < 90:
                        self.change_score(101-self.passed)
                    else:
                        self.change_score(10)
                    self.matches += 1
                    if self.matches >= len(self.eqs)/2:
                        controller.show_frame(ResultsScreen)
                        self.update_results(controller, self.score, self.passed)
                        return
                else:
                    colour = BUTTON_RED
                    self.change_score(-50)
                    self.red_buttons.extend([idx, self.button_down])

                self.buttons[idx].button.configure(bg=colour)
                self.buttons[self.button_down].button.configure(bg=colour)
                self.pressed = False

    # Function for creating the equations on the buttons
    def algebra_create(self, operation, x):
        if operation == "subtract":
            ans = random.randint(1, 20-x)  # Inclusive
            return([str(ans+x)+"−X="+str(ans), x])
        elif operation == "add":
            ans = random.randint(x+1, 20)  # Inclusive
            return([str(ans-x)+"+X="+str(ans), x])
        elif operation == "divide":
            ans = random.choice(list(range(2, math.floor(20/x)+1)))
            return([str(ans*x)+"÷X="+str(ans), x])
        elif operation == "multiply":
            num = random.choice(list(range(2, math.floor(20/x)+1)))
            return([str(num)+"×X="+str(num*x), x])

    # Function to update varaibles and display results screen
    def update_results(self, controller, score, time):
        controller.final_score = score
        controller.final_time = time
        controller.show_frame(ResultsScreen)


# Results Screen Displayed At End Of Gameplay
class ResultsScreen(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container, bg=BG_GREY)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0), weight=1)

        # Container to hold the text
        self.text_container = tk.Frame(self, bg='white', width=450, height=190)
        self.text_container.grid(column=0, row=0, columnspan=2, pady=(50, 0),
                                 padx=(30, 0), sticky='WN')

        self.text_container.grid_rowconfigure(0, weight=1)
        self.text_container.grid_columnconfigure(0, weight=1)
        self.text_container.grid_propagate(False)

        # Create text widget
        self.text = tk.Text(self.text_container, bg=BG_GREY, height=1, bd=0,
                            takefocus=0, font=("Open Sans Semibold", "29"),
                            fg="black")
        self.text.grid(column=0, row=0, sticky='NESW')
        self.text.insert('end', "Final Score: " + str(controller.final_score) +
                         " Points\nFinal Time: " + str(controller.final_time) +
                         " Seconds")
        self.text.configure(selectbackground=self.text.cget('bg'),
                            selectforeground=self.text.cget('fg'))
        self.text.configure(state=tk.DISABLED)

        # Leaderboard
        self.leaderboard_container = tk.Frame(self, bg='white',
                                              width=301, height=450)
        self.leaderboard_container.grid(column=2, row=0, rowspan=3,
                                        padx=(10, 10))

        self.leaderboard_container.grid_rowconfigure(0, weight=1)
        self.leaderboard_container.grid_columnconfigure(0, weight=1)
        self.leaderboard_container.grid_propagate(False)

        self.leaderboard = tk.Text(self.leaderboard_container, bg="white",
                                   bd=0, takefocus=0,
                                   font=("Oxygen Mono", "16"), fg="black")
        self.leaderboard.grid(column=0, row=0, sticky="NESW")
        self.leaderboard.configure(selectbackground=self.leaderboard.cget('bg'),
                                   selectforeground=self.leaderboard.cget('fg'),
                                   state=tk.DISABLED)

        # Input
        self.input_b_container = tk.Frame(self, width=330, height=30)
        self.input_b_container.grid(column=0, row=1, columnspan=2, sticky='W',
                                    padx=(30, 0))
        self.input_b_container.grid_rowconfigure(0, weight=1)
        self.input_b_container.grid_columnconfigure(0, weight=1)
        self.input_b_container.grid_propagate(False)

        self.input_b = tk.Entry(self.input_b_container,
                                font=("Open Sans Semibold", "16"))
        self.input_b.grid(row=0, column=0, sticky='NESW')
        self.input_b_container.grid_propagate(False)

        # Submit Button
        self.enter_button_container = tk.Frame(self, width=120, height=30)
        self.enter_button_container.grid(column=0, row=1, columnspan=2,
                                         sticky='W', padx=(363, 0))
        self.enter_button_container.grid_columnconfigure(0, weight=1)
        self.enter_button_container.grid_rowconfigure(0, weight=1)
        self.enter_button_container.grid_propagate(False)

        self.enter_button = \
            tk.Button(self.enter_button_container, text="SUBMIT", bg='white',
                      relief='flat', bd=0, font=("Open Sans Semibold", "22"),
                      command=lambda: self.add_to_leaderboard(controller))
        self.enter_button.grid(column=0, row=0, sticky="NESW")

        # Create two buttons
        self.play_button = bsha.BetterShadow(200, 100, self, "PLAY AGAIN")
        self.menu_button = bsha.BetterShadow(200, 100, self, "MAIN MENU")

        # Put each button in the right place
        for B in ((0, self.play_button), (1, self.menu_button)):
            B[1].grid(row=2, column=B[0], padx=(20, 0), pady=50)
            B[1].grid_propagate(False)

        # Set button commands
        self.play_button.button.configure(command=lambda:
                                          controller.show_frame(GameScreen))
        self.menu_button.button.configure(command=lambda:
                                          controller.show_frame(MainMenu))

        # Make sure leadeaerbord is shown when the screen first opens
        self.update_leaderboard()

        # Make submit button active
        self.enter_button.config(state=NORMAL)

    def add_to_leaderboard(self, controller):
        s = self.input_b.get()

        # Check for boundary cases
        if s.isalpha() is False:
            tk.messagebox.showerror("Invalid Name",
                                    "Name must only contain letters")
            return
        elif len(s) > 10:
            tk.messagebox.showerror("Invalid Name",
                                    "Name must be 10 characters or less")
            return

        # If boundary cases are passed, accept input and disable further entries
        self.enter_button.config(state=DISABLED)

        # Add entry to leaderboard data and sort it appropriately
        with open('leaderboard.csv', 'a+', newline='') as csvfile:
            csvfile.seek(0)
            reader = list(csv.reader(csvfile))+[[s, controller.final_score,
                                                controller.final_time]]
            sortedlist = sorted(reader, key=lambda elem: int(elem[1]),
                                reverse=True)

        # Write new leaderboard data back to the file
        with open('leaderboard.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i in range(min(len(sortedlist), 14)):  # Maximum of 14 entires
                writer.writerow(sortedlist[i])

        self.update_leaderboard()

    # Function to update displayed leaderboard
    def update_leaderboard(self):
        self.leaderboard.configure(state=NORMAL)
        self.leaderboard.delete("1.0", "end")  # Clear leaderboard
        self.leaderboard.insert("end",  "Leaderboard\n\n")  # Title

        # Write content of leaderboard file into text object
        with open("leaderboard.csv", "a+", newline='') as csvfile:
            csvfile.seek(0)
            reader = csv.reader(csvfile)
            for line in reader:
                s = str(line[1] + "pts " + str(line[2]) + "s\n")
                self.leaderboard.insert("end", str(line[0])+": " + s)

        self.leaderboard.configure(state=DISABLED)


if __name__ == "__main__":
    MathMatch()
    tk.mainloop()
