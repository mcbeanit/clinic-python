import pyodbc
import echart

# 26-sept-2014  run on behmsrv1  >>> 305808 records were inserted

connectionEChart = echart.getechartconnection()     #pyodbc.connect(eChartConn)
cursorEChart = connectionEChart.cursor()

#clinicConn = 'DRIVER={SQL Server};SERVER=BEHMSRV1\BKUPEXEC;DATABASE=mcbean_clinic;Trusted_Connection=yes'
clinicConn = 'DRIVER={SQL Server};SERVER=WELCOMETOSHIBA\SQLEXPRESS;DATABASE=mcbean_clinic;Trusted_Connection=yes'
clinicConnection = pyodbc.connect(clinicConn)
clinicCursor = clinicConnection.cursor()
echartUsersCursor = connectionEChart.cursor()

# - order: document_number,createdby,creationdate,modifiedby,modifieddate

sql = "INSERT INTO EChartAuditTrail (Document_number, CreatedBy, CreatedDate, ModifiedBy, ModifiedDate) VALUES (%d,'%s-echart','%s','%s-echart','%s')"

cursorEChart.execute(echart.getDocumentAudit(0))
docs = cursorEChart.fetchall();
count = 0

for audit in docs:

    count = count + 1
    createdDate =  audit[2].strftime('%Y-%m-%d %H:%M')
    modifiedDate = audit[4].strftime('%Y-%m-%d %H:%M')
    cmd = sql % (audit[0],audit[1],createdDate,audit[3],modifiedDate)
    clinicCursor.execute(cmd)

clinicCursor.commit() 
print '%d records were inserted' % count

# bulk update to set the new document number from the echart document number
print 'updatating document number'
updateDocNumber = 'UPDATE t1 SET t1.DocumentId = t2.DocumentId FROM EChartAuditTrail t1 INNER JOIN Document t2 on t1.Document_Number = t2.LegacyDocumentId'
clinicCursor.execute(updateDocNumber)
clinicCursor.commit()
clinicCursor.close()

# update the new user table with active echart users

sql = 'SELECT DISTINCT modifiedBy FROM EChartAuditTrail'
clinicCursor = clinicConnection.cursor()
clinicCursor.execute (sql)
users = clinicCursor.fetchall()

for user in users:
    sql = "insert into UserAccount (LoginName,DisplayName,IsActive) \
        select '%s-echart', '%s-echart',0 \
        where not exists \
            (select loginName from useraccount where LoginName = '%s-echart')"
    s = sql % (user[0],user[0],user[0])
    clinicCursor.execute(s)

sql = 'SELECT DISTINCT createdBy FROM EChartAuditTrail'
clinicCursor = clinicConnection.cursor()
clinicCursor.execute (sql)
users = clinicCursor.fetchall()

for user in users:
    sql = "insert into UserAccount (LoginName,DisplayName,IsActive) \
        select '%s-echart', '%s-echart',0 \
        where not exists \
            (select loginName from useraccount where LoginName = '%s-echart')"
    s = sql % (user[0],user[0],user[0])
    clinicCursor.execute(s)

clinicCursor.commit()
clinicCursor.close()

# need to find the identities in the new system for the user's in the echart audit trail

sql = 'SELECT loginName FROM UserAccount'
clinicCursor = clinicConnection.cursor()
clinicCursor.execute(sql)
users = clinicCursor.fetchall()

for user in users:
    print 'finding identity for %s and updating...' % user[0]
    sql = "SELECT UserAccountId FROM UserAccount WHERE LoginName = '%s'"
    query = sql % user[0]
    clinicCursor.execute(query)
    identity = clinicCursor.fetchall()
    for i in identity:
        sql = "UPDATE EChartAuditTrail SET ModifiedById=%d WHERE modifiedBy='%s'"
        query = sql % (i[0],user[0])
        clinicCursor.execute(query)
        clinicCursor.commit()
        sql = "UPDATE EChartAuditTrail SET CreatedById=%d WHERE createdBy = '%s'"
        query = sql % (i[0],user[0])
        clinicCursor.execute(query)
        clinicCursor.commit()
        
    clinicCursor.commit()

clinicConnection.close()

cursorEChart.close()
connectionEChart.close()

    