"""
130620: Initial
"""
import os, sys, re
root = r'C:\130521_Temp\Temp\poscoMES_M80\Pgm_Dev\2nd_iteration'
config_path = root + '\config'
publichtml_path = root + '\public_html'
src_path = root + '\src'

class RetrieveEOData(object):
    def run(self):
        retrieveFlag = 0
        accessorattribute_name = ''
        accessorattribute_association = ''
        accessorattribute_associationend = ''
        accessorattribute_associationotherend = ''
        accessorattribute_type = ''
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.endswith('EO.xml'):
                    f = fileinput.input(root+"\\"+ file, inplace=0, openhook=fileinput.hook_encoded('utf-8'))

                    for i, line in enumerate(f):
                        if re.search('\<AccessorAttribute', line):
                            retrieveFlag = 1
                        if retrieveFlag == 1:
                            if re.search('^(\t| )*Name.*=.*".*"',line):
                                accessorattribute_name = re.search('^(\t| )*Name.*=.*"(?P<name>.*)"',line).group('name')
##                                print(viewattribute_name)
                            elif re.search('^(\t| )*Association.*=.*".*"',line):
                                accessorattribute_association = re.search('^(\t| )*Association.*=.*"(?P<association>.*)"',line).group('association')
##                                print(viewattribute_ispersistent)
                            elif re.search('^(\t| )*AssociationEnd.*=.*".*"',line):
                                accessorattribute_associationend = re.search('^(\t| )*AssociationEnd.*=.*"(?P<associationend>.*)"',line).group('associationend')
##                                print(viewattribute_isnotnull)
                            elif re.search('^(\t| )*Precision.*=.*".*"',line):
                                accessorattribute_associationotherend = re.search('^(\t| )*Precision.*=.*"(?P<precision>.*)"',line).group('precision')
##                                print("Precision="+viewattribute_precision)
                            elif re.search('^(\t| )*Type.*=.*".*"',line):
                                accessorattribute_type = re.search('^(\t| )*Type.*=.*"(?P<type>.*)"',line).group('type')
##                                print("Precision="+viewattribute_precision)
                        if re.search('\</AccessorAttribute\>', line):
                            sys.stdout.write(returnstring += commonJobs.printPackageAndFilename(root+"\\"+file,r'com\\posco',r'\.xml'))
                            print('\t'+ viewattribute_name +'\t'+ viewattribute_ispersistent +'\t'+ viewattribute_isnotnull +'\t'+ viewattribute_precision +'\t'+ viewattribute_scale +'\t'+ viewattribute_type +'\t'+ viewattribute_aliasname +'\t'+ viewattribute_columntype +'\t'+ viewattribute_expression +'\t'+ viewattribute_sqltype)
                            retrieveFlag = 0
                            accessorattribute_name = accessorattribute_association = accessorattribute_associationend = accessorattribute_associationotherend = accessorattribute_type = ''
                    f.close()


    def fileprocess(self, fullfilepath):
        if os.access(fullfilepath, os.R_OK):
            with open(fullfilepath,'r',-1,encoding='utf-8') as fp:
                try:
                    lines = fp.readlines()
                    for i,line in enumerate(lines):
                        
                        for function in constants.functionsContainVO:
                            p = re.compile(r'\b{0}'.format(function))
                            m = p.search(line)
                            if m:
                                sys.stdout.write(fullfilepath+':::'+str(i+1)+'\t'+line)
                                break
                except:
                    print(str(sys.exc_info()[0]) + fullfilepath)
                    
temp = RetrieveEOData()
temp.run()
        
