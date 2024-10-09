# file: bf.py

'''
This is an implementation of the Brainfuck language interpreter based on the video
"Programming 'brainfuck' and virtual machines" by Aur Saraf in Pycon Israel 2017

Test examples:

This will output 'A':

    > python bf.py '++++++++[>++++++++<-]>+.'
    
This will output 'abc':

    > echo 'abcde' | python bf.py '+++[>,.<-]'
    
This will output 'abcde':

    > echo 'abcde' | python bf.py '+[>,.<]'
    
This will output 'hello':

    > echo hello | python bf.py '+++++++++[<+++++>-],[[-<--.++<+>>]<+.-<[->.<]>>,]' | xargs python bf.py
'''

import sys

def parse_parens(code):
    '''
    (Internal) Parse through the code to obtain the pairing of the parenthesis

    :meta private:
    :param code: the code to parse
    :type code: str

    :return: a dictionary indicting the matching parenthesis in the code
    :rtype: dict
    '''
    result = {}
    stack = []
    for i, c in enumerate(code):
        if c == '[':
            stack.append(i)
        elif c == ']':
            match = stack.pop()
            result[match] = i
            result[i] = match
    return result

assert parse_parens('') == {}
assert parse_parens('[]') == { 0: 1, 1: 0 }
assert parse_parens('[.]') == { 0: 2, 2: 0 }
assert parse_parens('[.[]]') == { 0: 4, 4: 0, 2: 3, 3: 2 }

def bf(code, in_stream=''):
    '''
    Run code with the provided input and return the result

    :param code: the code to run
    :type code: str
    :param in_stream: the input to the code
    :type in_stream: str, optional

    :return: the result from running the code
    :rtype: str
    '''
    out_stream = []

    def get():
        if get.in_ptr >= len(in_stream):
            return ''
        c = in_stream[get.in_ptr]
        get.in_ptr += 1
        return c
    get.in_ptr = 0

    def put(c):
        out_stream.append(c)
        
    brainfuck(code, getchar=get, putchar=put)
    return ''.join(out_stream)

def brainfuck(code, getchar=lambda: sys.stdin.read(1), putchar=sys.stdout.write):
    '''
    Run the code on the interpreter

    :param code: the code to run
    :type code: str
    :param getchar: the function to read the next input char
    :param putchar: the function to write the output char
    :type getchar: function, optional
    :type putchar: function, optional

    :return: nothing is returned from this function
    '''
    memory = [0] * 40000
    memory_ptr = 0
    instruction_ptr = 0
    
    matched_parens = parse_parens(code)
    
    code_length = len(code)
    while instruction_ptr >= 0 and instruction_ptr < code_length:
        instruction = code[instruction_ptr]
        if instruction == '+':
            memory[memory_ptr] = (memory[memory_ptr] + 1) % 256
        elif instruction == '-':
            memory[memory_ptr] = (memory[memory_ptr] - 1) % 256
        elif instruction == '>':
            memory_ptr = (memory_ptr + 1) % len(memory)
        elif instruction == '<':
            memory_ptr = (memory_ptr - 1) % len(memory)
        elif instruction == '[':
            if memory[memory_ptr] == 0:
                instruction_ptr = matched_parens[instruction_ptr]
        elif instruction == ']':
            instruction_ptr = matched_parens[instruction_ptr]
            continue
        elif instruction == ',':
            c = getchar();
            if c == '':
                break
            memory[memory_ptr] = ord(c)
        elif instruction == '.':
            putchar(chr(memory[memory_ptr]))
        else:
            pass
        instruction_ptr += 1
        
        #print(instruction_ptr, memory[:10])
        
    return

assert bf('') == ''
assert bf('++++++++++.') == '\n'
assert bf('+++++++++++++.---.') == '\r\n'
assert bf('++++++++[>++++++++<-]>+.') == 'A'
assert bf('+++[>,.<-]', 'abcde') == 'abc'
assert bf('+[>,.<]', 'abcde') == 'abcde'
assert bf(bf('+++++++++[<+++++>-],[[-<--.++<+>>]<+.-<[->.<]>>,]', 'hello, world!')) == 'hello, world!'

assert bf('.') == '\0'
assert bf('>+++++[-<+++>]<.') == '\x0f'

def main():
    '''
    The main function to call the intepreter
    
    The input is read from sys.stdin and output is written to sys.stdout

    Usage:

        python bf.py <code>
    '''
    assert len(sys.argv) == 2, "usage: bf.py <code>"
    _, code = sys.argv
    brainfuck(code)
    return 0

if __name__ == '__main__':
    main()

# --- end of file --- #
