#-*- coding: utf-8 -*-
##http://www.saltycrane.com/blog/2007/10/python-finditer-regular-expression/
"""
Python version: 2.7
Purpose: posui:showMessage
130412: Initial
130621: add
130711: add standardize parameter for addDataToDict(..); and make change on findCorrespondentKey(..) 
"""
import teoconstants

import sys, re, os, glob, shutil, fileinput
from datetime import datetime

##root_dir='C:\\130409_Temp\\Temp\\poscoMES_M80\\Pgm_Dev\\2nd_iteration\\'

##def addDataToDict():
##    rb = open_workbook('Label_KO.xls')
##    sheet = rb.sheet_by_name('Sheet1')
##    for i in range(1, sheet.nrows):
##        row = sheet.row(i)
##        labelDict[row[1].value] = row[2].value
##
##def addDataToDictLoweredValue():
##    rb = open_workbook('Label_KO.xls')
##    sheet = rb.sheet_by_name('Sheet1')
##    for i in range(1, sheet.nrows):
##        row = sheet.row(i)
##        if hasattr(row[2].value, 'lower'):
##            labelDictLower[row[1].value] = (row[2].value).lower()    # lower for case-insensitive
##        else: labelDictLower[row[1].value] = row[2].value

def addDataToDict(filename, lowercaseValue=0, standardize=0):
    """
    lowercaseValue: 0 keep all values in data file intact
                   !0 lowercase all values in data file
    standardize: 0 keep all values in data file intact
                !0 remove spaces, '<br>', '&nbsp;'
     """
    dataDict = {}
    if os.access(filename, os.R_OK):
        with open(filename,'r',-1,encoding='utf-8') as rf:
            lines = rf.readlines()
            for i, line in enumerate(lines):
                m = re.search(r'^(?P<leftValue>.*?)\=(?P<rightValue>.*)',line)
                if m:
##                    if lowercaseValue == 0:
##                        dataDict[m.group('leftValue')] = m.group('rightValue')
##                    else:
##                        dataDict[m.group('leftValue')] = m.group('rightValue').lower()
                    value = m.group('rightValue')
                    if lowercaseValue != 0:
                        value = value.lower()
                    if standardize != 0:
                        if re.search(' ', value):
                            value = value.replace(' ','')
                        if re.search('<br>', value, flags=re.IGNORECASE):
                            value = re.sub('<br>','',value,flags=re.IGNORECASE)
                        if re.search('\&nbsp;', value, flags=re.IGNORECASE):
                            value = re.sub('\&nbsp;','',value,flags=re.IGNORECASE)
                        dataDict[m.group('leftValue')] = m.group('rightValue')
                    dataDict[m.group('leftValue')] = value
    if not dataDict:
        print('Data dictionary is empty. Please check file existence!')
    return dataDict


def findCorrespondentKey(labelDict, value, lowStandardDict=None):
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

    if keyFound == '':  # in case of can not find the not key.endswith('0')
        for (k,v) in labelDict.items():
                if value == v:
                    keyFound = k
                    break
    
    if keyFound == '':  # in case cannot find the key for changed value above; keys could be endswith('0')
        for (k,v) in labelDict.items():
                if originalValue == v:
                    keyFound = k
                    break

    if keyFound == '' and lowStandardDict!=None:  
        for (k,v) in lowStandardDict.items():
                if value == v:
                    keyFound = k
                    break
                    
    if keyFound != '':
        return keyFound
    else:
        return originalValue

##def searchValueExistedInLabelList():
##    addDataToDict()
##    for i, findstring in enumerate(teoconstants.Case00List):
##        keyFound = ''
##        for(k,v) in labelDict.items():
##            if findstring == v.encode('utf-8'):
##                keyFound = k
##                print('     Found-->'+findstring.decode('utf-8')+'==>'+str(k))
##        if keyFound == '':
####            print('NOTFOUND for '+findstring.decode('utf-8'))
##            labelDictLower = addDataToDictLoweredValueFromPropertiesFile()
##            findstring = findstring.decode('utf-8')
##            keyFound = findCorrespondentKey(findstring)
##            if keyFound != findstring:
##                print('          Found2 '+findstring+' ---> '+ keyFound)
##            else: print('NOTFOUND for '+findstring)
            
def stringProcessing(string, delimiter):
    addDataToDict()
    if delimiter == '|':
        valueList = re.split('\|', string)
    else: valueList = re.split(delimiter, string)
    newString = ''
    for i, value in enumerate(valueList):
        keyFound = ''
        for(k,v) in labelDict.items():
            if value == v.encode('utf-8') and k.endswith('1'):
                keyFound = k
                break
        if keyFound:
            newString += keyFound + delimiter
        else:
            newString += value.decode('utf-8') + delimiter
    newString = newString.rstrip('|')
            
    print(string.decode('utf-8') +'==>'+newString)
    return newString

def stringListProcessing(stringList):
    for i, string in enumerate(stringList):
        stringProcessingWithStandards(string,'|')

def searchValueExistedInLabelListWithStandards():
    keyNotFoundSet = set()
    labelDictLower = addDataToDict('label_ko.properties',1)
    labelLoweredStandardedDict = addDataToDict('label_ko.properties',1,1)
    for findstring in teoconstants.Case00List:
##        findstring = findstring.decode('utf-8')
        keyFound = findCorrespondentKey(labelDictLower, findstring, labelLoweredStandardedDict)

        if keyFound != findstring:
            if not re.search('<br>', findstring):
                keyFound=re.sub('_000\d','_0000',keyFound)
##            print(findstring+' ---> '+ '<posui:showLabel key="'+keyFound+'" />')
##            print(findstring+' ---> '+'PosGlobalHandler.getLabel("'+keyFound+'")')
            print(keyFound + ' <--' + findstring)
        else:
            print(findstring)
            keyNotFoundSet.add(findstring)
        
##        if keyFound != findstring:
##            toolTip = re.sub('_000\d','_0000',keyFound)
##            print(findstring+' ---> '+ 'onmouseover="tooltipOn(\'<posui:showLabel key="'+toolTip+'" />\');" onmouseout="tooltipOff();"><posui:showLabel key="'+keyFound+'" />')
##        else:
##            print(findstring)
##            keyNotFoundSet.add(findstring)
            
    return keyNotFoundSet

def stringProcessingWithStandards(string, delimiter):
    labelDictLower = addDataToDict('label_ko.properties',1)
    if delimiter == '|':
        valueList = re.split('\|', string)
    else: valueList = re.split(delimiter, string)
    newString = ''
    for i, value in enumerate(valueList):
##        value = value.decode('utf-8')
        keyFound = findCorrespondentKey(labelDictLower, value)
        if keyFound != value:
            print(value+' ---> '+ keyFound)
            newString += keyFound + delimiter
        else:
            print('NOTFOUND for '+value)
            newString += value + delimiter
    newString = newString.rstrip('|')
            
    print(string+'==>'+newString)
    newString=re.sub('_000\d','_0000',newString)
    print('00_String==>'+newString)
    print('\n')
    return newString

#==main==================
def main():
	print ("Start time: " + str(datetime.now()))

	if teoconstants.Case00List:
		print('searchValueExistedInLabelListWithStandards()\n')
		x = searchValueExistedInLabelListWithStandards()
	
##	if teoconstants.Case00StringList:
##	    print('stringListProcessing()')
##	    stringListProcessing(teoconstants.Case00StringList)
##	    
	##if keyNotFoundList:
	##    print(keyNotFoundList)
##	if x:
##		print(x)

	print("\nEnd time: " + str(datetime.now()))

##main()
