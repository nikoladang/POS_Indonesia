"""
Purpose:
. getAppMessage(String msgid, String msgType, boolean isMultiLang)  => ex) getAppMessage("M23JS2011", PosMessageHandlerIF.ERROR,true)

. getAppMessage(String msgid, String[] var, String msgType, boolean isMultiLang) => getAppMessage("M50100122",val, PosMessageHandlerIF.ERROR, true) 
Example:
    From:
        String msg2 = msgHandler.getAppMessage("M80JS2257", PosMessageHandlerIF.ERROR).getMessageCont();
        rtnMsg = msgHandler.getAppMessage(P_M80JS1096, val, msgHandler.INFO).getMessageCont();
    To:
        String msg2 = msgHandler.getAppMessage("M80JS2257", PosMessageHandlerIF.ERROR, true).getMessageCont();
        rtnMsg = msgHandler.getAppMessage(P_M80JS1096, val, msgHandler.INFO, true).getMessageCont();
130729: Initial
NOTE: Remeber to re-check <<<EXCEPTION>>> entries
"""
import sys, os, re
from datetime import datetime

src_dir=r'C:\130723_DEV\DEV\src'

inplaceFlag = 1

def run(target_dir, inplaceFlag=0):
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.java'):
                with open(root+'\\'+file,'r',-1,encoding='utf-8') as rf:
                    lines = rf.readlines()
                    if inplaceFlag == 1:
                        wf = open(root+'\\'+file,'w',-1,encoding='utf-8')
                    for i, line in enumerate(lines):
                        if line.find('getAppMessage') != -1:
                            m = re.search('getAppMessage.*(?P<appendto>(Handler|HandlerIF)\.(DEBUG|INFO|WARN|ERROR|FATAL))',line)
                            if m:
                                appendto = m.group('appendto')
                                if re.search(appendto+' *, *true', line):
                                    sys.stdout.write('[[[AlreadyChanged]]]'+file +':#:'+str(i+1)+':@:'+ line)
                                else:
                                    sys.stdout.write(file +':#:'+str(i+1)+':@:'+ line)
                                    line = line.replace(appendto,appendto+', true')
                                    sys.stdout.write('==>'+line)
                            else:
                                sys.stdout.write('<<<EXCEPTION>>>'+file +':#:'+str(i+1)+':@:'+ line)

                        if inplaceFlag == 1:
                            wf.write(line)
                    if inplaceFlag == 1:
                        wf.close()

#==main==================
print ("Start time: " + str(datetime.now()))
print ("src_dir = " + src_dir)
print ("inplaceFlag = " + str(inplaceFlag) + "\n")

run(src_dir, inplaceFlag)

if inplaceFlag:
    print('\nINPLACE APPLIED!!!')

print("\nEnd time: " + str(datetime.now()))
