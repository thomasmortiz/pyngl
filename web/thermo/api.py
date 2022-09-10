from flask import render_template, redirect, session, url_for, request
from flask.views import MethodView
import json
import re
import pdb

from thermo.material_stream import MaterialStream
from thermo.form import GasStreamInputForm, GasStreamResultsForm
from thermo.property_package import PropertyPackage
from thermo.models import RawGasStream, FractionatedStream
import settings

class GasStreamInputAPI(MethodView):
    def get(self, raw_gas_stream):
        # TODO: Retrieve from database to recalculate results
        producer_name = db.StringField()
        processor_name = db.StringField()
        settlement_month = db.IntField()
        settlement_year = db.IntField()
        methane_mole_fraction = db.FloatField()
        ethane_mole_fraction = db.FloatField()
        propane_mole_fraction = db.FloatField()
        n_butane_mole_fraction = db.FloatField()
        i_butane_mole_fraction = db.FloatField()
        n_pentane_mole_fraction = db.FloatField()
        i_pentane_mole_fraction = db.FloatField()
        hexane_plus_mole_fraction = db.FloatField()
        carbon_dioxide_mole_fraction = db.FloatField()
        hydrogen_sulfide_mole_fraction = db.FloatField()
        nitrogen_mole_fraction = db.FloatField()
        oxygen_mole_fraction = db.FloatField()
        helium_mole_fraction = db.FloatField()
        methane_recovery_factor = db.FloatField()
        ethane_recovery_factor = db.FloatField()
        propane_recovery_factor = db.FloatField()
        n_butane_recovery_factor = db.FloatField()
        i_butane_recovery_factor = db.FloatField()
        n_pentane_recovery_factor = db.FloatField()
        i_pentane_recovery_factor = db.FloatField()
        hexane_plus_recovery_factor = db.FloatField()
        carbon_dioxide_recovery_factor = db.FloatField()
        hydrogen_sulfide_recovery_factor = db.FloatField()
        nitrogen_recovery_factor = db.FloatField()
        oxygen_recovery_factor = db.FloatField()
        helium_recovery_factor = db.FloatField()
        methane_price = db.FloatField()
        ethane_price = db.FloatField()
        propane_price = db.FloatField()
        n_butane_price = db.FloatField()
        i_butane_price = db.FloatField()
        n_pentane_price = db.FloatField()
        i_pentane_price = db.FloatField()
        hexane_plus_price = db.FloatField()
        carbon_dioxide_price = db.FloatField()
        hydrogen_sulfide_price = db.FloatField()
        nitrogen_price = db.FloatField()
        oxygen_price = db.FloatField()
        helium_price = db.FloatField()
        temperature = db.FloatField()
        pressure = db.FloatField()
        volume = db.FloatField()
        timestamp = db.DateTimeField()

        if raw_gas_stream:
            # Query database (by producer name, processor_name, settlement_month, settlement_year)
            input_data_as_json_string = session["gas_stream"]
            material_stream = MaterialStream.deserialize(str(input_data_as_json_string))
            hexane_plus_mole_fraction = 0.0
            for component in material_stream.components:
                if component.name == "methane":
                    form.methane_mole_fraction.data = component.mole_fraction
                    form.methane_recovery_factor.data = material_stream.recovery_factors["methane"]
                elif component.name == "ethane":
                    form.ethane_mole_fraction.data = component.mole_fraction
                    form.ethane_recovery_factor.data = material_stream.recovery_factors["ethane"]
                elif component.name == "propane":
                    form.propane_mole_fraction.data = component.mole_fraction
                    form.propane_recovery_factor.data = material_stream.recovery_factors["propane"]
                elif component.name == "i_butane":
                    form.i_butane_mole_fraction.data = component.mole_fraction
                    form.i_butane_recovery_factor.data = material_stream.recovery_factors["i_butane"]
                elif component.name == "n_butane":
                    form.n_butane_mole_fraction.data = component.mole_fraction
                    form.n_butane_recovery_factor.data = material_stream.recovery_factors["n_butane"]
                elif component.name == "i_pentane":
                    form.i_pentane_mole_fraction.data = component.mole_fraction
                    form.i_pentane_recovery_factor.data = material_stream.recovery_factors["i_pentane"]
                elif component.name == "n_pentane":
                    form.n_pentane_mole_fraction.data = component.mole_fraction
                    form.n_pentane_recovery_factor.data = material_stream.recovery_factors["n_pentane"]
                elif component.name == "n_hexane":
                    hexane_plus_mole_fraction += component.mole_fraction
                    form.hexane_plus_recovery_factor.data = material_stream.recovery_factors["n_hexane"]
                elif component.name == "n_heptane":
                    hexane_plus_mole_fraction += component.mole_fraction
                elif component.name == "n_octane":
                    hexane_plus_mole_fraction += component.mole_fraction
                elif component.name == "carbon_dioxide":
                    form.carbon_dioxide_mole_fraction.data = component.mole_fraction
                    form.carbon_dioxide_recovery_factor.data = material_stream.recovery_factors["carbon_dioxide"]
                elif component.name == "hydrogen_sulfide":
                    form.hydrogen_sulfide_mole_fraction.data = component.mole_fraction
                    form.hydrogen_sulfide_recovery_factor.data = material_stream.recovery_factors["hydrogen_sulfide"]
                elif component.name == "oxygen":
                    form.oxygen_mole_fraction.data = component.mole_fraction
                    form.oxygen_recovery_factor.data = material_stream.recovery_factors["oxygen"]
                elif component.name == "nitrogen":
                    form.nitrogen_mole_fraction.data = component.mole_fraction
                    form.nitrogen_recovery_factor.data = material_stream.recovery_factors["nitrogen"]
                elif component.name == "helium":
                    form.helium_mole_fraction.data = component.mole_fraction
                    form.helium_recovery_factor.data = material_stream.recovery_factors["helium"]
            form.hexane_plus_mole_fraction.data = hexane_plus_mole_fraction
            form.pressure.data = material_stream.pressure
            form.temperature.data = material_stream.temperature
            form.volume.data = material_stream.volume
        return

    def post(self):
        form = GasStreamInputForm()
        error = None
        pressure = 0.0
        temperature = 0.0
        composition = {}
        volume = 0.0
        data_source = settings.FLUID_PROPERTY_DATA_SOURCE
        recovery_factors = {}
        input_data_as_json_string = ""

        elif form.is_submitted() == True:
            name = ""
            for key in form.data:
                match_mole_fraction = re.search(r'(\D.+)_mole_fraction', key)
                match_recovery_factor = re.search(r'(\D.+)_recovery_factor', key)
                if match_mole_fraction:
                    name = match_mole_fraction.group(1)
                elif match_recovery_factor:
                    name = match_recovery_factor.group(1)
                if key == 'pressure':
                    pressure = form.data[key]
                elif key == 'temperature':
                    temperature = form.data[key]
                elif key == 'volume':
                    volume = form.data[key]
                elif match_mole_fraction:
                    # filter out entries that are not valid compounds
                    property_package = PropertyPackage(data_source)
                    if name in property_package.compound_names:
                        composition[name] = form.data[key]
                    elif name == "hexane_plus":
                        # Assume 60/30/10 n_hexane, n_heptane, n_octane split
                        # Gas Processors Association Standard 2261, “Analysis for Natural Gas and Similar 
                        # Gaseous Mixtures by Gas Chromatography,” 2000.
                        if property_package.library["name"] == "GPA_2145":
                            composition['n_hexane'] = settings.HEXANE_PLUS_N_HEXANE_FRACTION*form.data[key]
                            composition['n_heptane'] = settings.HEXANE_PLUS_N_HEPTANE_FRACTION*form.data[key]
                            composition['n_octane'] = settings.HEXANE_PLUS_N_OCTANE_FRACTION*form.data[key]
                elif match_recovery_factor:
                    property_package = PropertyPackage(data_source)
                    if name in property_package.compound_names:
                        recovery_factors[name] = form.data[key]
                    elif name == "hexane_plus":
                        if property_package.library["name"] == "GPA_2145":
                            recovery_factors['n_hexane'] = form.data[key]
                            recovery_factors['n_heptane'] = form.data[key]
                            recovery_factors['n_octane'] = form.data[key]
            mole_fraction_sum = 0.0
            for compound in composition:
                mole_fraction_sum += composition[compound]
            if abs(mole_fraction_sum - 1.0) > settings.FLOAT_COMPARE_TOLERANCE:
                return render_template('thermo/gas_stream_input.html', form=form, error=error)
            gas_stream = MaterialStream(pressure, temperature, composition, volume, data_source, recovery_factors)
            input_data_as_json_string = MaterialStream.serialize(gas_stream)
            # TODO Add pricing input data (manual or else automatic from free Quandl stream)
            # Add input data to session as cookie
            session["gas_stream"] = input_data_as_json_string
            if form.validate() == True:
                return redirect('/results')
            else:
                return render_template('thermo/gas_stream_input.html', form=form, error=error)
        return render_template('thermo/gas_stream_input.html', form=form, error=error)


class FractionationAPI(MethodView):
    def get(self):
        form = GasStreamResultsForm()
        error = None
        input_data_as_json_string = session["gas_stream"]
        material_stream = MaterialStream.deserialize(str(input_data_as_json_string))
        # Calculate results
        z = material_stream.compressibility_factor()
        form.compressibility_factor.data = z
        real_heating_value = material_stream.real_gas_heating_value()
        form.real_gas_heating_value.data = real_heating_value
        recovered_liquids = material_stream.recover_liquid_volumes()
        hexane_plus_volume = 0.0
        for key in recovered_liquids.keys():
            if key == 'ethane':
                form.ethane_recovered_volume.data = recovered_liquids[key]
            elif key == 'propane':
                form.propane_recovered_volume.data = recovered_liquids[key]
            elif key == 'i_butane':
                form.i_butane_recovered_volume.data = recovered_liquids[key]
            elif key == 'n_butane':
                form.n_butane_recovered_volume.data = recovered_liquids[key]
            elif key == 'i_pentane':
                form.i_pentane_recovered_volume.data = recovered_liquids[key]
            elif key == 'n_pentane':
                form.n_pentane_recovered_volume.data = recovered_liquids[key]
            elif key == 'n_hexane':
                hexane_plus_volume += recovered_liquids[key]
            elif key == 'n_heptane':
                hexane_plus_volume += recovered_liquids[key]
            elif key == 'n_octane':
                hexane_plus_volume += recovered_liquids[key]
        form.hexane_plus_recovered_volume.data = hexane_plus_volume
        residue_z = material_stream.residue_gas_compressibility_factor()
        form.residue_gas_compressibility_factor.data = residue_z
        residue_real_heating_value = material_stream.residue_real_gas_heating_value()
        form.residue_real_gas_heating_value.data = residue_real_heating_value
        residue_gas_volume = material_stream.residue_gas_volume()
        form.residue_gas_volume.data = residue_gas_volume
        residue_gas_energy = material_stream.residue_gas_energy()
        form.residue_gas_energy.data = residue_gas_energy
        # TODO Add valuation results ($)
        if form.validate_on_submit():
            return redirect('/input')
        return render_template('thermo/gas_stream_results.html', form=form, error=error)
