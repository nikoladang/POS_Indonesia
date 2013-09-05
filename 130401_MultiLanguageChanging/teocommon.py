"""
130701: add extList parameter for findString()
"""
import os, shutil, re, fileinput, sys

def rmtree(self, target_dir):
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
        print('Already delete '+target_dir)
    else:
        print(target_dir+' does not exist! Can not delete this directory.')

def cptree(self, source_dir, target_dir):
##        shutil.copytree("C:\draft\src", target_dir, ignore=shutil.ignore_patterns('*.*'))
    shutil.copytree(source_dir, target_dir)
    print('Copy tree successfully!')

"""
* files in fileList must be in lowercase.
"""
def copyListOfFiles(source_dir, target_dir, fileList):
  copiedCount=0
  for root, dirs, files in os.walk(source_dir):
        for file in files:
          if file.lower() in fileList:
                copiedCount += 1
                target = root.replace(sourceDir,targetDir)
                if not os.path.exists(target):
                  os.mkdir(target)
                print(file)
                shutil.copy2(root+'\\'+file, target+'\\'+file)
  print('\nCopied '+str(copiedCount)+' file(s)')

def bufcount(self, filename):
    f = open(filename)
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)
    return lines

def addjavacomment(self, comment, line):
    line = line.replace('\n','     '+comment+'\n')
    return line

"""
* fileobject = open(output_filename, 'w', -1, encoding='utf-8')
"""
def teoconsolefilelog(writefileobject, outputstring):
    sys.stdout.write(outputstring)
    writefileobject.write(outputstring)
