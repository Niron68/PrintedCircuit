from tkinter import *
from tkinter import filedialog
import os
from PrintedCircuit import *
from Graphe import *

class Window:
    
    def __init__(self, geometry = "1280x720", preview=(480, 360)):
        self.printed_circuit = ""
        self.reverse = True
        self.preview_size = preview
        self.window = Tk()
        self.window.geometry(geometry)
        self.window.title("PrintedCircuit")
        self.main_frame = Frame(self.window)
        self.init_input_frame()
        self.init_preview_frame()
        self.main_frame.pack()


    def init_input_frame(self):
        self.input_frame = Frame(self.main_frame)
        self.input_file_entry = Entry(self.input_frame)
        self.input_file_button = Button(self.input_frame, text="Browse", command=self.get_input_file)
        self.input_file_entry.grid(row=0, column=0)
        self.input_file_button.grid(row=0, column=1)
        self.input_frame.grid(row=0, column=0)


    def init_preview_frame(self):
        self.preview_frame = Frame(self.main_frame)
        self.label_side_preview = Label(self.preview_frame, text="SOUDURE")
        self.preview_canvas = Canvas(self.preview_frame, width = self.preview_size[0], height = self.preview_size[1], bg = "#000000")
        self.reverse_button = Button(self.preview_frame, text="reverse", command=self.reverse_canvas)
        self.label_side_preview.pack()
        self.preview_canvas.pack()
        self.reverse_button.pack()
        self.preview_frame.grid(column=0, row=1)


    def reverse_canvas(self):
        if self.printed_circuit != "":
            self.reverse = not self.reverse
            self.refresh_preview()


    def load_circuit(self, printed_circuit):
        self.printed_circuit = printed_circuit
        graphe = Graphe(printed_circuit.getRelativeCoord())
        self.refresh_preview()


    def refresh_preview(self):
        new_coord = self.printed_circuit.getCoordInCanvas(width=self.preview_size[0], height=self.preview_size[1], coord_list=self.printed_circuit.get_transformed_coord(-5), revert = self.reverse)
        new_corners = self.printed_circuit.getCoordInCanvas(width=self.preview_size[0], height=self.preview_size[1], coord_list=self.printed_circuit.get_transformed_coord(angle = -5, coord_list = self.printed_circuit.getCorner()), revert = not self.reverse)
        self.preview_canvas.delete("all")
        for coord in new_coord:
            self.preview_canvas.create_rectangle(coord*2, outline=("red" if coord not in new_corners else "lime"))
        self.label_side_preview['text'] = "SOUDURE" if self.reverse else "COMPOSANT"


    def get_input_file(self):
        filename = self.browse_file()
        self.input_file_entry.insert(END, filename)
        circuit = self.create_circuit_from_file(filename)
        if circuit != "":
            self.load_circuit(circuit)


    def create_circuit_from_file(self, filename):
        if os.path.exists(filename):
            coord_table = []
            with open(filename, 'r+') as f:
                origin_lines = f.readlines()
                coord_lines = [ line[1:] for line in origin_lines if line[0] == 'X']
                for line in coord_lines:
                    line_table = line.split('Y')
                    coord_table.append((float(line_table[0]), float(line_table[1])))
                f.close()
            return PrintedCircuit(coord_table)
        return ""


    def browse_file(self):
        return filedialog.askopenfilename()


    def mainloop(self):
        self.window.mainloop()
