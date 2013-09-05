#-*- coding: utf-8 -*-
##http://www.saltycrane.com/blog/2007/10/python-finditer-regular-expression/
"""
Python version: 2.7
Purpose: posui:showSelectList
130506: apply (not k.endswith('0'))
        ignore blank line inside 
        apply suffix 'MultiLang'
Note: If can find staticValue but can not find appropriate key for that value, prefix isMultiLang still set to "true"
        apply inplaceFag 1 (i.e can write to file)
     create function findCorrespondentKey()
130507: if can not find key, remove 'space', <br> or '&nbsp;'  --> find again ; checkFlag 2 3
        case-insensitive for searching value
130513: + label key， staticValues keys be in _0000 in order to show orginal value
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
keyNotFoundList = []
showSelectListCount = 0
alreadyChanged = 0
showSelectListChanged = 0
labelMainList=[]
inplaceFlag = 1
def run(target_dir, inplaceFlag=0):
    global showSelectListCount, alreadyChanged, showSelectListChanged, labelList
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

                label = ''
                staticValues = ''
                totalValue = ''
                for i, line in enumerate(f):
                    if(re.search('posui:showSelectList', line, re.IGNORECASE)):
                        showSelectListCount += 1
                        retrieveFlag = 1
                        showTextFields += line
                    if retrieveFlag == 1:
                        if line in ('\n', '\r\n'):  # ignore blank line
                            continue
                        if (not re.search('/>', line)) and (not re.search('posui:showSelectList', line)):
                            previousLineIndent = (re.search('^(?P<indent>[ \t]*)[a-zA-Z\</\n]?',line,re.IGNORECASE)).group('indent')
                            if re.search('label.*\=',line):   ##1111111111111111111111111111111
                                if(re.search("\<.*\>",line)):
                                    if inplaceFlag == 1:
                                        sys.stdout.write(line)
                                        continue
                                else:
                                    m = re.search('(?P<before>^.*)label.*=.*"(?P<label>.*)"',line)
                                    label = m.group('label')
                                    keyfoundFlag = 0
                                    keyFound = ''
                                    subList=[]
                                    subList.append(file)
                                    subList.append(i+1)
                                    subList.append(label)
                                    if inplaceFlag == 1:
                                        label = label.decode('utf-8')
                                    keyFound = findCorrespondentKey(label)
                                    if keyFound != label:
                                        keyfoundFlag = 1
                                        subList.append(1)
                                        keyFound = re.sub('_000\d','_0000',keyFound)
                                        line = m.group('before')+'label="'+keyFound+'"\n'
##                                        if inplaceFlag == 0:
##                                            print('FOUNDDDDDDD:'+ keyFound)
                                        if inplaceFlag == 1:
                                            line = line.encode('utf-8')
                                    else:
                                        subList.append(0)
                                    labelMainList.append(subList)
                            
                            elif(re.search('staticValues.*\=', line)):  ##222222222222222222222222222
                                if inplaceFlag == 0:
##                                    print('staticValues FOUND ==>'+line)
                                    pass
                                if(re.search("\<.*\>",line)):    ## E.g: totalValue="<%=PosM800500099ConstantsIF.C_LOV_ALL_VALUE%>"
                                    if inplaceFlag == 1:
                                        sys.stdout.write(line)
                                        continue
                                else:
                                    m = re.search('(?P<before>^.*)staticValues.*=.*"(?P<staticValues>.*)"',line)
                                    staticValues = m.group('staticValues')
                                    staticValues = re.sub('|$','',staticValues)
                                    newString = ''
                                    for value in re.split('\|',staticValues):
                                        subList=[]
                                        subList.append(file)
                                        subList.append(i+1)
                                        subList.append(value)
                                        if inplaceFlag == 1:
                                            value = value.decode('utf-8')
                                        keyFound = findCorrespondentKey(value)
                                        if keyFound != value:
                                            subList.append(1)
                                            keyFound = re.sub('_000\d','_0000',keyFound)
                                            newString += keyFound + '|'
                                            if inplaceFlag == 0:
                                                print('FOUNDDDDDDD:'+ keyFound)
                                        else:
                                            subList.append(0)
                                            newString += value + '|'
                                            if inplaceFlag == 0:
                                                print('CAN NOT FIND APPROPRIATE KEY for staticValues')
                                        labelMainList.append(subList)
                                    newString = re.sub('\|$','',newString)
                                    line = m.group('before')+'staticValues="'+newString+'"\n'
                                    if inplaceFlag == 1:
                                        line = line.encode('utf-8')
                            elif(re.search('totalValue.*\=', line)):    ##3333333333333333333333
##                                if inplaceFlag == 0:
##                                    print('totalValue FOUND ==>'+line)
                                if(re.search("\<.*\>",line) or re.search('"-+"',line)):    ## E.g: totalValue="<%=PosM800500099ConstantsIF.C_LOV_ALL_VALUE%>"   ; totalValue="------------"
                                    if inplaceFlag == 1:
                                        sys.stdout.write(line)
                                        continue
                                else:
                                    m = re.search('(?P<before>^.*)totalValue.*=.*"(?P<totalValue>.*)"',line)
                                    totalValue = m.group('totalValue')
                                    keyfoundFlag = 0
                                    subList=[]
                                    subList.append(file)
                                    subList.append(i+1)
                                    subList.append(totalValue)
                                    if inplaceFlag == 1:
                                        totalValue = totalValue.decode('utf-8')
                                    keyFound = findCorrespondentKey(totalValue)
                                    if keyFound != totalValue:
                                        keyfoundFlag = 1
                                        subList.append(1)
                                        line = m.group('before')+'totalValue="'+keyFound+'"\n'
                                        if inplaceFlag == 0:
                                            print('FOUNDDDDDDD:'+ keyFound)
                                        elif inplaceFlag == 1:
                                            line = line.encode('utf-8')
                                    else:
                                        subList.append(0)
                                    labelMainList.append(subList)
                                
                            showTextFields += line
                    if (re.search('/>', line)) and (retrieveFlag == 1):
                        retrieveFlag = 2
                        if re.search('isMultiLang', showTextFields) \
                           or re.search('isLabelMultiLang', showTextFields) \
                           or re.search('isTotalValueMultiLang', showTextFields) :
                            alreadyChanged += 1
                        if staticValues and not re.search('isMultiLang', showTextFields):
                            line = re.sub('^',previousLineIndent+'isMultiLang="true"\n', line)
                        else:
                            if label and totalValue=='' and not re.search('isLabelMultiLang', showTextFields):    # only label
                                line = re.sub('^',previousLineIndent+'isLabelMultiLang="true"\n', line)
                            elif totalValue and label=='' and not re.search('isTotalValueMultiLang', showTextFields):    # only totalValue
                                line = re.sub('^',previousLineIndent+'isTotalValueMultiLang="true"\n', line)
                            elif totalValue and label and not re.search('isLabelMultiLang', showTextFields) and not re.search('isTotalValueMultiLang', showTextFields):
                                line = re.sub('^',previousLineIndent+'isLabelMultiLang="true"\n', line)
                                line = re.sub('^',previousLineIndent+'isTotalValueMultiLang="true"\n', line)
                                    
                        showTextFields += line
                        if inplaceFlag == 0:
                            sys.stdout.write(showTextFields)
                    if retrieveFlag == 2:
                        retrieveFlag = 0
                        keyFound = ''
                        showTextFields = ''
                        label = ''
                        staticValues = ''
                        totalValue = ''

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
        elif checkFlag == 3:           checkFlag = 9
        elif checkFlag == 9:
            break

    if keyFound == '':  # in case of can not find the not key.endswith('0')
        for (k,v) in labelDict.items():
                if value == v:
                    keyFound = k

    if keyFound != '':
        return keyFound
    else:
        if(originalValue not in keyNotFoundList):
            keyNotFoundList.append(originalValue)
        if inplaceFlag == 0:
            pass

        return originalValue

def addDataToDictLoweredValue():
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

addDataToDictLoweredValue()
for folder in constantFolders:
    run(root_dir + "\\" + folder, inplaceFlag)
print('\nshowTextFieldsCount = ' + str(showSelectListCount))
print('alreadyChanged = ' + str(alreadyChanged))
print('showSelectListChanged = ' + str(showSelectListChanged)+'\n')

print('labelMainList Details')
for i,subList in enumerate(labelMainList):
    if subList[3] == 0: #Label found but can not find in label list
        print('KEYNOTFOUND '+str(i+1)+'\t'+subList[0]+' at line '+str(subList[1])+'\t@-@>'+subList[2])
    elif subList[3] == 1:
##        print(str(i+1)+'\t'+subList[0]+' at line '+str(subList[1])+'\t'+subList[2])
        pass
    
if keyNotFoundList:
    print('keyNotFoundList contains:')
    for i, key in enumerate(keyNotFoundList):
        print(' '+str(i+1)+'\t'+key)

print("\nEnd time: " + str(datetime.now()))

