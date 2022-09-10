from thermo.pure_component import PureComponent
import settings
import numpy as np
from numpy.linalg import solve
import xlwings as xw
import pdb

class PropertyPackage():
    def __init__(self, library, composition):
        self.library = library
        self.package_components = []
        for component in composition:
            name, mole_fraction, recovery_factor = component
            if library == "GPA_2145" and name == "hexane_plus":
                self.package_components.append(PureComponent(('n_hexane', settings.HEXANE_PLUS_N_HEXANE_FRACTION*mole_fraction, recovery_factor), 
                    self.library))
                self.package_components.append(PureComponent(('n_heptane', settings.HEXANE_PLUS_N_HEPTANE_FRACTION*mole_fraction, recovery_factor), 
                    self.library))
                self.package_components.append(PureComponent(('n_octane', settings.HEXANE_PLUS_N_OCTANE_FRACTION*mole_fraction, recovery_factor), 
                    self.library))
            else:    
                self.package_components.append(PureComponent(component, self.library))
        self._validate_composition()
    
    def _validate_composition(self):
        mole_fraction_sum = 0.0
        if len(self.package_components) == 0:   # Construction with empty component list OK
            return
        for component in self.package_components:
            mole_fraction_sum += component.mole_fraction
        if abs(mole_fraction_sum - 1.0) > settings.FLOAT_COMPARE_TOLERANCE:
            # TODO Return user to input mode
            print("Error: Sum of mole fractions in composition not equal to 1.0")
        return

    @classmethod
    def normalize_mole_fractions(cls, input_composition):
        input_data_vectors_as_tuples = list(zip(*input_composition))    # creates [(compounds), (mole_fractions)...] from [(compound, mole_fraction...)]
        input_mole_fractions = list(input_data_vectors_as_tuples[1])
        normalized_mole_fractions = np.zeros(len(input_mole_fractions))
        input_mole_fraction_sum = np.sum(input_mole_fractions)
        for component_index in range(0, len(input_mole_fractions)):
            normalized_mole_fractions[component_index] = input_mole_fractions[component_index]/input_mole_fraction_sum
        return normalized_mole_fractions.tolist()

    @classmethod
    def normalize_mole_fractions_from_excel(cls, begin_cell, end_cell):
        workbook = xw.Book.caller()
        input_mole_fractions = xw.Range(begin_cell + ':' + end_cell).value
        input_composition = []
        for mole_fraction in input_mole_fractions:
            input_composition.append(("", mole_fraction, 0.0))
        normalized_mole_fractions = PropertyPackage.normalize_mole_fractions(input_composition)
        xw.Range(begin_cell).options(transpose=True).value = normalized_mole_fractions
        return

    @classmethod
    def split_crude_oil_composition(cls, input_composition):
        # For now, this will only work for DWSIM.  TODO: Need to be able to configure settings.FLUID_PROPERTY_LIBRARY from UI.
        light_ends = []
        heavy_ends = []
        input_data_vectors_as_tuples = list(zip(*input_composition))    # creates [(compounds), (mole_fractions)...] from [(compound, mole_fraction...)]
        input_component_names = list(input_data_vectors_as_tuples[0]) 
        input_mole_fractions = list(input_data_vectors_as_tuples[1])
        for component_index in range(0, len(input_mole_fractions)):
            if input_component_names[component_index] == "Heptane plus":
                heavy_ends.append((input_component_names[component_index], input_mole_fractions[component_index]))
            else:
                light_ends.append((input_component_names[component_index], input_mole_fractions[component_index]))              
        return (light_ends, heavy_ends)
