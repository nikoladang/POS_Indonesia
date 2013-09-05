##http://www.saltycrane.com/blog/2007/10/python-finditer-regular-expression/
"""
Python version: 2.7
Purpose: posui:showLogo
130412: Initial
"""
import sys, re, os, glob, shutil, fileinput
from datetime import datetime
import teoconstants

##root_dir='C:\\130409_Temp\\Temp\\poscoMES_M80\\Pgm_Dev\\2nd_iteration\\'
root_dir='C:\\130411_Temp\\'
constantFolders=[
                 'public_html',
                 ]

showUtilityButtonsCount = 0
alreadyChanged = 0
showUtilityButtonsChanged = 0
inplaceFlag = 1
def run(target_dir, inplaceFlag=0):
    global showUtilityButtonsCount, alreadyChanged, showUtilityButtonsChanged
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.jsp') and (file.lower() in teoconstants.uipgms):
                if inplaceFlag == 0:   #improve performance
                    f = fileinput.input(root+"\\"+ file, inplace=inplaceFlag, openhook=fileinput.hook_encoded('utf-8'))
                elif inplaceFlag == 1:
                    f = fileinput.input(root+"\\"+ file, inplace=inplaceFlag)

                for i, line in enumerate(f):
                    if(re.search('posui:showUtilityButtons', line, re.IGNORECASE)):
                        showUtilityButtonsCount += 1
                        if(re.search('isMultiLang',line)):
                           alreadyChanged += 1
                        else:
                            showUtilityButtonsChanged += 1
                            line = line.replace('posui:showUtilityButtons','posui:showUtilityButtons isMultiLang="true"')

                            if inplaceFlag == 0:
                                sys.stdout.write(file+' : '+line)
                    if inplaceFlag == 1:
                        sys.stdout.write(line)

                f.close()

#==main==================
print ("Start time: " + str(datetime.now()))
print ("Root Dir = " + root_dir)
print ("inplaceFlag = " + str(inplaceFlag) + "\n")

for folder in constantFolders:
    run(root_dir + "\\" + folder, inplaceFlag)
print('\nshowUtilityButtonsCount = ' + str(showUtilityButtonsCount))
print('alreadyChanged = ' + str(alreadyChanged))
print('showUtilityButtonsChanged = ' + str(showUtilityButtonsChanged))

print("\nEnd time: " + str(datetime.now()))

    
