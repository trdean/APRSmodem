#!/usr/bin/env python

import AXFrame, bell202_tx

def main():
    dest = '0KJ5HY1'
    source = 'KB1JIJ1'
    addr = 'ThisShouldn\'tMatter'
    info = 'Test'
    packet = AXFrame.AX(dest, source, addr, info)
    AX = packet.getFrame()

    g = bell202_tx.Modulator(8000, 36, 0.3)
    g.output(AX)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
