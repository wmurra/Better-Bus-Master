import sys 
from pathlib import Path

import yaml
from colorama import Fore, Style, init

FROZEN = getattr(sys, 'frozen', False)

def read_yaml()->tuple[str,str,bool]:
    """
    Returns: name, version, debug (as bool)
    """
    yaml_path = get_yaml_path()
    if not yaml_path.exists():
        raise FileNotFoundError
    with yaml_path.open('r') as f:
        data:dict = yaml.safe_load(f)
        name = data.get('name', '')
        version = data.get('version', '')
        debug = data.get('debug', False)
    return name, version, debug

def get_yaml_path(frozen=False)->Path:
    if FROZEN:
        return Path(sys._MEIPASS, 'application.yaml')
    return Path('application.yaml')

def format_info(app_name, version, debug):
    return (
        f'{Fore.LIGHTBLACK_EX}APP INFO: {Fore.RESET}'
        f'{Fore.CYAN}app_name:{Fore.RESET}{app_name}'
        f'{Fore.CYAN}version: {Fore.RESET}{version}'
        f'{Fore.CYAN}debug: {Fore.RESET}{debug}'
    )

def main():
    init(autoreset=True)
    return format_info(*read_yaml())

if __name__ == "__main__":
    main()
