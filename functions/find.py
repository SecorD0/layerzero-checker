import asyncio
import logging
import random
from typing import List

import aiohttp
from aiohttp_socks import ProxyConnector
from latest_fake_useragent import UserAgent
from pretty_utils.type_functions.lists import split_list
from pretty_utils.type_functions.strings import format_number

from data import config
from functions.General import General
from utils.db_api.database import db, get_addresses
from utils.db_api.models import Address
from utils.miscellaneous.get_proxy import get_proxy


async def check(sem: asyncio.Semaphore, address_instance: Address):
    async with sem:
        await asyncio.sleep(random.randint(2, 10))
        try:
            proxy = get_proxy(address_instance=address_instance)
            connector = ProxyConnector.from_url(url=proxy.replace('socks5h', 'socks5'), rdns=True, force_close=True)
            headers = {
                'accept': '*/*',
                'accept-language': 'en',
                'priority': 'u=1, i',
                'referer': 'https://www.layerzero.foundation/eligibility',
                'user-agent': UserAgent().chrome,
            }
            async with aiohttp.ClientSession(headers=headers, connector=connector, connector_owner=False) as session:
                async with session.get(
                        url=f'https://www.layerzero.foundation/api/allocation/{address_instance.address.lower()}',
                        headers=headers,
                ) as response:
                    try:
                        response = await response.json()
                        address_instance.is_eligible = response.get('isEligible')
                        address_instance.drop_amount = response['zroAllocation'].get('asString')

                        cards = response.get('cards')
                        if cards:
                            address_instance.number_of_txs = cards.get('numberOfTx')
                            address_instance.number_of_networks = cards.get('numberOfChains')
                            topChains = cards.get('topChains')
                            if topChains:
                                address_instance.top_network = topChains[0]['chainName']

                            topProtocols = cards.get('topProtocols')
                            if topProtocols:
                                address_instance.top_protocol = topProtocols[0]['protocolName']

                    except:
                        if response.status == 403:
                            print(f"{config.RED}This proxy doesn't have access to the API: {proxy}{config.RESET_ALL}")

                        else:
                            logging.exception(f'get_request {response.status}')

        except:
            logging.exception('check')


async def run_checking(addresses: List[Address]):
    tasks = []
    sem = asyncio.Semaphore(1000)

    for address in addresses:
        task = asyncio.ensure_future(check(sem, address))
        tasks.append(task)

    await asyncio.gather(*tasks)


def find(loop) -> None:
    try:
        if not get_proxy():
            print(
                f"It's recommended to use a list of proxies for random selection. You haven't added any proxies. "
                f"Do you want to continue? ({config.LIGHTGREEN_EX}y{config.RESET_ALL}/{config.RED}n{config.RESET_ALL})"
            )
            answer = input('> ')
            print()
            if answer != 'y':
                return

        try:
            open(file=config.ADDRESSES_FILE, mode='r+')

        except IOError:
            print(f"{config.RED}You didn't close the {config.ADDRESSES_FILE} file!{config.RESET_ALL}")
            return

        print(f'Importing addresses from the spreadsheet to DB...')
        General.import_addresses()

        addresses = get_addresses()
        if not addresses:
            print(f"{config.RED}You didn't specify a single address!{config.RESET_ALL}")
            return

        not_checked_addresses = db.all(Address, Address.top_network.is_(None))
        asyncio.set_event_loop(loop)
        i = 0
        for address_list in split_list(s_list=not_checked_addresses, n=10):
            future = asyncio.ensure_future(run_checking(addresses=address_list))
            loop.run_until_complete(future)
            db.commit()
            i += 10
            print(f'{i}/{len(addresses)}')

        eligible_addresses = db.all(Address, Address.is_eligible.is_(True))
        total_tokens = 0
        for address in eligible_addresses:
            total_tokens += address.drop_amount

        average_amount = round(total_tokens / len(eligible_addresses)) if eligible_addresses else 0
        print(f'''

Eligible addresses: {config.LIGHTGREEN_EX}{format_number(len(eligible_addresses))}/{format_number(len(addresses))} ({round(len(eligible_addresses) / len(addresses) * 100, 2)}%){config.RESET_ALL}
Total tokens: {config.LIGHTGREEN_EX}{format_number(total_tokens)}{config.RESET_ALL}
Average tokens: {config.LIGHTGREEN_EX}{format_number(average_amount)}{config.RESET_ALL}''')

        General.export_addresses()
        not_checked_addresses = db.all(Address, Address.top_network.is_(None))
        if not_checked_addresses:
            print(
                f"\nThere are {config.RED}{len(not_checked_addresses)}{config.RESET_ALL} unchecked addresses left, "
                f"it's recommended to wait a while or refresh the proxy list and run the check again. "
                f"If you don't want to do this, manually delete the "
                f"{config.LIGHTGREEN_EX}{config.ADDRESSES_DB}{config.RESET_ALL} file."
            )

        else:
            db.execute('DROP TABLE addresses')

    except BaseException as e:
        logging.exception('find')
        print(f"\n{config.RED}Something went wrong in the 'find' function: {e}{config.RESET_ALL}\n")
