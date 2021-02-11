from tkinter import *
from PrintedCircuit import *
from Window import *

coord_table = []

with open('origine.txt', 'r+') as f:
    origin_lines = f.readlines()
    coord_lines = [ line[1:] for line in origin_lines if line[0] == 'X']
    for line in coord_lines:
        line_table = line.split('Y')
        coord_table.append((float(line_table[0]), float(line_table[1])))
    f.close()

circuit = PrintedCircuit(coord_table=coord_table)

window = Window()
window.load_circuit(circuit)
window.mainloop()