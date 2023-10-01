import glob
import os
cwd = os.getcwd()
py_list = glob.glob('events/*.py')
py_list.remove('events/__init__.py')
def cut_py(file_path):
    file_path = file_path.replace('.py', '')
    file_path = file_path.replace('events/', '')
    return file_path
__all__ = list(map(cut_py, py_list))