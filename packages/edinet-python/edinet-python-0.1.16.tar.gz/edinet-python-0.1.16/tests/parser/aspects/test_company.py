import os
import unittest
from edinet.parser.xbrl_file import XBRLFile
from edinet.parser.aspects.company import Company


class TestCompany(unittest.TestCase):

    def get_xbrl(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/xbrl2019.xbrl")
        xbrl = XBRLFile(path)
        return xbrl

    def test_history(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Company).history
        self.assertTrue(feature.value.startswith("2【沿革】"))

    def test_business_description(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Company).business_description
        self.assertTrue(feature.value.startswith("3【事業の内容】"))

    def test_affiliated_entities(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Company).affiliated_entities
        self.assertTrue(feature.value.startswith("4【関係会社の状況】"))

    def test_employees(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Company).employees
        self.assertTrue(feature.value.startswith("5【従業員の状況】"))
