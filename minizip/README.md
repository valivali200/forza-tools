# minizip-extractor
Extracts minizip archive contents.

**Not recommended for personal usage (just download the extracted files):**  
- Loads entire minizip into memory which means that it uses upwards of 10 GB of RAM
- Minizips might change along with file lists and I would have to modify them for each version

Extracted minizips:
- https://drive.google.com/drive/folders/1e6RB56iOks-bK-K4jwd6EFxErkC0T62F?usp=sharing

If you really want to use the script yourself:
- make sure you have 32GB of RAM (might work with 16GB for the small minizips and for the big one if you have a large pagefile)
- copy the minizip along with the chunk contents file from media/tracks/hendrix/ and paste them in your desired folder
- modify the file list to match the provided ones(**if it has changed**)
    - remove **"../../../../"** or **"\<PREZIPPED>d:\scratch\p4\woodstock\zipcache\pc\"** from each file name
    - remove the "**|1234**" from the end of each filename with regex
    - replace "**\\\\**" with "**/**"
- copy the script next to the minizip
- create a directory named "**out**"
- make sure you have atleast twice as much space free than the size of the minizip
- run `python minizip.py <minizip file> <corresponding filelist>`
- wait as it takes quite a while (because of the size of the minizips)
