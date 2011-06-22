#!/usr/bin/env python
##################################################################
# Transmits input from command line (first argument) as a Bell 202
# modulated signal to the default ALSA device.  
# Tom Dean
##################################################################

import sys, math
import alsaaudio, struct

class Modulator:

        #TODO: Bit-rate defined by periodsize...fix this by allowing bitrate to be an input
        def __init__(self, samplerate, periodsize, amplitude):
                self.samplerate = samplerate
                self.periodsize = periodsize
                self.amplitude = amplitude
                self.index = 0		#needed to keep phase continous
                self.a = alsaaudio.PCM()
                self.a.setchannels(1)
                self.a.setrate(self.samplerate)
                self.a.setformat(alsaaudio.PCM_FORMAT_S16_LE)
                self.a.setperiodsize(self.periodsize)

	#Creates the signal in the form of signed, 16 bit samples which can be passed to the ALSA device
        def generate(self, freq):
                sine = [int((2**15-1)*self.amplitude*math.sin(2*math.pi*freq*x/self.samplerate)) \
                                for x in range(self.index, self.index + self.periodsize)]
                form = '<%dh'%self.periodsize
                self.index += self.periodsize
                return struct.pack(form, *sine)

	#Takes a string and returns it as a string of raw little-endian binary (assuming ASCII input only)
        def string_to_bin(self, data):
                data = ''.join(['%x' % ord(n) for n in data])	#convert into a string of hex
                bin_string = ''	
                for n in data:
                        i = bin(int(n,16))[2:]			#convert each hex digit into binary
                        while len(i) < 4: i = '0' + i		#prepend binary with 0s as needed to make 4 bits long
                        bin_string += i				#add to string
                return bin_string

        def output(self, data):
                bin_string = self.string_to_bin(data)
                for n in bin_string:
                        if n is '1':
                                buff = self.generate(1200)
                        else:
                                buff = self.generate(2200)
                        self.a.write(buff)

def main():
        try:
                data = sys.argv[1]
        except IndexError:
                sys.stderr.write('Enter an input!\n')
                raise SystemExit, 1
        
        g = Modulator(8000, 36, 0.3)
        g.output(data)

if __name__ == "__main__":
        try:
                main()
        except KeyboardInterrupt:
                pass
