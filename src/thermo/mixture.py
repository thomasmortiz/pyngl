from thermo.property_package import PropertyPackage, PureComponent
import thermo.gpa_2145
from copy import deepcopy
import settings
import pdb

class Mixture():
    def __init__(self, property_package, temperature, pressure, volume):
        self.property_package = property_package
        self.temperature_base = temperature
        self.pressure_base = pressure
        self.volume = volume

    def ideal_gas_dry_heating_value(self):  # Btu/ft3
        ideal_ghv_dry = 0.0
        for package_component in self.property_package.package_components:
            if package_component.ideal_gas_ghv and package_component.mole_fraction:
                ideal_ghv_dry += (package_component.ideal_gas_ghv*package_component.mole_fraction)
            # Correct for pressure base--ignores difference in compressibility factor (OK for small pressure changes)
        ideal_ghv_dry *= (self.pressure_base/thermo.gpa_2145.GPA_2145_PRESSURE_BASE)
        return ideal_ghv_dry

    def compressibility_factor(self, component_name="mixture"):   # dimensionless
        z = 0.0
        if settings.USE_LEE_KESLER_COMPRESSIBILITY_FACTOR == True:
            #TODO implement Lee-Kesler method from legacy spreadsheet
            pass
        else:
            if self.property_package.library == "GPA_2145":
                # This is a two-term virial equation of state trunction method that uses the summation factors from GPA Standard 2145
                summation = 0.0
                for package_component in self.property_package.package_components:
                    if package_component.summation_factor and package_component.mole_fraction:
                        if component_name == package_component.name:
                            summation = (package_component.summation_factor*package_component.mole_fraction)
                            break
                        else:
                            summation += (package_component.summation_factor*package_component.mole_fraction)
                z = 1.0 - ((self.pressure_base/thermo.gpa_2145.GPA_2145_PRESSURE_BASE)*summation**2)
            else:
                # Unsupported
                pass
        return z

    def real_gas_dry_heating_value(self, hydrogen_sulfide):    # Btu/ft3
        z = 0.0
        ideal_ghv_dry = 0.0
        h2s_mole_fraction = 0.0
        if hydrogen_sulfide == True:
            z = self.compressibility_factor()
            ideal_ghv_dry = self.ideal_gas_dry_heating_value()
        else:
            property_package_without_h2s = PropertyPackage(self.property_package.library, [])
            for package_component in self.property_package.package_components:
                if package_component.name != "hydrogen_sulfide":
                    property_package_without_h2s.package_components.append(deepcopy(package_component))
                else:
                    h2s_mole_fraction = package_component.mole_fraction
            for package_wihtout_h2s_component in property_package_without_h2s.package_components:
                package_wihtout_h2s_component.mole_fraction *= (1.0/(1.0 - h2s_mole_fraction))
            mixture_without_h2s = Mixture(property_package_without_h2s, self.temperature_base, self.pressure_base, self.volume)
            z = mixture_without_h2s.compressibility_factor()
            ideal_ghv_dry = mixture_without_h2s.ideal_gas_dry_heating_value()
        if z > 0.0:
            return ideal_ghv_dry/z
        else:
            return 0.0

    def liquid_shrinkage_volume(self, component):  # gal
        z = self.compressibility_factor()
        gpm = 0.0
        recovered_liquid_volume = 0.0
        if z > 0:
            if component == "hexane_plus":
                for package_component in self.property_package.package_components:
                    if package_component.name in ['n_hexane', 'n_heptane', 'n_octane']:
                        gpm = 1.0/((package_component.ideal_gas_volume/settings.FT3_PER_MCF)*z)
                        recovered_liquid_volume += gpm*package_component.mole_fraction*self.volume*package_component.liquid_recovery_factor
            else:
                for package_component in self.property_package.package_components:
                    if component == package_component.name:
                        gpm = 1.0/((package_component.ideal_gas_volume/settings.FT3_PER_MCF)*z)
                        recovered_liquid_volume = gpm*package_component.mole_fraction*self.volume*package_component.liquid_recovery_factor
        return recovered_liquid_volume

    # TODO: Reduce duplication of calls to liquid_shrinkage_volume().  Need to call each of these methods 
    # independently inside spreadsheet cells, and also must ensure they are always mututally consistent

    def _gas_shrinkage_volume_of_recovered_liquid(self):  # Mcf
        z = self.compressibility_factor()
        recovered_liquid_volume = 0.0
        gas_shrinkage_volumes = {}
        for package_component in self.property_package.package_components:
            if package_component.name == "hexane_plus":
                if package_component.name in ['n_hexane', 'n_heptane', 'n_octane']:
                    recovered_liquid_volume = self.liquid_shrinkage_volume(package_component.name)
                    gas_shrinkage_volumes[package_component.name] += recovered_liquid_volume*package_component.ideal_gas_volume/settings.FT3_PER_MCF*z
            else:
                recovered_liquid_volume = self.liquid_shrinkage_volume(package_component.name)
                gas_shrinkage_volumes[package_component.name] = recovered_liquid_volume*package_component.ideal_gas_volume/settings.FT3_PER_MCF*z
        return gas_shrinkage_volumes

    def liquid_shrinkage_energy(self, component):  # MMBtu
        recovered_liquid_volume = 0.0
        recovered_liquid_energy = 0.0
        if component == "hexane_plus":
            for package_component in self.property_package.package_components:
                if package_component.name in ['n_hexane', 'n_heptane', 'n_octane']:
                    recovered_liquid_volume = self.liquid_shrinkage_volume(package_component.name)
                    recovered_liquid_energy += recovered_liquid_volume*package_component.liquid_ghv/settings.BTU_PER_MMBTU
        else:
            for package_component in self.property_package.package_components:
                if component == package_component.name:
                    recovered_liquid_volume = self.liquid_shrinkage_volume(package_component.name)
                    recovered_liquid_energy = recovered_liquid_volume*package_component.liquid_ghv/settings.BTU_PER_MMBTU
        return recovered_liquid_energy

    def plant_inlet_gas_energy(self, hydrogen_sulfide):
        inlet_gas_energy = self.volume*settings.FT3_PER_MCF*self.real_gas_dry_heating_value(True)/settings.BTU_PER_MMBTU
        if hydrogen_sulfide == False:
            for package_component in self.property_package.package_components:
                if package_component.name == 'hydrogen_sulfide':
                    inlet_gas_energy -= self.volume*package_component.mole_fraction*settings.FT3_PER_MCF*package_component.ideal_gas_ghv \
                    /(self.compressibility_factor()*settings.BTU_PER_MMBTU)
        return inlet_gas_energy

    def residue_gas_energy(self, hydrogen_sulfide):   # MMBtu
        recovered_liquid_energy = 0.0
        feed_gas_energy = self.plant_inlet_gas_energy(hydrogen_sulfide)
        for package_component in self.property_package.package_components:
            if package_component.name in ['ethane', 'propane', 'i_butane', 'n_butane', 'i_pentane', 'n_pentane', 'n_hexane', 'n_heptane', 'n_octane']:
                recovered_liquid_volume = self.liquid_shrinkage_volume(package_component.name)
                recovered_liquid_energy += recovered_liquid_volume*package_component.liquid_ghv/settings.BTU_PER_MMBTU
        residue_energy = feed_gas_energy - recovered_liquid_energy
        return residue_energy

    def _total_moles(self):  # lbmol
        z = self.compressibility_factor()
        total_moles = self.pressure_base*self.volume/(z*settings.UNIVERSAL_GAS_CONSTANT*(self.temperature_base + settings.FAHRENHEIT_TO_RANKINE))
        return total_moles

    def _component_moles(self):   # lbmol
        component_moles = {}
        total_moles = self._total_moles()
        for package_component in self.property_package.package_components:
            component_moles[package_component.name] = total_moles*package_component.mole_fraction
        return component_moles

    def _residue_gas_composition(self):
        feed_gas_total_moles = self._total_moles()
        feed_component_moles = self._component_moles()
        shrinkage_volumes = self._gas_shrinkage_volume_of_recovered_liquid()
        residue_moles = {}
        total_residue_moles = 0.0
        residue_composition = []
        for package_component in self.property_package.package_components:
            z_component = self.compressibility_factor(package_component.name)
            component_mole_shrinkage = shrinkage_volumes[package_component.name]*self.pressure_base/(z_component*settings.UNIVERSAL_GAS_CONSTANT
                *(self.temperature_base + settings.FAHRENHEIT_TO_RANKINE))
            residue_moles[package_component.name] = feed_component_moles[package_component.name] - component_mole_shrinkage
            total_residue_moles += residue_moles[package_component.name]
        for package_component in self.property_package.package_components:
            residue_mole_fraction = residue_moles[package_component.name]/total_residue_moles
            residue_composition.append((package_component.name, residue_mole_fraction, 0.0))
        return residue_composition

    def _residue_mixture(self, hydrogen_sulfide):
        residue_composition = self._residue_gas_composition()
        h2s_mole_fraction = 0.0
        property_package = PropertyPackage(self.property_package.library, [])
        for name, mole_fraction, recovery_factor in residue_composition:
            package_component = PureComponent((name, mole_fraction, recovery_factor), property_package.library)
            property_package.package_components.append(deepcopy(package_component))
            if name == "hydrogen_sulfide":
                h2s_mole_fraction = mole_fraction
                if hydrogen_sulfide == False:
                    property_package.package_components.pop()
        if hydrogen_sulfide == False:
            for package_component in property_package.package_components:
                package_component.mole_fraction *= (1.0/(1.0 - h2s_mole_fraction))
        residue_mixture = Mixture(property_package, self.temperature_base, self.pressure_base, self.residue_gas_volume())
        return residue_mixture

    def residue_compressibility_factor(self, hydrogen_sulfide=True):
        z = 0.0
        residue_mixture = self._residue_mixture(hydrogen_sulfide)
        z = residue_mixture.compressibility_factor()
        if z > 0:
            return z
        else:
            return 0.0

    def real_residue_gas_dry_heating_value(self, hydrogen_sulfide):   # Btu/ft3
        z = self.residue_compressibility_factor(hydrogen_sulfide)
        ideal_ghv_dry = self._residue_mixture(hydrogen_sulfide).ideal_gas_dry_heating_value()
        if z > 0.0:
            return ideal_ghv_dry/z
        else:
            return 0.0

    def residue_gas_volume(self, component_name="mixture"):
        gas_shrinkage_volumes = self._gas_shrinkage_volume_of_recovered_liquid()
        total_gas_shrinkage = sum(s for s in gas_shrinkage_volumes.values())
        residue_volume = self.volume - total_gas_shrinkage
        residue_composition = self._residue_gas_composition()
        for name, mole_fraction, recovery_factor in residue_composition:
            if name == component_name:
                residue_volume *= mole_fraction
        return residue_volume
