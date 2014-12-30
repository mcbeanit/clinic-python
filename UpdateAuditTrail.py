# final update of the AuditTrail table from the temp table EChartAuditTrail
# rmcbean - Oct 10, 2014
#

import pyodbc

#read cursor
#clinicConn = 'DRIVER={SQL Server};SERVER=BEHMSRV1\BKUPEXEC;DATABASE=mcbean_clinic;Trusted_Connection=yes'
clinicConn = 'DRIVER={SQL Server};SERVER=WELCOMETOSHIBA\SQLEXPRESS;DATABASE=mcbean_clinic;Trusted_Connection=yes'
clinicConnection = pyodbc.connect(clinicConn)
clinicCursor = clinicConnection.cursor()
delSql = 'DELETE FROM AuditTrail WHERE DataId = %d AND AuditTrailCategoryId in (1,2)'
insSql = "INSERT INTO AuditTrail (AuditTrailCategoryId, UserAccountId, EventDateTime, DataId) VALUES (%d,%d,'%s',%d)"

#delete update cursor

clinicConnectionUpdate = pyodbc.connect(clinicConn)
clinicUpdateCursor = clinicConnectionUpdate.cursor()

clinicCursor.execute("SELECT ModifiedDate, CreatedBy, CreatedDate, Document_Number, ModifiedById, CreatedById, DocumentId FROM EChartAuditTrail")
rows = clinicCursor.fetchall()

for row in rows:
    documentId = int(row.DocumentId)
    sql = delSql % documentId
    clinicUpdateCursor.execute(sql)

    # two inserts, one for creation event, one for modified event. echart only recorded two events, the modified
    # field was the last modification.

    sql = insSql % (1, int(row.CreatedById), row.CreatedDate, int(row.DocumentId))
    clinicUpdateCursor.execute(sql)
    sql = insSql % (2, int(row.ModifiedById), row.ModifiedDate, int(row.DocumentId))
    clinicUpdateCursor.execute(sql)
    

#done commit and close
clinicUpdateCursor.commit()
clinicUpdateCursor.close()
clinicCursor.close()
clinicConnection.close()
clinicConnectionUpdate.close()
