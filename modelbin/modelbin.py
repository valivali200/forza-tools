import os
import sys
import struct

def getUint32(offset):
    return int.from_bytes(model[offset:offset+4], 'little')
def getUint16(offset):
    return int.from_bytes(model[offset:offset+2], 'little')
def getSint32(offset):
    return int.from_bytes(model[offset:offset+4], 'little', signed=True)
def getSint16(offset):
    return int.from_bytes(model[offset:offset+2], 'little', signed=True)

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
        x = getSint16(offset)/32767
        y = getSint16(offset+2)/32767
        z = getSint16(offset+4)/32767
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
MeshIdx = []
MatIIdx = []

# parse entry indices into lists
for i in range(entries_count):
    if entries[i][0] == b'BdnI':
        IndBIdx.append(i)
    if entries[i][0] == b'BreV':
        VerBIdx.append(i)
    if entries[i][0] == b'hseM':
        MeshIdx.append(i)
    if entries[i][0] == b'ItaM':
        MatIIdx.append(i)

print('Materials:', len(MatIIdx))

# read bytes from entry headers
entry_headers_data = []
for i in range(entries_count):
    if entries[i] == entries[-1]:
        header_start = entries[i][1]
        header_size = entries[0][2] - header_start
    else:
        header_start = entries[i][1]
        header_size = entries[i+1][1] - entries[i][1]
    if header_size == 0:
        entry_headers_data.append([])
    else:
        entry_headers_data.append(model[header_start:header_start+header_size])

# parse entry headers
entry_headers = []
for i in entry_headers_data:
    if i == []:
        entry_headers.append([])
        continue
    bbox = []
    name_length = int.from_bytes(i[14:16], 'little') - 8
    name = i[16:16+name_length]
    if i[8:12] == b'xoBB':
        bbox = struct.unpack('6f', i[-24:])
    entry_headers.append([name, bbox])    

# get groups
groups = []
for i in MeshIdx:
    name = entry_headers[i][0]
    if name == b'Shadow':
        continue
    group_size = getUint32(entries[i][2]+43)
    groups.append([name, group_size])

# parse vertex positions from first VerB
vpos_offset = entries[VerBIdx[0]][2]
vpos_data = getVertexPositions(vpos_offset)
for i in vpos_data: # write to obj
    obj.write('v ' + str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n')
print('Vertices:', len(vpos_data))

# parse face indices
fi_offset = entries[IndBIdx[0]][2]
fi_data = getFaceIndices(fi_offset)
fi_count = 0
obj.write('g ' + str(groups[0][0])[2:-1] + '\n')
group_count = 1
next_group_start = groups[0][1]
for i in fi_data:
    if fi_count == next_group_start:
        obj.write('g ' + str(groups[group_count][0])[2:-1] + '\n')
        next_group_start += groups[group_count][1]
        group_count += 1
    obj.write('f ' + str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n')
    fi_count += 1
print('Face indices:', len(fi_data))