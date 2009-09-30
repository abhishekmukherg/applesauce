# bootstrap setuptools if necessary
from ez_setup import use_setuptools
use_setuptools()
#from distutils.core import setup

VERSION=0.1

from setuptools import setup

setup(name="applesauce",
        version=VERSION,
        packages=["applesauce", "applesauce.sprite"],
        scripts=["main.py"],
        install_requires = ['pygame'],
        package_data = {
            'gummy_panzer': ['images/*.png'],
        }
)

