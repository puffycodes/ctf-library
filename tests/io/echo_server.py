# file: echo_server.py

import argparse
from ctf_library.io.remote_connection import RemoteConnection
from ctf_library.io.remote_connection_shell import EchoServerShell

default_port = 8000

def main():
    parser = argparse.ArgumentParser(
        prog='echo-server',
        description='A server that echos back what it received'
    )
    parser.add_argument('--port', type=int, default=default_port,
                        help=f'port number to listen on (default={default_port})')
    parser.add_argument('--echo_count', type=int, default=1,
                        help='the number of times to echo the input from client')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='run in debug mode')
    args = parser.parse_args()

    shell = EchoServerShell(echo_count=args.echo_count, debug=args.debug)
    RemoteConnection.create_server(args.port, shell.echo_till_bye)

    return

if __name__ == '__main__':
    main()

# --- end of file --- #
