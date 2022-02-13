# modelbin-tool
This tool converts the .modelbin format to Wavefront obj.  
>Usage: `python modelbin.py <input file>`
>Example: `python modelbin.py hood.modelbin`
>*Outputs to **out.obj***  

Make sure to split model by group when importing.  
Example for Blender:  

![](./split-by-groups.png)

### **TODO**:
- Vertex positions ✓
- Face indices ✓
- Correct scaling
- Grouping ✓
- UVs
- Materials
- etc.