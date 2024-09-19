# file: remote_connection_shell.py

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
        return

    async def interactive(self, reader, writer):
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

# --- end of file --- #
