#unit test for echart module

import unittest
import echart

class PatientTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_stripAscii(self):
        assert 'hello' == strip_non_ascii('hello')
        assert '' == strip_non_ascii('')

    def test_getAuditTrail(self):
        sql = getDocumentAudit(100000)
        assert len(sql) > 0

    def test_getechartconnection(self):
        echart.getConnection()

    def test_getpatientlist(self):
        assert len(echart.getpatientlist()) > 0
        
       


if __name__ == '__main__':
    unittest.main()


