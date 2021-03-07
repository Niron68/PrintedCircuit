from tkinter import *
from tkinter import filedialog
import os
from PrintedCircuit import *

class Window:
    
    def __init__(self, geometry = "1280x720", preview=(480, 360)):
        self.printed_circuit = ""
        self.reverse = True
        self.preview_size = preview
        self.window = Tk()
        self.window.geometry(geometry)
        self.window.title("PrintedCircuit")
        self.main_frame = Frame(self.window)
        self.init_input_file_frame()
        self.init_preview_frame()
        self.init_input_frame()
        self.init_input_data_frame()
        self.main_frame.pack()


    def init_input_file_frame(self):
        self.input_file_frame = Frame(self.main_frame)
        self.input_file_button = Button(self.input_file_frame, text="Importer", command=self.get_input_file)
        self.input_file_button.pack()
        self.input_file_frame.grid(row=0, column=0)


    def init_preview_frame(self):
        self.preview_frame = Frame(self.main_frame)
        self.label_side_preview = Label(self.preview_frame, text="SOUDURE")
        self.preview_canvas = Canvas(self.preview_frame, width = self.preview_size[0], height = self.preview_size[1], bg = "#000000")
        self.reverse_button = Button(self.preview_frame, text="reverse", command=self.reverse_canvas)
        self.label_side_preview.pack()
        self.preview_canvas.pack()
        self.reverse_button.pack()
        self.preview_frame.grid(column=0, row=1)


    def init_input_frame(self):
        self.input_frame = Frame(self.main_frame)
        self.input_x_frame = Frame(self.input_frame)
        self.input_y_frame = Frame(self.input_frame)
        self.corner_label = Label(self.input_frame, text="Coins supérieur droit: ")
        self.input_x_label = Label(self.input_x_frame, text="X: ")
        self.input_y_label = Label(self.input_y_frame, text="Y: ")
        self.input_x_entry = Entry(self.input_x_frame)
        self.input_y_entry = Entry(self.input_y_frame)
        self.angle_label = Label(self.input_frame, text="Angle: 0")
        self.grandissement_label = Label(self.input_frame, text="Facteur de grandissement: 1")
        self.calculate_button = Button(self.input_frame, text="Calculer", command=self.calculate_angle)
        self.input_x_label.grid(row=0, column=0)
        self.input_x_entry.grid(row=0, column=1)
        self.input_y_label.grid(row=0, column=0)
        self.input_y_entry.grid(row=0, column=1)
        self.corner_label.pack()
        self.input_x_frame.pack()
        self.input_y_frame.pack()
        self.calculate_button.pack()
        self.angle_label.pack()
        self.grandissement_label.pack()
        self.input_frame.grid(row=0, column=1)


    def init_input_data_frame(self):
        self.input_data_frame = Frame(self.main_frame)
        self.input_move_speed_frame = Frame(self.input_data_frame)
        self.input_perf_speed_frame = Frame(self.input_data_frame)
        self.input_depth_frame = Frame(self.input_data_frame)
        self.file_path_frame = Frame(self.input_data_frame)
        self.input_move_speed_label = Label(self.input_move_speed_frame, text="Vitesse déplacement: ")
        self.input_perf_speed_label = Label(self.input_perf_speed_frame, text="Vitesse percage:          ")
        self.input_depth_label = Label(self.input_depth_frame, text="Profondeur:                 ")
        self.input_move_speed_entry = Entry(self.input_move_speed_frame)
        self.input_perf_speed_entry = Entry(self.input_perf_speed_frame)
        self.input_depth_entry = Entry(self.input_depth_frame)
        self.generate_button = Button(self.input_data_frame, text="Génerer", command=self.write)
        self.file_path_label = Label(self.file_path_frame, text="Sortie: ")
        self.file_path_entry = Entry(self.file_path_frame, state='normal', width=40)
        self.input_move_speed_label.grid(column=0, row=0)
        self.input_move_speed_entry.grid(column=1, row=0)
        self.input_perf_speed_label.grid(column=0, row=0)
        self.input_perf_speed_entry.grid(column=1, row=0)
        self.input_depth_label.grid(column=0, row=0)
        self.input_depth_entry.grid(column=1, row=0)
        self.file_path_label.grid(column=0, row=0)
        self.file_path_entry.grid(column=1, row=0)
        self.input_move_speed_frame.pack()
        self.input_perf_speed_frame.pack()
        self.input_depth_frame.pack()
        self.generate_button.pack()
        self.file_path_frame.pack()
        self.input_data_frame.grid(row=1, column=1)
        self.file_path_entry.bind('<1>', self.set_output)


    def reverse_canvas(self):
        if self.printed_circuit != "":
            self.reverse = not self.reverse
            self.refresh_preview()


    def load_circuit(self, printed_circuit):
        self.printed_circuit = printed_circuit
        self.corner_label['text'] = "Coins supérieur droit: " + str(printed_circuit.getCorner()[1])
        self.refresh_preview()


    def refresh_preview(self, angle = 0):
        new_coord = self.printed_circuit.getCoordInCanvas(width=self.preview_size[0], height=self.preview_size[1], coord_list=self.printed_circuit.get_transformed_coord(angle), revert = self.reverse)
        # new_corners = self.printed_circuit.getCoordInCanvas(width=self.preview_size[0], height=self.preview_size[1], coord_list=self.printed_circuit.get_transformed_coord(angle = angle, coord_list = self.printed_circuit.getCorner()), revert = not self.reverse)
        new_corners = self.printed_circuit.getCorner(new_coord)
        self.preview_canvas.delete("all")
        for coord in new_coord:
            self.preview_canvas.create_rectangle(coord*2, outline=("red" if coord not in new_corners else "lime"))
        self.label_side_preview['text'] = "SOUDURE" if self.reverse else "COMPOSANT"
        self.angle_label['text'] = "Angle: " + str(angle)


    def get_input_file(self):
        filename = Window.browse_file()
        circuit = self.create_circuit_from_file(filename)
        if circuit != "":
            self.load_circuit(circuit)


    def set_output(self, event = ''):
        path = filedialog.askdirectory()
        self.file_path_entry['state'] = 'normal'
        self.file_path_entry.delete(0, END)
        self.file_path_entry.insert(END, path)
        self.file_path_entry['state'] = 'disabled'


    def calculate_angle(self):
        x = float(self.input_x_entry.get())
        y = float(self.input_y_entry.get())
        point = (x, y)
        corners = self.printed_circuit.getCorner()
        angle = PrintedCircuit.get_angle(corners[0], corners[1], point)
        grandissement = PrintedCircuit.get_growth_factor(corners[0], corners[1], point)
        self.printed_circuit.update_attr(angle=angle, growth=grandissement)
        self.grandissement_label['text'] = "Facteur de grandissement: " + str(grandissement)
        self.refresh_preview(angle)


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


    def browse_file(event = ''):
        return filedialog.askopenfilename()


    def mainloop(self):
        self.window.mainloop()


    def generate_document(self):
        correct_coord = self.printed_circuit.get_correct_coord()
        move_speed = int(self.input_move_speed_entry.get())
        perf_speed = int(self.input_perf_speed_entry.get())
        depth = int(self.input_depth_entry.get())*(-1)
        res = "G94\nG1 Z1\n"
        for coord in correct_coord:
            res += "G1 X" + str(round(coord[0], 3)) + " Y" + str(round(coord[1], 3)) + " F" + str(move_speed) + ";\n"
            res += "G1 Z" + str(depth) + " F" + str(perf_speed) + "\n"
            res += "G1 Z1 F" + str(move_speed) + "\n"
        return res


    def write(self):
        filepath = self.file_path_entry.get()
        if os.path.exists(filepath):
            doc = self.generate_document()
            with open(filepath + '/resultat.txt', 'w') as f:
                f.write(doc)
                f.close()

