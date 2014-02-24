"""

140217: Initial
"""
import teoconstants

import cx_Oracle

import sys
from datetime import datetime

outputfilename = 'SoRe042_RetrieveVOFromMetadata_output.txt'

class RetrieveVOFromMetadata(object):
    def main(self):
        self.wf = open(outputfilename,'w', -1, encoding='utf-8')
        connectstring = teoconstants.masterdbconnectionstring
        
        voquerystring = teoconstants.sore04_retrieveV0fromMVCmeta
        bindlist = teoconstants.uipgms
        resultstring = self.executeQuery(connectstring, voquerystring, bindlist, 'mvc\t')
        sys.stdout.write(resultstring)
        self.wf.write(resultstring)
        
        voquerystring = teoconstants.sore04_retrieveV0fromMSGmeta
        bindlist = teoconstants.tclist
        resultstring = self.executeQuery(connectstring, voquerystring, bindlist, 'msg\t')
        sys.stdout.write(resultstring)
        self.wf.write(resultstring)

    def executeQuery(self, dbconnectionstring, querystring, bindinglist, rowoutputprefix):
        sqlbindingstring = ''
        query = querystring
        for item in bindinglist:
            sqlbindingstring += "'" +item+"',"
        sqlbindingstring = sqlbindingstring.rstrip(",")
        if query.find(':sqlbindingstring'):
           query = query.replace(':sqlbindingstring', sqlbindingstring)

        connstr = dbconnectionstring
        conn = cx_Oracle.connect(connstr)
        resultSet = conn.cursor()
        resultSet.execute(query)
##        for i in resultSet.description:
##            print(i)
        resultList = resultSet.fetchall()
        
        outputstring = ''
        for i, row in enumerate(resultList):
            outputstring += rowoutputprefix+row[0]+'\t'+row[1]+'\n' ##
        return outputstring
        
        

def run():
    startTime = datetime.now()
    print ("Start time: " + str(startTime))

    temp = RetrieveVOFromMetadata()
    temp.main()
    ##temp.fileprocess(r'C:\130617_Temp\Temp\poscoMES_M80\Pgm_Dev\2nd_iteration\src\com\posco\mes\m80\p050\app\process\GetYdOpIndiPrgStatTp.java')

    endTime = datetime.now()
    print("\nEnd time: " + str(endTime))
    print("Processing Time = " + str(endTime - startTime))
run()        
