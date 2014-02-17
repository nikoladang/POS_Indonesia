"""
130619 : Initial
"""
import SoRe04_RetrieveVOFromJavaJsp_00_constants as constants
import teocommon_operation

import os, sys, re
from datetime import datetime

root = r'C:\140107_India_CRM_M83'

src_path = root + '\src'
outputfilename = 'SoRe04_00_output_JavaJsp.txt'
##config_path = root + '\config'
publichtml_path = root + '\public_html'

class RetrieveVOFromJavaJsp(object):
    def main(self):
        self.wf = open(outputfilename,'w', -1, encoding='utf-8')
        self.retrieveVOFromJava(src_path)
        self.retrieveVOFromJsp(publichtml_path)
        self.wf.close()

    def retrieveVOFromJava(self, srcpath):
        for root, dirs, files in os.walk(srcpath):
            for file in files:
                if file.endswith('.java'):
                    self.core_fileprocess(root+'\\'+file)

    def retrieveVOFromJsp(self, publichtmlpath):
        for root, dirs, files in os.walk(publichtmlpath):
            for file in files:
                if file.endswith('.jsp'):
                    self.core_fileprocess(root+'\\'+file)
    
    def core_fileprocess(self, fullfilepath):
        if os.access(fullfilepath, os.R_OK):
            with open(fullfilepath,'r',-1,encoding='utf-8') as fp:
                try:
                    lines = fp.readlines()
                    outputstring = ''
                    for i,line in enumerate(lines):
                        for function in constants.functionsContainVO:
                            p = re.compile(r'\b{0}'.format(function))
                            m = p.search(line)
                            if m:
                                outputstring += fullfilepath+':::'+str(i+1)+'\t'+line
##                                sys.stdout.write(fullfilepath+':::'+str(i+1)+'\t'+line)
                                break   #need for improve performance
                    self.wf.write(outputstring)
                except:
                    print(str(sys.exc_info()[0]) + fullfilepath)

def run():
    startTime = datetime.now()
    print ("Start time: " + str(startTime))

    temp = RetrieveVOFromJavaJsp()
    temp.main()
    ##temp.fileprocess(r'C:\130617_Temp\Temp\poscoMES_M80\Pgm_Dev\2nd_iteration\src\com\posco\mes\m80\p050\app\process\GetYdOpIndiPrgStatTp.java')

    endTime = datetime.now()
    print("\nEnd time: " + str(endTime))
    print("Processing Time = " + str(endTime - startTime))
run()
