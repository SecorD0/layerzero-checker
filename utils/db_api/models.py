from typing import Optional

from pretty_utils.type_functions.classes import AutoRepr
from sqlalchemy import (Column, Integer, Text, Boolean, Float)
from sqlalchemy.orm import declarative_base

# --- Wallets
Base = declarative_base()


class Address(Base, AutoRepr):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    address = Column(Text, unique=True)
    proxy = Column(Text)
    is_eligible = Column(Boolean)
    drop_amount = Column(Float)
    number_of_txs = Column(Integer)
    number_of_networks = Column(Integer)
    top_network = Column(Text)
    top_protocol = Column(Text)

    def __init__(
            self, address: str, proxy: Optional[str] = None, is_eligible: bool = False, drop_amount: bool = 0.0,
            number_of_txs: int = 0, number_of_networks: int = 0, top_network: Optional[str] = None,
            top_protocol: Optional[str] = None
    ) -> None:
        self.address = address
        self.proxy = proxy
        self.is_eligible = is_eligible
        self.drop_amount = drop_amount
        self.number_of_txs = number_of_txs
        self.number_of_networks = number_of_networks
        self.top_network = top_network
        self.top_protocol = top_protocol
