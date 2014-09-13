# patient - domain object extending a person

import person

class Patient(person.Person):

    def __init__ (self):
        super(Patient, self).__init__() #base class initialization
        self.patientid = 0
        self.phn = ''
        self.providerid = 0
        self.chart = ''


#### some tests

print 'hello'

p = Patient()
p.patientid = 9
p.personid = 10
p.age = 99
print p.age



