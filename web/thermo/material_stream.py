from thermo.property_package import PropertyPackage
from thermo.pure_component import PureComponent
from copy import deepcopy
import json
import settings
import pdb

class MaterialStream():

    def __init__(self, pressure, temperature, composition, volume, data_source, recovery_factors):
        self.pressure = pressure    # psia
        self.temperature = temperature  # F
        self.composition = composition
        self.volume = volume    # Mcf
        self.data_source = data_source
        self.recovery_factors = recovery_factors
        self.property_package = None
        self.components = []
        self._set_property_package()
        self._set_components()

    def _set_property_package(self):
        self.property_package = PropertyPackage(self.data_source)
        return

    def _set_components(self):
        component = None
        for name, mole_fraction in list(zip(self.composition.keys(), self.composition.values())):
            for package_compound in self.property_package.compounds:
                if name == package_compound["name"]:
                    feed_compound = dict(package_compound)
                    feed_compound["mole_fraction"] = mole_fraction
                    component = PureComponent(deepcopy(feed_compound))
                    self.components.append(component)
        return

    def compressibility_factor(self):
        if abs(self.temperature - self.property_package.reference_state["temperature"]) < settings.FLOAT_COMPARE_TOLERANCE \
            and self.property_package.library["name"] == "GPA_2145":
                summation = 0.0
                for component in self.components:
                    if component.summation_factor and component.mole_fraction:
                        summation += component.summation_factor*component.mole_fraction
                z = 1.0 - ((self.pressure/self.property_package.reference_state["pressure"])*summation**2)
        else:
            z = 0.0 # TODO: Implement Lee-Kesler method for this case
        return z

    def _ideal_gas_heating_value(self):
        heating_value = 0.0
        for component in self.components:
            if component.ideal_gas_ghv and component.mole_fraction:
                heating_value += (component.ideal_gas_ghv*component.mole_fraction)
        # Correct for difference in pressure base.  Neglects difference in compressibility factor, but OK for small pressure changes
        heating_value *= (self.pressure/self.property_package.reference_state["pressure"])
        return heating_value

    def real_gas_heating_value(self):
        heating_value = self._ideal_gas_heating_value()
        z = self.compressibility_factor()
        if z > 0:
            return (heating_value/z)
        return 0.0

    def recover_liquid_volumes(self):
        recovered_liquid_volumes = {}
        z = self.compressibility_factor()
        for component in self.components:
            recovered_liquid_volumes[component.name] = self.recovery_factors[component.name]*self.volume*settings.FT3_PER_MCF \
            *component.mole_fraction/(z*component.ideal_gas_volume)
        return recovered_liquid_volumes

    def liquid_shrink_energy(self):
        return

    def _residue_composition(self):
        return

    def residue_gas_compressibility_factor(self):
        residue_composition = self._residue_composition()
        return

    def residue_real_gas_heating_value(self):
        residue_composition = self._residue_composition()
        return

    def residue_gas_volume(self):
        return

    def residue_gas_energy(self):
        return

    @classmethod
    def serialize(cls, material_stream):
        encoded_material_stream = {}
        if isinstance(material_stream, MaterialStream):
            encoded_material_stream["pressure"] = material_stream.pressure
            encoded_material_stream["temperature"] = material_stream.temperature
            encoded_material_stream["composition"] = material_stream.composition
            encoded_material_stream["volume"] = material_stream.volume
            encoded_material_stream["data_source"] = material_stream.data_source
            encoded_material_stream["recovery_factors"] = material_stream.recovery_factors
            encoded_material_stream["property_package"] = PropertyPackage.serialize(material_stream.property_package)
            encoded_components = []
            for component in material_stream.components:
                encoded_components.append(PureComponent.serialize(component))
            encoded_material_stream["components"] = encoded_components
            return json.dumps(encoded_material_stream)
        return ""

    @classmethod
    def deserialize(cls, encoded_material_stream_source):
        serialized_data = json.loads(encoded_material_stream_source)
        components = []
        composition = {}
        data_source = ""
        recovery_factors = {}
        pressure = 0.0
        temperature = 0.0
        volume = 0.0
        material_stream = MaterialStream(0.0, 0.0, {}, 0.0, "", {})
        for key in serialized_data:
            if key == "components":
                components = serialized_data[key]
            elif key == "composition":
                composition = serialized_data[key]
            elif key == "data_source":
                data_source = serialized_data[key]
            elif key == "recovery_factors":
                recovery_factors = serialized_data[key]
            elif key == "pressure":
                pressure = serialized_data[key]
            elif key == "temperature":
                temperature = serialized_data[key]
            elif key == "volume":
                volume = serialized_data[key]
        material_stream.pressure = pressure
        material_stream.temperature = temperature
        material_stream.composition = composition
        material_stream.volume = volume
        material_stream.data_source = data_source
        material_stream.recovery_factors = recovery_factors
        material_stream._set_property_package()
        material_stream._set_components()
        return material_stream
