# Convert and validate document location rows converted from EChart to EC2

import pyodbc

# clinicConn = 'DRIVER={SQL Server};SERVER=BEHMSRV1\BKUPEXEC;DATABASE=mcbean.clinic;Trusted_Connection=yes'

clinicConn = 'DRIVER={SQL Server};SERVER=WELCOMETOSHIBA\SQLEXPRESS;DATABASE=mcbean_clinic;Trusted_Connection=yes'
clinicConnection = pyodbc.connect(clinicConn)
clinicCursor = clinicConnection.cursor()
clinicCursorWrite = clinicConnection.cursor()

clinicCursor.execute('SELECT distinct documentlocationrootId, document_location, documentId FROM echartdocumentlocation')

loc = clinicCursor.fetchall()

for doc in loc:

    sql = "INSERT INTO DocumentLocation(DocumentLocationRootId, [Path], DocumentId) VALUES (%d,'%s',%d)" 
    sql = sql % (doc[0],doc[1],doc[2])
    clinicCursorWrite.execute(sql)
    

clinicCursorWrite.commit()
clinicCursorWrite.close()
clinicCursor.close()