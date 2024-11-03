# file: remote_connection_shell.py

#from common_util.hexdump import HexDump

class EchoServerShell:

    def __init__(self, debug=False):
        self.debug = debug
        return

    async def echo_till_bye(self, reader, writer):
        while True:
            # read input from client, including the newline '\n'
            inp = await reader.readline()
            if inp:
                if self.debug:
                    print(f'DEBUG: from client: "{inp}"')
                writer.write(f'{inp}')
                await writer.drain()
                if inp == 'bye\n':
                    if self.debug:
                        print(f'DEBUG: ending session')
                    writer.close()
                    break
            else:
                break
        return
    
class InteractiveClientShell:

    def __init__(self, debug=False):
        self.debug = debug
        self.eof = False
        return

    async def interactive_old(self, reader, writer):
        #while not reader.at_eof():
        while True:
            # read user input, which does not include newline '\n'
            user_inp = input('> ')
            if self.debug:
                print(f'DEBUG: user input: "{user_inp}"')
            writer.write(f'{user_inp}\n')
            await writer.drain()
            inp = await reader.read(1024)
            if inp:
                print(f'{inp}', end='')
            else:
                if self.debug:
                    print(f'DEBUG: EOF')
                break
        return

    async def interactive(self, reader, writer, user_prompt='> ', server_prompt='\n'):
        while True:
            user_input = input(user_prompt)
            if self.debug:
                print(f'DEBUG: user input: "{user_input}"')
            writer.write(user_input + '\n')
            await writer.drain()
            await self.get_response(reader, writer, until=server_prompt)
            if self.eof == True:
                break
        return
    
    async def get_response(self, reader, writer, until='\n'):
        if len(until) <= 0:
            raise ValueError(f'value of until cannot be empty')
        until_length = len(until)
        response = []
        while True:
            # use reader.read(1) instead of reader.readuntil(separator=until) because we want
            # to see what comes before the character stream (usually the server prompt) that
            # we are looking for
            inp = await reader.read(1)
            if inp:
                response.append(inp)
                print(f'{inp}', end='')
                # break because we have come to the server prompt
                if len(response) >= until_length and ''.join(response[-until_length:]) == until:
                    break
            else:
                # break because we have come to the EOF
                self.eof = True
                print(f'<EOF>', end='')
                break
        #if self.debug:
        #    print(HexDump.to_text(''.join(response).encode()))
        return
        
# --- end of file --- #
