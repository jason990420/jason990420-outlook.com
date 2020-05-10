import PySimpleGUI as sg

from Tool import read_file, save_file
from PySimpleGUI_Tool import Tree

menu = """
    Tips

    1. There's no file to load when new start.
    2. Use Insert to add items.
    3. Then you can do
       - delete, rename
       - sort, move up, move down
       - search new, search next, search previous
    4. To save tree if you want.
"""
font=('Courier New', 12, 'bold')
tree = Tree(column_width=30, font=font, row_height=23, num_rows=20)
size = (14, 1)

frame1 = [[Button('Load File'), Button('Save File'), Button('Quit')]]
frame2 = [[Button('Insert'), Button('Delete'), Button('Delete All'),
           Button('Rename')]]
frame3 = [[Button('Sort'), Button('Move Up'), Button('Move Down')]]
frame4 = [[Button('Search New', size=size),
           Button('Search Next', size=size, pad=(16, None)),
           Button('Search Previous', size=size)]]

layout = [[sg.Frame('', frame1, relief='raised'),
           sg.Frame('', frame2, relief='raised')],
          [sg.Frame('', frame3, relief='raised'),
           sg.Frame('', frame4, relief='raised')],
          [tree, sg.Multiline(menu, size=(50, 20), font=font, key='Multiline')]]

window = sg.Window('Tree Demo', layout=layout, finalize=True,
    use_default_focus=False)
tree.hide_header(window)

while True:

    event, values = window.read()

    if event in [None, 'Quit']:
        break
    elif event == 'Load File':
        dictionary = read_file('Book.json')
        if dictionary:
            tree.load_tree(dictionary)
    elif event == 'Save File':
        dictionary = tree.dump_tree()
        save_file('Book.json', dictionary)
    elif event == 'Delete':
        tree.delete_node(tree.where())
    elif event == 'Delete All':
        tree.delete_all_nodes()
    elif event == 'Rename':
        tree.rename(tree.where(), 'New_Name')
    elif event == 'Move Up':
        tree.move_node_up(tree.where())
    elif event == 'Move Down':
        tree.move_node_down(tree.where())
    elif event == 'Sort':
        tree.sort_tree(func=None)
    elif event == 'Insert':
        for i in range(4):
            tree.insert_node('', 'test_'+str(i), 'Text for test_'+str(i), update=False)
        tree.insert_node('', 'test_5', 'Text for test_5')
    elif event in ['Search New', 'Search Previous', 'Search Next']:
        key = tree.search('test_3', mode=event[7:])
        if key != None:
            tree.select(key)

    text = tree.get_value(tree.where())
    window['Multiline'].update(value=text)

window.close()