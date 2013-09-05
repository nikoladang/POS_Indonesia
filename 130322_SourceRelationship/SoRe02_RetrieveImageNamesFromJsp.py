"""
Purpose: retrieve all gif files used inside jsp
130611 : Initial
"""
from  Job07_JSPsRelatingToPGMIDs import JSPsRelatingToPGMIDs
import teoconstants
##from Job00_commonJobs import commonJobs

import os, fileinput, sys, re, shutil

target=r'C:\130521_Temp\Temp\poscoMES_M80\Pgm_Dev\2nd_iteration\public_html'

imageList = []
class RetrieveImageNamesFromJsp(object):
    def main(self, target_dir):
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.endswith('.jsp') and (file.lower() in teoconstants.uipgms):
                    f = fileinput.input(root+"\\"+ file, inplace=0, openhook=fileinput.hook_encoded('utf-8'))

                    for i, line in enumerate(f):
                        iterator = re.finditer(r'^.*(?P<imagename>\b.+\.gif\b)', line, re.IGNORECASE)
                        for match in iterator:
##                            print(file+':'+str(i+1)+'\t'+match.group('imagename'))
                            if (match.group('imagename') not in imageList):
                                imageList.append(match.group('imagename'))

                    if (imageList):
                        for value in imageList:
##                            print(commonJobs.printFilenameAndPackage(file,root,'public_html.*',r'\.jsp'))
                            print(file + '\t' + value)
                        imageList[:] = []



def run():
    pass
##    rev = RetrieveImageNamesFromJsp()
##    rev.main(target)
####    root = r'C:\130821_DEV\DEV'
####    config_dir = root + '\config'
####    publichtml_dir = root + '\public_html'
####    
####    x = JSPsRelatingToPGMIDs()
####    result = x.main(config_dir, publichtml_dir, teoconstants.uipgms)
####    for value in result:
####        print('----------@@##$$%%-------')
####        print(value)
    ##commonJobs.printFilenameAndPackage('fefsfsfs.java','com\\posco\\', r'com\\posco.*')
    ##print(commonJobs.printFilenameAndPackage.__doc__)
