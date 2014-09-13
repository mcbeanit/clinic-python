#unit test suite for clinic patient classes

import patient
import unittest
from datetime import date

class PatientTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_instantiate(self):
        p = patient.Patient()
            
    def test_calcage(self):
        p = patient.Patient();
        p.dateofbirth = date(1959,06,18)
        y = p.age

    def test_calcageInvalid(self):
        p = patient.Patient();
        
        

if __name__ == '__main__':
    unittest.main()