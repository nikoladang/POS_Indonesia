##http://www.saltycrane.com/blog/2007/10/python-finditer-regular-expression/
"""
Python version: 2.7
Purpose: remove help buttons defined at posui:showUtilityButtons
130525: Initial
NOTE: all components of posui:showUtilityButtons HAVE TO BE in one line.
"""
import sys, re, os, glob, shutil, fileinput
from datetime import datetime
import teoconstants

publichtml_dir=r'C:\130719_DEV\DEV\public_html'

inplaceFlag = 1
helpButtonsCount = 0
helpButtonsDelete = 0
exception = 0

"""
<posui:showUtilityButtons name="find|help|close" onclick="findMethod()|showHelp('/help/m80/m800502004pop01help.htm')|null"/>
----
<posui:showUtilityButtons name="find|close" onclick="findMethod()|null"/>
"""
def run(target_dir, inplaceFlag=0):
    global helpButtonsCount, alreadyChanged, helpButtonsDelete, exception
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.jsp') and (file.lower() in teoconstants.jsps):
                fullfilepath = root +'\\'+ file
                with open(fullfilepath,'r',-1,encoding='utf-8') as rf:
                    lines = rf.readlines()
                    if inplaceFlag != 0:
                        wf = open(fullfilepath,'w',-1,encoding='utf-8')
                    for i, line in enumerate(lines):
                        if(re.search('posui:showUtilityButtons.*help', line, re.IGNORECASE)):
                            originalLine = line
                            if re.search('help\|', line):
                                line = re.sub('help\|', '', line)
                                helpButtonsCount += 1
                            if re.search('showHelp.*?\|', line):
                                line = re.sub('showHelp.*?\|', '', line)
                                sys.stdout.write(file+':'+str(i+1) +'\t'+ line)
                                helpButtonsDelete += 1
                            else:
                                sys.stdout.write('<<<EXCEPTION>>>'+file+':'+str(i+1) +'\t'+ line)
                                exception += 1
                                if inplaceFlag != 0:
                                    wf.write(originalLine)
                                    continue

                        if inplaceFlag != 0:
                            wf.write(line)
                                
                    if inplaceFlag != 0:
                        wf.close()

#==main==================
print ("Start time: " + str(datetime.now()))
print ("public_html dir = " + publichtml_dir)
print ("inplaceFlag = " + str(inplaceFlag) + "\n")

run(publichtml_dir, inplaceFlag)
print('\nhelpButtonsCount = ' + str(helpButtonsCount))
print('helpButtonsDelete = ' + str(helpButtonsDelete))
if exception:
    print('exception = ' + str(exception))

print("\nEnd time: " + str(datetime.now()))

    
