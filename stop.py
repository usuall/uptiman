import time
import _thread  # New statement

import PySimpleGUI as sg

layout = [
    [sg.Button("loop", key="loop")],
    [sg.Button("break", key="break")]
]

window = sg.Window(
    "App",
    layout,
    location=(100, 300),
    margins=(0, 0),
    no_titlebar=False,
    alpha_channel=1,
    grab_anywhere=True,
    resizable=True,
    finalize=True,
    )

# FUNCTIONS
def loop_function():
    global stop                 # New statement
    x = 0
    
    print('stop00000 -->', stop)
    while x < 10 and not stop:  # New statement
        print('stop0-000 -->', stop)
        time.sleep(1)
        print(x)
        x += 1

# RUNNING LOOP
stop = False                    # New statement
print('stop1111 -->', stop)
while True:
    event, values = window.read(timeout=10)

    if event == "loop":
        stop = False    # New statement
        print('stop222 -->', stop)
        _thread.start_new_thread(loop_function, ()) # New statement

    if event == "break":
        stop = True             # New statement
        print('stop333 -->', stop)
        
    # closing program
    if event is None or event == "Exit":
        break

window.Close()