import sys
import logging as lg

mem_len = 30000

mem = [0] * mem_len
memPnt = 0

def run(chars: str) -> int:
    """
    Run a line of brainfuck code.
    
    ### Parameter:
    - `chars`: str
    
    The brainfuck code to run.
    
    ### Return:
    `int`:
    - `0` ran successful
    - `1` catched an error
    """
    global mem, memPnt
    codePnt = 0
    while codePnt < len(chars):
        if chars[codePnt] == '>':
            if memPnt < len(mem) - 1:
                memPnt += 1
            else:
                lg.warning('Out of bounds')
        elif chars[codePnt] == '<':
            if memPnt > 0:
                memPnt -= 1
            else:
                lg.warning('Out of bounds')
        elif chars[codePnt] == '+':
            mem[memPnt] += 1
        elif chars[codePnt] == '-':
            mem[memPnt] -= 1
        elif chars[codePnt] == '.':
            print(chr(mem[memPnt]), end='')
        elif chars[codePnt] == ',':
            mem[memPnt] = ord(input()[0])
        elif chars[codePnt] == '[':
            if mem[memPnt] == 0:
                while chars[codePnt] != ']':
                    codePnt += 1
                    if codePnt >= len(chars):
                        lg.error('Unmatched [')
                        return 1
        elif chars[codePnt] == ']':
            if mem[memPnt] != 0:
                while chars[codePnt] != '[':
                    codePnt -= 1
                    if codePnt < 0:
                        lg.error('Unmatched ]')
                        return 1
        elif chars[codePnt] == '/' and codePnt < len(chars) - 1 and chars[codePnt + 1] == '/':
            break
        codePnt += 1
    return 0


if len(sys.argv) == 2 and sys.argv[1] == '-h':
    print("""
Usage: bf <file.bf>
Commands:
    +: Adds 1 to the memory the pointer points to.
    -: Subtracts 1 from the memory the pointer points to.
    >: Point the pointer to the right block of memory.
    <: Point the pointer to the left block of memory.
    .: Print the ASCII value of the memory the pointer points to.
    ,: Read an ASCII value and store it in the memory the pointer points to.
    [: If the memory the pointer points to is 0, skip all the code until the matching ].
    ]: If the memory the pointer points to is not 0, skip all the code until the matching [.
Special commands in console mode:
    exit/quit/q: Exit the program.
    help: Print part 'Commands' and 'Special commands in console mode' of this help without titles.
    chkmem <n>: Print the value of the memory block number <n>.
    chkptdmem: Print the value of the memory block the pointer points to.
    clearmem: Reset all memory blocks to 0.
    clearptr: Reset the pointer to the first memory block.
    clearall: Reset all memory blocks to 0 and reset the pointer to the first memory block.
    runfile <file>: Run the code in the file <file>.
Special commands in file mode:
    //: Comment. Ignore everything after it until the end of the line. It don't need to be at the start of the line.
    #clearmem: Means command 'clearmem', see in 'Special commands in console mode'.
    #clearptr: Means command 'clearptr', see in 'Special commands in console mode'.
    #clearall: Means command 'clearall', see in 'Special commands in console mode'.
""")
    sys.exit(0)
elif len(sys.argv) > 2:
    lg.warning('Usage: bf <file.bf>')
    sys.exit(1)
elif len(sys.argv) < 2:
    # console mode
    while True:
        print()
        try:
            ip = input('>>> ')
        except EOFError:
            break
        except KeyboardInterrupt:
            continue
        except BaseException as e:
            print(f'{e.__class__}: {e}')
        if ip == 'exit' or ip == '\26' or ip == 'quit' or ip == 'q':
            break
        if ip == 'help':
            print("""
    +: Adds 1 to the memory the pointer points to
    -: Subtracts 1 from the memory the pointer points to
    >: Point the pointer to the right block of memory
    <: Point the pointer to the left block of memory
    .: Print the ASCII value of the memory the pointer points to
    ,: Read an ASCII value and store it in the memory the pointer points to
    [: If the memory the pointer points to is 0, skip all the code until the matching ] 
    ]: If the memory the pointer points to is not 0, skip all the code until the matching [
    exit/quit/q: Exit the program
    help: Print this help message
    chkmem <n>: Print the value of the memory block number <n>
    chkptdmem: Print the value of the memory block the pointer points to
    clearmem: Reset all memory blocks to 0
    clearptr: Reset the pointer to the first memory block
    clearall: Reset all memory blocks to 0 and reset the pointer to the first memory block
    runfile <file>: Run the code in the file <file>""")
            continue
        if ip[:7] == 'chkmem ':
            print(mem[int(ip[7:])])
            continue
        if ip == 'chkptdmem':
            print(mem[memPnt])
            continue
        if ip == 'clearmem':
            mem = [0] * mem_len
            continue
        if ip == 'clearptr':
            memPnt = 0
            continue
        if ip == 'clearall':
            mem = [0] * mem_len
            memPnt = 0
            continue
        if ip[:8] == 'runfile ':
            file = ip[8:]
            if file.startswith('"') and file.endswith('"') or file.startswith("'") and file.endswith("'"):
                file = file[1:-1]
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    run(f.read().strip())
            except FileNotFoundError:
                lg.error(f'File "{file}" not found')
                continue
            except BaseException as e:
                print(f'{e.__class__.__name__}: {e}')
            continue
        run(ip)
else:
    # file mode
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            for line in f:
                if line[:9] == '#clearmem':
                    mem = [0] * mem_len
                    continue
                if line[:9] == '#clearptr':
                    memPnt = 0
                    continue
                if line[:9] == '#clearall':
                    mem = [0] * mem_len
                    memPnt = 0
                    continue
                if run(line.strip()):
                    exit(1)
    except FileNotFoundError:
        lg.error(f'File "{sys.argv[1]}" not found')
        sys.exit(1)
