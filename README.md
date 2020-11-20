# jason990420-outlook.com
Two personel libraries

Note: All actions allowed for all files here, but should be with author name and the link of file.

1. Tool.py
   With general functions
   
``` Python
from Tool import *

# color_convert
>>> color_convert("#80A0FF", to_hex=True)
'#80A0FF'
>>> color_convert("#80A0FF")
(128, 160, 255)
>>> color_convert((128, 160, 255), to_hex=True)
'#80A0FF'
>>> color_convert((128, 160, 255))
(128, 160, 255)
>>> color_convert("blue", to_hex=True)
'#0000FF'
>>> color_convert("blue")
(0, 0, 255)

# f-string
>>> books = 10
>>> fmt = 'I have {books} books'
>>> f(fmt)
'I have 10 books'

# filter_
>>> def func(a, b, c):
    return True if a<b or a>c else False
>>> filter_(func, [1,2,3,4,5,6,7,8,9,10], 5, 8)
[1, 2, 3, 4, 9, 10]

# flat
>>> flat([1,[2,3,4], [5,6,[7,8,9],10]])
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# get_substring
>>> text = '<link rel="dns-prefetch" href="https://github.githubassets.com">'
>>> get_substring(text, 'href="', '">')
'https://github.githubassets.com'

# len_
>>> a, b, c, d = 1, '123', [1,2,3], (1,2,3)
>>> len_(a), len_(b), len_(c), len_(d)
(1, 3, 3, 3,)

# load_color_table
>>> load_color_table()
{'AliceBlue': '#f0f8ff', 'AntiqueWhite': '#faebd7', ...,  'yellow2': '#eeee00', 'yellow3': '#cdcd00', 'yellow4': '#8b8b00'}

# load_family_list
>>> load_family_list()
('System', '@System', 'Terminal', ...,  'Open Sans Semibold', 'SimHei', '@SimHei')

# mapping
>>> def func(a, b, c):
...     return a*b+c
... 
>>> mapping(func, [1,2,3,4], 10, 5)
[15, 25, 35, 45]

# txt file read and save
text = read_file('file1.txt')
if text != None:
    save_file('file2.txt', text)

# json file read and save
data = read_file('file1.json')
if data != None:
    save_file('file2.json', data)

# Picture file read and asve
image = read_file('file1.png')
if data != None:
    save_file('file2.png', image)

# URL read
html = read_URL(url, data=None, headers=None, encoding='utf-8', user='xxxx', password='xxxx', byte=False)

# transpose
>>> transpose([[1,2,3], [4,5,6], [7,8,9]])
[[1,4,7], [2,5,6], [7,8,9]]

# class Thread
T = Thread(func, sequence, fail=None, size=40)
Manage jobs for threading by list.
: Parameters
  func - callable method to thread.
  sequence - list of tuple, each arguments for func.
  fail - callable method if func return Fail.
  size - max size of thread queue.
: Return
  Obejct of Thread manager.
  
# types
>>> types([123, '123', [1, '1'], (1, '1'), {1:10}, {5}, 1.3])
[<class 'int'>, <class 'str'>, [<class 'int'>, <class 'str'>], (<class 'int'>, <class 'str'>), <class 'dict'>, <class 'set'>, <class 'float'>]
>>> types([123, '123', [1, '1'], (1, '1'), {1:10}, {5}, 1.3]) == [int, str, [int, str], (int, str), dict, set, float]
True
```


2. PySimpleGUI Tool

![Demo Picture](https://github.com/jason990420/jason990420-outlook.com/blob/master/Picture/Picture%20for%20Tree%20Demo.jpg)

   New Tree class with more functions
   - delete_node(self, key)
   - delete_nodes(self, keys)
   - delete_all_nodes(self)
   - dump_tree(self)
   - get_text(self, key)
   - get_value(self, key)
   - hide_header(self, window)
   - insert_node(self, parent, name, text, update=True)
   - load_tree(self, dictionary)
   - move_node_up(self, key)
   - move_node_down(self, key)
   - rename(self, key, text)
   - search(self, text=None, mode='New')
   - select(self, key='')
   - set_text(self, key, text)
   - set_value(self, key, text)
   - sort_tree(self, func=None)
   - where(self)
   
   Demo file to show how to use it.

   New Button Class for stadium shape background.
   
   ![Demo Picture](https://github.com/jason990420/jason990420-outlook.com/blob/master/Picture/Button%20Demo.jpg)
   
   - Class Button
   - function FileBrowse
   - function FileSaveAs
   - function FolderBrowse
   
   Demo file to show how to use it.
