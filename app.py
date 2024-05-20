import logging

from utils.miscellaneous.create_files import create_files
from data import config
from data.models import ProgramAction
from functions.check_addresses import check_addresses
from functions.parse_data import parse_data

if __name__ == '__main__':
    print(f'\nSoftware version: {config.GREEN}{config.VERSION}{config.RESET_ALL}\n')
    create_files()
    while True:
        action = None
        print('''Select the action:
1) Parse data about sybil addresses;
2) Check specified addresses if they are sybil;
3) Exit.''')
        try:
            action = int(input('> '))
            print()
            if action == ProgramAction.ParseData:
                parse_data()

            elif action == ProgramAction.CheckAddresses:
                check_addresses()

            else:
                break

        except KeyboardInterrupt:
            print()

        except ValueError:
            print(f"{config.RED}You didn't enter a number!{config.RESET_ALL}")

        except BaseException as e:
            logging.exception('main')
            print(f'\n{config.RED}Something went wrong: {e}{config.RESET_ALL}\n')

        if action:
            input(f'\nPress {config.LIGHTGREEN_EX}Enter{config.RESET_ALL} to exit.\n')
            break
