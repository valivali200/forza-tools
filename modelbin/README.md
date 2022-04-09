# modelbin-tool
This tool converts the .modelbin format to Wavefront obj.   

>Usage: `python modelbin.py <input file>`  
>Example: `python modelbin.py hood.modelbin`  
>*Outputs to **\<inputfile>.obj***


Make sure to split model by group when importing.  
Example for Blender:  

![](./split-by-groups.png)

### **TODO**:
- Correct scaling (Works on some models)
- Correct positioning
- UVs
- Materials
- etc.
