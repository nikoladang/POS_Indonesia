##http://www.saltycrane.com/blog/2007/10/python-finditer-regular-expression/
"""
Python version: 2.7
Purpose: in jsp, retrieve <title> .. </title> tag value 
130410: Initial
130411: Apply re-write to file;check the title has been change; re.IGNORECASE
    NOTE:remember add "flags=re.IGNORECASE" if want to apply case-insensitive for re.sub("re.IGNORECASE" alone not work)
    If the title has been processed, then pass ("if not ..")
    Apply backreference for regex
    Apply inplaceFlag, jspNames, jspLines, jspKeys, jspValues
130412: Apply teoconstants.uipgms
    + Remove space if can not find title at the first time
        * checkFlag = 0: original
        * checkFlag = 1: title after remove spaces
130412: implement titleCannotFound variable
"""
import sys, re, os, glob, shutil, fileinput
from datetime import datetime
import teoconstants
import Case00_commonJobs

publichtml_dir=r'C:\130712_DEV\DEV\public_html'
##root_dir='C:\\130417_dest\\'
labelDict = {}
titleCount = 0
showLabelFound=0
titleChanged = 0
titleCannotFound = 0
jspNames=[]
jspLines=[]
jspKeys=[]
jspValues=[]
checkFlagScreens=[]
checkFlagLevels=[]
titleNotFoundSet = set()
inplaceFlag=1
def run(target_dir, inplaceFlag=0):
    global titleCount, showLabelFound, titleChanged, titleCannotFound, jspNames, jspLines, checkFlagScreens, checkFlagLevels
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.jsp') and (file.lower() in teoconstants.jsps):
                print('Processing ' + file)
                with open(root+"\\"+ file,'r',-1,encoding='utf-8') as rf:
                    lines = rf.readlines()
                    if inplaceFlag == 1:
                        wf = open(root+"\\"+ file,'w',-1,encoding='utf-8')
                    for i, line in enumerate(lines):
                        if(re.search('<title>.*</title>', line, re.IGNORECASE)):
                            titleCount += 1
                            if re.search('posui:showLabel', line):
                                showLabelFound +=1
                            else:
                                title = (re.search('<title>(?P<title>.*)</title>', line, re.IGNORECASE)).group('title')
                                print("   " + file + " at line " + str(i+1) + " ==>" + title)
                                originalTitle = title
                                checkFlag = 0
                                while (checkFlag == 0) or (checkFlag == 1):
                                    for (k,v) in labelDict.items():
                                        if ((title == v) and k.endswith('0')):
                                            titleChanged += 1
                                            print('\tjustChanged ')
                                            if(checkFlag == 1):
                                                checkFlagScreens.append(file)
                                                checkFlagLevels.append(checkFlag)
                                            print('      VALUEFOUND '+file+' key = '+k+'  with checkFlag='+str(checkFlag))
                                            if inplaceFlag != 0:
                                                line = '<title>'+'<posui:showLabel key="'+k+'" />'+'</title>\n'
                                                jspNames.append(file)
                                                jspLines.append(i+1) ## because file lines start from 0
                                                jspKeys.append(k)
                                                jspValues.append(v)
                                            checkFlag = 9
                                            break
                                    if checkFlag == 0:
                                        title = title.replace(' ','')
                                        checkFlag = 1;
                                    elif checkFlag == 1:
                                        checkFlag = 2;
                                        titleCannotFound += 1
                                        titleNotFoundSet.add(originalTitle)
                                        print ('\t\tCANNOTFOUND '+ file+' title='+title )
                                    elif checkFlag == 9:
                                        break
                        if inplaceFlag != 0:
                            wf.write(line)
                    if inplaceFlag != 0:
                        wf.close()

#==main==================
print ("Start time: " + str(datetime.now()))
print ("inplaceFlag = " + str(inplaceFlag) + "\n")

labelDict = Case00_commonJobs.addDataToDict('label_ko.properties')
run(publichtml_dir, inplaceFlag)
print('\nTotal Title Count = ' + str(titleCount))
print('showLabelFound = ' + str(showLabelFound))
print('Title Changed = ' + str(titleChanged))
print('Title CANNOTFOUND = ' + str(titleCannotFound))
for i, (jsp, lineNo) in enumerate(zip(jspNames, jspLines)):
    print('  '+str(i+1)+'\t'+jsp+'\tat '+str(lineNo)+' : '+jspValues[i]+'-->'+jspKeys[i])
for j, (screen, level) in enumerate(zip(checkFlagScreens, checkFlagLevels)):
    print('    Special CheckFlagNo '+str(j+1)+': '+screen+' with checkFlag=' + str(level))
    
if inplaceFlag != 0:
    print('\n INPLACE APPLIED!!!')
print('=================')
for value in titleNotFoundSet:
    print(value)

print("\nEnd time: " + str(datetime.now()))

    
