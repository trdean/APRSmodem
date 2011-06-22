#!/usr/bin/env python

import sys, math, time
import struct, numpy
import numpy.fft

class Demodulate:

    def __init__(self, samplerate, periodsize):
        self.samplerate = samplerate
        self.periodsize = periodsize
        self.f = open('bell202', 'rb')

    def doFFT(self, data):
        form = '<%dh'%self.periodsize
        depack = struct.unpack(form, data)
        start = time.time()
        signal = numpy.array(depack)
        complexSpectrum = numpy.fft.fft(signal)
        amplitudeSpectrum = numpy.abs(complexSpectrum)
        elapsed = time.time() - start
        return list(amplitudeSpectrum)

    def decision(self, spectrum):
        if spectrum[5] >= spectrum[10]: return 1
        else: return 0

    def resultToAscii(self, data):
        while len(data)%8 != 0: data += '0'
        byteArray = []
        for n in range(0,len(data)/8): byteArray.append(chr(int(data[n*8:n*8+8],2)))
        return ''.join(byteArray)

    def demod(self):
        result = ''
        index = 0
        self.f.seek(index)
        data = self.f.read(2*self.periodsize)
        while len(data) == 72:
            spec = self.doFFT(data)
            result += str(self.decision(spec))
            index += 2*self.periodsize
            self.f.seek(index)
            data = self.f.read(2*self.periodsize)
        ascii = self.resultToAscii(result)
        return ascii
        

def main():
    d = Demodulate(8000, 36)
    data = d.demod()
    #print [n for n in data]
    
if __name__ == "__main__":
    main()
