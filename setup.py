
import os

from setuptools import setup
from Cython.Build import cythonize
from setuptools import setup, find_packages


EXCLUDE_FILES = [
    'main.py',
    'runpyuic.py',
    '__init__.py'
]


def get_ext_paths(root_dir, exclude_files):
    """get filepaths for compilation"""
    paths = []
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if os.path.splitext(filename)[1] != '.py':
                continue
            if filename in exclude_files:
                continue
            file_path = os.path.join(root, filename)
            paths.append(file_path)
    return paths


setup(
    name='app',
    version='0.1.0',
    packages=find_packages(),
    ext_modules=cythonize(get_ext_paths('gui', EXCLUDE_FILES),
                          compiler_directives={'language_level': 3}
                          )
)
