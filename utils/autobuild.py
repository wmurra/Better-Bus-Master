import platform
import subprocess
from pathlib import Path

from utils.read_yaml import read_yaml

def main():
    name, _, _ = read_yaml()
    frontend_path = Path(name, 'frontend')
    if platform.system() == 'Windows':
        command = f'start cmd /K "cd /d {frontend_path} && npm install && npm run autobuild'
    elif platform.system() == 'Darwin':
        command = f'osascript -e \'tell application "Terminal" to do script "cd {frontend_path} && npm install && npm run autobuild"\''
    subprocess.Popen(command, shell=True)

if __name__ == '__main__':
    main()