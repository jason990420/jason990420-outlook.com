"""
Personal uility for common functions
Author : Jason Yang
Create : 2020/03/31
Update : 2020/11/20
Version: 0.0.10

Revised:
- 2020/04/01 - version 0.01
  - Add '.gif' to Read_File and Write_File.
  - lowercase before checking file extension in Read_File and Write_File.
  - Return response, data in Read_URL for more processing.
- 2020/04/02 - version 0.0.2
  - Add list for kind of files.
  - Add '.py' to text_file
  - Add All and Any function.
- 2020/04/02 - version 0.0.3
  - Revise urllib.error to error.
- 2020/04/03 - version 0.0.4
  - Build test, some failures found and update.
- 2020/04/05 - version 0.0.5
  - Remove '\n' from Signal print statement.
  - Add one flag keyword byte for Read_URL to decide decoding or not.
        Sometime, we get bytes, like image file, not text from web.
  - Changed all status code starts with 2 as success for Read_URL.
  - Rename All to All_True, Any to Any_True.
  - Add Transpose function for 2D tuple and list.
  - Add Get_Substring function to find substring in string.
  - Add Insert_List function to insert value at index of list.
- 2020/04/07 - version 0.0.6
  - Add Flat_List to flat list from N-D dimension to 1D
  - Add F as f-string function for variable
  - Add user and password as options of Read_URL
  - Remove All_True and Any_True functions
  - Add Map, Filter functions for more paramters
  - Remove Insert_List for duplicate
- 2020/05/01 - version 0.0.7
  - Add Len for list and tupple, also for variables with other data type
  - Revise Map for different length arguments
- 2020/05/07 - version 0.0.7
  - Rename all function name for PEP8 compatible
- 2020/05/13 - version 0.0.8
  - Add color_convert for color data type conversion.
  - Add errors option for read_URL
  - Add Thread class for sequence thread management.
- 2020/05/20 - version 0.0.9
  - Add load_color_table for tkinter color name.
  - Add load_family_list for font families.
- 2020/11/20 - version 0.0.10
  - Add types for nested variable types
"""

import re
import json
import zlib
import brotli
import inspect
import _thread
from pathlib import Path
from PIL import Image, ImageColor
from urllib import request, error
from urllib.parse import urlsplit
from http import client
from copy import deepcopy
from base64 import b64encode, b64decode
from tkinter import Tk, font as tk_font
from lxml import etree

__text_file__  = ['.txt', '.py']
__json_file__  = ['.json']
__image_file__ = ['.jpg', '.bmp', '.png', '.gif']
__all_file__ = __text_file__ + __json_file__ + __image_file__

def color_convert(color, to_hex=False):
    """
    Convert color to specified type of color
    : Parameter
      color - tuple of integer, "#RRGGBB" of color or color name
      to_hex - Convert to '#RRGGBB' if True, else tuple of integer [r, g, b]
    : Return
      return same color with type 'mode'
    """
    if not isinstance(color, (tuple, list, str)):
        return None
    if isinstance(color, str):
        if color.startswith('#') and len(color)==7:
            return color if to_hex else tuple(bytes.fromhex(color[1:]))
        elif color in ImageColor.colormap:
            s = ImageColor.getcolor(color, 'RGB')
            return  "#%02X%02X%02X" % s if to_hex else s
    else:
        return "#%02X%02X%02X" % color if to_hex else color
    return None

def f(string):
    """
    F-type string, also for variable
    : Parameters
      string: str literal or variable
    : Return
      string with argument in { } replaced by eval, or string if it is not str
    """
    if not isinstance(string, str):
        signal('TypeError')
        return string
    tmp = string.replace('{{', chr(1))[::-1].replace('}}', chr(2))[::-1]
    expr = r'(?<!\{)\{([\w]+)\}'
    expressions = re.findall(expr, tmp)
    outer_locals = inspect.currentframe().f_back.f_locals
    for expression in expressions:
        tmp = tmp.replace(f'{{{expression}}}',
            str(eval(expression, globals(), outer_locals)))
    result = tmp.replace(chr(1), '{').replace(chr(2), '}')
    return result

def filter_(func, sequence, *argc):
    """
    filter function work for sequence with arguments
    : Parameters
      func: function to all element of sequence
      seuquence: list, tuple or non-sequence variable
      argc: tuple or single value if more argument required for function
    : Return
      list or non-sequence variable for func() true
    """
    if isinstance(sequence, (tuple, list)):
        return list(filter(lambda i:func(i, *argc), sequence))
    return sequence if func(sequence, *argc) else []

def flat(sequence):
    """
    Function to flat multi-dimensional list to 1D list
    : Parameters
      sequence: list to flat
    : Return
      1D list, or sequence if sequence is not a list
    """
    result = []
    if isinstance(sequence, list):
        for item in sequence:
            if isinstance(item, list):
                result += flat(item)
            else:
                result.append(item)
        return result
    else:
        return sequence

def get_substring(text, start, stop):
    """
    Find subtring between start and stop strings.
    : Parameter
      text - string to search
      start - string before target substring
      stop - string after target substring
    : Return
      Substring between start and sop strings in text.
    """
    if not (isinstance(text, str) and isinstance(start, str)
            and isinstance(stop, str)):
        return None
    if 0 in [len(text), len(start), len(stop)]:
        return None
    if start in text:
        return text.split(start)[1].split(stop)[0]
    else:
        return text.split(stop)[0]

def len_(sequence):
    """
    Return len(sequence)
    : Parameter
      sequence: any object
    : Return
      len(sequence) for list, tuple sequence, or 1 for other object.
    """
    return len(sequence) if isinstance(sequence, (tuple, list)) else 1

def load_color_table():
    """
    Get dictionary for color pairs, color name: color tuple.
    : Return
      dict, color_name: color_tuple (r, g, b)
      {} if no colors.json file or failed to load colors from web.
    """
    url = 'http://www.tcl.tk/man/tcl8.5/TkCmd/colors.htm'
    color_file = "colors.json"
    if Path(color_file).is_file():
        return read_file(color_file)
    else:
        response, data = read_URL(url)
        if response == None:
            return {}
        html = etree.HTML(data)
        ps = html.xpath('/html/body/dl/dd/table//p')
        colors = [p.text if i%4 == 0 else int(p.text)
            for i, p in enumerate(ps) if p.text!=None]
        table = {colors[i]:'#%02x%02x%02x'%tuple(colors[i+1:i+4])
            for i in range(0, len(colors), 4)}
        save_file(color_file, table)
        return table

def load_family_list():
    """
    Get list for font families.
    : Return
      List of font families.
    """
    root = Tk()
    families = tk_font.families()
    root.destroy()
    return families

def mapping(func, *args):
    """
    map function work for arguments, sequence or not sequence
    : Parameters
      func: function to all element of sequence
      argc: tuple or single value if more argument required for function
    : Return
      list, result of function func
      Element in argc will be extend to maximum length in argc.
    """
    lst = list(args)
    maximum = max(map(len_, args))
    new_list = []
    for item in lst:
        if isinstance(item, (tuple, list)):
            new_list.append(
                item*(maximum//len_(item))+item[:maximum%len_(item)])
        else:
            new_list.append([item]*maximum)
    return list(map(func, *new_list))

def read_file(filename, encoding='utf-8'):
    """
    Read any file and return the result. Method to open the file depend on
    the file extension.
    Legal file types listed in __all_file__
    :Parameter
      filename: path-like object.
      encoding: name of encoding, only be used in text mode.
    :Return
      None if failed, else depend on file extension
      string if file extension in __text_file__
      object if file extension in __json_file__
      PIL Image object if file extension __image_file__
    """
    path = Path(filename)
    if not path.is_file():
        signal('FileNotFoundError')
        return None
    suffix = path.suffix.lower()
    if suffix in __text_file__ + __json_file__:
        try:
            with open(path, 'rt', encoding=encoding) as f:
                if suffix in __text_file__:
                    data = f.read()
                elif suffix in __json_file__:
                    try:
                        data = json.load(f)
                    except:
                        signal('JSONDecodeError')
                        return None
        except:
            signal('OpenError')
            return None
    elif suffix in __image_file__:
        try:
            data = Image.open(path)
        except:
            signal('OpenError')
            return None
        # Image file Not Close for future operation
    else:
        signal('FileTypeError')
        return None
    return data

def read_URL(url, data=None, headers=None, encoding='utf-8', errors='ignore',
             user=None, password=None, byte=False):
    """
    Read text from URL
    Compress method for gzip, deflate, br dealed internally.
    :Parameter
      url     : string or a Request object.
      data    : an object specifying additional data to be sent, or None.
      headers : dictionary, header of Http request entity.
      encoding: name of encoding to convert bytes into string.
      errors  : error process, 'strict', 'ignore', 'replace', ...
      user    : string, user name.
      password: string, password.
      byte    : flag for not decoding by encoding
    :Return
      (None, None) if failed, else response, string of html content
    """
    if not headers:
        url_base = urlsplit(url).netloc
        headers = {
            'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,'
                       'application/json,'
                       'image/webp,image/apng,*/*;q=0.8,application/signed-exc'
                       'hange;v=b3;q=0.9'),
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': url_base,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWeb'
                           'Kit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.14'
                           '9 Safari/537.36')}
    if not (None in [user, password]):
        auth = str.encode("%s:%s" % (user, password))
        user_and_pass = b64encode(auth).decode("ascii")
        headers['Authorization'] = 'Basic %s' % user_and_pass
    try:
        req = request.Request(url, data=data, headers=headers)
    except:
        signal('ValueError')
        return None, None
    try:
        response = request.urlopen(req)
    except error.HTTPError as e:
        signal('HTTPError')
        return (None, None)
    except error.URLError as e:
        signal('URLError')
        return (None, None)
    if not str(response.status).startswith('2'):
        signal(client.responses[response.status])
        return (None, None)

    data = response.read()

    accept_encoding = response.headers['Content-Encoding']
    if accept_encoding == 'gzip':
        data = zlib.decompress(data, zlib.MAX_WBITS|16)
    elif accept_encoding == 'deflate':
        data = zlib.decompress(data, -zlib.MAX_WBITS)
    elif accept_encoding == 'br':
        data = brotli.decompress(data)
    html = data if byte else data.decode(encoding=encoding, errors=errors)

    return (response, html)

def save_file(filename, data, encoding='utf-8'):
    """
    Save any file. Method to read the file depend on the file extension.
    Legal file types listed in all_file
    :Parameter
      filename: path-like object.
      data    : data to write into file.
      encoding: name of encoding, only be used in text mode.
    :Return
      False if failed, else True
    """
    path = Path(filename)
    suffix = path.suffix.lower()
    if suffix in __text_file__+__json_file__:
        try:
            with open(path, 'wt', encoding=encoding) as f:
                if suffix in __text_file__:
                    f.write(data)
                elif suffix in __json_file__:
                    if isinstance(data, (dict, list, tuple, str, int, float,
                            True, False, None)):
                        json.dump(data, f)
                    else:
                        signal('TypeError')
                        return False
        except:
            signal('OpenError')
            return False
    elif suffix in __image_file__:
        try:
            data.save(path)
        except:
            signal('OpenError')
            return False
    else:
        signal('FileTypeError')
        return False
    return True

def signal(message, Print=True):
    """
    Function as an failure interface for methods defined here. If you have
    different GUI, you can redefine it.
    : Parameters
      message: object, error message generally in string
    : Return - None
    """
    if not isinstance(message, str):
        raise TypeError
    if Print:
        print(message)
    return message

class Thread():

    def __init__(self, func, sequence, fail=None, size=40):
        """
        Manage jobs for threading by list.
        : Parameters
          func - callable method to thread.
          sequence - list of tuple, each arguments for func.
          fail - callable method if func return Fail.
          size - max size of thread queue.
        : Return
          Obejct of Thread manager.
        """
        self.func = func
        self.fail = fail
        self.all = sequence
        self.total = len(self.all)
        self.temp = {}
        self.queue = {}
        self.size = size
        self.stop = False
        if callable(self.func) and isinstance(sequence, (tuple, list)):
            _thread.start_new_thread(self._host, ())

    def all_finished(self):
        """
        Return True if all threads finished.
        """
        return True if (
            sum(map(len, [self.queue, self.all, self.temp]))==0) else False

    def jobs_done(self):
        """
        Return the number of jobs done.
        """
        return self.total - self.jobs_left()

    def jobs_left(self):
        """
        Return the number of jobs not finished.
        """
        return len(self.all) + len(self.tmp) + len(self.queue)

    def queue_is_full(self):
        """
        Return True if queue is full.
        """
        return True if len(self.queue) == self.size else False

    def _get_a_key(self):
        """
        Get an integer ID for each new thread.
        """
        for i in range(self.size):
            if i not in self.queue:
                return i
        return None

    def _host(self):
        """
        Manager of all threads for thread run, failed process.
        """
        while True:
            if self.stop:
                break
            if len(self.all) == 0 and len(self.queue) == 0:
                self.stop = True
            length = min(self.size-len(self.queue), len(self.all))
            for i in range(length):
                self._queue_insert(self.func, self.all[i])
            self.all = self.all[length:]
            if len(self.temp) != 0:
                for key, value in self.temp.items():
                    self.all.append(value)
                self.temp = {}
                if callable(self.fail):
                    self.fail()

    def _queue_delete(self, key):
        """
        Delete thread in queue after thread done.
        """
        del self.queue[key]

    def _queue_insert(self, func, value):
        """
        Run thread and add it into queue.
        : Parameters
          func - callable function for thread
          value - tuple, arguements for func.
        : Return
          None
        """
        key = self._get_a_key()
        self.queue[key] = value
        _thread.start_new_thread(self._thread_func, (func, key, value))

    def _thread_func(self, func, key, value):
        """
        Internal thread for control of user thread.
        : Paramters
          func - callable function for thread
          key - integer ID for each new thread.
          value - tuple, arguements for func.
        : Return
          None
        """
        if self.stop:
            return
        if func(*value) == False:
            self.temp[key] = value
        self._queue_delete(key)

def transpose(sequence):
    """
    Tranpoose 2D list or tupple
    : Parameters
      sequence : 2D list or tuple
    : Return
      Transposed 2D list or tuple
    """
    if not isinstance(sequence, (list, tuple)):
        return sequence
    if len(sequence) == 0:
        return sequence
    if isinstance(sequence, list) and isinstance(sequence, list):
        return list(map(list, zip(*sequence)))
    if isinstance(sequence, tuple) and isinstance(sequence, tuple):
        return tuple(zip(*sequence))
    return sequence

def types(variable):
    """
    Return type of nested variable
    """
    kind = type(variable)
    if kind in (list, tuple):
        return kind([types(item) for item in variable])
    return kind
