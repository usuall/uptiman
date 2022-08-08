from tkhtmlview import html_parser
import PySimpleGUI as sg

def set_html(widget, html, strip=True):
    prev_state = widget.cget('state')
    widget.config(state=sg.tk.NORMAL)
    widget.delete('1.0', sg.tk.END)
    widget.tag_delete(widget.tag_names)
    html_parser.w_set_html(widget, html, strip=strip)
    widget.config(state=prev_state)

html = """
<td colspan="2" class="infobox-image"><a href="https://en.wikipedia.org/wiki/RoboCop" class="image">
<img alt="RoboCop (1987) theatrical poster.jpg" src="https://upload.wikimedia.org/wikipedia/en/thumb/1/16/RoboCop_%281987%29_theatrical_poster.jpg/220px-RoboCop_%281987%29_theatrical_poster.jpg" decoding="async" width="250" height="386" class="thumbborder" srcset="//upload.wikimedia.org/wikipedia/en/1/16/RoboCop_%281987%29_theatrical_poster.jpg 1.5x" data-file-width="248" data-file-height="374"></a>
<div class="infobox-caption" style="text-align:center">Directed by Paul Verhoeven<br>Release date July 17, 1987</div></td>
"""

font = ("Courier New", 12, 'bold')
sg.theme("DarkBlue3")
sg.set_options(font=font)

layout_advertise = [
    [sg.Multiline(
        size=(25, 10),
        border_width=2,
        text_color='white',
        background_color='green',
        disabled=True,
        no_scrollbar=True,
        expand_x=True,
        expand_y=True,
        key='Advertise')],
]

keypad = [
    ["Rad/Deg",          "x!",   "(",  ")", "%", "AC"],
    ["Inv",       "sin", "ln",   "7", "8", "9", "÷" ],
    ["Pi",        "cos", "log",  "4",  "5", "6", "x" ],
    ["e",         "tan", "√",    "1",  "2", "3", "-" ],
    ["Ans",       "EXP", "POW",  "0",  ".", "=", "+" ],
]

layout_calculator = [
    [sg.Button(
        key,
        size=(7, 4),
        expand_x=key=="Rad/Deg",
        button_color=('white', '#405373') if key in "1234567890" else sg.theme_button_color(),
     ) for key in line]
            for line in keypad]

layout = [
    [sg.Frame("Calculator", layout_calculator, expand_x=True, expand_y=True),
     sg.Frame("Advertise",  layout_advertise, expand_x=True, expand_y=True)],
]
window = sg.Window('Title', layout, finalize=True, use_default_focus=False)
for element in window.key_dict.values():
    element.block_focus()

advertise = window['Advertise'].Widget

html_parser = html_parser.HTMLTextParser()
set_html(advertise, html)
width, height = advertise.winfo_width(), advertise.winfo_height()

while True:

    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break
    print(event, values)

window.close()