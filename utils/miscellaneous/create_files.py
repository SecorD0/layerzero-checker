from pretty_utils.miscellaneous.files import touch

from data import config
from utils.miscellaneous.create_spreadsheet import create_spreadsheet


def create_files():
    touch(config.FILES_DIR)
    create_spreadsheet(path=config.ADDRESSES_FILE, headers=('address',), sheet_name='Addresses')


create_files()
