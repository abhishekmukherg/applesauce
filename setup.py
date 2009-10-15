# bootstrap setuptools if necessary
#from distribute_setup import use_setuptools
#use_setuptools()
import setuptools
from distutils.core import setup
import py2exe

VERSION=0.1

#from setuptools import setup

setup(name="applesauce",
        version=VERSION,
        packages=["applesauce", "applesauce.sprite"],
        entry_points={
            'gui_scripts': ['applesauce=applesauce.game:main'],
        },
        scripts=['main.py'],
        install_requires = ['pygame'],
        package_data = {
            'applesauce': ['images/*.png', 'level_data/*.ini', 'sounds/*.ogg'],
        },
        test_suite="tests.suite",
)

