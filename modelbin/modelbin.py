import os
import sys

def getUint32(offset):
    return int.from_bytes(model[offset:offset+4], 'little')
def getUint16(offset):
    return int.from_bytes(model[offset:offset+2], 'little')
def getSint32(offset):
    return int.from_bytes(model[offset:offset+4], 'little', True)
def getSint16(offset):
    return int.from_bytes(model[offset:offset+2], 'little', True)

def getFaceIndices(offset): # parse index buffer
    count = getUint32(offset)
    offset += 16
    faceIndices = []
    for i in range(int(count/3)):
        idx1 = getUint32(offset) + 1
        idx2 = getUint32(offset+4) + 1
        idx3 = getUint32(offset+8) + 1
        offset += 12
        faceIndices.append([idx1, idx2, idx3])
    return faceIndices

def getVertexPositions(offset): # parse first vertex buffer with positions for all vertices
    verts = getUint32(offset)
    offset += 16
    vertexPositions = []
    for i in range(0, verts):
        offset += 0
        x = getUint16(offset)/65535
        y = getUint16(offset+2)/65535
        z = getUint16(offset+4)/65535
        offset += 8
        vertexPositions.append([x,y,z])
    return vertexPositions

# open files
args = sys.argv[1:]
model = open(args[0], 'rb+').read()
obj = open('out.obj', 'w')

# parse Grub header
dataStart = getUint32(8)
entries_count = getUint32(16)

# create entry list
entries = []
entryListOffset = 20
for i in range(entries_count):
    entryType = model[entryListOffset:entryListOffset+4]
    header_offset = getUint32(entryListOffset+8)
    data_offset = getUint32(entryListOffset+12)
    data_size = getUint32(entryListOffset+16)
    entries.append([entryType, header_offset, data_offset, data_size])
    entryListOffset+=24

IndBIdx = []
VerBIdx = []

# parse entry indices into lists
for i in range(entries_count):
    if entries[i][0] == b'BdnI':
        IndBIdx.append(i)
    if entries[i][0] == b'BreV':
        VerBIdx.append(i)

# parse vertex positions from first VerB
vpos_offset = entries[VerBIdx[0]][2]
vpos_data = getVertexPositions(vpos_offset)
for i in vpos_data: # write to obj
    obj.write('v ' + str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n')

# parse face indices
fi_offset = entries[IndBIdx[0]][2]
fi_data = getFaceIndices(fi_offset)
for i in fi_data:
    obj.write('f ' + str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n')