"""
Purpose: Parse all VOs, extract all data relating to VO
130606: Initialize
130611: add printVOAndPackage
(p1, p2)
130620： remove printVOAndPackage
	add view attribute_scale
"""
from Job00_commonJobs import commonJobs

import bs4

import traceback
from datetime import datetime
import os, fileinput, sys,re

target=r'C:\130805_DEV\DEV\src\com\posco\mes'

class RetrieveDataForTbM00ViewObject(object):
    def main(self, target_dir):
        result = ''
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.endswith('VO.xml'):
##                    result += self.retrieveAttributeTag(root+"\\"+ file)
                    self.retrieveVOContent(root+"\\"+ file)
                    pass
        wf = open('Job01_RetrieveDataForTbM00ViewObject_00_output.txt','w', -1, encoding='utf-8')
        wf.write(result)
        wf.close()

    def retrieveVOContent(self, fullfilepath):
        with open(fullfilepath,'r',-1, encoding='utf-8') as rf:
            try:
                lines = rf.readlines()
            except:
                print(str(sys.exc_info()[0]) + fullfilepath)
        pass
    def retrieveAttributeTag(self, arg1, arg2=None):
        """
        Input 1 : retrieveAttributeTag(fullfilepath)
        Input 2 : retrieveAttributeTag(root, filename)
        """
        if arg2 == None:
            fullfilepath = arg1
            m = re.search(r'^(.*)\\(.*)', arg1)
            root = m.group(1)
            file = m.group(2)
        else:
            fullfilepath = arg1+"\\"+ arg2
        returnstring = ''
        retrieveFlag = 0
        viewattribute_name = ''
        viewattribute_ispersistent = ''
        viewattribute_isnotnull = ''
        viewattribute_precision = ''
        viewattribute_scale = ''
        viewattribute_type = ''
        viewattribute_aliasname = ''
        viewattribute_columntype = ''
        viewattribute_expression = ''
        viewattribute_sqltype = ''
        if os.access(fullfilepath, os.R_OK):
            with open(fullfilepath,'r',-1, encoding='utf-8') as rf:
                try:
                    lines = rf.readlines()
                    for line in lines:
                        if re.search('\<ViewAttribute', line):
                            retrieveFlag = 1
                        if retrieveFlag == 1:
                            if re.search('^(\t| )*Name.*=.*".*"',line):
                                viewattribute_name = re.search('^(\t| )*Name.*=.*"(?P<name>.*)"',line).group('name')
##                                print(viewattribute_name)
                            elif re.search('^(\t| )*IsPersistent.*=.*".*"',line):
                                viewattribute_ispersistent = re.search('^(\t| )*IsPersistent.*=.*"(?P<ispersistent>.*)"',line).group('ispersistent')
##                                print(viewattribute_ispersistent)
                            elif re.search('^(\t| )*IsNotNull.*=.*".*"',line):
                                viewattribute_isnotnull = re.search('^(\t| )*IsNotNull.*=.*"(?P<isnotnull>.*)"',line).group('isnotnull')
##                                print(viewattribute_isnotnull)
                            elif re.search('^(\t| )*Precision.*=.*".*"',line):
                                viewattribute_precision = re.search('^(\t| )*Precision.*=.*"(?P<precision>.*)"',line).group('precision')
##                                print("Precision="+viewattribute_precision)
                            elif re.search('^(\t| )*Scale.*=.*".*"',line):
                                viewattribute_scale = re.search('^(\t| )*Scale.*=.*"(?P<scale>.*)"',line).group('scale')
##                                print("Scale="+viewattribute_scale)
                            elif re.search('^(\t| )*Type.*=.*".*"',line):
                                viewattribute_type = re.search('^(\t| )*Type.*=.*"(?P<type>.*)"',line).group('type')
##                                print(viewattribute_type)
                            elif re.search('^(\t| )*AliasName.*=.*".*"',line):
                                viewattribute_aliasname = re.search('^(\t| )*AliasName.*=.*"(?P<aliasname>.*)"',line).group('aliasname')
##                                print(viewattribute_aliasname)
                            elif re.search('^(\t| )*ColumnType.*=.*".*"',line):
                                viewattribute_columntype = re.search('^(\t| )*ColumnType.*=.*"(?P<columntype>.*)"',line).group('columntype')
##                                print(viewattribute_columntype)
                            elif re.search('^(\t| )*Expression.*=.*".*"',line):
                                viewattribute_expression = re.search('^(\t| )*Expression.*=.*"(?P<expression>.*)"',line).group('expression')
##                                print(viewattribute_expression)
                            elif re.search('^(\t| )*SQLType.*=.*".*"',line):
                                viewattribute_sqltype = re.search('^(\t| )*SQLType.*=.*"(?P<sqltype>.*)"',line).group('sqltype')
##                                print(viewattribute_sqltype)
                        if re.search('\</ViewAttribute\>', line):
                            returnstring += commonJobs.printPackageAndFilename(root+"\\"+file,r'com\\posco',r'\.xml')
                            returnstring += '\t'+ viewattribute_name +'\t'+ viewattribute_ispersistent +'\t'+ viewattribute_isnotnull +'\t'+ viewattribute_precision +'\t'+ viewattribute_scale +'\t'+ viewattribute_type +'\t'+ viewattribute_aliasname +'\t'+ viewattribute_columntype +'\t'+ viewattribute_expression +'\t'+ viewattribute_sqltype + '\n'

                            retrieveFlag = 0
                            viewattribute_name = viewattribute_ispersistent = viewattribute_isnotnull = viewattribute_precision = viewattribute_scale = viewattribute_type = viewattribute_aliasname = viewattribute_columntype = viewattribute_expression = viewattribute_sqltype = ''
                    return returnstring
                except:
                    print(str(sys.exc_info()[0]) + fullfilepath)
##                    print(traceback.format_exc())

def run():
    startTime = datetime.now()
    print ("Start time: " + str(startTime))

    rev = RetrieveDataForTbM00ViewObject()
    rev.main(target)

    endTime = datetime.now()
    print("\nEnd time: " + str(endTime))
    print("Processing Time = " + str(endTime - startTime))

run()
