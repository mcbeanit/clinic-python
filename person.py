#model simple attributes of a person and some static methods

import string
from datetime import date


def SplitNames(personName):
    firstName = None
    middleName = None
    lastName = None
    name = personName.replace('Br','')
    name = name.replace('Bmr','')
    name = name.replace('Do Not Use','')
    name = name.replace('Expired','')
    name = name.replace("'",' ')
    
    names = name.split()

    items = len(names)

    if items == 1:
        lastName = names[0]

    if items == 2:
        lastName = names[0]
        firstName = names[1]

    if items == 3:
        lastName = names[0]
        firstName = names[1]
        middleName = names[2]
        
    
    return firstName,middleName,lastName

class Person(object):
    
    def __init__ (self):
        self.id = 0
        self.firstName = ''
        self.middleName = ''
        self.lastName = ''
        self.dateofbirth = None
        self.dateofdeath = None
        self.age = None
        self.address = ''
        self.city = ''
        self.province = ''
        self.provincecode = ''
        self.postalcode = ''
        self.gender =  ''

    def calculateAge(self):
        if self.dateofbirth is not None:
            self.age = date.today() - self.dateofbirth

# some simple tests

y = SplitNames('mcbean robert william')
assert y[0] == 'robert'
assert y[1] == 'william'
assert y[2] == 'mcbean'

#Person.SplitNames("sdfdfdf")

p = Person()
p.id = 999
p.firstName = 'robert'
print p

a = Person()
a.dateofbirth = date(1959,6,18)
a.calculateAge()
print a.age
