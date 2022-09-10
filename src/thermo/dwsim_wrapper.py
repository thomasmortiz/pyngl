import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'dwsim')))
import clr
clr.AddReference("DWSIM.Thermodynamics.StandaloneLibrary")
import pdb
from DWSIM.Thermodynamics.CalculatorInterface import Calculator
from DWSIM.Interfaces.Enums import StreamSpec
from DWSIM.Thermodynamics.Streams import MaterialStream
from DWSIM.Thermodynamics.Utilities.PetroleumCharacterization import GenerateCompounds
from DWSIM.SharedClasses.Utilities.PetroleumCharacterization.Assay import Assay
from DWSIM.Thermodynamics.BaseClasses import Compound
import settings
from uom.unit_converter import UnitConverter
from System import Double, Array, Nullable

class DWSIMWrapper():
    @classmethod
    def generate_oil_characterization(cls, assay_name, n_pseudos, adjustAf, adjustZR, molecular_weight, specific_gravity, normal_boiling_point, v_t_curve):
        # Viscosity curve data
        temperatures = [points[0] for points in v_t_curve]
        viscosities = [points[1] for points in v_t_curve]
        t1 = Nullable[Double](UnitConverter.convert_temperature(temperatures[0], "F", "K"))
        t2 = Nullable[Double](UnitConverter.convert_temperature(temperatures[1], "F", "K"))
        v1 = Nullable[Double](UnitConverter.convert_viscosity(viscosities[0], "ft2/s", "m2/s"))
        v2 = Nullable[Double](UnitConverter.convert_viscosity(viscosities[1], "ft2/s", "m2/s"))
        # Assay properties
        mw = Nullable[Double](molecular_weight)
        sg = Nullable[Double](specific_gravity)
        # TODO: Why does unit conversion break this next statement?
        # nbp = Nullable[Double](UnitConverter.convert_temperature(normal_boiling_point, "F", "K"))
        if abs(normal_boiling_point - 0.0) > settings.FLOAT_COMPARE_TOLERANCE:
            raise NotImplementedError("generate_oil_characterization does not currently support using NBP as an input parameter")
        nbp = Nullable[Double](normal_boiling_point)
        # Properties of lightest component in stream
        mw0 = settings.OIL_CHARACTERIZATION_MW_LIGHTEST_PSEUDOCOMPONENT
        sg0 = settings.OIL_CHARACTERIZATION_SG_LIGHTEST_PSEUDOCOMPONENT
        nbp0 = UnitConverter.convert_temperature(settings.OIL_CHARACTERIZATION_NBP_LIGHTEST_PSEUDOCOMPONENT, "F", "K")
        # Correlations
        Tccorr = settings.OIL_CHARACTERIZATION_TC_CORR
        Pccorr = settings.OIL_CHARACTERIZATION_PC_CORR
        AFcorr = settings.OIL_CHARACTERIZATION_AF_CORR
        MWcorr = settings.OIL_CHARACTERIZATION_MW_CORR
        compound_generator = GenerateCompounds()
        compound_data = compound_generator.GenerateCompounds(assay_name, n_pseudos, Tccorr, Pccorr, AFcorr, MWcorr, adjustAf, adjustZR, mw, sg, nbp, 
            v1, v2, t1, t2, mw0, sg0, nbp0)
        compounds = list(compound_data.Values)
        assay = Assay(mw, sg, nbp, t1, t2, v1, v2)
        return (compounds, assay)

    @classmethod
    def flash_t_p(cls, flash_from_temperature, flash_from_pressure, flash_to_temperature, flash_to_pressure, overall_volumetric_flow_rate, 
        light_ends_composition, light_ends_molar_flow_rate_fraction, oil_characterization, standard_pressure, 
        standard_temperature):
        flash_calculator = Calculator()
        flash_calculator.Initialize()
        property_package_name = settings.DWSIM_PROPERTY_PACKAGE
        property_package = flash_calculator.GetPropPackInstance(property_package_name)
        # Cast flash conditions to list type to support old, scalar (one-stage) input
        flash_from_pressure = flash_from_pressure if isinstance(flash_from_pressure, list) else [flash_from_pressure]
        flash_from_temperature = flash_from_temperature if isinstance(flash_from_temperature, list) else [flash_from_temperature]
        flash_to_pressure = flash_to_pressure if isinstance(flash_to_pressure, list) else [flash_to_pressure]
        flash_to_temperature = flash_to_temperature if isinstance(flash_to_temperature, list) else [flash_to_temperature]
        from_pressure = []
        from_temperature = []
        to_pressure = []
        to_temperature = []
        flashes = 0
        for pressure_stage in range(0,len(flash_to_pressure)):
            if flash_to_pressure[pressure_stage] > 0.0:
                flashes += 1
            else:
                break
        if flashes == 0:
            raise ValueError('No valid flash stage outlet pressures.')
        compound_names = []
        mole_fractions = []
        assay = None
        heavy_ends = None
        light_ends = None
        if light_ends_composition:
            compound_names = [components[0] for components in light_ends_composition]
            mole_fractions = [components[1] for components in light_ends_composition]
            light_ends = flash_calculator.CreateMaterialStream(compound_names, mole_fractions)
            light_ends.SetPropertyPackage(property_package)
            light_ends.ClearAllProps()
            light_ends.SetProp("fraction", "Overall", None, "", "mole", mole_fractions)
        compound_names = []
        mole_fractions = []
        if oil_characterization:
            compounds, assay = oil_characterization
            compound_names = [compound.Name for compound in compounds]
            mole_fractions = [compound.MoleFraction*(1.0 - light_ends_molar_flow_rate_fraction) for compound in compounds]
            heavy_ends = MaterialStream("", "")
            DWSIMWrapper._add_components_to_material_stream(compounds, heavy_ends)
            heavy_ends.SetPropertyPackage(property_package)
            heavy_ends.ClearAllProps()
            heavy_ends.SetProp("fraction", "Overall", None, "", "mole", mole_fractions)
        flashed_phase_rates = [0.0, 0.0]    # [liquid_rate, vapor_rate]
        mixture = None
        liquid = None
        for flash_stage in range(0,flashes):
            from_pressure.append(Double(UnitConverter.convert_pressure(flash_from_pressure[flash_stage], "psia", "Pa")))
            from_temperature.append(Double(UnitConverter.convert_temperature(flash_from_temperature[flash_stage], "F", "K")))
            to_pressure.append(Double(UnitConverter.convert_pressure(flash_to_pressure[flash_stage], "psia", "Pa")))
            to_temperature.append(Double(UnitConverter.convert_temperature(flash_to_temperature[flash_stage], "F", "K")))
            if flash_stage == 0: # Mix heavy and light ends for first stage flash
                mixture = DWSIMWrapper._mix_and_flash_material_streams([light_ends, heavy_ends], property_package, from_pressure[flash_stage], 
                    from_temperature[flash_stage], to_pressure[flash_stage], to_temperature[flash_stage], overall_volumetric_flow_rate)
            else: # Flash liquid phase from preceding stage for remaining stages
                mixture = DWSIMWrapper._mix_and_flash_material_streams(liquid, property_package, from_pressure[flash_stage], 
                    from_temperature[flash_stage], to_pressure[flash_stage], to_temperature[flash_stage], overall_volumetric_flow_rate)
            # Retrieve liquid phase composition for subsequent stage flashes
            liquid_compounds = DWSIMWrapper._extract_liquid_composition(mixture)
            liquid = MaterialStream("", "")
            DWSIMWrapper._add_components_to_material_stream(liquid_compounds, liquid)
            phase_data = mixture.GetPresentPhases(None, None)
            if "Liquid" in phase_data[1]:
                liquid_flow_rate = mixture.GetProp("totalFlow", "Liquid", None, "", "mole")
                liquid_molecular_weight = mixture.GetSinglePhaseProp("molecularWeight", "Liquid", "", None)
                liquid_density = mixture.GetSinglePhaseProp("density", "Liquid", "mass", None)
                liquid_volumetric_flow_rate = liquid_flow_rate[0]*liquid_molecular_weight[0]/(settings.KMOL_TO_MOL*liquid_density[0])
                # Return final shrunken oil rate from last stage (assume incompressible)
                flashed_phase_rates[0] = UnitConverter.convert_volume(liquid_volumetric_flow_rate, "m3", "bbl")
                # Recalculate overall volumetric flow rate to correspond to residual liquid for next stage
                overall_volumetric_flow_rate = flashed_phase_rates[0]
            if "Vapor" in phase_data[1]:
                vapor_flow_rate = mixture.GetProp("totalFlow", "Vapor", None, "", "mole")
                vapor_molecular_weight = mixture.GetSinglePhaseProp("molecularWeight", "Vapor", "", None)
                vapor_density = mixture.GetSinglePhaseProp("density", "Vapor", "mass", None)
                vapor_volumetric_flow_rate = vapor_flow_rate[0]*vapor_molecular_weight[0]/(settings.KMOL_TO_MOL*vapor_density[0])
                # Return sum of flashed gas rates at standard conditions for all stages 
                flashed_phase_rates[1] += UnitConverter.convert_volume_to_standard_conditions(vapor_volumetric_flow_rate, "m3", "Mcf", 
                    UnitConverter.convert_pressure(flash_to_pressure[flash_stage], "psia", "Pa"), 
                    UnitConverter.convert_temperature(flash_to_temperature[flash_stage], "F", "K"), 
                    UnitConverter.convert_pressure(standard_pressure, "psia", "Pa"), 
                    UnitConverter.convert_temperature(standard_temperature, "F", "K"))
            # pdb.set_trace()
        return flashed_phase_rates

    @classmethod
    def _add_components_to_material_stream(cls, components, material_stream):
        try:
            # add pseudocomponents as new Compound objects to each phase
            for component in components:
                for phase_index in range(0, material_stream.Phases.get_Count()):
                    compound = Compound(component.Name, "")
                    compound.MoleFraction = component.MoleFraction
                    compound.ConstantProperties = component.ConstantProperties
                    # pdb.set_trace()
                    material_stream.Phases[phase_index].Compounds.Add(compound.Name, compound)
        except Exception as e:
            raise e
        return

    @classmethod
    def _mix_and_flash_material_streams(cls, material_streams, property_package, flash_from_pressure, flash_from_temperature, flash_to_pressure, 
        flash_to_temperature, overall_volumetric_flow_rate):
        mixture = None
        compounds = []
        stream_mole_fractions = []
        stream_flow_rates = []
        stream_pressures = []
        mixture_mole_fractions = []
        mixture_flow_rate = 0.0
        mixture_pressure = 0.0
        mixture_temperature = 0.0
        material_streams = material_streams if isinstance(material_streams, list) else [material_streams]
        try:
            mixture = MaterialStream("", "")
            for material_stream in material_streams:
                DWSIMWrapper._add_components_to_material_stream(list(material_stream.Phases[0].Compounds.Values), mixture)
                stream_mole_fractions = [compound.MoleFraction for compound in list(material_stream.Phases[0].Compounds.Values)]
                mixture_mole_fractions.extend(stream_mole_fractions)
                # pdb.set_trace()
            mixture.SetPropertyPackage(property_package)
            mixture.ClearAllProps()
            # First, flash using dummy flow rate to get correct phase composition and density
            mixture.SetProp("temperature", "Overall", None, "", "", [flash_from_temperature])
            mixture.SetProp("pressure", "Overall", None, "", "", [flash_from_pressure])
            mixture.SetProp("totalFlow", "Overall", None, "", "mole", [1.0])
            mixture.SetProp("fraction", "Overall", None, "", "mole", mixture_mole_fractions)
            mixture.NormalizeOverallMoleComposition()
            mixture.SpecType = StreamSpec.Temperature_and_Pressure
            mixture.Calculate(True, True)
            mixture_density = mixture.GetProp("density", "Overall", None, "", "mass")[0]
            mixture_mw = mixture.GetProp("molecularWeight", "Overall", None, "", "mass")[0]
            mixture.ClearAllProps()
            # Next, calculate correct flow rate and reflash to source temperature and pressure
            mixture_flow_rate = DWSIMWrapper._calculate_mixture_flow_rate(mixture_density, mixture_mw, overall_volumetric_flow_rate, "mole")
            mixture.SetProp("temperature", "Overall", None, "", "", [flash_from_temperature])
            mixture.SetProp("pressure", "Overall", None, "", "", [flash_from_pressure])
            mixture.SetProp("totalFlow", "Overall", None, "", "mole", [mixture_flow_rate])
            mixture.SetProp("fraction", "Overall", None, "", "mole", mixture_mole_fractions)
            mixture.NormalizeOverallMoleComposition()
            mixture.SpecType = StreamSpec.Temperature_and_Pressure
            mixture.Calculate(True, True)
            # Finally, flash to target temperature and pressure
            mixture.SetProp("temperature", "Overall", None, "", "", [flash_to_temperature])
            mixture.SetProp("pressure", "Overall", None, "", "", [flash_to_pressure])
            mixture.Calculate(True, True)
        except Exception as e:
            raise e
        return mixture

    @classmethod
    def _calculate_mixture_flow_rate(cls, mixture_density, mixture_mw, overall_volumetric_flow_rate, basis):
        overall_mass_flow_rate = mixture_density*UnitConverter.convert_volume(overall_volumetric_flow_rate, "bbl", "m3")
        overall_molar_flow_rate = overall_mass_flow_rate*settings.KMOL_TO_MOL/mixture_mw
        if basis == "mass":
            return overall_mass_flow_rate
        elif basis == "mole":
            return overall_molar_flow_rate
        else:
            return 0.0

    @classmethod
    def _extract_liquid_composition(cls, mixture):
        liquid_compounds = []
        for phase in list(mixture.Phases):
            if phase.Value.Name == 'OverallLiquid':
                liquid_compounds = list(phase.Value.Compounds.Values)
                # pdb.set_trace()
        if len(liquid_compounds) == 0:
            raise ValueError('No liquid phase found in mixture.  Next flash stage will fail.')
        return liquid_compounds
