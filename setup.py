# This file is part of applesauce.
#
# applesauce is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# applesauce is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with applesace.  If not, see <http://www.gnu.org/licenses/>.
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

