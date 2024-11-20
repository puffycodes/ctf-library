# file: ctf_challenge_shell.py

import re
from ctf_library.hash.hash_search import HashSearch

class HTVChallengeShell:

    # Challenge String:
    #
    # Give me input where sha256(LtrUUo1tkRuwS24O + input).hexdigest().endswith('0'*6)
    # Answer (limit 1024 bytes)> 

    def __init__(self):
        self.challenge_re = r'.*sha256\((.*) \+ input\).*endswith\((.*)\)'
        return

    # PoW challenge for hack the vote 2024
    async def answer_challenge(self, reader, writer, debug=False):
        inp = await reader.readuntil(separator=b'> ')
        if inp:
            print(f'{inp.decode()}', end='')
            match_result = re.match(self.challenge_re, inp.decode())
            if debug:
                print(match_result)
            if match_result != None:
                if debug:
                    print(match_result.group(0))
                    print(match_result.group(1))
                    print(match_result.group(2))
                prefix = match_result.group(1)
                search_target = match_result.group(2)
                if search_target == "'0'*6":
                    search_target = '000000'
                reply = HashSearch.search_hash_htv(prefix, search_target)
                if reply == None:
                    print(f'cannot find a hash')
                    exit()
                else:
                    print(reply)
                writer.write(reply + '\n')
                await writer.drain()
        return
        
# --- end of file --- #
