##http://www.saltycrane.com/blog/2007/10/python-finditer-regular-expression/
"""
Python version: 2.7
Purpose: posui:Title Image Application
Applied Cases:
    -
    -
    -
Not applied cases:
    - srcs attribute belongs to <posui:showImageButtons
                                    srcs="/img/m800004butstx.gif|/img/m800009butstx.gif|/img/m800017butstx.gif|/img/m800018butstx.gif|/img/m800027butstx.gif"
                                    ... />
    -
Manually do case : images/ (because only find 2 entries with this case)
    - <td height=5 colspan=2><img src="images/blank.gif" width=1 height=5></td>
130415: Initial
"""
import sys, re, os, glob, shutil, fileinput
from datetime import datetime
import teoconstants

publichtml_dir=r'C:\draft\zzz'
inplaceFlag = 0

imgSrcCount = 0
alreadyChanged = 0
justChange = 0
exception = 0
jspNames=[]
jspLines=[]
def run(target_dir, inplaceFlag=0):
    global imgSrcCount, alreadyChanged, justChange, jspNames, jspLines, exception
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.jsp') and (file.lower() in teoconstants.jsps):
                if inplaceFlag == 0:   #improve performance
                    f = fileinput.input(root+"\\"+ file, inplace=inplaceFlag, openhook=fileinput.hook_encoded('utf-8'))
                elif inplaceFlag == 1:
                    f = fileinput.input(root+"\\"+ file, inplace=inplaceFlag)
                with open(root+"\\"+ file,'r',-1,encoding='utf-8') as rf:
                    lines = rf.readlines()
                    if inplaceFlag == 1:
                        wf = open(root+'\\'+file, 'w',-1,encoding='utf-8')
                    for i, line in enumerate(lines):
                        if((re.search('<img src=', line, re.IGNORECASE) or (re.search('input type\=.?image', line, re.IGNORECASE))
                            or (re.search('background.*:.*url.*/img', line, re.IGNORECASE)))
                        and not re.search('<img src=.*images/', line, re.IGNORECASE)):
                            imgSrcCount += 1
                            if(re.search('posui:showResourceValue',line)):
                               alreadyChanged += 1
                            else:
                                m = re.search('/img/(?P<imgName>.*\.gif)',line)
                                if m :
                                    imgName = m.group('imgName')
                                    line = line.replace('/img/','')
                                    line = line.replace(imgName,'<posui:showResourceValue key="image"  type="2"/>'+imgName)
                                    jspNames.append(file)
                                    jspLines.append(i+1) ## because file lines start from 0
                                    justChange += 1
                                    sys.stdout.write(file+' at '+str(i+1)+':'+line)
                                else:
                                    sys.stdout.write('<<<EXCEPTION>>>'+file+' at '+str(i+1)+':'+line)
                                    exception += 1
                                    
                        if inplaceFlag != 0:
                            wf.write(line)
            
                    if inplaceFlag != 0:
                        wf.close()

#==main==================
print ("Start time: " + str(datetime.now()))
print ("public_html dir = " + publichtml_dir)
print ("inplaceFlag = " + str(inplaceFlag) + "\n")

run(publichtml_dir, inplaceFlag)

if inplaceFlag:
    print('\nINPLACE APPLIED!!!')
print('\nimgSrcCount = ' + str(imgSrcCount))
print('alreadyChanged = ' + str(alreadyChanged))
print('justChange = ' + str(justChange))
print('exception = ' + str(exception))

if inplaceFlag == 1 and jspNames:
    print('\n========Changing Details========')
    for i, (jsp, lineNo) in enumerate(zip(jspNames, jspLines)):
        print('  '+str(i+1)+'\t'+jsp+'\tat '+str(lineNo))

print("\nEnd time: " + str(datetime.now()))

    
