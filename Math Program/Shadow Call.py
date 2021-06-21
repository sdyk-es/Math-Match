import tkinter as tk
import ShadowLabels as sha


#Configure Root Window
root = tk.Tk()
root.geometry('500x600')
root.configure(bg = '#F8F8F8')


label_1 = sha.ShadowLabel(300, 100, root, "Label 1")
label_1.shadow_label.grid(row=0,column=0,padx=100,pady=100)
label_1.shadow_label.grid_propagate(False)

label_2 = sha.ShadowLabel(300, 200, root, "Label 2")
label_2.shadow_label.grid(row=2,column=0)
label_2.shadow_label.grid_propagate(False)


tk.mainloop()