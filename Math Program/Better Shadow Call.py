import tkinter as tk
import BetterShadows as bsha


#Configure Root Window
root = tk.Tk()
root.geometry('500x600')
root.configure(bg = '#F8F8F8')

c = 0
def increment():
    global c
    c += 1
    label_2.button.configure(text = ('Print',c))

def printc():
    global c
    print(c)

label_1 = bsha.BetterShadow(300, 100, root, "Increment")
label_1.grid(row=0,column=0,padx=100,pady=100)
label_1.grid_propagate(False)

label_1.button.configure(command=increment)


label_2 = bsha.BetterShadow(300, 200, root, "Print 0")
label_2.grid(row=2,column=0)
label_2.grid_propagate(False)

label_2.button.configure(command=printc)


tk.mainloop()