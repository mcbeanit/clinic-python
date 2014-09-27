
# access to echart database objects for conversion and support

import pyodbc

mdb = 'j:\datafile\medtech97.mdb'
eChartConn = r"Driver={Microsoft Access Driver (*.mdb)};Dbq=%s" % mdb   #dev


def getechartconnection():
    return pyodbc.connect(eChartConn)

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 31 < ord(c) < 127)
    return ''.join(stripped)

def getConnection():
    pass

def nonetostr(s):
    if s is None:
        return ''
    else:
        return s

def getdocumentSql(id):
    return 'SELECT document_number, date_of_document, date_of_index, dat_index_number, mt_doctor_number, \
                   category \
    FROM document_description WHERE dat_index_number = %d' % id

def getpatientlist():
    return 'SELECT dat_index_number FROM patient_demographics'

	
def getShortCutCodes():
	return 'SELECT ShortcutCode,ReplacementText FROM LU_SHORTCUTCODES'

def getDocumentAudit(startAt):
    return 'SELECT document_number,createdby,creationdate,modifiedby,modifieddate FROM DOCUMENT_DESCRIPTION where document_number > %d' % startAt



