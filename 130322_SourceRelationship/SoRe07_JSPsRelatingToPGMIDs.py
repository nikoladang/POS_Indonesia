"""
Purpose: retrieve jsp from service, jsp files
Cases: 3 cases
    1. All the jsp that START with the same pgm pattern
    2. In _service.xml file: strings that ends with .jsp
    3. In .jsp file: jsp import pattern
    4. In jsp file: window.open(..)  <-- MANUALLY
130701: Initial
130821: main function return result 
"""
from SoRe00_commonJobs import commonJobs
import teocommon_operation
import teoconstants

import sys, os, re
from datetime import datetime

root = r'C:\140107_India_CRM_M83'
output_filename = r'SoRe07_00_output.txt'

def run():
    startTime = datetime.now()
    print ("Start time: " + str(startTime))
    
    config_dir = root + '\config'
    publichtml_dir = root + '\public_html'
    tmp = JSPsRelatingToPGMIDs()
    tmp.main(config_dir, publichtml_dir, teoconstants.uipgms,output_filename)

    endTime = datetime.now()
    print("\nEnd time: " + str(endTime))
    print("Processing Time = " + str(endTime - startTime))

class JSPsRelatingToPGMIDs(object):
    def main(self, configdir, publichtmldir, uipgms, outputfilename=''):
        patternset = set()
        for value in uipgms:
            patternset.add(value.rstrip('.jsp'))

        #Step 1
        aSet = self.findFileNamesContainString(publichtmldir,tuple(patternset),0,'.jsp')

        #Then Step 2
        mainList = self.transformToSubLists(aSet, replaceextension='_service.xml')
        bSet = self.retrieveJSPsFromServiceFile(configdir, mainList)

        #Then Step 3
        resultSet = []
        resultSet.extend(aSet)
        resultSet.extend(bSet)
        cSet = self.retrieveJSPsFromJSPFile(publichtmldir, resultSet)
        resultSet.extend(cSet)

        returnList = []
        if outputfilename:
            wf = open(outputfilename,'w', -1, encoding='utf-8')
        for value in sorted(set(resultSet)):
            splitList = value.split('\t')
##            packfilename = value.partition('\t')[2].replace('\t','.').replace('public_html.','')
            packfilename =  splitList[1].replace('public_html.','') +    \
                            '.' +   \
                            splitList[2]
                    
            fullfilepath = teocommon_operation.convertPackageFilenameToFullpath(publichtmldir, packfilename)
            returnList.append(value)
            if os.path.isfile(fullfilepath):    #filter active files for the final result
                if outputfilename:
                    wf.write(value+'\n')
                pass
            else:
                print('<<<JSP file does not exist!!!>>>'+value)
                
        if outputfilename:
            wf.close()

        return returnList

    def findFileNamesContainString(self, source_dir, findpattern_or_patterntuple, regex=0, extList=('')):
        """
        Job07__00_output.txt:   ProgramID | package | filename
        patterntuple: MUST be a tuple. (can create a set or list at first, then cast to tuple)
                         because endswith(..) only accept tuple
        """
        created_program_id = 'findFileNamesContainString<<Job07_JSPsRelatingToPGMIDs'
        print('Start 1' + created_program_id)
        returnSet = []
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                lowerfile = file.lower()
                if lowerfile.endswith(extList):
                    if isinstance(findpattern_or_patterntuple, str):    # one pgm
                        findpattern = findpattern_or_patterntuple
                        if regex == 0:
                            if lowerfile.find(findpattern) != -1:
                                returnSet.append(findpattern.lower()+'\t'+commonJobs.printPackageAndFilename(root+"\\"+file,r'public_html')+'\t'+created_program_id)
                        else:
                            if re.search(findpattern, lowerfile):
                                pass
                    else:    # many pgms
                        patterntuple = findpattern_or_patterntuple
##                        if lowerfile.startswith(patterntuple):
##                            returnSet.append(file[:10].lower()+'\t'+commonJobs.printPackageAndFilename(root+"\\"+file,r'public_html'))                        
                        for findpattern in patterntuple:
                            if regex == 0:
                                if lowerfile.find(findpattern) != -1:
                                    returnSet.append(findpattern.lower()+'\t'+commonJobs.printPackageAndFilename(root+"\\"+file,r'public_html')+'\t'+created_program_id)
        return returnSet

    def retrieveJSPsFromServiceFile(self, configdir, pgmidandservicesublists):
        created_program_id = 'retrieveJSPsFromServiceFile<<Job07_JSPsRelatingToPGMIDs'
        print('Start 2' + created_program_id)
        returnSet = []
        for value in pgmidandservicesublists:
            fileFoundFlag = 0
            for root, dir, files in os.walk(configdir):
                for file in files:
                    if file.lower() == value[1].lower():
                        fileFoundFlag = 1
                        with open(root+"\\"+ file,'r',-1,encoding='utf-8') as rf:
                            lines = rf.readlines()
                            for line in lines:
                                if line.find('.jsp') != -1:
                                    m = re.search('value.*\=.*"(.*\.jsp)', line)
                                    if m:
                                        n = re.search('.*config(.*)service',root)
                                        package = 'public_html.' + n.group(1).replace('\\','')
                                        returnSet.append(value[0] +'\t'+ package + '\t'+m.group(1)+'\t'+created_program_id)
                if fileFoundFlag == 1:
                    break
        return returnSet

    def retrieveJSPsFromJSPFile(self, publichtmldir, pgmidandjsplist):
        created_program_id = 'retrieveJSPsFromJSPFile<<Job07_JSPsRelatingToPGMIDs'
        print('Start 3' + created_program_id)
        returnSet = set()
        for value in pgmidandjsplist:
            splitList = value.split('\t')
            pgmid = splitList[0]
            jspfile = splitList[1] +'\\'+ splitList[2]
            jspfile = jspfile.replace('\t','.').replace('public_html.','').rstrip('.jsp')
            fullfilepath = teocommon_operation.convertPackageFilenameToFullpath(publichtmldir, jspfile,'.jsp')
            if os.path.isfile(fullfilepath):
                with open(fullfilepath,'r',-1,encoding='utf-8') as rf:
                    lines = rf.readlines()
                    for i, line in enumerate(lines):
                        # tb_m00_screen_vs_jsps : pgmid | jsp_filepackage | jsp_filename | created_program_id
                        if re.search('<%@.*\.jsp',line):    #case 3
                            m = re.search('<%@.*"(.*)"', line)
                            if m:
                                returnSet.add(pgmid+'\t[[[JSP imported]]]<from '+jspfile+'>\t'+m.group(1)+'\t'+created_program_id)
                        if re.search('window\.open',line):  #case 4
                            line = line.replace('\t','')
                            line = splitList[2]+':#:'+str(i+1)+':@:'+line
                            teokeepf = '*'
                            returnSet.add(pgmid+'\t[[[JSP window.open(..)]]]<from '+jspfile+'>\t'+line+'\t'+created_program_id + '\t'+teokeepf)
            else:
                pass
        return returnSet

    def transformToSubLists(self, stringslist, replaceextension=''): #private class
        returnList = []
        if not replaceextension:
            print('[[[replaceextension is NULL!]]]')
        for string in stringslist:
            splitList = string.split('\t')
            pgmid = splitList[0]
            file = splitList[2]
            if replaceextension:
                file = file.replace('.jsp',replaceextension)
            subList = []
            subList.append(pgmid)
            subList.append(file)
            returnList.append(subList)
        return returnList
