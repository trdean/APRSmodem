#!/usr/bin/env python
import bellToFile, AXFrame

dest = ' KJ5HY1'
source = 'KB1JIJ1'
addr = 'ThisShouldn\'tMatter'
info = 'Test'
packet = AXFrame.AX(dest, source, addr, info)
AXPacket = packet.getFrame()
print [n for n in AXPacket]
m = bellToFile.Modulator(8000,36, 0.3)
m.output(AXPacket)
