# convert/update patient rows from echart to mcbean.clinic
# 21 May 2014

import echart
import pyodbc
import person

#mdb = 'j:\datafile\medtech97.mdb'
#eChartConn = r"Driver={Microsoft Access Driver (*.mdb)};Dbq=%s" % mdb   #dev
#eChartConn = r"Driver={Microsoft Access Driver (*.mdb)};Dbq=%s" % mdb #behm

connectionEChart = echart.getechartconnection()     #pyodbc.connect(eChartConn)
cursorEChart = connectionEChart.cursor()

clinicConn = 'DRIVER={SQL Server};SERVER=WELCOMETOSHIBA\SQLEXPRESS;DATABASE=mcbean_clinic;Trusted_Connection=yes'
clinicConnection = pyodbc.connect(clinicConn)
clinicCursor = clinicConnection.cursor()

cursorEChart.execute('SELECT dat_index_number, patient_name, provincecode, personal_health_number, date_of_birth, \
        sex, address, city, province, postal_code, phone_home, phone_work FROM Patient_Demographics')

rows = cursorEChart.fetchall()

print '-- begin sql script'

for row in rows:
    patientId = row[0]
    patientName = echart.nonetostr(row[1])
    patientName = patientName.replace("'",' ')
    provinceCode = row[2]
    phn = row[3]
    dob = row[4]
    gender = row[5]
    address = row[6]
    city = row[7]
    province = row[8]
    postalcode = row[9]
    homePhone = row[10]
    workPhone = row[11]
    celPhone = None
    
    names = person.SplitNames(patientName)

    firstName = names[0]
    middleName = names[1]
    lastName = names[2]

    #print 'convert->', patientName

    cmd = "exec spCreateUpdatePatient @patientId, @patientName, @firstName, @middleName, @lastName, @DateOfBirth, NULL, @Address, @City, @Province, \
            @Gender, @Phn, @HomePhone, @CelPhone, @WorkPhone"

    #%  \
     # (patientId, patientName, firstName, middleName, lastName, dob, None, address, city, provinceCode, gender, phn, phoneHome, workPhone, None)

    #cmd = cmd.replace("'None'", 'NULL')

    ##  what the stored procedure is looking for.    
    ##	@PatientId INT,
    ##	@DisplayName varchar(100),
    ##	@FirstName varchar(50),
    ##	@MiddleName varchar(50),
    ##	@LastName varchar(50),
    ##	@DateOfBirth datetime,
    ##	@DateOfDeath datetime,
    ##	@Address VARCHAR(100),
    ##	@City VARCHAR(50),
    ##	@Province VARCHAR(50),
    ##	@Gender char(1),
    ##	@PHN VARCHAR(100),
    ##	@HomePhone VARCHAR(100),
    ##	@CelPhone VARCHAR(100),
    ##	@WorkPhone VARCHAR(100)

    cmd = cmd.replace ('@patientId',  str(patientId) )
    cmd = cmd.replace ('@patientName', "'" + patientName + "'")

    firstName = 'NULL' if firstName is None else ("'" + str(firstName) + "'")
    cmd = cmd.replace ('@firstName', firstName)

    middleName = 'NULL' if middleName is None else "'" + str(middleName) + "'"
    cmd = cmd.replace ('@middleName', middleName)

    lastName = 'NULL' if lastName is None else "'" + str(lastName) + "'"
    cmd = cmd.replace ('@lastName', lastName)

    dob = 'NULL' if dob is None else "'" + str(dob) + "'"
    cmd = cmd.replace ('@DateOfBirth', dob)

    #address

    address = echart.nonetostr(address)
    address = echart.strip_non_ascii(address)
    address = address.strip()
    address = address.replace("'","''")
    
    if not address:
        address = 'NULL'
    else:
        assert not address == None
        address = "'" + address + "'"

    assert not address is None
    assert not address == 'None'

    cmd = cmd.replace('@Address', address)

    #city

    city = echart.nonetostr(city)
    city = echart.strip_non_ascii(city)
    city = city.strip()

    if city:
        city = "'" + city + "'"
    else:
        city = 'NULL'
        
    cmd = cmd.replace('@City', city)

    # province or province code - ab, alberta, etc

    province = echart.nonetostr(province)
    province = echart.strip_non_ascii(province)
    province = province.strip()
    
    if province:
        province = "'" + province + "'"
    else:
        province = 'NULL'

    cmd = cmd.replace('@Province', province)

    # gender - m,f,male,female

    gender = echart.nonetostr(gender)
    gender = echart.strip_non_ascii(gender)
    gender = gender.strip()

    if gender:
        gender = "'" + gender + "'"
    else:
        gender = 'NULL'
            
    cmd = cmd.replace('@Gender', gender)
    
    #phn
    phn = echart.nonetostr(phn)
    phn = echart.strip_non_ascii(phn)
    phn = phn.strip()

    if phn:
        phn = "'" + phn + "'"
    else:
        phn = 'NULL'

    cmd = cmd.replace('@Phn', phn)

    #homephone

    homePhone = echart.nonetostr(homePhone)
    homePhone = echart.strip_non_ascii(homePhone)
    homePhone = homePhone.strip()

    if homePhone:
        homePhone = "'" + homePhone + "'"
    else:
        homePhone = 'NULL'

    cmd = cmd.replace('@HomePhone', homePhone)

    # celphone

    celPhone = echart.nonetostr(celPhone)
    celPhone = echart.strip_non_ascii(celPhone)
    celPhone = celPhone.strip()

    if celPhone:
        celPhone = "'" + celPhone + "'"
    else:
        celPhone = 'NULL'

    cmd = cmd.replace('@CelPhone', celPhone)

    # work phone

    workPhone = echart.nonetostr(workPhone)
    workPhone = echart.strip_non_ascii(workPhone)
    workPhone = workPhone.strip()

    if workPhone:
        workPhone = "'" + workPhone + "'"
    else:
        workPhone = 'NULL'

    cmd = cmd.replace('@WorkPhone', workPhone)

    print cmd
    assert cmd.find('None') == -1
    
    #print patientId, patientName, address, len(address)


    try:
        pass
        clinicCursor.execute(cmd)
        #clinicCursor.commit()

    except:
        print "Error: " , cmd
        
        exit(1)


print '-- end sql script'
clinicCursor.commit()
connectionEChart.close()
clinicCursor.close()
clinicConnection.close()


