from tkinter import *

class Window:
    
    def __init__(self, geometry = "1280x720", preview=(720, 480)):
        self.printed_circuit = ""
        self.reverse = True
        self.preview_size = preview
        self.window = Tk()
        self.window.geometry(geometry)
        self.window.title("PrintedCircuit")
        self.main_frame = Frame(self.window)
        self.label_side_preview = Label(self.main_frame, text="SOUDURE")
        self.preview_canvas = Canvas(self.main_frame, width = preview[0], height = preview[1], bg = "#000000")
        self.reverse_button = Button(self.main_frame, text="reverse", command=self.reverse_canvas)
        self.label_side_preview.pack()
        self.preview_canvas.pack()
        self.reverse_button.pack()
        self.main_frame.pack()


    def reverse_canvas(self):
        if self.printed_circuit != "":
            self.reverse = not self.reverse
            self.refresh_preview()


    def load_circuit(self, printed_circuit):
        self.printed_circuit = printed_circuit
        self.refresh_preview()


    def refresh_preview(self):
        new_coord = self.printed_circuit.getCoordInCanvas(width=self.preview_size[0], height=self.preview_size[1], revert = self.reverse)
        new_corners = self.printed_circuit.getCoordInCanvas(width=self.preview_size[0], height=self.preview_size[1], coord_list=self.printed_circuit.getCorner(), revert = not self.reverse)
        self.preview_canvas.delete("all")
        for coord in new_coord:
            self.preview_canvas.create_rectangle(coord*2, outline=("red" if coord not in new_corners else "lime"))
        self.label_side_preview['text'] = "SOUDURE" if self.reverse else "COMPOSANT"


    def mainloop(self):
        self.window.mainloop()
