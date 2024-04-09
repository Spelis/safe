from shlex import split as shlex
import argparse

#! Current Name: Slow As Fuck Editor / SAFE

parser = argparse.ArgumentParser(
                    prog='SAFE: Slow As F**k Editor',
                    description='Edit files in a shell-like environment to make editing slower')

parser.add_argument('filename',default='',nargs='?',help='filename to open, leave blank to create new file')

args = parser.parse_args()
print(args.filename)
if args.filename == '':
    buffer = ['']
else:
    with open(args.filename,'r') as f:
        buffer = str(f.read()).split('\n')

while 1:
    try:
        line = input(">")
        line = shlex(line)
        line[0] = line[0].lower()
        if line[0] == 'edit':
            buffer[int(line[1])] = line[2]
        if line[0] == 'insert':
            buffer.insert(int(line[1]),line[2])
        if line[0] == 'cat':
            for l,i in enumerate(buffer):
                print(str(l),i)
        if line[0] == 'cls' or line[0] == 'clear':
            print('\033c')
    except Exception as e:
        print(e)