##http://www.saltycrane.com/blog/2007/10/python-finditer-regular-expression/
"""
Python version: 2.7
Purpose: apply multilang for alert
130514: Initial
"""
import teoconstants
import Case00_commonJobs
import teocommon

import sys, re, os, glob, shutil, fileinput
from datetime import datetime

##publichtml_dir=r'C:\130502_TempSources\130318_Temp\Temp\poscoMES_M80\Pgm_Dev\2nd_iteration\public_html'
publichtml_dir=r'C:\130828_DEV\DEV\public_html'
output_filename = r'Case31__00_log_output.txt'

inplaceFlag = 0
messageDict = {}
confirmNotFoundSet = set()
confirmTotalCount = 0
justChange = 0

def run(wflog, target_dir, inplaceFlag=0):
    global confirmTotalCount, alreadyChanged, justChange
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.jsp') and (file.lower() in teoconstants.jsps):
                with open(root+"\\"+ file,'r',-1,encoding='utf-8') as rf:
                    lines = rf.readlines()
                    if inplaceFlag != 0:
                        wf = open(root+"\\"+ file,'w',-1,encoding='utf-8')
                    for i, line in enumerate(lines):
                        if(re.search('^(\t| )*.*confirm *\(', line) and not re.search('^(\t| )*//',line)):
                            confirmTotalCount += 1
                            teocommon.teoconsolefilelog(wflog, file+' '+str(i+1)+':'+line)
                            if re.search('\<%',line):
                                teocommon.teoconsolefilelog(wflog, '\t\tmanually change case 01!!!\n')
                                if inplaceFlag != 0:
                                    wf.write(line)
                                continue
                            elif re.search('["\'] *\+',line) or re.search('\+ *["\']',line):
                                teocommon.teoconsolefilelog(wflog, '\t\tmanually change case 02!!!\n')
                                if inplaceFlag != 0:
                                    wf.write(line)
                                continue
                            elif not re.search('["\']',line):
                                teocommon.teoconsolefilelog(wflog, '\t\tcareful manually change case 03!!!\n')
                                if inplaceFlag != 0:
                                    wf.write(line)
                                continue
##                            m = re.search(r'(?P<previousIndent>.*)confirm *\( *(?P<sign>["\'])(?P<confirm>.*)(?P=sign) *\)(?P<latter>.*)',line)
                            m = re.search(r'(?P<previousIndent>.*)confirm *\( *(?P<sign>["\'])(?P<confirm>.*)(?P=sign) *\)(?P<latter>.*)',line)
                            if m:
                                previousIndent = m.group('previousIndent')
                                latter = m.group('latter')
                                findString = m.group('confirm')
                                if findString.find(r'\n') != -1:# if the alert contains '\n' then replace with '\\n' (because the tag lib posui:showMessage with cause error if alert contains '\n')
                                    findString = findString.replace(r'\n',r'\\n')
                                keyFound = ''
                                for (k,v) in messageDict.items():
                                    if findString == v:
                                        keyFound = k
                                        line = re.sub('^','///',line)
                                        newLine = previousIndent+'<posui:showMessage type="5" msg="'+keyFound+'" displayType="4" scriptTagFlag="N" isMultiLang="true"/>'+latter+'\n'
                                        line += newLine
                                        justChange += 1
                                        teocommon.teoconsolefilelog(wflog, '\tjustChanged:#:'+file+':@:'+str(i+1)+'\t'+newLine)
                                        break
                                if keyFound != '':
                                    pass
                                else:
                                    confirmNotFoundSet.add(findString)
                        if inplaceFlag == 1:
                            wf.write(line)
                    if inplaceFlag == 1:
                        wf.close()

#==main==================
wflog = open(output_filename, 'w', -1, encoding='utf-8')
teocommon.teoconsolefilelog(wflog,"Start time: " + str(datetime.now()) + '\n')
teocommon.teoconsolefilelog(wflog,"publichtml_dir = " + publichtml_dir + '\n')
teocommon.teoconsolefilelog(wflog,"inplaceFlag = " + str(inplaceFlag) + "\n\n")


messageDict = Case00_commonJobs.addDataToDict('message_ko.properties')
run(wflog, publichtml_dir, inplaceFlag)

if confirmNotFoundSet:
    teocommon.teoconsolefilelog(wflog,'\nconfirmNotFoundSet:\n')
    for i, value in enumerate(confirmNotFoundSet):
        teocommon.teoconsolefilelog(wflog,str(i+1)+'\t@=@>'+value+'\n')

if inplaceFlag:
    print('\nINPLACE APPLIED!!!')
teocommon.teoconsolefilelog(wflog,'\nconfirmTotalCount = ' + str(confirmTotalCount)+'\n')
teocommon.teoconsolefilelog(wflog,'justChange = ' + str(justChange)+'\n')

teocommon.teoconsolefilelog(wflog,"\nEnd time: " + str(datetime.now())+'\n')
wflog.close()
