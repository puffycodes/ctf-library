# file: remote.py

# Ref: https://github.com/jquast/telnetlib3/
# Ref: https://stackoverflow.com/questions/75778543/python-telnetlib3-examples

import asyncio, telnetlib3

class RemoteConnection:

    @staticmethod
    def open_connection(host, port, shell):
        '''
        Open a connection to host:port and run 
        
        shell is a function with the following signature:

            async def shell(reader, writer)

        where reader is a TelnetReader and writer is a TelnetWriter
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
        '''
        reader, writer = await telnetlib3.open_connection(
            host, port, shell=shell
        )
        await writer.protocol.waiter_closed
        return
    
    @staticmethod
    def create_server(port, shell):
        '''
        Wait for connections on port and process using shell
        '''
        loop = asyncio.get_event_loop()
        coro = telnetlib3.create_server(port=port, shell=shell)
        server = loop.run_until_complete(coro)
        loop.run_until_complete(server.wait_closed())
        return
    
# --- end of file --- #
