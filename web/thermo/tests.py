import os
import sys
# Set the path for project imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import settings
from thermo.material_stream import MaterialStream
import pdb

class TestMaterialStreamMethods(unittest.TestCase):

    def setUp(self):
        self.temperature = 60.0
        self.pressure = 14.696
        self.composition = {}
        self.composition = {"methane": 0.7, "ethane": 0.1, "propane": 0.09, "i_butane": 0.025, "n_butane": 0.025, "i_pentane": 0.02, 
        "n_pentane": 0.02, "hexane_plus": 0.01, "hydrogen_sulfide": 0.01}
        self.volume = 1000.0
        self.data_source = settings.FLUID_PROPERTY_DATA_SOURCE
        self.recovery_factors = {}
        self.recovery_factors = {"methane": 0.0, "ethane": 0.75, "propane": 0.98, "i_butane": 0.98, "n_butane": 0.98, "i_pentane": 0.98, 
        "n_pentane": 0.98, "hexane_plus": 0.98, "hydrogen_sulfide": 0.0}
        os.chdir('..') # App config settings include file search paths relative to root directory
        self.gas_stream = MaterialStream(self.pressure, self.temperature, self.composition, self.volume, 
            self.data_source, self.recovery_factors)
        return

    def test_compressibility_factor(self):
        z = self.gas_stream.compressibility_factor()
        self.assertTrue(abs(z - 0.99449885560191) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_real_gas_heating_value(self):
        heating_value = self.gas_stream.real_gas_heating_value()
        self.assertTrue(abs(heating_value - 1499.3774920912401) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_recover_liquid_volumes(self):
        recovered_liquid_volumes = self.gas_stream.recover_liquid_volumes()
        self.assertTrue(abs(recovered_liquid_volumes['ethane'] - 2011.7068949814834) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def tearDown(self):
        os.chdir('thermo')
        return

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestMaterialStreamMethods('test_compressibility_factor'))
    suite.addTest(TestMaterialStreamMethods('test_real_gas_heating_value'))
    suite.addTest(TestMaterialStreamMethods('test_recover_liquid_volumes'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
