"""
130708: Initial
"""
import teocommon_operation
import teo_find
from Job03_RetrieveJavaSourceRelateToPGMs import RetrieveJavaSourceRelateToPGMs

from bs4 import BeautifulSoup

import shutil, os, sys, re, logging, time
from distutils import dir_util
from subprocess import Popen
from datetime import datetime

source_root = r'C:\130805_DEV\DEV'
target_root = r'C:\130805_DEV_temp'
lib_dir = r'C:\draft\draft'
batchFile = r'SlabYard_Builds.bat'
logFile = r'teoAntLog.txt'

buildFile = target_root+'\\'+'build.xml'
source_dir = source_root + '\zzzsrc'
target_dir = target_root + '\src'

class CopyJavaFromListAndComplie(object):
    def main(self):
##        print('Begin JOB0 (Copied lib_dir)')
##        dir_util.copy_tree(lib_dir, target_root) # copy libs
##
##        print('Begin JOB1 (Copied main set file)')
##        mainset = teocommon_operation.readFileToSet('Job11_CopyJavaFromListAndCompile_00_input_mainshort.txt')
##        self.copyFromPackageFilenameList(source_dir,target_dir,mainset)
##
##        print('Begin JOB2 (Copied manually files)')
##        self.manuallyCopyFilesProcessing(source_dir, target_dir, 'Job11_CopyJavaFromListAndCompile_00_input_manualcopyfiles.txt')
##
##        print('Begin JOB3 (Copied manually dirs)')
##        ## can choose one of two below functions or both 
####        dirsset = self.retrieveDirectoriesFromBuildXMLFile(source_dir, buildFile)
##        dirsset = teocommon_operation.readFileToSet('Job11_CopyJavaFromListAndCompile_00_input_manualcopydirs_copyandsolveimport.txt')
##        self.manuallyCopyDirsProcessing(source_dir, target_dir, dirsset)

        print('Begin JOB4 (run batch and process log file)')
        self.runBatchFileAndProcessLogFile(target_root, batchFile, logFile)

    def manuallyCopyFilesProcessing(self, sourcedir, targetdir, filename):
        job03class = RetrieveJavaSourceRelateToPGMs()
        filesset = teocommon_operation.readFileToSet(filename)
        relatedjavafoundset = job03class.retrieveJavaFilesFromPackagefilenameList(sourcedir, filesset)
        self.copyFromPackageFilenameList(source_dir,target_dir,relatedjavafoundset)

    def manuallyCopyDirsProcessing(self, sourcedir, targetdir, packdirsset):
        teocommon_operation.copyDirs(sourcedir, targetdir, packdirsset)
        # solve the consequences for the above command
        job03class = RetrieveJavaSourceRelateToPGMs()
        javafoundset = set()
        for packdir in packdirsset:
            fulldirpath = sourcedir+'\\'+packdir.replace('.','\\')
            if os.path.isdir(fulldirpath):
                filesList = teo_find.findFilesInDirectory(fulldirpath,'.java')
                for file in filesList:
                    packagefilename = job03class.convertFullpathToPackageFileName(file)
                    javafoundset.add(packagefilename)

        relatedjavafoundset = job03class.retrieveJavaFilesFromPackagefilenameList(sourcedir, javafoundset)
        self.copyFromPackageFilenameList(sourcedir,targetdir,relatedjavafoundset)

    def copyFromPackageFilenameList(self, sourcedir, targetdir, dirsset):
        teocommon_operation.copyFromPackageFilenameList(sourcedir,targetdir,dirsset)        

    def runBatchFileAndProcessLogFile(self, root, batchfilename, logfilename):
        while True:
            p = Popen(target_root+'\\'+batchFile, cwd=target_root)
            stdout, stderr = p.communicate()
            retrievedSet = self.retrieveJavasFromLog(target_root+'\\'+logFile)

            if not retrievedSet:
                break
            job03class = RetrieveJavaSourceRelateToScreen()
            relatedjavafoundset = job03class.retrieveJavaFilesFromPackagefilenameList(source_dir, retrievedSet)
            self.copyFromPackageFilenameList(source_dir,target_dir,relatedjavafoundset)

    def retrieveJavasFromLog(self, logfilename):
        returnSet = set()
        setsfromlog = self.parseLogForSubsets(logfilename)
        if setsfromlog:
            for value in setsfromlog:
                newstring = value[1].rpartition('.')[0]+'.'+value[0]
                returnSet.add(newstring)
        return returnSet
        
    def parseLogForSubsets(self, logfilename):
        resultSet = set()
        if os.access(logfilename, os.R_OK):
            with open(logfilename,'r',-1,encoding='utf-8') as fp:
                try:
                    lines = fp.readlines()
                    resultList = []

                    for i,line in enumerate(lines):
                        if re.search('^    \[javac\] symbol  : class',line) \
                           or re.search('^    \[javac\] symbol  : variable',line):
                            line = re.sub(r'\n','',line)
                            line = line.rstrip()
                            symbol = line.rpartition(r' ')[2]
                        if re.search('^    \[javac\] location: class',line) \
                           or re.search('^    \[javac\] location: interface',line):
                            line = re.sub(r'\n','',line)
                            line = line.rstrip()
                            location = line.rpartition(r' ')[2]
                            subList = []
                            subList.append(symbol)
                            subList.append(location)
                            resultList.append(subList)
                    resultSet = set(tuple(sorted(i)) for i in resultList) # remove duplications
                    return resultSet
                except:
##                    print(str(sys.exc_info()[0])+str(sys.exc_info()[1])+str(sys.exc_info()[2]))
                    logging.exception("Something awful happened!")
                    
    def retrieveDirectoriesFromBuildXMLFile(self, srcpath, buildfilename, mindirdepth=6):
        """
        mindirdepth: the least occurences of '.' character in string
        """
        resultSet = set()
        if os.access(buildfilename, os.R_OK):
            with open(buildfilename,'r',-1,encoding='utf-8') as rf:
                try:
                    lines = rf.readlines()
                    filecontent = ''
                    for line in lines:
                        filecontent += line

                    soup = BeautifulSoup(filecontent)
                    tmpSet = set()
                    for tag in soup.find_all('include'):
                        value = tag['name']
                        if re.search('com/posco/mes.*\*\*',value):
                            value = value.rpartition('/**')[0]
                            value = value.replace('/','.')
                            if value.count('.') >= mindirdepth: ###
                                tmpSet.add(value)
                    resultSet = self.filterActiveDirs(srcpath, tmpSet)
                    return resultSet
                except:
                    logging.exception('ERROR in retrieveDirectoriesFromBuildXMLFile(..)')
                    pass
                
    def filterActiveDirs(self, srcpath, dirset):
        resultSet = set()
        for adir in dirset:
            dirpath = srcpath +'\\'+ adir.replace('.','\\')
            if os.path.isdir(dirpath):
                resultSet.add(adir)
        return resultSet

def run():
    startTime = datetime.now()
    print ("Start time: " + str(startTime))
    
    tmp = CopyJavaFromListAndComplie()
    tmp.main()
    ##x = tmp.retrieveDirectoriesFromBuildXMLFile(source_dir, target_root+'\\'+'build.xml')
    ##for i in x:
    ##    print(i)
        
    ##tmp2.copyDirs(source_dir, target_dir, x)
    
    endTime = datetime.now()
    print("\nEnd time: " + str(endTime))
    print("Processing Time = " + str(endTime - startTime))

run()
