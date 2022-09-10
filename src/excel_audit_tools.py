import xlwings as xw
import settings
from thermo.property_package import PropertyPackage
from thermo.mixture import Mixture
from thermo.dwsim_wrapper import DWSIMWrapper
from uom.unit_converter import UnitConverter
import numpy as np
import pdb

@xw.func
def ideal_gas_dry_heating_value(compounds, mole_fractions, recovery_factors, pressure, temperature, volume):
    composition = list(zip(compounds, mole_fractions, recovery_factors))
    property_package = PropertyPackage(settings.FLUID_PROPERTY_LIBRARY, composition)
    results = Mixture(property_package, temperature, pressure, volume).ideal_gas_dry_heating_value()
    return results

@xw.func
def real_gas_dry_heating_value(compounds, mole_fractions, recovery_factors, pressure, temperature, volume, hydrogen_sulfide=True):
    composition = list(zip(compounds, mole_fractions, recovery_factors))
    property_package = PropertyPackage(settings.FLUID_PROPERTY_LIBRARY, composition)
    results = Mixture(property_package, temperature, pressure, volume).real_gas_dry_heating_value(hydrogen_sulfide)
    return results

@xw.func
def compressibility_factor(compounds, mole_fractions, recovery_factors, pressure, temperature, volume):
    composition = list(zip(compounds, mole_fractions, recovery_factors))
    property_package = PropertyPackage(settings.FLUID_PROPERTY_LIBRARY, composition)
    results = Mixture(property_package, temperature, pressure, volume).compressibility_factor()
    return results

@xw.func
def liquid_shrinkage_volume(compounds, mole_fractions, recovery_factors, pressure, temperature, volume, component):
    composition = list(zip(compounds, mole_fractions, recovery_factors))
    property_package = PropertyPackage(settings.FLUID_PROPERTY_LIBRARY, composition)
    results = Mixture(property_package, temperature, pressure, volume).liquid_shrinkage_volume(component)
    return results

# @xw.func
# def gas_shrinkage_volume_of_recovered_liquid(compounds, mole_fractions, recovery_factors, pressure, temperature, volume, component):
#     composition = list(zip(compounds, mole_fractions, recovery_factors))
#     property_package = PropertyPackage(settings.FLUID_PROPERTY_LIBRARY, composition)
#     results = Mixture(property_package, temperature, pressure, volume)._gas_shrinkage_volume_of_recovered_liquid(component)
#     return results

@xw.func
def liquid_shrinkage_energy(compounds, mole_fractions, recovery_factors, pressure, temperature, volume, component):
    composition = list(zip(compounds, mole_fractions, recovery_factors))
    property_package = PropertyPackage(settings.FLUID_PROPERTY_LIBRARY, composition)
    results = Mixture(property_package, temperature, pressure, volume).liquid_shrinkage_energy(component)
    return results

@xw.func
def plant_inlet_gas_energy(compounds, mole_fractions, recovery_factors, pressure, temperature, volume, hydrogen_sulfide=True):
    composition = list(zip(compounds, mole_fractions, recovery_factors))
    property_package = PropertyPackage(settings.FLUID_PROPERTY_LIBRARY, composition)
    results = Mixture(property_package, temperature, pressure, volume).plant_inlet_gas_energy(hydrogen_sulfide)
    return results

@xw.func
def residue_gas_energy(compounds, mole_fractions, recovery_factors, pressure, temperature, volume, hydrogen_sulfide=True):
    composition = list(zip(compounds, mole_fractions, recovery_factors))
    property_package = PropertyPackage(settings.FLUID_PROPERTY_LIBRARY, composition)
    results = Mixture(property_package, temperature, pressure, volume).residue_gas_energy(hydrogen_sulfide)
    return results
 
@xw.func
def real_residue_gas_dry_heating_value(compounds, mole_fractions, recovery_factors, pressure, temperature, volume, hydrogen_sulfide=True):
    composition = list(zip(compounds, mole_fractions, recovery_factors))
    property_package = PropertyPackage(settings.FLUID_PROPERTY_LIBRARY, composition)
    results = Mixture(property_package, temperature, pressure, volume).real_residue_gas_dry_heating_value(hydrogen_sulfide)
    return results

@xw.func
def residue_compressibility_factor(compounds, mole_fractions, recovery_factors, pressure, temperature, volume):
    composition = list(zip(compounds, mole_fractions, recovery_factors))
    property_package = PropertyPackage(settings.FLUID_PROPERTY_LIBRARY, composition)
    results = Mixture(property_package, temperature, pressure, volume).residue_compressibility_factor()
    return results

@xw.func
def residue_gas_volume(compounds, mole_fractions, recovery_factors, pressure, temperature, volume, component_name="mixture"):
    composition = list(zip(compounds, mole_fractions, recovery_factors))
    property_package = PropertyPackage(settings.FLUID_PROPERTY_LIBRARY, composition)
    results = Mixture(property_package, temperature, pressure, volume).residue_gas_volume(component_name)
    return results

# @xw.func
# def normalize_mole_fractions(compounds, mole_fractions):
#     recovery_factors = np.zeros(len(mole_fractions)).tolist()
#     composition = list(zip(compounds, mole_fractions, recovery_factors))
#     property_package = PropertyPackage(settings.FLUID_PROPERTY_LIBRARY, composition)
#     results = property_package.normalize_mole_fractions()
#     return results

@xw.func
@xw.ret(expand='table')
def flash_t_p(compounds, mole_fractions, flash_from_pressure, flash_from_temperature, flash_to_pressure, flash_to_temperature, volume, plus_mw, 
    plus_spec_grav, plus_nbp, viscosity_data, standard_pressure, standard_temperature):
    overall_composition = list(zip(compounds, mole_fractions))
    n_pseudos = settings.OIL_CHARACTERIZATION_NUMBER_OF_PSEUDOCOMPONENTS
    adjustAf = settings.OIL_CHARACTERIZATION_ADJUST_ACENTRIC_FACTORS
    adjustZR = settings.OIL_CHARACTERIZATION_ADJUST_RACKETT_PARAMETERS
    assay_name = settings.OIL_CHARACTERIZATION_ASSAY_NAME
    temperatures = [viscosity_data[0], viscosity_data[1]]
    viscosities = [viscosity_data[2], viscosity_data[3]]
    v_t_curve = list(zip(temperatures, viscosities))
    # DWSIM works on the basis of steady-state flow rates.  We calculate all results on a unit time basis here.
    overall_volumetric_flow_rate = volume
    light_ends_composition, heavy_ends_composition = PropertyPackage.split_crude_oil_composition(overall_composition)
    oil_characterization = DWSIMWrapper.generate_oil_characterization(assay_name, n_pseudos, adjustAf, adjustZR, plus_mw, plus_spec_grav, plus_nbp, v_t_curve)
    light_ends_molar_flow_rate_fraction = 1.0
    if ("Heptane plus" in heavy_ends_composition[0]):
        light_ends_molar_flow_rate_fraction -= heavy_ends_composition[0][1]
    results = DWSIMWrapper.flash_t_p(flash_from_temperature, flash_from_pressure, flash_to_temperature, flash_to_pressure, overall_volumetric_flow_rate, 
        light_ends_composition, light_ends_molar_flow_rate_fraction, oil_characterization, standard_pressure, standard_temperature)
    # Returns an array that will translate to a 2x1 cell array in Excel
    reformatted_results = np.array([[results[0]], [results[1]]])
    return reformatted_results
