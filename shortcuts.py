import pyodbc
import echart

connectionEChart = echart.getechartconnection()     #pyodbc.connect(eChartConn)
cursorEChart = connectionEChart.cursor()

clinicConn = 'DRIVER={SQL Server};SERVER=BEHMSRV1\BKUPEXEC;DATABASE=mcbean.clinic;Trusted_Connection=yes'
clinicConnection = pyodbc.connect(clinicConn)
clinicCursor = clinicConnection.cursor()

cursorEChart.execute(echart.getShortCutCodes())

codes = cursorEChart.fetchall();

for code in codes:
    print "INSERT INTO ShortCutCode (Code,ReplaceText) VALUES ('%s', '%s')"  % (code[0], code[1])