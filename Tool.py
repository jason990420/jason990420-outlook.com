"""
Personal uility for common functions
Author : Jason Yang
Version: 0.0.5
Created: 2020/03/31
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
"""
import re
import json
import zlib
import brotli
import inspect
from pathlib import Path
from PIL import Image
from urllib import request, error
from urllib.parse import urlsplit
from http import client
from copy import deepcopy
from base64 import b64encode, b64decode

__text_file__  = ['.txt', '.py']
__json_file__  = ['.json']
__image_file__ = ['.jpg', '.bmp', '.png', '.gif']
__all_file__ = __text_file__ + __json_file__ + __image_file__

def Signal(message):
    """
    Function as an failure interface for methods defined here. If you have
    different GUI, you can redefine it.
    : Parameters
      message: object, error message generally in string
    : Return - None
    """
    if isinstance(message, str):
        print(message)
    else:
        raise TypeError

def Read_File(filename, encoding='utf-8'):
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
        Signal('FileNotFoundError')
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
                        Signal('JSONDecodeError')
                        return None
        except:
            Signal('OpenError')
            return None
    elif suffix in __image_file__:
        try:
            data = Image.open(path)
        except:
            Signal('OpenError')
            return None
        # Image file Not Close for future operation
    else:
        Signal('FileTypeError')
        return None
    return data

def Save_File(filename, data, encoding='utf-8'):
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
                        Signal('TypeError')
                        return False
        except:
            Signal('OpenError')
            return False
    elif suffix in __image_file__:
        try:
            data.save(path)
        except:
            Signal('OpenError')
            return False
    else:
        Signal('FileTypeError')
        return False
    return True

def Read_URL(url, data=None, headers=None, encoding='utf-8',
             user=None, password=None, byte=False):
    """
    Read text from URL
    Compress method for gzip, deflate, br dealed internally.
    :Parameter
      url     : string or a Request object.
      data    : an object specifying additional data to be sent, or None.
      headers : dictionary, header of Http request entity.
      encoding: name of encoding to convert bytes into string.
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
            'Host': f'{url_base}',
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
        Signal('ValueError')
        return None, None
    try:
        response = request.urlopen(req)
    except error.HTTPError as e:
        Signal('HTTPError')
        return (None, None)
    except error.URLError as e:
        Signal('URLError')
        return (None, None)
    if not str(response.status).startswith('2'):
        Signal(client.responses[response.status])
        return (None, None)

    data = response.read()

    accept_encoding = response.headers['Content-Encoding']
    if accept_encoding == 'gzip':
        data = zlib.decompress(data, zlib.MAX_WBITS|16)
    elif accept_encoding == 'deflate':
        data = zlib.decompress(data, -zlib.MAX_WBITS)
    elif accept_encoding == 'br':
        data = brotli.decompress(data)
    html = data if byte else data.decode(encoding)

    return (response, html)

def Transpose(sequence):
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

def Get_Substring(text, start, stop):
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

def Flat(sequence):
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
                result += Flat(item)
            else:
                result.append(item)
        return result
    else:
        return sequence

def F(string):
    """
    F-type string, also for variable
    : Parameters
      string: str literal or variable
    : Return
      string with argument in { } replaced by eval, or string if it is not str
    """
    if not isinstance(string, str):
        Signal('TypeError')
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

def Map(func, sequence, *argc):
    """
    map function work for sequence with arguments
    : Parameters
      func: function to all element of sequence
      seuquence: list, tuple or non-sequence variable
      argc: tuple or single value if more argument required for function
    : Return
      list or value, result of function func
    """
    if isinstance(sequence, (tuple, list )):
        return list(map(lambda i:func(i, *argc), sequence))
    return func(sequence, *argc)

def Filter(func, sequence, *argc):
    """
    filter function work for sequence with arguments
    : Parameters
      func: function to all element of sequence
      seuquence: list, tuple or non-sequence variable
      argc: tuple or single value if more argument required for function
    : Return
      list or non-sequence variable for func() true
    """
    if isinstance(sequence, (tuple, list )):
        return list(filter(lambda i:func(i, *argc), sequence))
    return sequence if func(sequence, *argc) else []