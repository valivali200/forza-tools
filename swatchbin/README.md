# swatchbin-tool
This tool converts the Forza .swatchbin format to whatever image format you want.

>**First install the required modules:**
>`pip install texture2ddecoder pillow`  

>Usage: `python swatchbin.py <input file> <output file>`  
>Example: `python swatchbin.swatchbin texture.py out.png`

It works perfectly with most compressions but it has a few artifacts with **BC4_SNORM** and **BC5_SNORM** which are quite rare anyway. I think I implemented all compressions but if you find any that don't work create an issue and I'll take a look at it.  
