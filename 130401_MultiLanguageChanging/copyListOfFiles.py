
import os, shutil
import teoconstants

##sourceDir='C:\\130415_src'
sourceDir='C:\\130409_Temp\\Temp\\poscoMES_M80\\Pgm_Dev\\2nd_iteration\\public_html'
targetDir='C:\\130417_dest\\public_html'

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
        print(target)
        if not os.path.exists(target):
          os.mkdir(target)
        print(file)
        shutil.copy2(root+'\\'+file, target+'\\'+file)
  print('\nCopied '+str(copiedCount)+' file(s)')


copyListOfFiles(sourceDir, targetDir, teoconstants.uipgms)
