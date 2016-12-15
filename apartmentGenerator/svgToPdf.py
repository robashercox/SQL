import os
import time
cmdString1 = 'DEL "' + PDF + '"'
cmdString2 = '"C:\Program Files\Inkscape\inkscape" "' + SVG + '" --export-pdf="' + PDF + '"'
cmdString3 = cmdString1 + " " + cmdString2
print cmdString3
if ACTIVATE == True:
    os.system(cmdString1)
    time.sleep(1)
    os.system(cmdString2)
