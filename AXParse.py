#!/usr/bin/env python

import sys, crcmod, struct

class AXParser:

        def __init__(self, packet):
            self.FCS = ''
            self.DestinationData = ''
            self.SourceData = ''
            self.ctrl = ''
            self.digiAddress = ''
            self.info = ''
            if not self.checkFCS(packet): print "Warning: Invalid Checksum"
            restored = self.restoreEndianess(packet)
            self.parse(restored)
            print "Destination: " + self.DestinationData
            print "Source: " + self.SourceData
            print "Address: " + self.digiAddress
            print "Information: " + self.info

        def parse(self, data):
                data = data[1:-1]       #discard flag
                self.FCS = data[-3:-1]
                data = data[:-2]
                self.DestinationData = data[:7]
                data = data[7:]
                self.SourceData = data[:7]
                data = data[7:]
                self.checkData = data
                data = data.split("\x03\xf0")
                if data[1] == '':
                        print "Bad packet: Missing Control Field and/or Protocol ID"
                        raise SystemExit, 1
                self.digiAddress = data[0]
                self.info = data[1]
                return

        def restoreEndianess(self, packet):
                first = packet[:-3]
                last = packet[-1]
                work = first + last
                result = ''
                for n in range(0,len(work)):
                        octet = bin(ord(work[n]))[2:]
                        while len(octet) < 8: octet = '0' + octet
                        octet = octet[::-1]
                        result += chr(int(octet, 2))
                final = result[:-1] + packet[-3:-1] + result[-1]
                return final

        def checkFCS(self, packet):
            crc = crcmod.predefined.mkCrcFun('x-25')
            calcFCS = ['0x00', '0x00']
            sentFCS = packet[-3:-1]
            checkBlock = packet[15:-3]
            crcVal = hex(crc(checkBlock))
            calcFCS[0] = crcVal[:4]
            calcFCS[1] = '0x' + crcVal[4:]
            calcFCS = [chr(int(n,16)) for n in calcFCS]
            if calcFCS == [n for n in sentFCS]: return True
            else: return False


def main():
    parse = AXParser(packet)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
