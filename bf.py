import sys
import logging as lg

mem_len = 30000

mem = [0] * mem_len
memPnt = 0

def run(chars):
    global mem, memPnt
    codePnt = 0
    while codePnt < len(chars):
        if chars[codePnt] == '>':
            if memPnt < len(chars):
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
            while mem[memPnt] == 0:
                codePnt += 1
                if chars[codePnt] == ']':
                    break
        elif chars[codePnt] == ']':
            while mem[memPnt] != 0:
                codePnt -= 1
                if chars[codePnt] == '[':
                    break
        codePnt += 1


if len(sys.argv) == 2 and sys.argv[1] == '-h':
    print('Usage: bf.py <file.bf>')
    sys.exit(-1)
elif len(sys.argv) > 2:
    print('Usage: bf.py <file.bf>')
    sys.exit(1)
elif len(sys.argv) < 2:
    # console mode
    while True:
        print()
        try:
            ip = input('>>> ')
        except EOFError:
            break
        except Exception as e:
            print(f'{e.__class__}: {e}')
        if ip == 'exit' or ip == '\26':
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
    exit: Exit the program
    help: Print this help message
    chkmem <n>: Print the value of the memory block number <n>
    chkptdmem: Print the value of the memory block the pointer points to
    resetmem: Reset all memory blocks to 0
    resetptr: Reset the pointer to the first memory block
    resetall: Reset all memory blocks to 0 and reset the pointer to the first memory block
    runfile <file>: Run the code in the file <file>""")
            continue
        if ip[:7] == 'chkmem ':
            print(mem[int(ip[7:])])
            continue
        if ip[:9] == 'chkptdmem':
            print(mem[memPnt])
            continue
        if ip[:8] == 'resetmem':
            mem = [0] * mem_len
            continue
        if ip[:8] == 'resetptr':
            memPnt = 0
            continue
        if ip[:8] == 'resetall':
            mem = [0] * mem_len
            memPnt = 0
            continue
        if ip[:8] == 'runfile ':
            with open(ip[8:], 'r') as f:
                run(f.read().strip())
            continue
        run(ip)
else:
    # file mode
    with open(sys.argv[1], 'r') as f:
        run(f.read().strip())
