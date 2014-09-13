# copy document_description to new clinic database

import pyodbc
import echart

connectionEChart = echart.getechartconnection()     #pyodbc.connect(eChartConn)
cursorEChart = connectionEChart.cursor()

clinicConn = 'DRIVER={SQL Server};SERVER=WELCOMETOSHIBA\SQLEXPRESS;DATABASE=mcbean_clinic;Trusted_Connection=yes'
clinicConnection = pyodbc.connect(clinicConn)
clinicCursor = clinicConnection.cursor()

cursorEChart.execute(echart.getpatientlist())
patients = cursorEChart.fetchall();

print 'starting conversion'

for patient in patients:
    id = patient[0]
    print 'importing docs for patient: %d' % id
    query = echart.getdocumentSql(id)
    clinicCursor.execute(query)
    docs = clinicCursor.fetchall()
    print len(docs)


print 'conversion complete'
clinicCursor.commit()
connectionEChart.close()
clinicCursor.close()
clinicConnection.close()