from typing import List

from pretty_utils.databases import sqlalchemy_

from utils.db_api.models import Base, Address


# --- Functions
def get_addresses() -> List[Address]:
    return db.all(Address)


# --- Miscellaneous
db = sqlalchemy_.DB('sqlite:///files/addresses.db', pool_recycle=3600, connect_args={'check_same_thread': False})

db.create_tables(Base)
