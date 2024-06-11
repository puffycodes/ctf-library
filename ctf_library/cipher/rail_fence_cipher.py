# file: rail_fence_cipher.py

class RailFenceCipher:
    
    def __init__(self):
        return
    
    def encrypt(self, text, key, offset=0, verbose=False):
        length = len(text)
        positions = self.get_positions(length, key, offset=offset, verbose=verbose)
        
        cipher_parts = []
        for _ in range(key):
            cipher_parts.append('')
        if verbose:
            print(cipher_parts)
            
        i = 0
        for pos in positions:
            cipher_parts[pos] += text[i]
            i += 1
            
        if verbose:
            print(cipher_parts)
            
        return ''.join(cipher_parts)
    
    def decrypt(self, text, key, offset=0, verbose=False):
        length = len(text)
        positions = self.get_positions(length, key, offset=offset, verbose=verbose)
        counts = self.get_counts(length, key, offset=offset, verbose=verbose)
        
        i = 0

        cipher_parts = []

        for count in counts:
            cipher_parts.append(text[i:i+count])
            i += count

        if verbose:
            print(cipher_parts)
            
        plain_text = ''
        for pos in positions:
            plain_text = plain_text + cipher_parts[pos][0]
            cipher_parts[pos] = cipher_parts[pos][1:]
        
        return plain_text
    
    def get_counts(self, length, key, offset=0, verbose=False):
        positions = self.get_positions(length, key, offset=offset, verbose=verbose)

        counts = []
        for _ in range(key):
            counts.append(0)
        if verbose:
            print(counts)

        for pos in positions:
            counts[pos] += 1

        if verbose:
            print(counts)
            
        return counts
    
    def get_positions(self, length, key, offset=0, verbose=False):
        positions = []
        
        pos = 0
        step = 1
        for i in range(length + offset):
            if i >= offset:
                if verbose:
                    print(pos, step)                    
                positions.append(pos)
                
            pos += step
            if pos >= key:
                pos = key - 2
                step = -1
            elif pos < 0:
                pos = 1
                step = 1

        return positions
    
# --- end of file --- #
