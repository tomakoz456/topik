# -*- coding: utf-8 -*-
import cv2
import os
import glob
import pathlib
import hashlib
import numpy as np

_max_width = 1200
_max_height = 900
_debug = True
_verbose_level = {0:'silent', 1:'info', 2:'debug'}
_photos_dir_path = r'K:\trainman\fb'
# _photos_dir_path = r'Y:\Pictures\instagram'
# _photos_dir_path = r'C:\Users\kogut\Pictures\sky'
_thumb_dir = r'C:\Users\kogut\Documents\.kpics'
_thumb_height = 123


def print_info(msg, level=0):
    if _debug == True and level <= 1:
        print_info(msg)

def access_filesystem(path):
    """
    Checks if the specified filesystem path is accessible with read and write permissions.

    Args:
        path (str): The path to the filesystem resource to check.

    Returns:
        bool: True if the path is accessible with read and write permissions, 
              False if an error occurs or the path is not accessible.

    Raises:
        OSError: If an unexpected error occurs during the access check.
    """
    try:
        os.access(path, os.R_OK | os.W_OK)
    except OSError as e:
        print_info("Error accessing filesystem: %s" % e)
        return False
    return True

def show(title, image):
    """
    Displays an image in a window using OpenCV.

    Args:
        title (str): The title of the window where the image will be displayed.
        image (numpy.ndarray): The image to be displayed.

    Notes:
        - The function waits for a key press to close the window.
        - The window is destroyed after the key press.
    """
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def resize(image):
    """
    Resize an image to fit within the maximum width and height constraints.
    Parameters:
        image (numpy.ndarray): The input image to be resized. It is expected to be a NumPy array.
    Returns:
        numpy.ndarray: The resized image if resizing is successful, or the original image if an error occurs.
    Notes:
        - The function uses the global variables `_max_width` and `_max_height` to determine the maximum dimensions.
        - If the image dimensions exceed the maximum constraints, the image is resized while maintaining its aspect ratio.
        - If an error occurs during resizing, the original image is returned, and an error message is printed.
    """
    image_width, image_height = image.shape[:2]

    if image_width > _max_width or image_height > _max_height:
        proportion = image_width / image_height
        try:
            return cv2.resize(image, (_max_width, _max_height))
        except Exception as e:
            print_info("Error resizing image: %s" % e)
            return image

def md5(str):
    """
    Computes the MD5 hash of a given string.

    Args:
        str (str): The input string to hash.

    Returns:
        str: The hexadecimal representation of the MD5 hash.

    Note:
        This function requires the `hashlib` module to be imported.
        The input string must be encoded to bytes before hashing.
    """
    return hashlib.md5(str).hexdigest()

def scan_dir(_photos_dir_path):
    """
    Scans a directory for image files and returns a dictionary of their paths.
    This function traverses the given directory recursively, identifying files
    with specific image extensions (.jpg, .jpeg, .png). It collects the full
    paths of these files and stores them in a dictionary, where the keys are
    incremental integers starting from 0, and the values are the corresponding
    file paths.
    Args:
        _photos_dir_path (str): The path to the directory to scan for image files.
    Returns:
        dict: A dictionary where keys are integers and values are the full paths
              of the image files found in the directory. Returns an empty dictionary
              if no image files are found or if the provided path is not a directory.
    Notes:
        - The function prints informational messages during the scanning process.
        - If the provided path is not a directory, the function prints an error
          message and returns 0.
    """
    _photos = []
    _photo_list = {}
    if not os.path.isdir(_photos_dir_path):
        print_info("Photos dir path is not a directory: %s" % _photos_dir_path, level=1)
        return 0
    print_info("Start scanning photos directory in: %s" % _photos_dir_path, level=1)
    for root, sub_folder, files in os.walk(_photos_dir_path):
        
        if '_files' not in root:

            print_info("scan root dir: %s" % root, level=1)
            
            if len(files) > 0:
                for _file in files:
                    _file_name = _file.endswith(_file)
                    _extension = pathlib.Path(_file).suffix
                    if(_extension in ('.jpg', '.jpeg', '.png')):
                        _full_path = os.path.join(root, _file)
                        print_info("Full path: %s" % _full_path, level=1)
                        _photos.append(_full_path)
                        _photo_list[len(_photo_list)] = _full_path

    return _photo_list


def thumb(_photo_path):
    _thumb_dir = r'C:\Users\kogut\Documents\.kpics'


if __name__ == '__main__':
    _photos_dir_path = r'K:\trainman\fb'
    # _photos_dir_path = r'Y:\Pictures\instagram'
    # _photos_dir_path = r'C:\Users\kogut\Pictures\sky'
    _thumb_dir = r'C:\Users\kogut\Documents\.kpics'
    _thumb_height = 123
    _photos = scan_dir(_photos_dir_path)
    _html = ''
    _thumb_dir_name = hashlib.md5(_photos_dir_path.encode()).hexdigest()
    _thumb_dir_path = os.path.join(_thumb_dir, _thumb_dir_name)
    id = 0
    if os.path.isdir(_thumb_dir_path) == False:    
        try:
            os.mkdir(_thumb_dir_path)
        except OSError:
            print_info("Creation of the directory %s failed" % _thumb_dir_path)
        except FileExistsError:
            print_info("Directory %s already exists" % _thumb_dir_path)
    for _photo_id in _photos:
        # if _photo_id is 10:
            # break
        _path = _photos[_photo_id]
        _thumb_name = "%s.%s" % (hashlib.md5(_path.encode()).hexdigest(), _path.split('.')[-1])
        # _thumb_path = os.path.join(_thumb_dir_path, _thumb_name)
        _thumb_full_path = os.path.join(_thumb_dir_path, _thumb_name)
        if os.path.isfile(_path) and not os.path.isfile(_thumb_full_path):
            photo = cv2.imread(_path)
            if photo is None:
                print_info("Ignoring wrong photo file path: %s" % _path, level=1)
                continue
            print_info("photo dimmension for: %s" % _path)
            photo_height, photo_width = photo.shape[:2]
            # proportion = photo_width / photo_height
            thumb_height = _thumb_height

            # scale = photo_height / thumb_height
            # thumb_width = int(photo_width / scale) 
            # if photo_height > photo_width:
            #     thumb_width = photo_width / scale
            # elif photo_height < photo_width:
            #     thumb_width = photo_width / scale
            # else:
            #     thumb_width = photo_width / scale
            thumb_width = int((thumb_height * photo_width) / photo_height)
            print_info("%sx%s -> %sx%s: %s" % (photo_width, photo_height, thumb_width, thumb_height, _path))
            # if (thumb_width / thumb_height) is not proportion:
                # print_info("wrong photo dimmension for file: %s => %s" % (_path, proportion))
            _thumb = cv2.resize(photo, (int(thumb_width), int(thumb_height)), thumb_width/photo_width, thumb_height/photo_height)
            cv2.imwrite(_thumb_full_path, _thumb)

            _html += '<a id="photo-' + str(id) + '" href="' + _path + '" class="thumb" title="' + os.path.basename(_path) + ' in ' + os.path.dirname(_path) + '">'
            _html += '<img src="' + _thumb_full_path + '" alt="'+ os.path.basename(_thumb_full_path) + '" width="'+ str(thumb_width) +'" height="'+ str(thumb_height) + '"/>'
            _html += '</a>'
            id += 1
            # print_info(_thumb_full_path)

_html_name = 'index.html'
_html_path = os.path.join(_thumb_dir_path, _html_name)

_template_head_path = r'Y:\dev\topik-1\template\kpics\head_index.html'
_template_end_path = r'Y:\dev\topik-1\template\kpics\end_index.html'
_css = r'Y:\dev\topik-1\template\kpics\index.css'
html = ''

_template = ''
with open(_template_head_path) as f:
    lines = f.readlines()
    for line in lines:
        _template += line
    # html += lines.splitlines()

_template_footer = ''
with open(_template_end_path) as f:
    lines = f.readlines()
    for line in lines:
        _template_footer += line
    
with open(_html_path, 'w') as f:
    f.writelines(_template)
    f.writelines(_html)
    f.writelines(_template_footer)
# print_info(_template)
# html += _html


# html += _template.splitlines()
# _html = html
# with open(_html_path, 'w') as f:
#     f.writelines(_html)

import shutil
css_path = os.path.join(_thumb_dir_path, os.path.basename(_css))
if not os.path.isfile(css_path):
    shutil.copy2(_css, css_path)