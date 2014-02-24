"""
prerequisites: use SoRe07_JSPsRelatingToPGMIDs.py for retrieve teoconstants.jsps data
130611 : Initial
130613: + apply for multi-screen
    + apply global variable for screenJavaList (IMPORTANT)
    + keep import *
    + retrieve import class from jsp
130626: write the output to file
130702: retrieve java files from cmjavafilelist
    retrieve java files from TC-NUI by conncting to MASTER DB
130708: add retrieveJavaFilesFromPackagefilenameList(..,..)

TODO: deprecate 2 functions convertPackageFilenameToFullpath, convertFullpathToPackageFileName with teocommon_operation.py
"""
from SoRe00_commonJobs import commonJobs
import teoconstants

import cx_Oracle

import os, fileinput, sys, glob, re, shutil
from datetime import datetime

##root = r'C:\130617_Temp\Temp\poscoMES_M80\Pgm_Dev\2nd_iteration'
##root = r'C:\convert_source_old5\convert_source'
##root = r'D:\03_Downloads\abc\abc\Temp\poscoMES_M60\Pgm_Dev\2nd_iteration'
root = r'C:\140107_India_CRM_M83'
config_path = root + '\config'
publichtml_path = root + '\public_html'
src_path = root + '\src'
outputfilename = 'SoRe03_RetrieveJavaSourceRelateToPGMs_00_output.txt'

screenJavaList = [] ##GLOBAL

def run():
    startTime = datetime.now()
    print ("Start time: " + str(startTime))

    rev = RetrieveJavaSourceRelateToPGMs()
    rev.main(src_path, config_path, publichtml_path, commonJobs.convertToLowerdFileList(teoconstants.jsps))

    endTime = datetime.now()
    print("\nEnd time: " + str(endTime))
    print("Processing Time = " + str(endTime - startTime))

class RetrieveJavaSourceRelateToPGMs(object):
    def main(self, srcpath, configpath, publichtmlpath, uipgmslist):
        self.wf = open(outputfilename,'w', -1, encoding='utf-8')
        self.retrieveJavaFilesFromJspAndService(srcpath, configpath, publichtmlpath, uipgmslist)
        self.retrieveJavaFilesFromTC(srcpath, teoconstants.tclist)
##        self.retrieveJavaFilesFromCMJavaFileList(srcpath, srcpath+"\\"+teoconstants.cm_package_path, teoconstants.cmjavafilelist)
        self.wf.close()

    def retrieveJavaFilesFromJspAndService(self, srcpath, configpath, publichtmlpath, uipgmslist):
        global screenJavaList
        serviceList = []
        for value in uipgmslist:
            serviceList.append(value.replace('.jsp','_service.xml'))
        for root, dirs, files in os.walk(configpath):
            for file in files:
                if file.endswith('_service.xml') and (file.lower() in serviceList):
                    self.retrieveJavaFromFile(srcpath, root+"\\"+ file)
                    for root2, dirs2, files2 in os.walk(publichtmlpath):
                        for file2 in files2:
                            if file2.endswith('.jsp') and (file2.lower() == (file.replace('_service.xml','.jsp')).lower()):
                                self.retrieveJavaFromFile(srcpath, root2+"\\"+ file2.lower())
                                break
                    filteredList = self.filterActiveJavaFileList(srcpath, screenJavaList)
                    outputstring = ''
                    for value in filteredList:
                        outputstring += 'UI' +'\t'+ file.replace('_service.xml','') +'\t'+ value +'\n'
##                        print(file.replace('_service.xml','') +'\t'+ value)
                    self.wf.write(outputstring)
                    screenJavaList[:] = []

    def retrieveJavaFilesFromTC(self, srcpath, tclist):
        global screenJavaList
        sqlbindingstring = ''
        query = teoconstants.sore03_retrievejavafromtcquery
        for tc in tclist:
            sqlbindingstring += "'" +tc+"',"
        sqlbindingstring = sqlbindingstring.rstrip(",")
        if query.find(':sqlbindingstring'):
           query = query.replace(':sqlbindingstring', sqlbindingstring)

        connstr = teoconstants.masterdbconnectionstring
        conn = cx_Oracle.connect(connstr)
        resultSet = conn.cursor()
        resultSet.execute(query)
        resultList = resultSet.fetchall()
##        for i, value in enumerate(resultSet.description):
##            print(value[0])
        previousrows0value = ''
        for i, rows in enumerate(resultList):
            if rows[0]!=previousrows0value or (i+1)==len(resultList):
                if (i+1)==len(resultList):
                    screenJavaList.append(rows[1])
                    fullfilepath = self.convertPackageFilenameToFullpath(srcpath, rows[1])
                    self.recur(srcpath, fullfilepath)
                filteredList = self.filterActiveJavaFileList(srcpath, screenJavaList)
                outputstring = ''
                for value in filteredList:
                    outputstring += 'NUI' +'\t'+ previousrows0value+'\t'+value+'\n'
                self.wf.write(outputstring)
                screenJavaList[:] = []
                if (i+1) != len(resultList):
                    screenJavaList.append(rows[1])
                    fullfilepath = self.convertPackageFilenameToFullpath(srcpath, rows[1])
                    self.recur(srcpath, fullfilepath)
            else:
                screenJavaList.append(rows[1])
                fullfilepath = self.convertPackageFilenameToFullpath(srcpath, rows[1])
                self.recur(srcpath, fullfilepath)
            previousrows0value = rows[0]
        
    
    def retrieveJavaFilesFromCMJavaFileList(self, srcpath, cmpackagepath, cmjavafilelist):
        global screenJavaList
        for root, dirs, files in os.walk(cmpackagepath):
            for file in files:
                if file in cmjavafilelist:
                    screenJavaList.append(commonJobs.printPackageAndFilename(root+"\\"+file, r'com\\posco',r'\.java').replace('\t','.'))
                    self.recur(srcpath, root+"\\"+file)
                    filteredList = self.filterActiveJavaFileList(srcpath, screenJavaList)
                    outputstring = ''
                    for value in filteredList:
                        outputstring += 'NUICM' +'\t' +file+'\t'+value+'\n'
                    self.wf.write(outputstring)
                    screenJavaList[:] = []

    def retrieveJavaFilesFromPackagefilenameList(self, srcpath, packfilenamelist):
        global screenJavaList
        for value in packfilenamelist:
            screenJavaList.append(value)
            fullfilepath = self.convertPackageFilenameToFullpath(srcpath, value)
            self.recur(src_path, fullfilepath)
        filteredList = self.filterActiveJavaFileList(srcpath, screenJavaList)
        
        returnSet = set(filteredList[:]) # clone
        screenJavaList[:] = [] # empty; This is a MUST bececause screenJavaList is global var
        return returnSet
        

    def recur(self, srcpath, fullfilepath, depth=100):
        global screenJavaList
        if depth == 0:
            return 0
        localJavaList = []
        fiG = fileinput.input(fullfilepath, inplace=0, openhook=fileinput.hook_encoded('utf-8'))
        try:
            for i, line in enumerate(fiG):
                if (re.match(r'import', line.strip())
                    and re.search(r'com\.posco\.mes\.', line)):
                    line = line.strip('import')
                    line = line.strip()
                    line = line.strip(";")
                    line = line.strip('\r\n')

                    if line not in screenJavaList:
                        localJavaList.append(line)
##                        print('Depth ' + str(depth) + '\t'+ line +'\t'+fullfilepath)  ##

                if re.search(r'public class', line):    #performance improve
                    break;
        except:
            outputstring = str(sys.exc_info()[0]) + fullfilepath +'\n'
##            self.wf.write(outputstring)
            return 0
        finally:
            fiG.close()

        for value in localJavaList:
            if value not in screenJavaList: ##
                screenJavaList.append(value)
                if not re.search(r'\*',value):
                    value = value.replace('.','\\') + ('.java')
                    value = srcpath +'\\'+ value
    ##                print(value)
                    self.recur(srcpath, value, depth-1)

    def filterActiveJavaFileList(self, srcpath, filelist):  ##remove the does-not-exist file out of list
        newlist = []
        for value in filelist:
            filepath = srcpath +'\\'+ value.replace('.','\\') + '.java'
            if os.path.isfile(filepath) or re.search(r'com\.posco\.mes.*\*',value):
                newlist.append(value)
        return newlist

    def convertPackageFilenameToFullpath(self, srcpath, packagefilename, extension='.java'):
        fullfilepath = packagefilename.replace('.','\\') + extension
        fullfilepath = srcpath +'\\'+ fullfilepath
        return fullfilepath
    """
    input: C:\130617_Temp\Temp\poscoMES_M80\Pgm_Dev\2nd_iteration\src\com\posco\mes\m80\p050\app\monitoring\client\yarddata\PosYardObjectsMgrIF.java
    output:com.posco.mes.m80.p050.app.monitoring.client.yarddata.PosYardObjectsMgrIF
    """
    def convertFullpathToPackageFileName(self, fullfilepath, extension='.java'):
        fullfilepath = fullfilepath.replace('\\','.')
        fullfilepath = fullfilepath.rstrip(extension)
        m = re.search('^.*(?P<packagefilename>com\.posco\.mes.*)',fullfilepath)
        return m.group('packagefilename')

    """
    Service.xml: - 
    JSP: - '<%@ page import="com.posco.mes.m80.p050.app.constants.PosM800ConstantsIF" %>'
         - '<jsp:useBean id="m80_Bean" class="com.posco.mes.m80.p050.ui.bean.PosM800501003Beans" />'
    """
    def retrieveJavaFromFile(self, srcpath, fullfilepath):
        global screenJavaList
        javafilesFound = []
        f = fileinput.input(fullfilepath, inplace=0, openhook=fileinput.hook_encoded('utf-8'))
        if re.search(r'_service.xml',fullfilepath):
            p = re.compile(r'\<process name.*class *\= *"(?P<fullclass>com\.posco\.mes.*?)"')
        elif re.search(r'.jsp', fullfilepath):
            p = re.compile(r'(page *import *\= *"|\<jsp\:useBean.*)(?P<fullclass>com\.posco\.mes.*?)"')
        for i, line in enumerate(f):
            if p.search(line):
                m = p.search(line)
                fullclass = m.group('fullclass')
                m2 = re.search(r'^(?P<package>.*)\.(?P<classname>.*)',fullclass)
                classname = m2.group('classname')
                package = m2.group('package')
    ##                            print(file +'\t'+ classname +'\t'+ package)
                fullfilepath = self.convertPackageFilenameToFullpath(srcpath, fullclass)
                javafilesFound.append(fullfilepath)
        f.close()
        for value in javafilesFound:
            convertedValue = self.convertFullpathToPackageFileName(value)
            if convertedValue not in screenJavaList:
                screenJavaList.append(convertedValue)
            self.recur(srcpath, value)
