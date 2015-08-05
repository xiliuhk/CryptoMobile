__author__ = 'x37liu'

import os
import sys
import argparse
from wrapper import Cipher

def main():

    # prepare cmd cheat sheet
    helpFile = open('helpFile', 'r')
    helpStr = helpFile.read()
    helpFile.close()

    # read args
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description = helpStr)
    parser.add_argument('task',
                        choices = ['ip', 'ci', 'de'],
                        help = 'Task to complete')
    parser.add_argument('key', type = str, help = 'AES key')
    parser.add_argument('count', type = str, help = 'Count')
    parser.add_argument('direct', type = str, help = 'Direction')
    parser.add_argument('bearer', type = int, help = 'Bearer')
    parser.add_argument('data', type = str, help = 'Stream')
    parser.add_argument('mode', nargs = '?', default='ss',
                        choices = ['ss', 'fs', 'sf', 'ff'],
                        help = 'Data I/O options')
    parser.add_argument('output', nargs = '?', type = str, help = 'Output path')

    args = parser.parse_args()

    parseArgs(args)

def output(data, path = ""):
    if path == "":
        sys.stdout.write(data)
        return
    else:
        file = open(path, 'w')
        file.write(data)
        file.close()

def parseArgs(args):
    count = int(args.count, 16)
    if args.mode == 'ff' or args.mode == 'fs':
        if not os.path.exists(args.data):
            sys.stdout.write('Invalid Data!\n')
            return
        file = open(args.data, 'r')
        data = file.read()
        file.close()
    else: 
        data = args.data
    cipher = Cipher()
    out = ""
    if args.task == 'ip':
        out = cipher.IP(args.key, count, args.direct, args.bearer, data)
    elif args.task == 'ci': 
        out = cipher.encrypt(args.key, count, args.direct, args.bearer, data)
    else: 
        out = cipher.decrypt(args.key, count, args.direct, args.bearer, data)
    if args.mode == 'ss' or args.mode == 'fs':
        output(out, "")
    elif args.output:
        output(out, args.output)
    else: 
        outPath = raw_input('Please specify output path:')
        output(out, outPath)
    
main()