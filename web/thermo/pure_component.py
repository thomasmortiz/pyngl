import json

class PureComponent():

    def __init__(self, compound):
        self.name = compound["name"]
        self.mole_fraction = compound["mole_fraction"]
        self.molar_mass = compound["molar_mass"]
        self.ideal_gas_volume = compound["ideal_gas_volume"]
        self.summation_factor = compound["summation_factor"]
        self.liquid_ghv = compound["liquid_ghv"]
        self.ideal_gas_ghv = compound["ideal_gas_ghv"]

    @classmethod
    def serialize(cls, component):
        encoded_component = {}
        if isinstance(component, PureComponent):
            encoded_component["name"] = component.name
            encoded_component["mole_fraction"] = component.mole_fraction
            encoded_component["molar_mass"] = component.molar_mass
            encoded_component["ideal_gas_volume"] = component.ideal_gas_volume
            encoded_component["summation_factor"] = component.summation_factor
            encoded_component["liquid_ghv"] = component.liquid_ghv
            encoded_component["ideal_gas_ghv"] = component.ideal_gas_ghv
            return json.dumps(encoded_component)
        return ""

    @classmethod
    def deserialize(cls, encoded_component_source):
        serialized_data = json.loads(encoded_component_source)
        name = ""
        mole_fraction = 0.0
        molar_mass = 0.0
        ideal_gas_volume = 0.0
        summation_factor = 0.0
        liquid_ghv = 0.0
        ideal_gas_ghv = 0.0
        component = PureComponent({})
        for key in property_package_data:
            if key == "name":
                name = serialized_data[key]
            elif key == "mole_fraction":
                mole_fraction = serialized_data[key]
            elif key == "molar_mass":
                molar_mass = serialized_data[key]
            elif key == "ideal_gas_volume":
                ideal_gas_volume = serialized_data[key]
            elif key == "summation_factor":
                summation_factor = serialized_data[key]
            elif key == "liquid_ghv":
                liquid_ghv = serialized_data[key]
            elif key == "ideal_gas_ghv":
                ideal_gas_ghv = serialized_data[key]
        component.name = name
        component.mole_fraction = mole_fraction
        component.molar_mass = molar_mass
        component.ideal_gas_volume = ideal_gas_volume
        component.summation_factor = summation_factor
        component.liquid_ghv = liquid_ghv
        component.ideal_gas_ghv = ideal_gas_ghv
        return component
