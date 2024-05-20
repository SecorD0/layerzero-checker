import logging

from pretty_utils.type_functions.lists import split_list

from data import config
from functions.General import General
from utils.db_api.database import db, get_checking_addresses
from utils.db_api.models import MarkedAddress, ReportedAddress


def check_addresses() -> None:
    try:
        if not db.all(MarkedAddress) or not db.all(ReportedAddress):
            print(f'{config.RED}Start parsing data about sybil addresses first!{config.RESET_ALL}')
            return

        try:
            open(file=config.ADDRESSES_FILE, mode='r+')

        except IOError:
            print(f"{config.RED}You didn't close the {config.ADDRESSES_FILE} file!{config.RESET_ALL}")
            return

        print(f'Importing addresses from the spreadsheet to DB...')
        General.import_addresses()

        print(f'\nn\taddress\tmarked_as_sybil\tnumber_of_reports\tissue_ids')
        checking_addresses = get_checking_addresses()
        total_marked = 0
        total_reported = 0
        n = 1
        for address_list in split_list(s_list=checking_addresses, n=100):
            for address_instance in address_list:
                if db.one(MarkedAddress, MarkedAddress.address == address_instance.address):
                    address_instance.marked_as_sybil = True
                    total_marked += 1

                reports = db.all(ReportedAddress, ReportedAddress.address == address_instance.address)
                if reports:
                    address_instance.number_of_reports = len(reports)
                    total_reported += 1
                    for report in reports:
                        address_instance.issue_ids = f'{address_instance.issue_ids}{report.issue_id},'

                    address_instance.issue_ids = address_instance.issue_ids[:-1]

                print(
                    f'{n}\t{address_instance.address}\t{address_instance.marked_as_sybil}\t'
                    f'{address_instance.number_of_reports}\t{address_instance.issue_ids}'
                )
                n += 1

            db.commit()

        print(f'''
{config.RED}{total_marked}/{len(checking_addresses)} ({round(total_marked / len(checking_addresses) * 100, 2)}%){config.RESET_ALL} addresses marked as sybil.
{config.RED}{total_reported}/{len(checking_addresses)} ({round(total_reported / len(checking_addresses) * 100, 2)}%){config.RESET_ALL} addresses reported.''')

        General.export_addresses()

    except BaseException as e:
        logging.exception('check_addresses')
        print(f"\n{config.RED}Something went wrong in the 'check_addresses' function: {e}{config.RESET_ALL}\n")
