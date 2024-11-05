# file: interactive_client.py

import argparse
from ctf_library.io.remote_connection import RemoteConnection
from ctf_library.io.remote_connection_shell import InteractiveClientShell

default_host = 'localhost'
default_port = 8000

def main():
    parser = argparse.ArgumentParser(
        prog='interactive-client',
        description='A client that send the user input to the server'
    )
    parser.add_argument('--host', default=default_host,
                        help=f'host name to connect to (default={default_host})')
    parser.add_argument('--port', type=int, default=default_port,
                        help=f'port number to connection to (default={default_port})')
    parser.add_argument('--single_line', action='store_true', default=False,
                        help='use an interactive shell that read a single line')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='run in debug mode')
    args = parser.parse_args()
    
    shell = InteractiveClientShell(debug=args.debug)
    if args.single_line:
        RemoteConnection.open_connection(
            args.host, args.port, shell.interactive
        )
    else:
        RemoteConnection.open_connection(
            args.host, args.port, shell.interactive_unbounded
        )
    return

if __name__ == '__main__':
    main()

# --- end of file --- #
