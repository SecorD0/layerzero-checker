import os
import platform
import sys
from pathlib import Path

from colorama import Fore, Style

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()

else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

if platform.system() == 'Windows':
    GREEN = ''
    LIGHTGREEN_EX = ''
    RED = ''
    BLUE = ''
    RESET_ALL = ''

else:
    GREEN = Fore.GREEN
    LIGHTGREEN_EX = Fore.LIGHTGREEN_EX
    RED = Fore.RED
    BLUE = Fore.BLUE
    RESET_ALL = Style.RESET_ALL

FILES_DIR = os.path.join(ROOT_DIR, 'files')

ADDRESSES_DB = os.path.join(FILES_DIR, 'addresses.db')

ERRORS_FILE = os.path.join(FILES_DIR, 'errors.log')

ADDRESSES_FILE = os.path.join(FILES_DIR, 'addresses.xlsx')
initialList = os.path.join(FILES_DIR, 'initialList.txt')

VERSION = '1.1.0'
