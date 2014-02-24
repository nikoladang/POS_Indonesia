"""
130619 : Initial
"""
import SoRe04_RetrieveVOFromJavaJsp_00_constants as constants
import teocommon_operation
from SoRe00_commonJobs import commonJobs

import os, sys, re
from datetime import datetime

root = r'C:\140107_India_CRM_M83'

src_path = root + '\src'
outputfilename = 'SoRe04_RetrieveVOFromJavaJsp_output.txt'
publichtml_path = root + '\public_html'

class RetrieveVOFromJavaJsp(object):
    def main(self):
        self.wf = open(outputfilename,'w', -1, encoding='utf-8')
        self.wf.write(str(datetime.now())+'\t'+root+'\n')
        self.retrieveVOFromJava(src_path)
        self.retrieveVOFromJsp(publichtml_path)
        self.wf.close()

    def retrieveVOFromJava(self, srcpath):
        for root, dirs, files in os.walk(srcpath):
            for file in files:
                if file.endswith('.java'):
                    self.core_fileprocess(root+'\\'+file, 'java')

    def retrieveVOFromJsp(self, publichtmlpath):
        for root, dirs, files in os.walk(publichtmlpath):
            for file in files:
                if file.endswith('.jsp'):
                    self.core_fileprocess(root+'\\'+file, 'jsp')

    def core_fileprocess(self, fullfilepath, filetype):
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
                                if filetype == 'java':
                                    outputstring += commonJobs.printPackageAndFilename(fullfilepath,r'com\\posco')+'\t:::'+str(i+1)+line.replace('\t',' ')  #normalize by remove tab in lines
                                elif filetype == 'jsp':
                                    outputstring += commonJobs.printPackageAndFilename(fullfilepath,r'public_html\\')+'\t:::'+str(i+1)+line.replace('\t',' ')
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

    endTime = datetime.now()
    print("\nEnd time: " + str(endTime))
    print("Processing Time = " + str(endTime - startTime))
