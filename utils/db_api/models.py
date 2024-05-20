from pretty_utils.type_functions.classes import AutoRepr
from sqlalchemy import (Column, Integer, Text, Boolean)
from sqlalchemy.orm import declarative_base

# --- Wallets
Base = declarative_base()


class MarkedAddress(Base, AutoRepr):
    __tablename__ = 'marked_addresses'

    id = Column(Integer, primary_key=True)
    address = Column(Text, unique=True)

    def __init__(self, address: str) -> None:
        self.address = address


class ReportedAddress(Base, AutoRepr):
    __tablename__ = 'reported_addresses'

    id = Column(Integer, primary_key=True)
    address = Column(Text)
    issue_id = Column(Integer)

    def __init__(self, address: str, issue_id: int) -> None:
        self.address = address
        self.issue_id = issue_id


class CheckingAddress(Base, AutoRepr):
    __tablename__ = 'checking_addresses'

    id = Column(Integer, primary_key=True)
    address = Column(Text, unique=True)
    marked_as_sybil = Column(Boolean)
    number_of_reports = Column(Integer)
    issue_ids = Column(Text)

    def __init__(
            self, address: str, marked_as_sybil: bool = False, number_of_reports: bool = 0, issue_ids: str = ''
    ) -> None:
        self.address = address
        self.marked_as_sybil = marked_as_sybil
        self.number_of_reports = number_of_reports
        self.issue_ids = issue_ids
