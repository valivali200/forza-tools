import os
import sys
import zlib

list_only_mode = False # only print filenames with info (debug)
padding_after_first_list = False # Only use with GeoChunk0.minizip because of some weird padding

args = sys.argv[1:]

if not len(args) == 2:
    print("Usage: python minizip.py <minizip> <filelist>")
    exit(1)

print("Loading filelist...")
filelist = open(args[1], 'r').readlines()
files_in_filelist = len(filelist)
print("Files: ", files_in_filelist)

print("Loading minizip...")
minizip = open(args[0], 'rb+').read()
print("Size: " + str(round(len(minizip)/1000000000, 3)) + "GB")

# utility
def getUint32(offset):
    return int.from_bytes(minizip[offset:offset+4], 'little')
def getUint16(offset):
    return int.from_bytes(minizip[offset:offset+2], 'little')
def getSint32(offset):
    return int.from_bytes(minizip[offset:offset+4], 'little', signed=True)
def getSint16(offset):
    return int.from_bytes(minizip[offset:offset+2], 'little', signed=True)

# check if it is a minizip file
idstring = minizip[0:4]
if idstring != b'PGZP':
    print('Not a minizip file')
    exit(2)

# get header info
info_offset = getUint32(8)
file_count = getUint32(12)
folder_count = getUint32(16)
index_block_size = getUint32(20)

print('Files:', file_count)

# parse first list (unused)
offset = info_offset + 4
folders = []
for i in range(folder_count):
    folders.append(getUint32(offset))
    offset += 4
if padding_after_first_list:
    offset += 4
file_data_start = getUint32(offset)
offset += 12

# parse file info
flag = 0
files = []
count = 0
for i in range(file_count):
    if count == index_block_size:
        flag = getUint32(offset)
        offset += 8
        count = 0
    size = getUint32(offset)

    folder_index = getUint16(offset+6)
    data_end = getUint32(offset+8)
    files.append([size,flag,folder_index,data_end])
    offset += 12
    count += 1

#create directories
if not list_only_mode:
    print("Creating directories...")
    for line in filelist:
        directory = 'out/'
        name = line.replace('\n', '')

        for i in name.split('/')[0:-1]:
            directory = directory + i + '/'
            if not(os.path.exists(directory)):
                os.mkdir(directory)

print("FILE SIZE COMPRESSED_SIZE OFFSET OFFSET_FROM_BLOCK 4GB_BLOCKS")

# decompress files
errors = 0
offset = file_data_start # goto the start of the data
file_index = 1

for i in range(file_count):
    size = files[i][0]
    filename = str(filelist[i][0:-1])
    if not list_only_mode:
        out_file = open('out/'+filename, 'wb')

    if i%512 == 0: # check if it's the first file in a block and calculate it's compressed size
        zsize = files[i][3]
    elif (i+1)%512 == 0:
        zsize = files[i][3] - offset + files[i+1][1]*4294967296
    else:
        zsize = files[i][3]-files[i-1][3]

    data = minizip[offset:offset+zsize] # get data

    if not list_only_mode:
        try:
            out_file.write(zlib.decompress(data, -15)) # decompress and write data to file
        except:
            print("Error: Could not decompress file " + str(i))
            errors += 1

    print(str(file_index) + '/' + str(files_in_filelist), filename, size, zsize, offset, files[i][3], files[i][1])
    file_index += 1
    offset+=zsize
    if not list_only_mode:
        out_file.close()
print('Errors:', errors)
