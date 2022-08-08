import PySimpleGUI as sg

def main():
    layout = [  [sg.Text('My Window')],
                [sg.Combo([1,23,3,4,5], size=(10,5), key='-C-', enable_events=True)],
                [sg.Text(size=(12,1), key='-OUT-')],
                [sg.Button('Go'), sg.Button('Exit')]  ]

    window = sg.Window('Window Title', layout, finalize=True)
    #window['-C-'].bind('<KeyRelease>', 'KEY DOWN')

    while True:             # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '-C-KEY DOWN':
            window['-C-'].Widget.event_generate('<Down>')
    window.close()

if __name__ == '__main__':
    main()