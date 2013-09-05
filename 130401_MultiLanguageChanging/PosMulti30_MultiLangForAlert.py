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
output_filename = r'Case30__00_log_output.txt'

inplaceFlag = 0
messageDict = {}
alertNotFoundSet = set()
alertTotalCount = 0
justChanged = 0
def run(wflog, target_dir, inplaceFlag=0):
    global alertTotalCount, alreadyChanged, justChanged
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.jsp') and (file.lower() in teoconstants.jsps):
                with open(root+"\\"+ file,'r',-1,encoding='utf-8') as rf:
                    lines = rf.readlines()
                    if inplaceFlag == 1:
                        wf = open(root+"\\"+ file,'w',-1,encoding='utf-8')
                    for i, line in enumerate(lines):
                        if(re.search('^(\t| )*alert *\(', line)):
                            alertTotalCount += 1
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
    ##                            m = re.search(r'\( *(["\'])(?P<alert>.*)\1 *\)',line)
    ##                            m = re.search(r'(?P<previousIndent>.*)alert *\( *(["\'])(?P<alert>.*)\2 *\)',line)
                            m = re.search(r'(?P<previousIndent>.*)alert *\( *(?P<sign>["\'])(?P<alert>.*)(?P=sign) *\)(?P<latter>.*)',line)
                            if m:
                                previousIndent = m.group('previousIndent')
                                latter = m.group('latter')
                                alert = m.group('alert')
                                if alert.find(r'\n') != -1:  # if the alert contains '\n' then replace with '\\n' (because the tag lib posui:showMessage with cause error if alert contains '\n')
                                    alert = alert.replace(r'\n',r'\\n')
                                keyFound = ''
                                for (k,v) in messageDict.items():
                                    if alert == v:
                                        keyFound = k
                                        line = re.sub('alert','///alert',line)
                                        newLine = previousIndent+'<posui:showMessage type="5" msg="'+keyFound+'" displayType="2" scriptTagFlag="N" isMultiLang="true"/>'+latter+'\n'
                                        line += newLine
                                        justChanged += 1
                                        teocommon.teoconsolefilelog(wflog, '\tjustChanged:#:'+file+':@:'+str(i+1)+'\t'+newLine)
                                        break
                                if keyFound != '':
                                    pass
                                else:
                                    alertNotFoundSet.add(alert)
                        if inplaceFlag != 0:
                            wf.write(line)
                    if inplaceFlag != 0:
                        wf.close()

#==main==================
wflog = open(output_filename, 'w', -1, encoding='utf-8')
teocommon.teoconsolefilelog(wflog,"Start time: " + str(datetime.now()) + '\n')
teocommon.teoconsolefilelog(wflog,"publichtml_dir = " + publichtml_dir + '\n')
teocommon.teoconsolefilelog(wflog,"inplaceFlag = " + str(inplaceFlag) + "\n\n")

messageDict = Case00_commonJobs.addDataToDict('message_ko.properties')
run(wflog, publichtml_dir, inplaceFlag)

if alertNotFoundSet:
    teocommon.teoconsolefilelog(wflog,'\nalertNotFoundSet:\n')
    for i, alert in enumerate(alertNotFoundSet):
        teocommon.teoconsolefilelog(wflog,str(i+1)+'\t@=@>'+alert+'\n')

if inplaceFlag:
    print('\nINPLACE APPLIED!!!')
teocommon.teoconsolefilelog(wflog,'\nalertTotalCount = ' + str(alertTotalCount)+'\n')
teocommon.teoconsolefilelog(wflog,'justChanged = ' + str(justChanged)+'\n')

teocommon.teoconsolefilelog(wflog,"\nEnd time: " + str(datetime.now())+'\n')
wflog.close()
