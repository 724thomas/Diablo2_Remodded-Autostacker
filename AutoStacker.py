import tkinter as tk
from tkinter import ttk
import threading
import win32api, win32con
import keyboard
import time
from PIL import ImageGrab, ImageOps
from numpy import *

# Global variables
running = False
inventory_cords, diff, cube_button_cords = (1877, 542),65.5,(997, 1044)

def NleftClick(x, y, a):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(a)

def trainColorGrab(cords):
    box = (cords)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

def qol_stack(inventory_cords, diff, cube_button_cords):
    global running
    try:
        while running:
            col = int(entry1.get())
            row = int(entry2.get())
            if keyboard.is_pressed('+'):
                keyboard.press_and_release('u')
                x, y = inventory_cords
                time.sleep(0.3)
                keyboard.press("ctrl")
                for i in range(col):
                    for j in range(row):
                        item = trainColorGrab(((x - 5) + (i * diff), (y - 5) + (j * diff), (x + 5) + (i * diff), (y + 5) + (j * diff)))
                        if item >= 500:
                            NleftClick(int(x + (i * diff)), int(y + (j * diff)), 0.05)
                            NleftClick(*cube_button_cords, 0.05)
                keyboard.release("ctrl")
                keyboard.press_and_release('esc')
    except ValueError:
        label_result.config(text="Please enter valid integers")

def on_resolution_selected(event):
    global inventory_cords, diff, cube_button_cords
    resolution_coordinates = {
        "2560x1440": [(1877, 542),65.5,(997, 1044)],
        "1920x1080": [(1416, 410), 49, (757, 790)],
        "1600x900": [(1180, 341), 40.8, (632, 657)],
        "1366x768": [(1008, 292), 34.6, (539, 562)],
        "1280x720": [(944, 273), 32.4, (504, 525)]
    }
    selected_resolution = resolution_var.get()
    inventory_cords, diff, cube_button_cords = resolution_coordinates[selected_resolution]

def start_qol_stack():
    global running
    running = True
    thread = threading.Thread(target=qol_stack, args=(inventory_cords, diff, cube_button_cords))
    thread.start()

def stop_qol_stack():
    global running
    running = False

def open_instructions_window():
    instruction_window = tk.Toplevel(root)
    instruction_window.title("Instructions")
    instructions = """
    Storage Bag Autostacker Instruction:
    - 1: From top left corner of your inventory, write how many columns, rows of items to be stacked.
    - 2: Press "Start Qol Stack" button.
    - 3: Open up inventory and cube with only QOL storage bag inside cube.
    - 4: press "+" button on keyboard and wait.
    - 5: Repeatable with multiple "+" key presses.
    - 6: Press "Stop Qol Stack" to end.
    
    - Put's everything into cube. So be careful to include some items in col*row area.
    - Currently works only on listed resolutions.
    - Still few bugs.
    
    - dev: github.com/724thomas
    """
    tk.Label(instruction_window, text=instructions, justify=tk.LEFT, padx=10).pack()

root = tk.Tk()
root.title("Diablo2 ReMoDDeD")

resolutions = ["2560x1440","1920x1080", "1600x900", "1366x768", "1280x720"]
resolution_var = tk.StringVar()

resolution_dropdown = ttk.Combobox(root, textvariable=resolution_var, values=resolutions, state="readonly")
resolution_dropdown.pack()
resolution_dropdown.bind("<<ComboboxSelected>>", on_resolution_selected)
resolution_dropdown.current(0)  # Default to the first resolution in the list

label_col = tk.Label(root, text="Col:")
label_col.pack()
entry1 = tk.Entry(root)
entry1.pack()

label_row = tk.Label(root, text="Row:")
label_row.pack()
entry2 = tk.Entry(root)
entry2.pack()

button_start = tk.Button(root, text="Start Qol Stack", command=start_qol_stack)
button_start.pack()

button_stop = tk.Button(root, text="Stop Qol Stack", command=stop_qol_stack)
button_stop.pack()

instructions_button = tk.Button(root, text="About", command=open_instructions_window)
instructions_button.pack()

label_result = tk.Label(root, text="")
label_result.pack()

root.mainloop()
