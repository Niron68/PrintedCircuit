from tkinter import *
from PrintedCircuit import *

coord_table = []
REVERSE = True

with open('origine.txt', 'r+') as f:
    origin_lines = f.readlines()
    coord_lines = [ line[1:] for line in origin_lines if line[0] == 'X']
    for line in coord_lines:
        line_table = line.split('Y')
        coord_table.append((float(line_table[0]), float(line_table[1])))
    f.close()

preview_width = 720
preview_height = 500

circuit = PrintedCircuit(coord_table)

corners = circuit.getCoordInCanvas(width=preview_width, height=preview_height, coord_list=circuit.getCorner(), revert = not REVERSE)

canvas_coord = circuit.getCoordInCanvas(width=preview_width, height=preview_height, revert = REVERSE)

def reverse_canvas():
    global REVERSE
    REVERSE = not REVERSE
    new_coord = circuit.getCoordInCanvas(width=preview_width, height=preview_height, revert = REVERSE)
    new_corners = circuit.getCoordInCanvas(width=preview_width, height=preview_height, coord_list=circuit.getCorner(), revert = not REVERSE)
    canvas.delete("all")
    for coord in new_coord:
        canvas.create_rectangle(coord*2, outline=("red" if coord not in new_corners else "lime"))
    label_sens['text'] = "SOUDURE" if REVERSE else "COMPOSANT"

window = Tk()

window.title("PrintedCircuit")
window.geometry("1280x720")

main_frame = Frame(window)

label_sens = Label(main_frame, text=("SOUDURE" if REVERSE else "COMPOSANT"))
label_sens.pack()

canvas = Canvas(main_frame, width = preview_width, height = preview_height, bg = "#000000")
for coord in canvas_coord:
    canvas.create_rectangle(coord*2, outline=("red" if coord not in corners else "lime"))
canvas.pack()

reverse_button = Button(main_frame, text="reverse", command=reverse_canvas)
reverse_button.pack()

main_frame.pack()

window.mainloop()