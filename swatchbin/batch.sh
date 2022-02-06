#converts all .swatchbin files in current directory to .png
for filename in *.swatchbin; python swatchbin.py $filename $filename.png; end
