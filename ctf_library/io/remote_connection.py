# file: remote_connection.py

'''
Remote Connection

A set of wrapper functions around the Telnetlib3 library for easy running
of server and client code.
'''

# Ref: https://github.com/jquast/telnetlib3/
# Ref: https://telnetlib3.readthedocs.io/en/latest/
# Ref: https://stackoverflow.com/questions/75778543/python-telnetlib3-examples

import asyncio, telnetlib3

class RemoteConnection:
    '''
    In all functions:

        The parameter shell is a function with the following signature:

            async def shell(reader, writer)

        where reader is a TelnetReader and writer is a TelnetWriter.
    '''

    @staticmethod
    def open_connection(host, port, shell):
        '''
        Open a connection to host:port and run shell
        '''
        loop = asyncio.get_event_loop()
        coro = telnetlib3.open_connection(host, port, shell=shell)
        reader, writer = loop.run_until_complete(coro)
        loop.run_until_complete(writer.protocol.waiter_closed)
        return
    
    @staticmethod
    async def open_connection_async(host, port, shell):
        '''
        Open a connection to host:port and run shell

        Usage:

            asyncio.run(RemoteConnection.open_connection_async(host, port, shell))

        or

            # When event_loop is already running, e.g. in Jupyter Notebook,
            # simply wait on the coroutine to complete.
            await RemoteConnection.open_connection_async(host, port, shell)
        '''
        reader, writer = await telnetlib3.open_connection(
            host, port, shell=shell
        )
        await writer.protocol.waiter_closed
        return
    
    @staticmethod
    def create_server(port, shell, host=None):
        '''
        Wait for connections on port and process using shell
        '''
        loop = asyncio.get_event_loop()
        coro = telnetlib3.create_server(host=host, port=port, shell=shell)
        server = loop.run_until_complete(coro)
        loop.run_until_complete(server.wait_closed())
        return
    
    @staticmethod
    async def create_server_async(port, shell, host=None):
        '''
        Wait for connections on port and process using shell

        Usage:

            # Create and run a separate server task
            server_task = asyncio.create_task(RemoteConnection.create_server_async(port, shell))

        or

            # Wait on the completion of the server task
            await RemoteConnection.create_server_async(port, shell)
        '''
        server = await telnetlib3.create_server(host=host, port=port, shell=shell)
        await server.wait_closed()
        return
    
# --- end of file --- #
