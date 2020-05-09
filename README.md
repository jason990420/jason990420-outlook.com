# jason990420-outlook.com
Two personel libraries

1. Tool.py
   With general functions
   
``` Python
from Tool import *

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

# get_substring
>>> text = '<link rel="dns-prefetch" href="https://github.githubassets.com">'
>>> get_substring(text, 'href="', '">')
'https://github.githubassets.com'

# flat
>>> flat([1,[2,3,4], [5,6,[7,8,9],10]])
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# f-string
>>> books = 10
>>> fmt = 'I have {books} books'
>>> f(fmt)
'I have 10 books'

# len_
>>> a, b, c, d = 1, '123', [1,2,3], (1,2,3)
>>> len_(a), len_(b), len_(c), len_(d)
(1, 3, 3, 3,)

# mapping
>>> def func(a, b, c):
...     return a*b+c
... 
>>> mapping(func, [1,2,3,4], 10, 5)
[15, 25, 35, 45]

# filter_
>>> def func(a, b, c):
    return True if a<b or a>c else False
>>> filter_(func, [1,2,3,4,5,6,7,8,9,10], 5, 8)
[1, 2, 3, 4, 9, 10]
```

2. PySimpleGUI Tool
   New Tree class with functions
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
