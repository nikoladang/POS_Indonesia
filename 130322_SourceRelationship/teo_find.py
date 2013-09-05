"""
130719: add findPosTag
"""
import sys, os, re
import teoconstants

"""
findFileNamesContainString(source_dir,('m800502002','m800500018'),0,'.jsp')
"""
def findFileNamesContainString(source_dir, findpattern_or_patterntuple, regex=0, extList=('')):
    wf = open('Job07__00_output.txt','w', -1, encoding='utf-8')
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            lowerfile = file.lower()
            if lowerfile.endswith(extList):
                if isinstance(findpattern_or_patterntuple, str):
                    findpattern = findpattern_or_patterntuple
                    if regex == 0:
                        if lowerfile.find(findpattern) != -1:
##                            print(file[:10]+'\t'+)
                            pass
                    else:
                         if re.search(findpattern, lowerfile):
                             pass
                else:
                    patterntuple = findpattern_or_patterntuple
                    if lowerfile.startswith(patterntuple):
                        print(file)

def findFilesInDirectory(root, extList=('')):
    resultList = []
    for root, dirs, files in os.walk(root):
        for file in files:
            if file.endswith(extList):
                resultList.append(root+'\\'+file)
    return resultList

"""
* ///Files in fileList must be in lowercase.
* Regex implementation: regex != 0
        Note: r'\n' for searching '\n' character without regex
* extList: list of extensions that will look for string ('.jsp','.java',..)

source_dir = r'C:\130723_DEV\DEV\src'
findString(source_dir,'import com.posco.mes.common.bl.PosBusinessLogicFactory;',exttuple=('.java'))
findString(source_dir,'showMessage.*var',regex=1, filenamelist=teoconstants.jsps)
"""
def findString(source_dir_or_fullfilepath, findpattern, regex=0, filenamelist=None, exttuple=('')):
    if filenamelist != None:
        loweredFileNameSet = set()
        for file in filenamelist:
            loweredFileNameSet.add(file.lower())
        
    if os.path.isfile(source_dir_or_fullfilepath):
        fullfilepath = source_dir_or_fullfilepath
        return self.findStringInAFile(fullfilepath, findpattern, regex)
    elif os.path.isdir(source_dir_or_fullfilepath):
        source_dir = source_dir_or_fullfilepath
        result = ''
        for root, dirs, files in os.walk(source_dir_or_fullfilepath):
            for file in files:
                if file.endswith(exttuple):
                    fullfilepath = root +"\\"+ file
                    if filenamelist != None:
                        if file.lower() in loweredFileNameSet:
                            result += findStringInAFile(fullfilepath, findpattern, regex)
                    else:
                        result += findStringInAFile(fullfilepath, findpattern, regex)
        return result
    else:
        print('InvalidPath')

"""
TODO: apply excludedstring
findPosTag(source_dir,'posui:showTextFields', filenameset=teoconstants.jsps, includedstring='isMultiLang')
"""
def findPosTag(source_dir_or_fullfilepath, tagname, includedstring=None, regex=0, filenameset=None, excludedstring=None,):
    retrieveFlag = 0 # 1: start retrieve; 2: end retrieve
    tagContent = ''
    if os.path.isfile(source_dir_or_fullfilepath):
        fullfilepath = source_dir_or_fullfilepath
        pass
    elif os.path.isdir(source_dir_or_fullfilepath):
        source_dir = source_dir_or_fullfilepath

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.jsp') and (file.lower() in filenameset):
                fullfilepath = root+'\\'+file
                print(fullfilepath)
                if os.access(fullfilepath, os.R_OK):
                    with open(fullfilepath,'r',-1,encoding='utf-8') as rf:
                        lines = rf.readlines()
                        for i, line in enumerate(lines):
##                            if(re.search(tagname, line, re.IGNORECASE)):
                            if line.find(tagname) != -1:
                                retrieveFlag = 1
                                tagContent += line
                            if retrieveFlag == 1:
                                if (not re.search('/>', line)) and (not re.search(tagname, line)):
                                    tagContent += line
                            if (re.search('/>', line)) and (retrieveFlag == 1):
                                retrieveFlag = 2
                                tagContent += line
                                if includedstring != None:
                                    if regex == 0:
                                        if tagContent.find(includedstring) != -1:
                                            sys.stdout.write(tagContent)
                                    else:
                                        if re.search(includedstring, tagContent):
                                            sys.stdout.write(tagContent)
                                        
                                else: sys.stdout.write(tagContent)
                            if retrieveFlag == 2:
                                retrieveFlag = 0
                                tagContent = ''
    

def findStringInAFile(fullfilepath, findpattern, regex=0):
    resultString = ''
    m = os.path.split(fullfilepath)
    filename = m[1]
    if os.access(fullfilepath, os.R_OK):
        with open(fullfilepath,'r',-1,encoding='utf-8') as rf:
            try:
                lines = rf.readlines()
                for i, line in enumerate(lines):
                    if regex == 0:
                        if line.find(findpattern) != -1:
                            resultString += filename +':#:'+str(i+1)+':@:'+ line
                    else:
                        if re.search(findpattern, line):
                            resultString += filename +':#:'+str(i+1)+':@:'+ line
            except:
                print(str(sys.exc_info()[1]) + fullfilepath)
    return resultString
                    


source_dir = r'C:\130805_DEV\DEV\src'
##findFileNamesContainString(source_dir,('m800502002','m800500018'),0,'.jsp')
##print(findString(source_dir,'yardui:showYardTD', filenamelist=teoconstants.jsps))
##print(findString(source_dir,'import com.posco.mes.common.bl.PosBusinessLogicFactory;',exttuple=('.java')))
##print(findString(source_dir,'showMessage.*var',regex=1, filenamelist=teoconstants.jsps))
##findPosTag(source_dir,'<posui:showUtilityButtons', filenameset=teoconstants.jsps)
##print(findString(source_dir,'getAppMessage.*(Handler|HandlerIF)\.(ERROR|INFO)',regex=1, exttuple=('.java')))
##print(findString(source_dir,'synchronize',regex=0, exttuple=('.java')))
