from tkinter import *

class Window:
    
    def __init__(self, geometry = "1280x720", preview=(720, 480)):
        self.window = Tk()
        self.window.geometry(geometry)
        self.window.title("PrintedCircuit")
        self.main_frame = Frame(self.window)
        self.label_side_preview = Label(self.main_frame, text="SOUDURE")
        self.preview_canvas = Canvas(self.main_frame, width = preview[0], height = preview[1], bg = "#000000")
        self.reverse_button = Button(self.main_frame, text="reverse", command=self.reverse_canvas)


    def reverse_canvas(self):
        pass


    def mainloop(self):
        self.window.mainloop()
