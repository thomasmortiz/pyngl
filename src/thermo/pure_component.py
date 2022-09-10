import thermo.gpa_2145

class PureComponent():
    def __init__(self, component, library):
        name, mole_fraction, recovery_factor = component
        self.name = name
        self.mole_fraction = mole_fraction  # dimensionless
        self.molar_mass = 0.0   # lbm/lbmol
        self.ideal_gas_volume = 0.0   # ft3 ideal gas/gal liquid
        self.summation_factor = 0.0   # dimensionless
        self.ideal_gas_ghv = 0.0 # Btu/ft3
        self.liquid_ghv = 0.0   # Btu/gal
        self.liquid_recovery_factor = recovery_factor  # dimensionless
        if library == "GPA_2145":
            for library_component in thermo.gpa_2145.GPA_2145_PROPERTIES:
                if name == library_component["name"]:
                    self.molar_mass = library_component["molar_mass"]
                    self.ideal_gas_volume = library_component["ideal_gas_volume"]
                    self.summation_factor = library_component["summation_factor"]
                    self.ideal_gas_ghv = library_component["ideal_gas_ghv"]
                    self.liquid_ghv = library_component["liquid_ghv"]
                    break
