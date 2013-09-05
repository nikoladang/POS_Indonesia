"""
130614: Initial
130619： add strippattern for printFilenameAndPackage
"""
import sys,re

class commonJobs(object):
    """
strippattern: define extension that need to be strip; if null then keep extension
    """
    def printPackageAndFilename(fullfilepath, packagepattern, strippattern=r''):
        """
C:\130521_Temp\Temp\poscoMES_M80\Pgm_Dev\2nd_iteration\src\com\posco\mes\m81\p050\app\process\m800502003\PosGetRollInstructionData.java
--->printPackageAndFilename(root+"\\"+file,r'com\\posco',r'\.java')
com.posco.mes.m81.p050.app.process.m800502003   PosGetRollInstructionData
        """
        m = re.search(r'(?P<package>{0}.*)\\(?P<filename>.*)'.format(packagepattern),fullfilepath)
        if m:
            package = m.group('package')
            package = package.replace('\\','.')
            filename = m.group('filename')
            if strippattern != '':
                filename = re.sub(strippattern,'',filename)
        else:
            return '<<<Invalid Filepath Format>>>'+fullfilepath
        return package +'\t'+ filename

    def convertToLowerdFileList(fileNameList):
        loweredFileNameList = ['']
        for file in fileNameList:
            loweredFileNameList.append(file.lower())
        return loweredFileNameList
               
