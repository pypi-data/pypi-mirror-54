from pathlib import Path
from subprocess import Popen, PIPE
import requests
import os

from RattletrapPython.version import __version__

rattletrap_path = Path(__file__).absolute().parent / 'rattletrap.exe'

class rattletrapException(Exception):
    pass

def get_binary():
    rattletrap_version = __version__
    rattletrap_link_windows = f"https://github.com/tfausak/rattletrap/releases/download/{rattletrap_version}/rattletrap-{rattletrap_version}-windows.exe"
    rattletrap_response = requests.get(rattletrap_link_windows)
    rattletrap_path.open("wb").write(rattletrap_response.content)

def check_for_binary():
    if not os.path.isfile(rattletrap_path):
        print('Downloading Rattletrap Binary')
        get_binary()

def parse(replay: str, json: Path, compact = False):
    check_for_binary()
    if not os.path.isfile(replay):
        raise FileNotFoundError
    run_command(replay, json, mode='decode')

def generate(json: str, replay: Path):
    check_for_binary()
    if not os.path.isfile(json):
        raise FileNotFoundError
    run_command(json, replay, mode='encode')

def run_command(input: str, output: str, mode: str, compact=False, fast=False):
    compact_arg = '-c'
    fast_arg = '-f'
    mode_arg = '-m'
    input_arg = '-i'
    output_arg = '-o'
    modes = ['encode', 'decode']
    if mode not in modes:
        raise TypeError

    call = Popen([str(rattletrap_path), input_arg, input, output_arg, output, mode_arg, mode], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = call.communicate(b"input data that is passed to subprocess' stdin")
    if call.returncode != 0:
        # an error happened!
        err_msg = "%s. Code: %s" % (err.strip(), call.returncode)
        raise rattletrapException(err_msg)
    elif len(err):
        err_msg = "%s. Code: %s" % (err.strip(), call.returncode)
        raise rattletrapException(err_msg)