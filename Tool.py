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
  - Add 206 code Partial Content as success for Read_URL.
  - Rename All to All_True, Any to Any_True.
  - Add Transpose function for 2D tuple and list.
  - Add Get_Substring function to find substring in string.
  - Add Insert_List function to insert value at index of list.
"""
import json
import zlib
import brotli
from pathlib import Path
from PIL import Image
from urllib import request, error
from urllib.parse import urlsplit
from http import client
from copy import deepcopy

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

def Read_URL(url, data=None, headers=None, encoding='utf-8', byte=False):
    """
    Read text from URL
    Compress method for gzip, deflate, br dealed internally.
    :Parameter
      url     : string or a Request object.
      data    : an object specifying additional data to be sent, or None.
      headers : dictionary, header of Http request entity.
      encoding: name of encoding to convert bytes into string.
      byte    : flag for not decoding by encoding
    :Return
      (None, None) if failed, else response, string of html content
    """
    if not headers:
        url_base = urlsplit(url).netloc
        headers = {
            'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,'
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
    if response.status not in [200, 206]:
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

def All_True(seq, function, arg):
    """
    All find all items meet all arg in function
    : Parameters
      seq     : list or tupple, sequence to be checked
      function: function to do the check.
      arg     : list of tuple, all required arguments
    : Return
      list or tuple, meet check function with all arg
    """
    if not (isinstance(seq, (list, tuple)) and
            isinstance(arg, (list, tuple))):
        return None
    def func(arg1, arg2):
        result = function(arg1, arg2)
        return result
    try:
        r = list(map(lambda x: list(map(lambda y: func(x, y), arg)), seq))
        result = [item for i, item in enumerate(seq) if not (False in r[i])]
    except:
        Signal('TypeError')
        return None
    if isinstance(seq, tuple):
        return tuple(result)
    return result

def Any_True(seq, function, arg):
    """
    All find all items meet any arg in function
    : Parameters
      seq     : list or tupple, sequence to be checked
      function: function to do the check.
      arg     : list of tuple, all required arguments
    : Return
      list or tuple, meet check function with any arg
    """
    if not (isinstance(seq, (list, tuple)) and
            isinstance(arg, (list, tuple))):
        return None
    def func(arg1, arg2):
        return function(arg1, arg2)
    try:
        r = list(map(lambda x: list(map(lambda y: func(x, y), arg)), seq))
        result = [item for i, item in enumerate(seq) if (True in r[i])]
    except:
        Signal('TypeError')
        return None
    if isinstance(seq, tuple):
        return tuple(result)
    return result

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

def Insert_List(sequence, index, value):
    """
    Insert value into list at index
    : Parameter
      sequence: list
      index   : where the value to insert into list
      value   : value to insert
    : Return
      new list with insert value at index
    """
    if not (isinstance(sequence, list) and isinstance(index, int)):
        return sequence
    tmp = deepcopy(sequence)
    tmp[index:index] = [value]
    return tmp