#!/usr/bin/python3
import os

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
UI_FILES = [os.path.join(THIS_DIR, ui_file) for ui_file in os.listdir(THIS_DIR) if ui_file.endswith('.ui')]
PYUIC5_PATH = r'env\Scripts\pyuic5.exe' if os.name == 'nt' else 'pyuic5'

for ui_file in UI_FILES:
    py_file = ui_file[:-3] + '_ui.py'
    cmd = PYUIC5_PATH + ' -x ' + ui_file + ' -o ' + py_file
    os.system(cmd)
