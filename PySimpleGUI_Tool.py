"""
Tool for PySimpleGUI
Author  - Jason Yang
Date    - 2020/05/12
Version - 0.0.3

History

- 2020/05/08
  - New Tree class for more methods and functions, but with only name and
    one text value for each node.
- 2020/05/10
  - New Button class for stadium shape background
- 2020/05/11
  - Revised for auto_size_button in class Button.
- 2020/05/12
  - Revised button_color can be like 'black'.
  - Revised len of button_text to check halfwidth and fullwidth if character.
"""

from io import BytesIO
from unicodedata import east_asian_width

import PySimpleGUI as sg
from PIL import Image, ImageDraw

class Button(sg.Button):
    """
    New Button class of PySimpleGUI with stadium shape background.
    Disabled state not shown well.    
    """
    def __init__(
        self, button_text='', button_type=sg.BUTTON_TYPE_READ_FORM,
        target=(None, None), tooltip=None, file_types=(("ALL Files", "*.*"), ),
        initial_folder=None, disabled=False, enable_events=False, font=None,
        size=(None, None), auto_size_button=True, button_color=None, pad=None,
        disabled_button_color=None, focus=False, key=None, visible=True,
        bind_return_key=False, metadata=None, min_size=False):
        """
        Initial Button class, remove options
        - image_file, image_data, image_size
        - use_ttk_buttons
        - change_submits (also removed in all related functions)
        - border_width

        : Parameters - Please refer to sg.Button
          min_size - Bool, True to set size to width of button_text.
        : Return Instance of new Button class
        """
        data = self._image(
            button_text, font, button_color, size, auto_size_button)
        if button_color:
            color = [button_color[0], sg.theme_background_color()]
        else:
            color = [sg.DEFAULT_BUTTON_COLOR[0], sg.theme_background_color()]
        super().__init__(
            button_text=button_text, button_type=button_type, image_data=data,
            target=target, tooltip=tooltip, file_types=file_types, pad=pad,
            initial_folder=initial_folder, disabled=disabled, size=size,
            enable_events=enable_events, font=font, button_color=color,
            auto_size_button=auto_size_button, focus=focus, key=key,
            disabled_button_color=disabled_button_color, visible=visible,
            bind_return_key=bind_return_key, border_width=0, metadata=metadata)

    def _font(self, font):
        """
        Convert string or sequence of font to family, size and style.
        : Parameters
          font - str, list or tupple, tkinter font
        : Return
          family (str), size (int), style (str)
        """
        if isinstance(font, str):
            lst = list(font)
            faimly, size = lst[0], int(lst[1])
        else:
            lst = font
            family, size = lst[:2]
        style = lst[2] if len(lst)>2 else ''
        return (family, size, style)

    def _image(self, button_text, font, button_color, size, auto_size_button):
        """
        Create image data for PySimpleGUI.
        : Parameter
          font - None, str, list or tuple, tkinter font
          button_color - None, tuple(text_color, background_color)
          size - None, (int, int), size (width, height) in chars
        : Return
          data - image data for PySimpleGUI.
        """
        color = button_color if button_color else ('white', 'blue')
        s1 = size[0] if size[0]!=None else sg.DEFAULT_BUTTON_ELEMENT_SIZE[0]
        if auto_size_button:
            s1 = self._len(button_text)
        text, background = color
        font = font if font else sg.DEFAULT_FONT
        family, s2, style = self._font(font)
        width, height = int(s1*s2*0.7), s2*3
        radius = height//2
        im = Image.new(
            mode='RGBA', size=(width+height, height), color=(255, 255, 255, 0))
        image = ImageDraw.Draw(im, mode='RGBA')
        image.ellipse((0, 0, height, height), fill=background)
        image.ellipse((width, 0, width+height, height), fill=background)
        image.rectangle((radius, 0, radius+width, height), fill=background)
        with BytesIO() as output:
            im.save(output, format="PNG")
            data = output.getvalue()
        return data

    def _len(self, text):
        length = 0
        for char in text:
            length += 2 if east_asian_width(char) in 'AFW' else 1
        return length

def FileBrowse(
        button_text='Browse', target=(sg.ThisRow, -1), pad=None, key=None,
        file_types=(("ALL Files", "*.*"),), initial_folder=None, tooltip=None,
        size=(None, None), auto_size_button=None, button_color=None,
        enable_events=False, font=None, disabled=False, metadata=None):
    """
    Select File for read, refer to PySimpleGUI FileBrowse
    """
    return Button(
        button_text=button_text, button_type=sg.BUTTON_TYPE_BROWSE_FILE,
        target=target, file_types=file_types, initial_folder=initial_folder,
        tooltip=tooltip, size=size, auto_size_button=auto_size_button,
        enable_events=enable_events, disabled=disabled, pad=pad, key=key,
        button_color=button_color, font=font, metadata=metadata)

def FileSaveAs(
        button_text='Save As...', target=(sg.ThisRow, -1), enable_events=False,
        file_types=(("ALL Files", "*.*"),), initial_folder=None, font=None,
        disabled=False, tooltip=None, size=(None, None), auto_size_button=None,
        button_color=None, pad=None, key=None, metadata=None):
    """
    Select File for Save, refer to PySimpleGUI FileSaveAs
    """
    return Button(
        button_text=button_text, button_type=sg.BUTTON_TYPE_SAVEAS_FILE,
        target=target, file_types=file_types, initial_folder=initial_folder,
        tooltip=tooltip, size=size, disabled=disabled, font=font, pad=pad,
        auto_size_button=auto_size_button, button_color=button_color,
        enable_events=enable_events, key=key, metadata=metadata)

def FolderBrowse(
        button_text='Browse', target=(sg.ThisRow, -1), initial_folder=None,
        tooltip=None, size=(None, None), auto_size_button=None,
        button_color=None, disabled=False, enable_events=False, font=None,
        pad=None, key=None, metadata=None):
    """
    Select Folder, refer to PySimpleGUI FolderBrowse
    """
    return Button(
        button_text=button_text, button_type=sg.BUTTON_TYPE_BROWSE_FOLDER,
        target=target, initial_folder=initial_folder, tooltip=tooltip,
        size=size, auto_size_button=auto_size_button, disabled=disabled,
        button_color=button_color, enable_events=enable_events, font=font,
        pad=pad, key=key, metadata=metadata)

class Tree(sg.Tree):
    """
    Tree for node name shown only, with load from dictionary, dump tree to
    dictionary, delete node, rename node, move node up, move node down,
    where the selection, set node text, read node text, set node value,
    read node text, set select, hide_header, sort nodes

    ** Must call hide_tree(window) after window finalized !!!
    """
    def __init__(self, column_width=30, font=('Courier New', 12), key='TREE',
                 text_color='black', background_color='white', num_rows=25,
                 row_height=28):
        """
        Tree is a subclass of sg.Tree with more methods and functions.
        : Parameters
          column_width - int, width of tree in chars.
          font - font for character style in tree view.
          key - str, tree reference key in PySimpleGUI.
          text_color - color, text color.
          background_color - coor, background color.
          num_rows - int, height of tree view in lines.
          row_height - int, height of line in pixels.
        : Return
          Instance of Tree
        """
        self.key = key
        self.text = None
        self.list = []
        self.treedata = sg.TreeData()
        self._init(lines=num_rows, width=column_width, row_height=row_height,
                   text=text_color, background=background_color, font=font,
                   key=key)

    def delete_all_nodes(self):
        """
        Delete all nodes in Tree.
        """
        keys = [tag.key for tag in self.treedata.tree_dict[''].children]
        self.delete_nodes(keys)

    def delete_node(self, key, update=True):
        """
        Delete node 'key' from tree. After delete, selection will move up.
        : Parameters
          key - str, node key tp remove
        """
        self._all_nodes()
        if key and key in self.list:
            pre_key = self._previous_key(key)
            node = self.treedata.tree_dict[key]
            self.treedata.tree_dict[node.parent].children.remove(node)
            node_list = [node]
            while node_list != []:
                temp = []
                for item in node_list:
                    temp += item.children
                    del self.treedata.tree_dict[item.key]
                    del item
                node_list = temp
            if update:
                self.tree.update(values=self.treedata)
                self.select(pre_key)

    def delete_nodes(self, keys):
        """
        Delete all nodes with key in keys.
        : Parameters
          keys - sequence of key
        """
        for key in keys:
            self.delete_node(key, update=False)
        self.tree.update(values=self.treedata)
        self.select('0')

    def dump_tree(self):
        """
        Save treedata to dictionary
        Dictionary pairs in key: [parent, children, text, values]
        : Return
          dictionary for treedata
        """
        dictionary = {}
        for key, node in self.treedata.tree_dict.items():
            children = [n.key for n in node.children]
            dictionary[key]   = [node.parent, children, node.text, node.values]
        return dictionary

    def get_text(self, key):
        """
        Get node name
        : Parameters
          key - str, key of node
        : Return
          str, name text of node
        """
        return self.treedata.tree_dict[key].text

    def get_value(self, key):
        """
        Get values[0] of node.
        : Parameters
          key - str, key of node
        : Return
          str, value of node
        """
        values = self.treedata.tree_dict[key].values
        return values[0] if values else ''

    def hide_header(self, window):
        """
        Hide header of tree.
        : Parameters
          window - instance of sg.Window
        """
        self.tree = window[self.key]
        self.tree.Widget.configure(show='tree')

    def insert_node(self, parent, name, text, update=True):
        """
        Insert a new node under parent, by name and text
        : Parameters
          parent - str, key of parent node, '' for root.
          name - str, name of new node
          text - str, value of node
          update - bool, True to update treedata into tree.
        : return
          None
        """
        if name:
            key = self._new_key()
            self.treedata.Insert(parent, key, name, [text])
            if update:
                self.tree.update(values=self.treedata)

    def load_tree(self, dictionary):
        """
        Load dcitionary into self.treedata and update self.tree
        : Parameters
          dictionary - data for treedata in Tree.
            Dictionary pairs in key: [parent, children, text, values]
            parent, children are key of nodes, values in [str]
        """
        children = dictionary[''][1]
        table = {'':''}
        while children != []:
            temp = []
            for child in children:
                node = dictionary[child]
                table[child] = self._new_key()
                self.treedata.Insert(
                    table[node[0]], table[child], node[2], node[3])
                temp += node[1]
            children = temp
        self.tree.update(values=self.treedata)

    def move_node_up(self, key):
        """
        Move node up in tree structure, not position only.
        : Parameters
          key - str, key of node
        """
        if not key:
            return
        node = self.treedata.tree_dict[key]
        if not key:
            return
        pre = self._previous_key(key)
        pre_node = self.treedata.tree_dict[pre]
        if not pre:
            return
        if pre == node.parent:
            pre_parent_node = self.treedata.tree_dict[pre_node.parent]
            index = pre_parent_node.children.index(pre_node)
            pre_parent_node.children = (pre_parent_node.children[:index] +
                [node] + pre_parent_node.children[index:])
            self.treedata.tree_dict[node.parent].children.remove(node)
            node.parent = pre_parent_node.key
        else:
            if node.parent == pre_node.parent:
                parent_node = self.treedata.tree_dict[node.parent]
                index = parent_node.children.index(pre_node)
                parent_node.children.remove(node)
                parent_node.children = (parent_node.children[:index] +
                    [node] + parent_node.children[index:])
            else:
                pre_parent_node = self.treedata.tree_dict[pre_node.parent]
                pre_parent_node.children.append(node)
                self.treedata.tree_dict[node.parent].children.remove(node)
                node.parent = pre_parent_node.key
        self.tree.update(values=self.treedata)
        self.select(key)

    def move_node_down(self, key):
        """
        Move node down in tree structure, not position only.
        : Parameters
          key - str, key of node
        """
        if not key:
            return
        nxt = self._next_not_children(key)
        if not nxt:
            return
        node = self.treedata.tree_dict[key]
        nxt_node = self.treedata.tree_dict[nxt]
        if nxt_node.children == []:
            self.treedata.tree_dict[node.parent].children.remove(node)
            parent_node = self.treedata.tree_dict[nxt_node.parent]
            index = parent_node.children.index(nxt_node)
            parent_node.children = (parent_node.children[:index+1] +
                [node] + parent_node.children[index+1:])
            node.parent = nxt_node.parent
        else:
            self.treedata.tree_dict[node.parent].children.remove(node)
            nxt_node.children = [node] + nxt_node.children
            node.parent = nxt_node.key
        self.tree.update(values=self.treedata)
        self.select(key)

    def rename(self, key, text):
        """
        Rename node text
        : Parameters
          key - str, key of node
          txt - str, new text for node
        """
        if key and text:
            self.set_text(key, text)

    def search(self, text=None, mode='New'):
        """
        Search name in tree.
        :Parameters
          text - str, name of node.
          next - str, 'New' for new search, 'Previous' for previous node,
            'Next' for next node.
        :Return
          key of node, None if not found.
        """
        if len(self.treedata.tree_dict) < 2 or (mode=='New' and not text):
            return None
        self._all_nodes()
        where = self.where()
        index = self.list.index(where) if where else -1
        if mode == 'New':
            self.text = text.lower()
            return self._search_next_node(-1)
        if mode == 'Previous':
            return self._search_previous_node(index)
        elif mode == 'Next':
            return self._search_next_node(index)
        return None

    def select(self, key=''):
        """
        Move the selection of node to node key.
        : Parameters
          key - str, key of node.
        """
        iid = self._key_to_id(key)
        if iid:
            self.tree.Widget.see(iid)
            self.tree.Widget.selection_set(iid)

    def set_text(self, key, text):
        """
        Set new node name
        : Parameters
          key - str, key of node.
          text - str, new name of node.
        """
        self.treedata.tree_dict[key].text = text
        self.tree.update(key=key, text=text)

    def set_value(self, key, text):
        """
        Set values[0] of node to new value 'text'.
        : Parameters
          key - str, key of node.
          text - str, new value of node.
        """
        self.treedata.tree_dict[key].values[0] = text

    def sort_tree(self, func=None):
        """
        Sort children list of all nodes by node name.
        : Parameter
          func - function name to process text for sorting key.
            def func(text):
                ...
                return new_text
            called by tree.sort_tree(func)
        : Return
          None, result upadted into Tree.
        """
        pre_select_key = self.where()
        for key, node in self.treedata.tree_dict.items():
            children = node.children
            if func:
                node.children = sorted(
                    children, key=lambda child: func(child.text))
            else:
                node.children = sorted(children, key=lambda child: child.text)
        self.tree.update(values=self.treedata)
        self.select(pre_select_key)

    def where(self):
        """
        Get where the selection
        : Return
          str, key of node, '' for root node
        """
        item = self.tree.Widget.selection()
        return '' if len(item) == 0 else self.tree.IdToKey[item[0]]

    def _all_nodes(self, parent='', new=True):
        """
        Get all keys of nodes in list order.
        : Parameter
          parent - str, key of starting node.
          new - True for begiinning of search.
        : Return
          None, result in self.list
        """
        if new:
            self.list = []
        children = self.treedata.tree_dict[parent].children
        for child in children:
            self.list.append(child.key)
            self._all_nodes(parent=child.key, new=False)

    def _init(self, lines=25, width=30, row_height=28, text='black',
              background='white', font=('Courier New', 12), key='TREE'):
        """
        Initialization for sg.Tree
        : Parameter
          lines - int, lines of tree view
          width - int, width of tree view in chars.
          row_height - int, line height of tree view in pixels.
          text - color for text.
          background - color of background.
          font - font of text
          key - str, key of element in PySimpleGUI.
        : return
          None
        """
        super().__init__(data=self.treedata, headings=['Notes',], pad=(0, 0),
        show_expanded=False, col0_width=width, auto_size_columns=False,
        visible_column_map=[False,], select_mode=sg.TABLE_SELECT_MODE_BROWSE,
        enable_events=True, text_color=text, background_color=background,
        font=font, num_rows=lines, row_height=row_height, key=key)

    def _key_to_id(self, key):
        """
        Convert PySimplGUI element key to tkinter widget id.
        : Parameter
          key - str, key of PySimpleGUI element.
        : Return
          id - int, id of tkinter widget
        """
        for k, v in self.tree.IdToKey.items():
            if v == key:
                return k
        return None

    def _new_key(self):
        """
        Find a unique Key for new node, start from '1' and not in node list.
        : Return
          str, unique key of new node.
        """
        i = 0
        while True:
            i += 1
            if str(i) not in self.treedata.tree_dict:
                return str(i)

    def _previous_key(self, key):
        """
        Find the previous node key in tree list.
        : Parameter
          key - str, key of node.
        : Return
          str, key of previous node.
        """
        self._all_nodes('')
        index = self.list.index(key)
        result = '' if index==0 else self.list[index-1]
        return result

    def _next_not_children(self, key):
        """
        Find next node key, where node are not children of node 'key'.
        : Parameter
          key - str, key of node.
        : Return
          str, key of next node.
        """
        self._all_nodes('')
        index = self.list.index(key) + 1
        while index < len(self.list):
            parent = []
            p = self.treedata.tree_dict[self.list[index]].parent
            while True:
                parent.append(p)
                p = self.treedata.tree_dict[p].parent
                if p == '': break
            if key in parent:
                index += 1
            else:
                return self.list[index]
        return None

    def _search_next_node(self, index):
        """
        Search next one node.
        :Return
          key of next node, None for not found.
        """
        if not self.text:
            return None
        length = len(self.list)
        for i in range(index+1, length):
            key = self.list[i]
            if self.text in self.treedata.tree_dict[key].text.lower():
                return key
        return None

    def _search_previous_node(self, index):
        """
        Search previous one node.
        :Return
          key of previous node, None for not found.
        """
        if not self.text:
            return None
        for i in range(index-1, -1, -1):
            key = self.list[i]
            if self.text in self.treedata.tree_dict[key].text.lower():
                return key
        return None
