"""
130708: Initial
130709: add copyDirs
130722: add filterActiveFromPackFilenames(...)
"""
import os, shutil, re
from distutils import dir_util

"""
TODO Performance improve:
    When finish copy a file, then continue to new loop
        This will wrong when want to copy 2 file with the same name(different extensions) in same directory
         because it will copy only the first file then break ( the second file will not be copied)
    It will faster if overwrite flag = 0
"""
def copyFromPackageFilenameList(sourcedir, targetdir, packfileset, exttuple=('.java','.jsp','.xml'), overwrite=0):
    print('Begin teocommon_operation.copyFromPackageFilenameList '+ str(exttuple))
    for file in packfileset:
        if file.endswith(exttuple):
            file = file.rsplit('.',1)[0]    # remove extenstions
        tmplist = file.rsplit('.',1)
        try:
            package = tmplist[0]
            filename = tmplist[1]
        except:
            continue

        sourceroot = sourcedir +'\\'+ package.replace('.','\\')
        targetroot = targetdir +'\\'+ package.replace('.','\\')
        sourcefile = sourceroot+'\\'+filename+'.java'
        targetfile = targetroot+'\\'+filename+'.java'

        if not os.path.isdir(sourceroot):
            continue
        if targetfile.find('*') != -1:
            print('Do not copy file because this is an * import all :' + targetfile)
            continue
        if overwrite == 0:
            if os.path.isfile(targetfile):
                continue # improve performance

        for entry in os.listdir(sourceroot):
            entryfullpath = sourceroot +'\\'+ entry
            if os.path.isfile(entryfullpath):
                if entry.startswith(filename+'.'):
                    if not os.path.exists(targetroot):
                        os.makedirs(targetroot)
                    shutil.copy2(sourcefile, targetfile)
                    print('[[[CopiedAFile]]]'+targetfile)
                    break    # improve performance
                else:
##                    print('<<<FileNotMatch teocommon_operation.copyFromPack..>>>'+' '+filename+'###'+entry)
                    pass
            else:
##                print('<<<InvalidPath teocommon_operation.copyFromPack..>>>'+sourcefile)
                pass
"""
dirsset : ('com.posco.mes.m80.p050.app.monitoring.client',..)
"""
def copyDirs(sourceroot, targetroot, dirsset):
    print('teocommon_operation.copyDirs : '+sourceroot)
    for adir in dirsset:
        if adir: # Cauz if adir is empty, it will copy all root
            source = sourceroot +'\\'+ adir.replace('.','\\')
            target = targetroot +'\\'+ adir.replace('.','\\')
            if os.path.isdir(source):
                dir_util.copy_tree(source, target)
                print('[[[CopiedADir]]]'+target)
            else: print('<<<Cannot copyDirs --> Invalid directory>>>'+source)

def readFileToSet(filename):
    dataSet = set()
    if os.access(filename, os.R_OK):
        with open(filename,'r',-1,encoding='utf-8') as rf:
            lines = rf.readlines()
            for i, line in enumerate(lines):
                line = line.replace('\n','')
                dataSet.add(line)
    if not dataSet:
        print('Data set is empty. Please check file existence!')
    return dataSet


def convertFullpathToPackageFilename1(self, fullfilepath, packpattern, extension='.java'):
    fullfilepath = fullfilepath.replace('\\','.')
    fullfilepath = fullfilepath.rstrip(extension)
    m = re.search('^.*(?P<packagefilename>com\.posco\.mes.*)',fullfilepath)
    return m.group('packagefilename')
"""
input: C:\130617_Temp\Temp\poscoMES_M80\Pgm_Dev\2nd_iteration\src\com\posco\mes\m80\p050\app\monitoring\client\yarddata\PosYardObjectsMgrIF.java
output:com.posco.mes.m80.p050.app.monitoring.client.yarddata.PosYardObjectsMgrIF
.packpattern: package pattern
.extkeepf：extension keeping flag; 0: remove the extension, 1: keep the extension
"""
def convertFullpathToPackageFilename(fullfilepath, packpattern=r'com\.posco\.mes.*', extkeepf=0, addextension=''):
    tmpList = fullfilepath.rpartition('.')
    packagefilename = tmpList[0].replace('\\','.')
    if extkeepf:
        extension = '.'+tmpList[2]
    else:
        extension = ''
    m = re.search(r'^.*(?P<packagefilename>{0})'.format(packpattern), packagefilename)
    return m.group('packagefilename')+extension
    

"""
If packagefilename's containing extension, then keep it
"""
def convertPackageFilenameToFullpath(srcpath, packagefilename, addextension=''):
    if packagefilename.endswith(tuple(('.jsp','.java','.xml'))):
        tmpList = packagefilename.rpartition('.')
        filename = tmpList[0]
        extension = tmpList[2]
        fullfilepath = filename.replace('.','\\') + '.' + extension
    else:
        fullfilepath = packagefilename.replace('.','\\') + addextension
    fullfilepath = srcpath +'\\'+ fullfilepath
    return fullfilepath

def filterActiveFromPackFilenames(srcpath, packfilelist, addextension=''):
    returnList = []
    for value in packfilelist:
        fullfilepath = convertPackageFilenameToFullpath(srcpath, value, addextension)
        if os.path.isfile(fullfilepath):
            returnList.append(value)
    return returnList

##def filterActiveFromPackFilenames(srcpath, packfilelist, addextension=''):
##    returnList = []
##    for value in packfilelist:
##        if packagefilename.endswith('.jsp','.java','.xml'):
##            pass
##        else:
##            fullfilepath = srcpath +'\\'+ value.replace('.','\\')+ addextension
##        if os.path.isfile(fullfilepath):
##            returnList.append(value)
##    return returnList

##tmp = teocommon_operation()
##source_dir = r'C:\130617_Temp\Temp\poscoMES_M80\Pgm_Dev\2nd_iteration\src'
##target_dir = r'C:\130617_Tz\src'
##aset = tmp.readFileToSet('draft.txt')
##tmp.copyFromPackageFilenameList(source_dir,target_dir,aset)
