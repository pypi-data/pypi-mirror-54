import pip
import os
import sys
import platform
import subprocess
from pathlib import Path
from tabpy.models.utils import setup_utils

# pip 10.0 introduced a breaking change that moves the location of main
try:
    from pip import main
except ImportError:
    from pip._internal import main


def install_dependencies(packages):
    pip_arg = ['install'] + packages + ['--no-cache-dir']
    if hasattr(pip, 'main'):
        pip.main(pip_arg)
    else:
        pip._internal.main(pip_arg)


def main():
    install_dependencies(['sklearn', 'pandas', 'numpy',
                          'textblob', 'nltk', 'scipy'])
    print('==================================================================')
    # Determine if we run python or python3
    if platform.system() == 'Windows':
        py = 'python'
    else:
        py = 'python3'

    if len(sys.argv) > 1:
        config_file_path = sys.argv[1]
    else:
        config_file_path = setup_utils.get_default_config_file_path()
    print(f'Using config file at {config_file_path}')
    port, auth_on, prefix = setup_utils.parse_config(config_file_path)
    if auth_on:
        auth_args = setup_utils.get_creds()
    else:
        auth_args = []

    directory = str(Path(__file__).resolve().parent / 'scripts')
    # Deploy each model in the scripts directory
    for filename in os.listdir(directory):
        subprocess.run([py, f'{directory}/{filename}', config_file_path]
                       + auth_args)


if __name__ == '__main__':
    main()
