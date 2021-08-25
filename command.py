# Copyright 2021 Kristofer Henderson
#
# MIT License:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is furnished 
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
File: command.py
Author: Kris Henderson
"""

import subprocess
import os

networks = {
    'testnet': ['--testnet-magic', '1097911063'],
    'mainnet': ['--mainnet']
}

node_socket_env = {
    'testnet': 'TESTNET_CARDANO_NODE_SOCKET_PATH',
    'mainnet': 'MAINNET_CARDANO_NODE_SOCKET_PATH',
    'active': 'CARDANO_NODE_SOCKET_PATH'
}

class Command:
    @staticmethod
    def write_to_file(filename, data):
        with open(filename, 'w') as file:
            file.write(data)

    @staticmethod
    def print_command(command):
        print('Command: ', end='')
        for c in command:
            if ' ' not in c:
                print('{} '.format(c), end='')
            else:
                print('\"{}\" '.format(c), end='')
        print('')

    @staticmethod
    def run(command, network, input=None):
        envvars = os.environ

        if network != None:
            envvars[node_socket_env['active']] = os.environ[node_socket_env[network]]
            command.extend(networks[network])

        Command.print_command(command)
        try:
            completed = subprocess.run(command, check=True, capture_output=True, text=True, input=input, env=envvars)
        except subprocess.CalledProcessError as e:
            print('{} ERROR {}'.format(command[0], e.returncode))
            print('output: {}'.format(e.output))
            print('stdout: {}'.format(e.stdout))
            print('stderr: {}'.format(e.stderr))
            raise e

        # print("Command stdout: {}".format(completed.stdout.strip('\r\n')))
        return completed.stdout.strip('\r\n')
