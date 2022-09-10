import unittest
import excel_audit_tools
from unittest import TestSuite, TextTestRunner
import settings
import xlwings as xw
from thermo.property_package import PropertyPackage
import pdb

class TestXLWingsUDFMethods(unittest.TestCase):
    def setUp(self):
        self.compounds = ['methane', 'ethane', 'hydrogen_sulfide']
        self.mole_fractions = [0.5, 0.4, 0.1]
        self.recovery_factors = [0.0, 0.98, 0.0]
        self.library = "GPA_2145"
        self.temperature = 60.0 # F
        self.pressure = 14.696  # psia
        self.volume = 1000.0 # Mcf
        self.hydrogen_sulfide = True
        self.from_temperature = 99.0 # F
        self.from_pressure = 1800.0  # psia
        self.to_temperature = 60.0 # F
        self.to_pressure = 14.65  # psia
        self.plus_mw = 180.64
        self.plus_spec_grav = 0.822
        self.plus_nbp = 0.0
        self.viscosity_data = [0, 0, 0, 0]
        return
 
    def test_ideal_gas_dry_heating_value(self):
        results = excel_audit_tools.ideal_gas_dry_heating_value(self.compounds, self.mole_fractions, self.recovery_factors, self.pressure, 
            self.temperature, self.volume)
        self.assertTrue(abs(results - 1276.5900) < settings.FLOAT_COMPARE_TOLERANCE)
        results = excel_audit_tools.ideal_gas_dry_heating_value(self.compounds, self.mole_fractions, self.recovery_factors, 14.65, 
            self.temperature, self.volume)
        self.assertTrue(abs(results - 1272.5941) < settings.FLOAT_COMPARE_TOLERANCE)
        results = excel_audit_tools.ideal_gas_dry_heating_value(['methane', 'hexane_plus', 'hydrogen_sulfide'], [0.5, 0.4, 0.1], [0.0, 0.98, 0.0], 
            self.pressure, self.temperature, self.volume)
        self.assertTrue(abs(results - 2620.3980) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_real_gas_dry_heating_value(self):
        results = excel_audit_tools.real_gas_dry_heating_value(self.compounds, self.mole_fractions, self.recovery_factors, self.pressure, 
            self.temperature, self.volume, self.hydrogen_sulfide)
        self.assertTrue(abs(results - 1282.4994) < settings.FLOAT_COMPARE_TOLERANCE)
        results = excel_audit_tools.real_gas_dry_heating_value(self.compounds, self.mole_fractions, self.recovery_factors, self.pressure, 
            self.temperature, self.volume, False)
        self.assertTrue(abs(results - 1353.4037) < settings.FLOAT_COMPARE_TOLERANCE)
        results = excel_audit_tools.real_gas_dry_heating_value(self.compounds, self.mole_fractions, self.recovery_factors, 14.65, 
            self.temperature, self.volume, False)
        self.assertTrue(abs(results - 1349.1494) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_compressibility_factor(self):
        results = excel_audit_tools.compressibility_factor(self.compounds, self.mole_fractions, self.recovery_factors, self.pressure, 
            self.temperature, self.volume)
        self.assertTrue(abs(results - 0.9954) < settings.FLOAT_COMPARE_TOLERANCE)     
        results = excel_audit_tools.compressibility_factor(self.compounds, self.mole_fractions, self.recovery_factors, 15.0, 
            self.temperature, self.volume)
        self.assertTrue(abs(results - 0.9953) < settings.FLOAT_COMPARE_TOLERANCE)
        return    

    def test_liquid_shrinkage_volume(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        results = excel_audit_tools.liquid_shrinkage_volume(self.compounds, self.mole_fractions, self.recovery_factors, self.pressure, 
            self.temperature, self.volume, "hexane_plus")
        self.assertTrue(abs(results - 4368.8473) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_liquid_shrinkage_energy(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        results = excel_audit_tools.liquid_shrinkage_energy(self.compounds, self.mole_fractions, self.recovery_factors, self.pressure, 
            self.temperature, self.volume, "propane")
        self.assertTrue(abs(results - 250.6505) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_plant_inlet_gas_energy(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        results = excel_audit_tools.plant_inlet_gas_energy(self.compounds, self.mole_fractions, self.recovery_factors, self.pressure, 
            self.temperature, self.volume, self.hydrogen_sulfide)
        self.assertTrue(abs(results - 2723.9999) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_residue_gas_energy(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        results = excel_audit_tools.residue_gas_energy(self.compounds, self.mole_fractions, self.recovery_factors, self.pressure, 
            self.temperature, self.volume, self.hydrogen_sulfide)
        self.assertTrue(abs(results - 377.3811) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_real_residue_gas_dry_heating_value(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        results = excel_audit_tools.real_residue_gas_dry_heating_value(self.compounds, self.mole_fractions, self.recovery_factors, self.pressure, 
            self.temperature, self.volume, self.hydrogen_sulfide)
        self.assertTrue(abs(results - 1163.9761) < settings.FLOAT_COMPARE_TOLERANCE)
        results = excel_audit_tools.real_residue_gas_dry_heating_value(self.compounds, self.mole_fractions, self.recovery_factors, self.pressure, 
            self.temperature, self.volume, False)
        self.assertTrue(abs(results - 1369.9023) < settings.FLOAT_COMPARE_TOLERANCE)
        results = excel_audit_tools.real_residue_gas_dry_heating_value(self.compounds, self.mole_fractions, self.recovery_factors, 14.65, 
            self.temperature, self.volume, False)
        self.assertTrue(abs(results - 1365.1853) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_residue_compressibility_factor(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        results = excel_audit_tools.residue_compressibility_factor(self.compounds, self.mole_fractions, self.recovery_factors, self.pressure, 
            self.temperature, self.volume)
        self.assertTrue(abs(results - 0.9946) < settings.FLOAT_COMPARE_TOLERANCE)     
        results = excel_audit_tools.residue_compressibility_factor(self.compounds, self.mole_fractions, self.recovery_factors, 15.0, 
            self.temperature, self.volume)
        self.assertTrue(abs(results - 0.9945) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def test_residue_gas_volume(self):
        self.compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide']
        self.mole_fractions = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.recovery_factors = [0.0, 0.75, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.0]
        results = excel_audit_tools.residue_gas_volume(self.compounds, self.mole_fractions, self.recovery_factors, self.pressure, 
            self.temperature, self.volume)
        self.assertTrue(abs(results - 337.0000) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    # def test_normalize_mole_fractions_from_excel(self):
    #     xw.Book('excel_audit_tools.xlsm').set_mock_caller()
    #     # For input compounds = ['methane', 'ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'hexane_plus', 'hydrogen_sulfide', 
    #     #                       'carbon_dioxide', 'nitrogen', 'oxygen', 'helium']
    #     # Expects input mole fractions = [0.65, 0.1, 0.05, 0.025, 0.025, 0.025, 0.025, 0.1, 0.005, 0.0, 0.0, 0.0, 0.0]
    #     PropertyPackage.normalize_mole_fractions_from_excel()
    #     normalized_mole_fractions = xw.Range('B7:B19').value
    #     self.assertTrue(abs(normalized_mole_fractions[0] - 0.6468) < settings.FLOAT_COMPARE_TOLERANCE)
    #     self.assertTrue(abs(normalized_mole_fractions[1] - 0.0995) < settings.FLOAT_COMPARE_TOLERANCE)
    #     self.assertTrue(abs(normalized_mole_fractions[2] - 0.0498) < settings.FLOAT_COMPARE_TOLERANCE)
    #     self.assertTrue(abs(normalized_mole_fractions[3] - 0.0249) < settings.FLOAT_COMPARE_TOLERANCE)
    #     self.assertTrue(abs(normalized_mole_fractions[4] - 0.0249) < settings.FLOAT_COMPARE_TOLERANCE)
    #     self.assertTrue(abs(normalized_mole_fractions[5] - 0.0249) < settings.FLOAT_COMPARE_TOLERANCE)
    #     self.assertTrue(abs(normalized_mole_fractions[6] - 0.0249) < settings.FLOAT_COMPARE_TOLERANCE)
    #     self.assertTrue(abs(normalized_mole_fractions[7] - 0.0995) < settings.FLOAT_COMPARE_TOLERANCE)
    #     self.assertTrue(abs(normalized_mole_fractions[8] - 0.0050) < settings.FLOAT_COMPARE_TOLERANCE)
    #     return

    def test_flash_t_p(self):
        self.compounds = ['Methane', 'Ethane', 'Propane', 'Isobutane', 'N-butane', 'Isopentane', 'N-pentane', 'N-hexane', 'Heptane plus', 'Hydrogen sulfide', 
        'Carbon dioxide', 'Nitrogen', 'Oxygen', 'Helium-4']
        self.mole_fractions = [0.0612, 0.0576, 0.0743, 0.0253, 0.0614, 0.0347, 0.0421, 0.0610, 0.5808, 0.0000, 0.0015, 0.0000, 0.0000, 0.0000]
        self.volume = 1124.9    # bbl
        self.from_temperature = 87.0 # F
        self.from_pressure = 289.65  # psia
        self.to_temperature = 60.0 # F
        self.to_pressure = 14.65  # psia
        self.standard_pressure = 14.65  # psia
        self.standard_temperature = 60.0    # F
        results = excel_audit_tools.flash_t_p(self.compounds, self.mole_fractions, self.from_pressure, self.from_temperature, self.to_pressure, self.to_temperature, 
            self.volume, self.plus_mw, self.plus_spec_grav, self.plus_nbp, self.viscosity_data, self.standard_pressure, self.standard_temperature)
        self.assertTrue(abs(results[0] - 1013.8265) < settings.FLOAT_COMPARE_TOLERANCE)
        self.assertTrue(abs(results[1] - 185.9709) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def tearDown(self):
        return

    def test_two_stage_flash_t_p(self):
        self.compounds = ['Methane', 'Ethane', 'Propane', 'Isobutane', 'N-butane', 'Isopentane', 'N-pentane', 'N-hexane', 'Heptane plus', 'Hydrogen sulfide', 
        'Carbon dioxide', 'Nitrogen', 'Oxygen', 'Helium-4']
        self.mole_fractions = [0.0612, 0.0576, 0.0743, 0.0253, 0.0614, 0.0347, 0.0421, 0.0610, 0.5808, 0.0000, 0.0015, 0.0000, 0.0000, 0.0000]
        self.volume = 1124.9    # bbl
        self.from_temperature = [87.0, 70.0, 60.0] # F
        self.from_pressure = [289.65, 100, 14.65]  # psia
        self.to_temperature = [70.0, 60.0, 0.0] # F
        self.to_pressure = [100.0, 14.65, 0.0]  # psia
        self.standard_pressure = 14.65  # psia
        self.standard_temperature = 60.0    # F
        results = excel_audit_tools.flash_t_p(self.compounds, self.mole_fractions, self.from_pressure, self.from_temperature, self.to_pressure, self.to_temperature, 
            self.volume, self.plus_mw, self.plus_spec_grav, self.plus_nbp, self.viscosity_data, self.standard_pressure, self.standard_temperature)
        # pdb.set_trace()
        self.assertTrue(abs(results[0] - 1027.0393) < settings.FLOAT_COMPARE_TOLERANCE)
        self.assertTrue(abs(results[1] - 165.3901) < settings.FLOAT_COMPARE_TOLERANCE)
        return

    def tearDown(self):
        return

def suite():
    suite = TestSuite()
    suite.addTest(TestXLWingsUDFMethods('test_ideal_gas_dry_heating_value'))
    suite.addTest(TestXLWingsUDFMethods('test_real_gas_dry_heating_value'))
    suite.addTest(TestXLWingsUDFMethods('test_compressibility_factor'))
    suite.addTest(TestXLWingsUDFMethods('test_liquid_shrinkage_volume'))
    suite.addTest(TestXLWingsUDFMethods('test_liquid_shrinkage_energy'))
    suite.addTest(TestXLWingsUDFMethods('test_plant_inlet_gas_energy'))
    suite.addTest(TestXLWingsUDFMethods('test_residue_gas_energy'))
    suite.addTest(TestXLWingsUDFMethods('test_real_residue_gas_dry_heating_value'))
    suite.addTest(TestXLWingsUDFMethods('test_residue_compressibility_factor'))
    suite.addTest(TestXLWingsUDFMethods('test_residue_gas_volume'))
    # suite.addTest(TestXLWingsUDFMethods('test_normalize_mole_fractions_from_excel'))
    suite.addTest(TestXLWingsUDFMethods('test_flash_t_p'))
    suite.addTest(TestXLWingsUDFMethods('test_two_stage_flash_t_p'))

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
