#-*- coding: utf-8 -*-
##http://www.saltycrane.com/blog/2007/10/python-finditer-regular-expression/
"""
Python version: 2.7
Purpose: posui:showTextFields
130415: Initial
     Apply previousLineIndent
130416:  label processing: retrieve label value, find key
         add keyfoundFlag
         + implement inplaceFlag=1
"""
import sys, re, os, glob, shutil, fileinput
from datetime import datetime
from xlrd import open_workbook
import teoconstants

root_dir='C:\\130521_Temp\\Temp\\poscoMES_M80\\Pgm_Dev\\2nd_iteration\\'
##root_dir='C:\\jdev904_MULTI\\j2ee\\home\\applications\\M84010APP\\'
##root_dir='C:\\130417_dest\\'
constantFolders=[
                 'public_html',
##                 'M84010WEB',
                 ]

labelDict = {}
showTextFieldsCount = 0
alreadyChanged = 0
showTextFieldsChanged = 0
labelMainList=[]
inplaceFlag = 1
def run(target_dir, inplaceFlag=0):
    global showTextFieldsCount, alreadyChanged, showTextFieldsChanged, labelList
    retrieveFlag = 0 # 1: start retrieve; 2: end retrieve
    showTextFields = ''
    previousLineIndent = ''
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.jsp') and (file.lower() in teoconstants.uipgms):
                print('Processing ' + file)
                if inplaceFlag == 0:   #improve performance
                    f = fileinput.input(root+"\\"+ file, inplace=inplaceFlag, openhook=fileinput.hook_encoded('utf-8'))
                elif inplaceFlag == 1:
                    f = fileinput.input(root+"\\"+ file, inplace=inplaceFlag)

                for i, line in enumerate(f):
                    if(re.search('posui:showTextFields', line, re.IGNORECASE)):
                        showTextFieldsCount += 1
                        retrieveFlag = 1
                        showTextFields += line
                    if retrieveFlag == 1:
                        if (not re.search('/>', line)) and (not re.search('posui:showTextFields', line)):
                            previousLineIndent = (re.search('^(?P<indent>[ \t]*)[a-zA-Z\</\n]?',line,re.IGNORECASE)).group('indent')
                            if re.search('label\=',line):
                                m = re.search('(?P<before>^.*)label="(?P<label>.*)"',line)
                                label = m.group('label')
                                keyfoundFlag = 0
                                labelSubList=[]
                                labelSubList.append(file)
                                labelSubList.append(i+1)
                                labelSubList.append(label)
                                if inplaceFlag == 1:
                                    label = label.decode('utf-8')
                                keyFound = findCorrespondentKey(label)
                                if keyFound != label:
                                    keyfoundFlag = 1
                                    labelSubList.append(1)
                                    labelSubList.append(keyFound)
                                    line = m.group('before')+'label="'+keyFound+'"\n'
                                    if inplaceFlag == 0:
                                        print('FOUNDDDDDDD:'+ keyFound)
                                    elif inplaceFlag == 1:
                                        line = line.encode('utf-8')
                                else:
                                    labelSubList.append(0)
                                labelMainList.append(labelSubList)
                            showTextFields += line
                    if (re.search('/>', line)) and (retrieveFlag == 1):
                        retrieveFlag = 2
                        if re.search('isMultiLang="true"', showTextFields):
                            alreadyChanged += 1
                        else:
                            line = re.sub('^',previousLineIndent+'isMultiLang="true"\n', line)
                            showTextFields += line
                            
                        if inplaceFlag == 0:
                            sys.stdout.write(showTextFields)
                    if retrieveFlag == 2:
                        retrieveFlag = 0
                        showTextFields = ''

                    if inplaceFlag == 1:
                        sys.stdout.write(line)

                f.close()

def findCorrespondentKey(value):
    keyFound = ''
    checkFlag = 0
    originalValue = value
    if value == '': #  keep the last '|' if have --> staticNames="90|180|270|360|" staticValues="M00L12078_0001|M00L12093_0001|M00L12097_0001|M00L12064_0001|"
        return ''
    elif re.search('_000\d$',value): # performance tuning
        return value
    if hasattr(value, 'lower'): # used for case-insensitive comparition
        value = value.lower()
    while not checkFlag == 9:
        for (k,v) in labelDict.items():
            if((value == v) and not k.endswith('0')):
                keyFound = k
                checkFlag = 9
                break
            
        if checkFlag == 0:
            if re.search(' ', value):
                value = value.replace(' ','')
                checkFlag = 1
            elif re.search('<br>', value):
                value = value.replace('<br>','')
                checkFlag = 2
            elif re.search('\&nbsp;',value):
                value = value.replace(r'&nbsp;','')
                checkFlag = 3
            else: checkFlag = 9
        elif checkFlag == 1:
            if re.search('<br>', value):
                value = value.replace('<br>','')
                checkFlag = 2
            elif re.search('\&nbsp;',value):
                value = value.replace(r'&nbsp;','')
                checkFlag = 3
            else: checkFlag = 9
        elif checkFlag == 2:
            if re.search('\&nbsp;',value):
                value = value.replace(r'&nbsp;','')
                checkFlag = 3
            else: checkFlag = 9
        elif checkFlag == 3:
            checkFlag = 9
        elif checkFlag == 9:
            break

    if keyFound != '':
        return keyFound
    else:
        if(originalValue not in keyNotFoundList):
            keyNotFoundList.append(originalValue)
        if inplaceFlag == 0:
            pass

        return originalValue

def addDataToDict():
    rb = open_workbook('Label_KO.xls')
    sheet = rb.sheet_by_name('Sheet1')
    for i in range(1, sheet.nrows):
        row = sheet.row(i)
        if hasattr(row[2].value, 'lower'):
            labelDict[row[1].value] = (row[2].value).lower()    # lower for case-insensitive
        else: labelDict[row[1].value] = row[2].value

#==main==================
print ("Start time: " + str(datetime.now()))
print ("Root Dir = " + root_dir)
print ("inplaceFlag = " + str(inplaceFlag) + "\n")

addDataToDict()
for folder in constantFolders:
    run(root_dir + "\\" + folder, inplaceFlag)
print('\nshowTextFieldsCount = ' + str(showTextFieldsCount))
print('alreadyChanged = ' + str(alreadyChanged))
print('showTextFieldsChanged = ' + str(showTextFieldsChanged)+'\n')

print('labelMainList Details')
for i,subList in enumerate(labelMainList):
    if subList[3] == 0 and not re.search('_000\d$',subList[2]): #Label found but can not find in label list
        print('KEYNOTFOUND '+str(i+1)+'\t'+subList[0]+' at line '+str(subList[1])+'\t'+subList[2])
    elif subList[3] == 1: # can not find appropriate key for label
        print(str(i+1)+'\t'+subList[0]+' at line '+str(subList[1])+'\t'+subList[2] +'\treplacedWith-->'+(subList[4]).encode('utf-8'))

print("\nEnd time: " + str(datetime.now()))

    
