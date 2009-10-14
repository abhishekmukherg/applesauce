# bootstrap setuptools if necessary
from distribute_setup import use_setuptools
use_setuptools()
#from distutils.core import setup

VERSION=0.1

from setuptools import setup

setup(name="applesauce",
        version=VERSION,
        packages=["applesauce", "applesauce.sprite"],
        entry_points={
            'gui_scripts': ['applesauce=applesauce.game:main'],
        },
        install_requires = ['pygame'],
        package_data = {
            'applesauce': ['images/*.png', 'level_data/*.ini'],
        },
        test_suite="tests.suite",
)

