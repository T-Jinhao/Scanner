#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

import threading
from interactive.funcs import util
from interactive.completer import modules

Commands = {
    'info': [],
    'set': [],
    'usemodule': modules.usemodule,
    'run': [],
    'main': [],
    'help': [],
    'exit': []
}

Usage = {
    'info': 'Display worker module options.',
    'help': 'Displays the help menu.',
    'exit': 'Exit Scanner.',
    'main': 'Back to the main menu.',
    'run': 'Start the given worker module.',
    'usemodule': 'Use a Scanner module.',
    'set': 'Set a worker option.'
}

Info = {
    'Taskname': ['False', '', 'The uniquely identifies of current work.']
}