import PySimpleGUI as sg
from PySimpleGUI_Tool import Button, FileBrowse, FileSaveAs, FolderBrowse

color  = ('#ffffff', '#0000ff')
font   = ('Courier New', 16, 'bold')
layout = [[sg.Button('test', size=(10, 1), font=font, button_color=color),
           sg.FileBrowse(font=font, button_color=color),
           sg.FileSaveAs(font=font, button_color=color),
           sg.FolderBrowse(font=font, button_color=color)],
          [Button('test', size=(10, 1), font=font, button_color=color),
           FileBrowse(font=font),
           FileSaveAs(font=font),
           FolderBrowse(font=font)]]

window = sg.Window('Button Demo', layout=layout, finalize=True,
    use_default_focus=False)

while True:

    event, values = window.read()

    if event == None:
        break

window.close()