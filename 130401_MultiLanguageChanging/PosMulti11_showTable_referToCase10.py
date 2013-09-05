# -*- coding: cp949 -*-
##http://www.saltycrane.com/blog/2007/10/python-finditer-regular-expression/
"""
Python version: 2.7
Purpose: posui:showHeaderTable
130417: Initial; retrieve showHeaderTable tag with inplaceFlag = 0
		 implement isMultiLang, toolTipLocales...
130418:
130420:  add headerModifying(..) function; keyNotFoundList
         add headerListProcessing(..) function
130422: + comment ##                                   +indent+'isNoToolTipsScript="true"\n' \
        + add toolTips
--NOTE-----
Abnormal Entry: * 1. headers = "　;전체합계;입고;인출;이적;출고;기타(위치수정)"
                * 2. <posui:showHeaderTable headers = "단|FROM BED|이전위치|선택"-->tag and headers on the same line
                    ==> MANUALLY break this into 2 lines, in order to process code
"""
import sys, re, os, glob, shutil, fileinput
from datetime import datetime
from xlrd import open_workbook
import teoconstants

##root_dir='C:\\130409_Temp\\Temp\\poscoMES_M80\\Pgm_Dev\\2nd_iteration\\'
root_dir='C:\\130417_dest\\'
constantFolders=[
                 'public_html',
                 ]

labelDict = {}
keyNotFoundList = []
showHeaderTableCount = 0
alreadyChanged = 0
showHeaderTableChanged = 0
inplaceFlag = 0
def run(target_dir, inplaceFlag=0):
    global showHeaderTableCount, alreadyChanged, showHeaderTableChanged
    retrieveFlag = 0 # 1: start retrieve; 2: end retrieve
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            showHeaderTable = ''
            oldHeader=''
            if file.endswith('.jsp') and (file.lower() in teoconstants.uipgms):
                print('Processing '+file)
                if inplaceFlag == 0:   #improve performance
                    f = fileinput.input(root+"\\"+ file, inplace=inplaceFlag, openhook=fileinput.hook_encoded('utf-8'))
                elif inplaceFlag == 1:
                    f = fileinput.input(root+"\\"+ file, inplace=inplaceFlag)

                for i, line in enumerate(f):
                    if(re.search('posui:showTable', line, re.IGNORECASE)):
                        showHeaderTableCount += 1
                        retrieveFlag = 1
                        showHeaderTable += line
                    if retrieveFlag == 1:
                        if(not re.search('posui:showTable', line))and(not re.search('/>', line)):
                            showHeaderTable += line
                            indent = (re.search('^(?P<indent>[ \t]*)[a-zA-Z\</\n]?',line,re.IGNORECASE)).group('indent')
                        if(re.search('headers.*\=.*"\<%\=',showHeaderTable)):   # E.g: headers = "<%=headerTit%>"
                           if inplaceFlag == 0:
                               print('  Unappropriate header found at line '+str(i+1))
                           retrieveFlag = 2
                           continue
                        elif(re.search('headers.*\=',line)and(line.count('"')==2)):
                            headIndent = indent
                            oldHeader=(re.search('.*\"(?P<header>.*)\"',line)).group('header')
                            if(inplaceFlag == 0):
                                print('oldHeader case 1='+oldHeader)
                            line = appendToolTipsToNewHeader(oldHeader, headIndent)
                            if inplaceFlag == 1:
                                line = line.encode('utf-8')
                            oldHeader=''
                        elif(re.search('headers.*\=',line)and(line.count('"')==1)):
                            headIndent = indent
                            oldHeader=(re.search('.*\"(?P<header>.*)',line)).group('header')
                            continue
                        elif((oldHeader != '') and (line.count('"')==0)):
                            oldHeader += (re.search('^[ \t]*(?P<header>.*)',line)).group('header')
                            continue
                        elif((oldHeader != '') and (line.count('"')==1)):
                            oldHeader += (re.search('^[ \t]*(?P<header>.*)\"',line)).group('header')
                            oldHeader = oldHeader.replace('\r','')
                            oldHeader = re.sub(';$','',oldHeader)
                            if(inplaceFlag == 0):
                                print('oldHeader case 2='+oldHeader)
                            line = appendToolTipsToNewHeader(oldHeader, headIndent)
                            if inplaceFlag == 1:
                                line = line.encode('utf-8')
                            oldHeader=''
                            
                        
                        if (re.search('/>', line)):
                            retrieveFlag = 2
                            if (not re.search('isMultiLang', showHeaderTable)):
                                line = indent+'isMultiLang="true"\n' \
                                       +indent+'tableEvent="nowrap style=\'table-layout:fixed\'"\n' \
                                       +indent+'toolTipLocales="en"\n' \
                                       +indent+'isColspanFix="true"\n' \
                                       +line
                            else:   print('fffffffffffffffffffffffff')
                            showHeaderTable += line
                            if inplaceFlag == 0:
                                sys.stdout.write(showHeaderTable)
                    if retrieveFlag == 2:
                        showHeaderTable = ''
                        retrieveFlag = 0
                                       
                        
                    if inplaceFlag == 1:
                        sys.stdout.write(line)

                f.close()
def headerModifying(string):
    newString = ''
    for i, value in enumerate(re.split('\|',string)):
        keyFound = ''
        checkFlag = 0
        if inplaceFlag == 1:
            value = value.decode('utf-8')
        while checkFlag == 0 or checkFlag == 1:
            for (k,v) in labelDict.items():
                if((value == v) and k.endswith('1')):
##                    print('FOUNDFOUNDFOUND ' + k)
                    if checkFlag == 1:
##                        print('FOUNDFOUNDFOUND ' + k)
                        pass
                    keyFound = k
                    checkFlag = 9
                    break
                
            if checkFlag == 0:
                value = value.replace(' ','')
                checkFlag = 1;
            elif checkFlag == 1:
                checkFlag = 9;
            elif checkFlag == 9:
                break
        

        if keyFound != '':
            newString += keyFound + '|'
        else:
            newString += value + '|'
            if(value not in keyNotFoundList):
                keyNotFoundList.append(value)
            if inplaceFlag == 0:
##                print('Cannot find key for value ==>'+value)
                pass
    newString = re.sub('\|$','',newString)
    return newString

def headerListProcessing(stringContainsSemicolon, headerIndent=''):
    headerList = re.split(';',stringContainsSemicolon)
    newHeadersString=''
##    print(headerList)

    for i, value in enumerate(headerList):
        if i == 0:  # first element on list
            if len(headerList) == 1:
                newHeadersString += headerIndent+'headers="'+headerModifying(value)+'"\n'
            elif len(headerList) > 1:
                newHeadersString += headerIndent+'headers="'+headerModifying(value)+';\n'
                headerIndent += ' '*len('headers="')
        elif (i+1) == len(headerList):   # last element on list
            newHeadersString += headerIndent+headerModifying(value)+'"\n'
        else:
            newHeadersString += headerIndent+headerModifying(value)+';\n'
    if inplaceFlag == 0:
        print('newHeadersString = \r'+newHeadersString)
    return newHeadersString

def appendToolTipsToNewHeader(string, headerIndent=''):
    headerString = headerListProcessing(string, headerIndent)
    toolTipsString = re.sub('headers','toolTips',headerString)
    toolTipsString = re.sub('_0001','_0000',toolTipsString)
    headerString = headerString + toolTipsString     # combinedString
    if inplaceFlag == 0:
        print('new CombinedString\n'+headerString)
    return headerString
    
    
    
        

def addDataToDict():
    rb = open_workbook('Label_KO.xls')
    sheet = rb.sheet_by_name('Sheet1')
    for i in range(1, sheet.nrows):
        row = sheet.row(i)
        labelDict[row[1].value] = row[2].value

#==main==================
print ("Start time: " + str(datetime.now()))
print ("Root Dir = " + root_dir)
print ("inplaceFlag = " + str(inplaceFlag) + "\n")


addDataToDict()
for folder in constantFolders:
    run(root_dir + "\\" + folder, inplaceFlag)
print('\nshowHeaderTableCount = ' + str(showHeaderTableCount))
print('alreadyChanged = ' + str(alreadyChanged))
print('showHeaderTableChanged = ' + str(showHeaderTableChanged))

if keyNotFoundList:
    print('keyNotFoundList contains:')
    for i, key in enumerate(keyNotFoundList):
        print(' '+str(i+1)+'\t'+key)

print("\nEnd time: " + str(datetime.now()))

    
