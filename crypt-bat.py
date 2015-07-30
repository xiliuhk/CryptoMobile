__author__ = 'x37liu'

import os
import sys
import argparse
import csv
from wrapper import Cipher

HEADER = ['ID','Task','Key','Count','Direction','Bearer','Data','Data','Source']

def main():

    parser = argparse.ArgumentParser(description = 'AES IP/Cipher/Decipher in batch.')
    parser.add_argument('batch', type = str, help = 'input csv file path')
    parser.add_argument('output', type = str, help = 'output csv file path')
    args = parser.parse_args()
    parseBatch(args)

def parseBatch(args):
    outFile = open(args.output, 'wb')
    writer = csv.writer(outFile)
    if not os.path.exists(args.batch):
        sys.stdout.write('Invalid input path! \n')
        return
    with open(args.batch, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        isHead = True
        for row in reader:
            if isHead:
                isHead = False
                continue
            id = row[0]
            task = row[1]
            key = row[2]
            cnt = int(row[3], 16)
            direct = row[4]
            bearer = int(row[5])
            source = row[7]

            if source == 'f':
                if not os.path.exists(row[6]):
                    sys.stdout.write('Invalid path at task ' + id + '\n')
                    exit()
                dataFile = open(row[6], 'r')
                data = dataFile.read()
                dataFile.close()
            elif source == 's':
                data = row[6]
            else:
                sys.stdout.write('Invalid data source ' + id + '\n')
            print(id + " : " + data)

            cipher = Cipher()
            if task == 'Integrity Check':
                out = cipher.IP(key, cnt, direct, bearer, data)
            elif task == 'Cipher':
                out = cipher.encrypt(key, cnt, direct, bearer, data)
            elif task == 'Decipher':
                out = cipher.decrypt(key, cnt, direct, bearer, data)
            else:
                sys.stdout.write('Invalid task ' + id + '\n')
                exit()
            writer.writerow((id, out))

    outFile.close()

main()