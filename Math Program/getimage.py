import tkinter as tk
import os



def get_image(image):
  dir = os.path.dirname(__file__) # Gets the path of where the program is
  filename = os.path.join(dir, 'Images',str(image)) # Gets the path of where the images are stored.
  img = tk.PhotoImage(file=filename)
  return img

