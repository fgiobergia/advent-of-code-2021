from collections import namedtuple
from functools import reduce

Packet = namedtuple("Packet", "version type length payload")

def read_packet(seq, pos):
    init_pos = pos
    pversion = int(seq[pos:pos+3], 2)
    ptype = int(seq[pos+3:pos+6], 2)

    pos += 6
    if ptype == 4: # literal value
        read_on = True
        number = ""
        while read_on:
            block = seq[pos:pos+5]
            if block[0] == "0":
                # stop reading
                read_on = False
            number += block[1:]
            pos += 5
        number = int(number, 2)

        return Packet(pversion, ptype, pos - init_pos, number)
    else: # handle all other values equally
        lentype = seq[pos]
        pos += 1
        packets = []
        if lentype == "0": # number of bits to read
            tot_len = int(seq[pos:pos+15], 2)
            pos += 15
            bits_read = 0
            while bits_read < tot_len:
                packet = read_packet(seq, pos)
                packets.append(packet)
                bits_read += packet.length # increase # of bits read
                pos += packet.length
        else: # number of packets to read
            tot_len = int(seq[pos:pos+11], 2)
            pos += 11
            for _ in range(tot_len):
                packet = read_packet(seq, pos)
                packets.append(packet)
                pos += packet.length
        
        return Packet(pversion, ptype, pos - init_pos, packets)
    
def sum_versions(dec):
    if isinstance(dec.payload, int):
        return dec.version
    else:
        return dec.version + sum(sum_versions(p) for p in dec.payload)

def eval(packet):

    funcs = {
        0: sum,
        1: lambda p: reduce(lambda a,b: a*b, p),
        2: min,
        3: max,
        5: lambda x: x[0] > x[1],
        6: lambda x: x[0] < x[1],
        7: lambda x: x[0] == x[1],
    }

    if packet.type == 4:
        return packet.payload
    
    packet_values = [ eval(p) for p in packet.payload ]

    return funcs[packet.type](packet_values)

if __name__ == "__main__":
    with open("day16.input") as f:
        payload = f.read().strip()
    bp = "".join([ bin(int(x,16))[2:].zfill(4) for x in payload ]) #

    dec = read_packet(bp, 0)
    print(sum_versions(dec))
    print(eval(dec))