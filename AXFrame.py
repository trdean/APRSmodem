#!/usr/bin/env python

import sys, crcmod, struct

class AX:

        def __init__(self, dest, source, addr, info):
            self.crc = crcmod.predefined.mkCrcFun('x-25')
            self.flag = ['0x7e']
            self.ctrlField = ['0x03']
            self.protocolID = ['0xf0']
            self.setDestinationData(dest)
            self.setSourceData(source)
            self.setDigiAddress(addr)
            self.setInformation(info)
            self.computeFCS()
            self.AX = self.frame()
            return 

        def setDestinationData(self, data):
            if len(data) is 7:
                self.destination = [hex(ord(n)) for n in data]
                return True
            else:
                return False

        def setSourceData(self, data):
            if len(data) is 7:
                self.source = [hex(ord(n)) for n in data]
                return True
            else:
                return False

        def setDigiAddress(self, data):
            if len(data) <= 56:
                self.address = [hex(ord(n)) for n in data]
                return True
            else:
                return False

        def setInformation(self, data):
            if len(data) in range(1, 256):
                self.info = [hex(ord(n)) for n in data]
                return True
            else:
                return False

        def computeFCS(self):
            self.FCS = ['0x00', '0x00']
            crcString = self.address + self.ctrlField + self.protocolID + self.info
            crcString = self.make_BigEndian(crcString)
            crcString = [chr(int(n, 2)) for n in crcString]
            crcVal = hex(self.crc(''.join(crcString)))
            self.FCS[0] = crcVal[:4]
            self.FCS[1] = '0x' + crcVal[4:]
            print self.FCS
            return

        def frame(self):
            self.flag = self.make_BigEndian(self.flag)
            self.destination = self.make_BigEndian(self.destination)
            self.source = self.make_BigEndian(self.source)
            self.address = self.make_BigEndian(self.address)
            self.ctrlField = self.make_BigEndian(self.ctrlField)
            self.protocolID = self.make_BigEndian(self.protocolID)
            self.info = self.make_BigEndian(self.info)
            self.FCS = self.make_LittleEndian(self.FCS)
            AXString = self.flag + self.destination + self.source + self.address \
                       + self.ctrlField + self.protocolID + self.info + self.FCS \
                       + self.flag
            AXString = [chr(int(n,2)) for n in AXString]
            AXString = ''.join(AXString)
            return AXString

        def make_LittleEndian(self, data):
            for n in range(0, len(data)):
                i = bin(int(data[n][2:],16))[2:]
                while len(i) < 8: i = '0' + i
                data[n] = i
            return data

        def make_BigEndian(self, data):
            data = self.make_LittleEndian(data)
            for n in range(0, len(data)):
                data[n] = data[n][::-1]
            return data

        def getFrame(self):
            return self.AX

def main():
    dest = '0KJ5HY1'
    source = 'KB1JIJ1'
    addr = 'ThisShouldn\'tMatter'
    info = 'Test'
    packet = AX(dest, source, addr, info)
    AXFrame = packet.getFrame()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
