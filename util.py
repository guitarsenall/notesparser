def lines(file):
    for line in file: yield line
    yield '\n'

def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block)    # .strip()
            block = []

def leadingspaces(line):
    # count leading spaces in a line
    return len(line) - len(line.lstrip(' '))


