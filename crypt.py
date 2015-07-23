__author__ = 'x37liu'
import sys
import os
# prepare cmd cheat sheet
helpFile = open('helpFile', 'r')
helpStr = helpFile.read()
helpFile.close()

# config
cmdList = ['-b', '-ci', '-de', '-ip']
modeList = ['-ff', '-sf', '-fs', '-ss']
curDir = os.getcwd()
scriptPath = __file__

# start
sys.stdout(
        '******************************************************************************\n' \
       +'*                    AES Ciphering / Deciphering Tool                        *\n' \
       +'*   Batch Process: -b [batch file name]                                      *\n' \
       +'*   Single Process: [task] [mode] [key] [count] [direction] [bearer] [data]  *\n' \
       +'*   Help:  help                                                              *\n' \
       +'*   Exit:  exit                                                              *\n' \
       +'******************************************************************************\n')

while True:
    cmd = raw_input('')
    if cmd == 'exit':
        break
    elif cmd == 'help':
        sys.stdout(helpStr)
    else:
        task = cmd

