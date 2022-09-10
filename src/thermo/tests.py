# Set the path for imports
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from thermo.property_package import PropertyPackage
from thermo.mixture import Mixture
from thermo.dwsim_wrapper import DWSIMWrapper
from unittest import TestSuite, TextTestRunner
import settings
import pdb

class TestPropertyPackageMethods(unittest.TestCase):
    def setUp(self):
        self.library = "GPA_2145"
        self.composition = [('methane', 0.5, 0.0), ('propane', 0.5, 0.98)]
        return
 
    def test_validate_property_package(self):
        package = PropertyPackage(self.library, self.composition)
        # TODO test for misaligned columns of compounds and mole fractions
        # TODO test for invalid composition (sum(mole_fractions) != 1.0)
        self.assertTrue(package is not None)
        return

    def test_normalize_mole_fractions(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.65, 0.1, 0.05, 0.025, 0.025, 0.025, 0.025, 0.1, 0.005]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        self.composition = list(zip(self.compounds, self.mole_fractions, self.recovery_factors))
        normalized_mole_fractions = PropertyPackage.normalize_mole_fractions(self.composition)
        self.assertTrue(abs(normalized_mole_fractions[0] - 0.6468) < settings.FLOAT_COMPARE_TOLERANCE)
        self.assertTrue(abs(normalized_mole_fractions[1] - 0.0995) < settings.FLOAT_COMPARE_TOLERANCE)
        self.assertTrue(abs(normalized_mole_fractions[2] - 0.0498) < settings.FLOAT_COMPARE_TOLERANCE)
        self.assertTrue(abs(normalized_mole_fractions[3] - 0.0249) < settings.FLOAT_COMPARE_TOLERANCE)
        self.assertTrue(abs(normalized_mole_fractions[4] - 0.0249) < settings.FLOAT_COMPARE_TOLERANCE)
        self.assertTrue(abs(normalized_mole_fractions[5] - 0.0249) < settings.FLOAT_COMPARE_TOLERANCE)
        self.assertTrue(abs(normalized_mole_fractions[6] - 0.0249) < settings.FLOAT_COMPARE_TOLERANCE)
        self.assertTrue(abs(normalized_mole_fractions[7] - 0.0995) < settings.FLOAT_COMPARE_TOLERANCE)
        self.assertTrue(abs(normalized_mole_fractions[8] - 0.0050) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def tearDown(self):
        return

class TestDWSIMWrapper(unittest.TestCase):
    def setUp(self):
        self.from_temperature = 87.0    # F
        self.from_pressure = 289.65 # psia
        self.to_temperature = 60.0  # F
        self.to_pressure = 14.65    # psia
        self.standard_pressure = 14.65  # psia
        self.standard_temperature = 60.0    # F
        self.volumetric_flowrate = 1124.9   #bbl/s (time unit unused)
        self.composition = [('Methane', 0.0612), ('Ethane', 0.0576), ('Propane', 0.0743), ('Isobutane', 0.0253), ('N-butane', 0.0614), ('Isopentane', 0.0347), 
        ('N-pentane', 0.0421), ('N-hexane', 0.0610), ('Hydrogen sulfide', 0.0), ('Carbon dioxide', 0.0015), ('Nitrogen', 0.0000), 
        ('Oxygen', 0.0000), ('Helium-4', 0.0000)]
        return
 
    def test_flash_t_p(self):
        oil_characterization = DWSIMWrapper.generate_oil_characterization("TestDWSIMWrapper.test_flash_t_p_Oil_0", 10, True, True, 174.6, 0.8037, 0.0, [(0,0), (0,0)])
        results = DWSIMWrapper.flash_t_p(self.from_temperature, self.from_pressure, self.to_temperature, self.to_pressure, self.volumetric_flowrate, self.composition, 
            0.4192, oil_characterization, self.standard_pressure, self.standard_temperature)
        self.assertTrue(abs(results[0] - 1012.2374) < settings.FLOAT_COMPARE_TOLERANCE)
        self.assertTrue(abs(results[1] - 185.7122) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def tearDown(self):
        return

class TestMixtureMethods(unittest.TestCase):
    def setUp(self):
        self.compounds = ['methane', 'ethane', 'hydrogen_sulfide']
        self.mole_fractions = [0.5, 0.4, 0.1]
        self.recovery_factors = [0.0, 0.98, 0.0]
        self.library = "GPA_2145"
        self.composition = list(zip(self.compounds, self.mole_fractions, self.recovery_factors))
        self.property_package = PropertyPackage(self.library, self.composition)
        self.temperature = 60.0 # F
        self.pressure = 14.696  # psia
        self.volume = 1000.0    # Mcf
        self.hydrogen_sulfide = True
        return

    def test_ideal_gas_dry_heating_value(self):
        results = Mixture(self.property_package, self.temperature, self.pressure, self.volume).ideal_gas_dry_heating_value()
        self.assertTrue(abs(results - 1276.5900) < settings.FLOAT_COMPARE_TOLERANCE)
        results = Mixture(self.property_package, self.temperature, 14.65, self.volume).ideal_gas_dry_heating_value()
        self.assertTrue(abs(results - 1272.5941) < settings.FLOAT_COMPARE_TOLERANCE)
        results = Mixture(PropertyPackage(self.library, [('methane', 0.5, 0.0), ('hexane_plus', 0.4, 0.98), ('hydrogen_sulfide', 0.1, 0.0)]), 
            self.temperature, self.pressure, self.volume).ideal_gas_dry_heating_value()
        self.assertTrue(abs(results - 2620.3980) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_real_gas_dry_heating_value(self):
        results = Mixture(self.property_package, self.temperature, self.pressure, self.volume).real_gas_dry_heating_value(self.hydrogen_sulfide)
        self.assertTrue(abs(results - 1282.4994) < settings.FLOAT_COMPARE_TOLERANCE)
        results = Mixture(self.property_package, self.temperature, self.pressure, self.volume).real_gas_dry_heating_value(False)
        self.assertTrue(abs(results - 1353.4037) < settings.FLOAT_COMPARE_TOLERANCE)
        results = Mixture(self.property_package, self.temperature, 14.65, self.volume).real_gas_dry_heating_value(False)
        self.assertTrue(abs(results - 1349.1494) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_compressibility_factor(self):
        results = Mixture(self.property_package, self.temperature, self.pressure, self.volume).compressibility_factor()
        self.assertTrue(abs(results - 0.9954) < settings.FLOAT_COMPARE_TOLERANCE)     
        results = Mixture(self.property_package, self.temperature, 15.0, self.volume).compressibility_factor()
        self.assertTrue(abs(results - 0.9953) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_liquid_shrinkage_volume(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        self.composition = list(zip(self.compounds, self.mole_fractions, self.recovery_factors))
        self.property_package = PropertyPackage(self.library, self.composition)
        results = Mixture(self.property_package, self.temperature, self.pressure, self.volume).liquid_shrinkage_volume("hexane_plus")
        self.assertTrue(abs(results - 4368.8473) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_liquid_shrinkage_energy(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        self.composition = list(zip(self.compounds, self.mole_fractions, self.recovery_factors))
        self.property_package = PropertyPackage(self.library, self.composition)
        results = Mixture(self.property_package, self.temperature, self.pressure, self.volume).liquid_shrinkage_energy("propane")
        self.assertTrue(abs(results - 250.6505) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_plant_inlet_gas_energy(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        self.composition = list(zip(self.compounds, self.mole_fractions, self.recovery_factors))
        self.property_package = PropertyPackage(self.library, self.composition)
        results = Mixture(self.property_package, self.temperature, self.pressure, self.volume).plant_inlet_gas_energy(self.hydrogen_sulfide)
        self.assertTrue(abs(results - 2723.9999) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_residue_gas_energy(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        self.composition = list(zip(self.compounds, self.mole_fractions, self.recovery_factors))
        self.property_package = PropertyPackage(self.library, self.composition)
        results = Mixture(self.property_package, self.temperature, self.pressure, self.volume).residue_gas_energy(self.hydrogen_sulfide)
        self.assertTrue(abs(results - 377.3811) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_real_residue_gas_dry_heating_value(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        self.composition = list(zip(self.compounds, self.mole_fractions, self.recovery_factors))
        self.property_package = PropertyPackage(self.library, self.composition)
        results = Mixture(self.property_package, self.temperature, self.pressure, self.volume).real_residue_gas_dry_heating_value(self.hydrogen_sulfide)
        self.assertTrue(abs(results - 1163.9761) < settings.FLOAT_COMPARE_TOLERANCE)
        results = Mixture(self.property_package, self.temperature, self.pressure, self.volume).real_residue_gas_dry_heating_value(False)
        self.assertTrue(abs(results - 1369.9023) < settings.FLOAT_COMPARE_TOLERANCE)
        results = Mixture(self.property_package, self.temperature, 14.65, self.volume).real_residue_gas_dry_heating_value(False)
        self.assertTrue(abs(results - 1365.1853) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_residue_compressibility_factor(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        self.composition = list(zip(self.compounds, self.mole_fractions, self.recovery_factors))
        self.property_package = PropertyPackage(self.library, self.composition)
        results = Mixture(self.property_package, self.temperature, self.pressure, self.volume).residue_compressibility_factor()
        self.assertTrue(abs(results - 0.9946) < settings.FLOAT_COMPARE_TOLERANCE)     
        results = Mixture(self.property_package, self.temperature, 15.0, self.volume).residue_compressibility_factor()
        self.assertTrue(abs(results - 0.9945) < settings.FLOAT_COMPARE_TOLERANCE)
        return   

    def test_residue_gas_volume(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        self.composition = list(zip(self.compounds, self.mole_fractions, self.recovery_factors))
        self.property_package = PropertyPackage(self.library, self.composition)
        results = Mixture(self.property_package, self.temperature, self.pressure, self.volume).residue_gas_volume()
        self.assertTrue(abs(results - 337.0000) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def tearDown(self):
        return

def suite():
    suite = TestSuite()
    suite.addTest(TestPropertyPackageMethods('test_validate_property_package'))
    suite.addTest(TestDWSIMWrapper('test_flash_t_p'))
    suite.addTest(TestMixtureMethods('test_ideal_gas_dry_heating_value'))
    suite.addTest(TestMixtureMethods('test_real_gas_dry_heating_value'))
    suite.addTest(TestMixtureMethods('test_compressibility_factor'))
    suite.addTest(TestMixtureMethods('test_liquid_shrinkage_volume'))
    suite.addTest(TestMixtureMethods('test_liquid_shrinkage_energy'))
    suite.addTest(TestMixtureMethods('test_plant_inlet_gas_energy'))
    suite.addTest(TestMixtureMethods('test_residue_gas_energy'))
    suite.addTest(TestMixtureMethods('test_real_residue_gas_dry_heating_value'))
    suite.addTest(TestMixtureMethods('test_residue_compressibility_factor'))
    suite.addTest(TestMixtureMethods('test_residue_gas_volume'))

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
