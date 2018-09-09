import tkinter as tk
import time
from tkinter import font as tkfont

gui = tk.Tk()
gui.geometry("800x600")
c = tk.Canvas(gui ,width=800 ,height=600)
c.pack()

normal_font = tkfont.Font(size=12)
bold_font = tkfont.Font(family="Arial", size=12, weight="bold")

c.create_text(50,50, text="This is normal", font=normal_font)
c.create_text(50,100, text="This is bold", font=bold_font)

gui.mainloop()