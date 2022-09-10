import json
import pdb

class PropertyPackage():

    def __init__(self, data_source):
        self.library = {}
        self.units = []
        self.compounds = []
        self.reference_state = {}
        self.compound_names = []

        property_data = {}
        try:
            with open (data_source) as properties:
                property_data = json.load(properties)
                for key in property_data:
                    if key == "library":
                        self.library = property_data[key]
                    if key == "units":
                        self.units = property_data[key]
                    elif key == "compounds":
                        self.compounds = property_data[key]
                    elif key == "reference_state":
                        self.reference_state = property_data[key]
            self._extract_compound_names()
        except Exception as e:
            pass    # Instantiates empty object

    def _extract_compound_names(self):
        for compound in self.compounds:
            self.compound_names.append(compound["name"])
        return

    @classmethod
    def serialize(cls, property_package):
        encoded_property_package = {}

    def default(self, property_package):
        if isinstance(property_package, PropertyPackage):
            encoded_property_package["library"] = property_package.library
            encoded_property_package["units"] = property_package.units
            encoded_property_package["compounds"] = property_package.compounds
            encoded_property_package["reference_state"] = property_package.reference_state
            encoded_property_package["compound_names"] = property_package.compound_names
            return json.dumps(encoded_property_package)
        return ""

    @classmethod
    def deserialize(cls, encoded_property_package_source):
        serialized_data = json.loads(encoded_property_package_source)
        compound_names = []
        compounds = []
        library = {}
        reference_state = {}
        units = []
        property_package = PropertyPackage("")
        for key in property_package_data:
            if key == "compound_names":
                compound_names = property_package_data[key]
            elif key == "compounds":
                compounds = property_package_data[key]
            elif key == "library":
                library = property_package_data[key]
            elif key == "reference_state":
                reference_state = property_package_data[key]
            elif key == "units":
                units = property_package_data[key]
        property_package.compound_names = compound_names
        property_package.compounds = compounds
        property_package.library = library
        property_package.reference_state = reference_state
        property_package.units = units
        return property_package
