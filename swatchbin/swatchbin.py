from PIL import Image
import os
import sys
import texture2ddecoder

args = sys.argv[1:]
if len(args) < 2:
    print("Usage: swatchbin.py <input file> <output file>")
    exit(1)

swatch = open(args[0], 'rb+').read()

offset = int.from_bytes(swatch[8:12], 'little')
width = int.from_bytes(swatch[76:80], 'little')
height = int.from_bytes(swatch[80:84], 'little')
data_length = int.from_bytes(swatch[36:40], 'little')
compression = swatch[116]
data = swatch[offset:offset+data_length]

print(args[0])
print("Data offset:", offset)
print("Image width:", width)
print("Image height:", height)
print("Image size:", data_length)

if compression == 0:
    decoded = texture2ddecoder.decode_bc1(data, width, height)
    out = Image.frombytes('RGBA', (width, height), decoded, 'raw', ('BGRA'))
    print("Compression: BC1")

elif compression == 3:
    decoded = texture2ddecoder.decode_bc4(data, width, height)
    out = Image.frombytes('RGBA', (width, height), decoded, 'raw', ('BGRA'))
    print("Compression: BC4")

elif compression == 4:
    decoded = texture2ddecoder.decode_bc4(data, width, height)
    out = Image.frombytes('RGBA', (width, height), decoded, 'raw', ('BGRA'))
    print("Compression: BC4_SNORM")

elif compression == 5:
    decoded = texture2ddecoder.decode_bc5(data, width, height)
    out = Image.frombytes('RGBA', (width, height), decoded, 'raw', ('BGRA'))
    print("Compression: BC5")
    
elif compression == 6:
    decoded = texture2ddecoder.decode_bc5(data, width, height)
    out = Image.frombytes('RGBA', (width, height), decoded, 'raw', ('BGRA'))
    print("Compression: BC5_SNORM")

elif compression == 7:
    decoded = texture2ddecoder.decode_bc6(data, width, height)
    out = Image.frombytes('RGBA', (width, height), decoded, 'raw', ('BGRA'))
    print("Compression: BC6")

elif compression == 9:
    decoded = texture2ddecoder.decode_bc7(data, width, height)
    out = Image.frombytes('RGBA', (width, height), decoded, 'raw', ('BGRA'))
    print("Compression: BC7")

elif compression == 13:
    out = Image.frombytes('RGBA', (width, height), data, 'raw', ('RGBA'))
    print("Compression: R8B8G8A8")

elif compression == 19:
    out = Image.frombytes('L', (width, height), data, 'raw', ('L'))
    print("Compression: A8")

else:
    print("Unknown compression")
    exit(2)

out.save(args[1])
print("Done!\n")
