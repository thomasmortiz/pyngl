import settings
import pdb

class UnitConverter():
    @classmethod
    def convert_pressure(cls, value, source, target):
        pressure = value
        if source in ["psia"]:
            if target == "Pa" and source == "psia":
                pressure = value*settings.PSIA_TO_PA 
            else:
                raise NotImplementedError("Unit conversion from {1} to {2} unsupported".format(source, target))
        else:
            raise NotImplementedError("Unit conversion from {1} to {2} unsupported".format(source, target))
        return pressure

    @classmethod
    def convert_temperature(cls, value, source, target):
        temperature = value
        if source in ["F"]:
            if target == "K" and source == "F":
                temperature = ((value - 32.0)*5.0/9.0) + settings.CELSIUS_TO_KELVIN
            else:
                raise NotImplementedError("Unit conversion from {1} to {2} unsupported".format(source, target))
        else:
            raise NotImplementedError("Unit conversion from {1} to {2} unsupported".format(source, target))
        return temperature

    @classmethod
    def convert_volume(cls, value, source, target):
        volume = value
        if source in ["m3", "bbl", "ft3"]:
            if target == "Mcf" and source == "m3":
                volume = value*settings.M3_TO_MCF
            elif target == "m3" and source == "bbl":
                volume = value/settings.M3_TO_BBL
            elif target == "bbl" and source == "m3":
                volume = value*settings.M3_TO_BBL
            elif target == "ft3" and source == "bbl":
                volume = value/settings.FT3_TO_BBL
            elif target == "bbl" and source == "ft3":
                volume = value*settings.FT3_TO_BBL
            else:
                raise NotImplementedError("Unit conversion from {1} to {2} unsupported".format(source, target))
        else:
            raise NotImplementedError("Unit conversion from {1} to {2} unsupported".format(source, target))
        return volume

    @classmethod
    def convert_volume_to_standard_conditions(cls, value, source, target, pressure, temperature, standard_pressure, standard_temperature):
        standard_volume = value
        if source in ["m3", "bbl", "ft3"]:
            if target == "Mcf" and source == "m3":
                volume = UnitConverter.convert_volume(value, source, target)
                standard_volume = volume*(pressure/standard_pressure)*(standard_temperature/temperature)
                # pdb.set_trace()
            else:
                raise NotImplementedError("Unit conversion from {1} to standard {2} unsupported".format(source, target))
        else:
            raise NotImplementedError("Unit conversion from {1} to standard {2} unsupported".format(source, target))
        return standard_volume

    @classmethod
    def convert_density(cls, value, source, target):
        density = value
        if source in ["api_gravity"]:
            if target == "specific_gravity" and source == "api_gravity":
                density = 141.5/(value + 131.5)
            elif target == "lbm/ft3" and source == "api_gravity":
                density = (141.5/(value + 131.5))*settings.REFERENCE_DENSITY_OF_WATER
            elif target == "kg/m3" and source == "api_gravity":
                density = (141.5/(value + 131.5))*settings.REFERENCE_DENSITY_OF_WATER/settings.KG_PER_M3_TO_LBM_PER_FT3
            else:
                raise NotImplementedError("Unit conversion from {1} to {2} unsupported".format(source, target))
        elif source in ["lbm/ft3"]:
            if target == "kg/m3" and source == "lbm/ft3":
                density = value/settings.KG_PER_M3_TO_LBM_PER_FT3
            else:
                raise NotImplementedError("Unit conversion from {1} to {2} unsupported".format(source, target))
        else:
            raise NotImplementedError("Unit conversion from {1} to {2} unsupported".format(source, target))
        return density

    @classmethod
    def convert_viscosity(cls, value, source, target):
        viscosity = value
        if source in ["ft2/s"]:
            if target == "m2/s" and source == "ft2/s":
                viscosity = value*settings.FT2_PER_S_TO_M2_PER_S
            else:
                raise NotImplementedError("Unit conversion from {1} to {2} unsupported".format(source, target))
        else:
            raise NotImplementedError("Unit conversion from {1} to {2} unsupported".format(source, target))
        return viscosity
