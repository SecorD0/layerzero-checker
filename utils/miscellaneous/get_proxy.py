import random
from typing import Optional

from pretty_utils.miscellaneous.files import read_lines

from data import config
from utils.db_api.models import Address


def get_proxy(address_instance: Optional[Address] = None) -> Optional[str]:
    proxy = None
    if address_instance and address_instance.proxy:
        proxy = address_instance.proxy

    else:
        proxies = read_lines(path=config.PROXIES_FILE, skip_empty_rows=True)
        if proxies:
            proxy = random.choice(proxies)

    if (
            proxy and
            'http' not in proxy
            and 'socks5' not in proxy
    ):
        proxy = f'http://{proxy}'

    return proxy
