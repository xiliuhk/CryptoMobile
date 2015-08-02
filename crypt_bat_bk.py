__author__ = 'x37liu'

import os
import sys
import csv
from wrapper import Cipher

HEADER = ['ID','Task','Key','Count','Direction','Bearer','Data','Data','Source']

class AES_Batch:
    def __init__(self):
        self.cipher = Cipher()

    def parseBatch(self, input, output):
        outFile = open(output, 'wb')
        writer = csv.writer(outFile)
        if not os.path.exists(input) or input == output:
            outFile.close()
            os.remove(output)
            return 'Invalid input path! \n'
        with open(input, 'rb') as csvfile:
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
                        return 'Invalid path at task ' + id + '\n'
                    dataFile = open(row[6], 'r')
                    data = dataFile.read()
                    dataFile.close()
                elif source == 's':
                    data = row[6]
                else:
                    return 'Invalid data source ' + id + '\n'

                if task == 'Integrity Check':
                    out = self.cipher.IP(key, cnt, direct, bearer, data)
                elif task == 'Cipher':
                    out = self.cipher.encrypt(key, cnt, direct, bearer, data)
                elif task == 'Decipher':
                    out = self.cipher.decrypt(key, cnt, direct, bearer, data)
                else:
                    return 'Invalid task ' + id + '\n'
                writer.writerow((id, out))
        outFile.close()
        return ''
