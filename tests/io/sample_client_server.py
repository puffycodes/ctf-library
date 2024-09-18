# file: sample_client_server.py

'''
Client and Server Demo

Provide a sample client and a sample server
'''

import random
import argparse
import asyncio
from ctf_library.io.remote_connection import RemoteConnection

default_host = 'localhost'
default_port = 8000

class ClientServerDemoShell:
    '''
    Contain both the client and server shells, and other variables
    '''

    def __init__(self):
        '''
        Initializes the variables
        '''
        self.client_responses = [
            'I am good.',
            'I like python but I don\'t like snakes.',
            'The quick brown fox jumps over the lazy dog.',
        ]
        self.client_send_random_response = False
        return

    async def server_shell(self, reader, writer):
        '''
        Handle the server communication with one connected client
        '''
        writer.write('What do you have to say? ')
        inp = await reader.readline()
        if inp:
            print(f'client says this: {inp}', end='')
            writer.write(f'You said this: {inp}')
            writer.write(f'It is not easy to do echo.')
            await writer.drain()
        writer.close()
        return

    async def client_shell(self, reader, writer):
        '''
        Handle the client communication with server
        '''
        # read something
        inp = await reader.readuntil(separator=b'? ')
        if not inp:
            # end of file
            print(f'EOF', end='')
        else:
            print(f'{inp.decode()}', end='')
            # response with something
            if self.client_send_random_response:
                reply = random.choice(self.client_responses) + '\n'
                print(f'{reply}', end='')
            else:
                reply = input() + '\n'
            writer.write(reply)
            # wait for reply
            inp = await reader.read()
            if not inp:
                # end of file
                print(f'EOF', end='')
            else:
                print(f'{inp}', end='')
        print()
        return

def start_server(port):
    '''
    Start a server
    '''
    shell = ClientServerDemoShell()
    RemoteConnection.create_server(port, shell.server_shell)
    return

def start_client(host, port, send_random_response=False):
    '''
    Start a client
    '''
    shell = ClientServerDemoShell()
    shell.client_send_random_response = send_random_response
    RemoteConnection.open_connection(host, port, shell.client_shell)
    return

async def start_client_and_server_async(host, port, rounds=10, terminate=True):
    '''
    A demo on how to start both a client and a server in the
    same process
    '''
    shell = ClientServerDemoShell()
    shell.client_send_random_response = True
    server_task = asyncio.create_task(
        RemoteConnection.create_server_async(port, shell.server_shell)
    )
    for round in range(rounds):
        print(f'round {round+1}:')
        await RemoteConnection.open_connection_async(
            host, port, shell.client_shell
        )
        await asyncio.sleep(2)
    if not terminate:
        print(f'server waiting for more connections ...')
        await server_task
    return

def start_client_and_server(host, port):
    '''
    Start both client and server
    '''
    asyncio.run(start_client_and_server_async(host, port))
    return

def main():
    parser = argparse.ArgumentParser(
        prog='client-server-demo',
        description='a client and server demo'
    )
    parser.add_argument('--host', default=default_host,
                        help='name of host')
    parser.add_argument('--port', default=default_port, type=int,
                        help='port number')
    parser.add_argument('-s', '--server', action='store_true',
                        default=False,
                        help='run as a server (default is to run as a client)')
    parser.add_argument('-r', '--random', action='store_true',
                        default=False,
                        help='send a random message (only applicable to client)')
    parser.add_argument('--demo', action='store_true', default=False,
                        help='run a demo with both client and server')
    args = parser.parse_args()
    if args.demo:
        start_client_and_server(args.host, args.port)
    else:
        if args.server:
            start_server(args.port)
        else:
            start_client(args.host, args.port, send_random_response=args.random)
    return

if __name__ == '__main__':
    main()

# --- end of file --- #
