import os
import unittest

from my_tools.manifest_parser import AndroidManifestXmlParser

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class AbleToRetrieveMainActivity(unittest.TestCase):
    """AndroidManifestXmlParser should be able to retrieve the main activity name"""

    def test_get_main_activity_name_simple(self):
        parser = AndroidManifestXmlParser(os.path.join(__location__, "AndroidManifest.xml"))
        self.assertEqual(parser.get_main_activity_name(), "it.uniroma2.adidiego.apikeytestapp.MainActivity")

    def test_get_main_activity_name_alias(self):
        parser = AndroidManifestXmlParser(os.path.join(__location__, "AndroidManifest2.xml"))
        self.assertEqual(parser.get_main_activity_name(), "com.xlythe.calculator.material.Calculator")

    def test_get_main_activity_name_relative(self):
        parser = AndroidManifestXmlParser(os.path.join(__location__, "AndroidManifest3.xml"))
        self.assertEqual(parser.get_main_activity_name(), "com.ducky.tracedrawingLite.MainActivity")

    def test_get_main_activity_name_relative2(self):
        parser = AndroidManifestXmlParser(os.path.join(__location__, "AndroidManifest4.xml"))
        self.assertEqual(parser.get_main_activity_name(), "com.WiringDiagramMobil.TroneStudio.WiringDiagramMobil")
