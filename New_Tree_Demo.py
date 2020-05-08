import PySimpleGUI as sg

from Tool import read_file, save_file
from PySimpleGUI_Tool import Tree

def convert(text):
    temp = text.replace('__init__', ' ')    # Set __init__ lowest
    temp = temp.replace('_', '|')           # Set '_' to highest
    return temp

font=('Courier New', 12, 'bold')
tree = Tree(column_width=30, font=font, row_height=23)
layout = [[sg.Button('Load File'),   sg.Button('Save File'),
           sg.Button('Delete'),      sg.Button('Rename'),
           sg.Button('Move Up'),     sg.Button('Move Down'),
           sg.Button('Sort'),        sg.Button('Insert'),
           sg.Button('Quit')],
          [tree, sg.Multiline('', size=(80, 25), font=font, key='Multiline')]]

window = sg.Window('test', layout=layout, finalize=True)
tree.hide_header(window)

while True:

    event, values = window.read()

    if event in [None, 'Quit']:
        break
    elif event == 'Load File':
        dictionary = read_file('Book.json')
        tree.load_tree(dictionary)
    elif event == 'Save File':
        dictionary = tree.dump_tree()
        save_file('Book.json', dictionary)
    elif event == 'Delete':
        tree.delete_node(tree.where())
    elif event == 'Rename':
        tree.rename(tree.where(), 'New_Name')
    elif event == 'Move Up':
        tree.move_node_up(tree.where())
    elif event == 'Move Down':
        tree.move_node_down(tree.where())
    elif event == 'Sort':
        tree.sort_tree(func=convert)
    elif event == 'Insert':
        for i in range(4):
            tree.insert_node('', 'test_'+str(i), 'Text for test_'+str(i), update=False)
        tree.insert_node('', 'test_5', 'Text for test_5')

    text = tree.get_value(tree.where())
    window['Multiline'].update(value=text)

window.close()