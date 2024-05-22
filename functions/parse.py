import logging
import os
import re
import time
import urllib.request

import requests
from pretty_utils.miscellaneous.files import read_lines
from pretty_utils.type_functions.lists import split_list

from data import config
from utils.db_api.database import db
from utils.db_api.models import MarkedAddress, ReportedAddress, Base


def parse() -> None:
    try:
        if db.one(MarkedAddress) or db.one(ReportedAddress):
            print(
                f"You've already parsed data about sybil addresses. Do you want to delete it and start over? "
                f"({config.LIGHTGREEN_EX}y{config.RESET_ALL}/{config.RED}n{config.RESET_ALL})"
            )
            answer = input('> ')
            print()
            if answer != 'y':
                return

            db.execute('DROP TABLE marked_addresses')
            db.execute('DROP TABLE reported_addresses')
            db.create_tables(Base)

        print(f'Downloading the {config.LIGHTGREEN_EX}initialList.txt{config.RESET_ALL} file from LayerZero GitHub...')
        if not os.path.isfile(config.initialList):
            urllib.request.urlretrieve(
                url='https://raw.githubusercontent.com/LayerZero-Labs/sybil-report/main/initialList.txt',
                filename=config.initialList
            )

        print(f'Importing addresses from the text file to the DB...')
        sybil_addresses = read_lines(config.initialList)
        i = 0
        for address_list in split_list(s_list=sybil_addresses, n=10000):
            try:
                insert_it = []
                for address in address_list:
                    insert_it.append(MarkedAddress(address=address))
                    i += 1

                db.insert(insert_it)
                print(f'{i}/{len(sybil_addresses)}')

            except:
                logging.exception('marked_as_sybil')

        print(f'A total of {config.LIGHTGREEN_EX}{len(sybil_addresses)}{config.RESET_ALL} addresses were parsed.')

        print('Parsing reported addresses from the GitHub issues...')
        total_reported = 0
        for page in range(100):
            insert_it = []
            response = requests.get(
                f'https://api.github.com/repos/LayerZero-Labs/sybil-report/issues?state=open&per_page=100&page={page}'
            )
            issues = response.json()
            if isinstance(issues, dict):
                message = issues.get('message')
                if message:
                    print(f"\n{config.RED}Failed to use the GitHub API: {message}{config.RESET_ALL}\n")
                    break

            if not issues:
                break

            for issue in issues:
                try:
                    body: str = issue.get('body')
                    if body:
                        addresses = re.findall('0x' + r'\w' * 40, body.lower())
                        for address in addresses:
                            insert_it.append(ReportedAddress(address=address, issue_id=issue.get('number')))

                except:
                    logging.exception('issue')

            db.insert(insert_it)
            total_reported += len(insert_it)
            print(f'Page {config.LIGHTGREEN_EX}{page + 1}{config.RESET_ALL} was parsed.')
            time.sleep(2)

        print(f'A total of {config.LIGHTGREEN_EX}{total_reported}{config.RESET_ALL} addresses were reported.')

    except BaseException as e:
        logging.exception('parse')
        print(f"\n{config.RED}Something went wrong in the 'parse' function: {e}{config.RESET_ALL}\n")
