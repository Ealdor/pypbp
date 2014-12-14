# -*- coding: utf-8 -*-

# An advanced setup script to create multiple executables and demonstrate a few
# of the features available to setup scripts
#
# hello.py is a very simple 'Hello, world' type script which also displays the
# environment in which the script runs
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

import sys
from cx_Freeze import setup, Executable

options = {
    'build_exe': {
        'includes': [
            'cells',
            'constants',
            'init',
            'table'
        ]
    }
}

executables = [
    Executable('main.py')
]

setup(name='Pypbp',
      version='1.0',
      description='Paint by pairs using python and pygame',
      options=options,
      executables=executables
      )