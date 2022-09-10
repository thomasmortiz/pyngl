from flask_wtf import FlaskForm
from wtforms import validators, FloatField, IntegerField, StringField
import settings

class GasStreamInputForm(FlaskForm):
    producer_name = StringField('producer_name',
        validators=[
            validators.Length(1, 80, "Please enter producer name")
        ])
    processor_name = StringField('processor_name',
        validators=[
            validators.Length(1, 80, "Please enter processor name")
        ])
    settlement_month = IntegerField('settlement_month',
        validators=[
            validators.NumberRange(1, 12, "Must be between 1 and 12")
        ])
    settlement_year = IntegerField('settlement_year',
        validators=[
            validators.NumberRange(1900, 9999, "Please enter valid year")
        ])
    methane_mole_fraction = FloatField('methane_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    methane_recovery_factor = FloatField('methane_recovery_factor', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    methane_price = FloatField('methane_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    ethane_mole_fraction = FloatField('ethane_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    ethane_recovery_factor = FloatField('ethane_recovery_factor', default=0.75, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    ethane_price = FloatField('ethane_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    propane_mole_fraction = FloatField('propane_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    propane_recovery_factor = FloatField('propane_recovery_factor', default=0.98, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    propane_price = FloatField('propane_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    i_butane_mole_fraction = FloatField('i_butane_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    i_butane_recovery_factor = FloatField('i_butane_recovery_factor', default=0.98, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    i_butane_price = FloatField('i_butane_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    n_butane_mole_fraction = FloatField('n_butane_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    n_butane_recovery_factor = FloatField('n_butane_recovery_factor', default=0.98, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    n_butane_price = FloatField('n_butane_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    i_pentane_mole_fraction = FloatField('i_pentane_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    i_pentane_recovery_factor = FloatField('i_pentane_recovery_factor', default=0.98, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    i_pentane_price = FloatField('i_pentane_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    n_pentane_mole_fraction = FloatField('n_pentane_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    n_pentane_recovery_factor = FloatField('n_pentane_recovery_factor', default=0.98, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    n_pentane_price = FloatField('n_pentane_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    hexane_plus_mole_fraction = FloatField('hexane_plus_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    hexane_plus_recovery_factor = FloatField('hexane_plus_recovery_factor', default=0.98, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    hexane_plus_price = FloatField('hexane_plus_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    carbon_dioxide_mole_fraction = FloatField('carbon_dioxide_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    carbon_dioxide_recovery_factor = FloatField('carbon_dioxide_recovery_factor', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    carbon_dioxide_price = FloatField('carbon_dioxide_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    hydrogen_sulfide_mole_fraction = FloatField('hydrogen_sulfide_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    hydrogen_sulfide_recovery_factor = FloatField('hydrogen_sulfide_recovery_factor', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    hydrogen_sulfide_price = FloatField('hydrogen_sulfide_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    oxygen_mole_fraction = FloatField('oxygen_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    oxygen_recovery_factor = FloatField('oxygen_recovery_factor', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    oxygen_price = FloatField('oxygen_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    nitrogen_mole_fraction = FloatField('nitrogen_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    nitrogen_recovery_factor = FloatField('nitrogen_recovery_factor', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    nitrogen_price = FloatField('nitrogen_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    helium_mole_fraction = FloatField('helium_mole_fraction', 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    helium_recovery_factor = FloatField('helium_recovery_factor', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    helium_price = FloatField('helium_price', default=0.0, 
        validators=[
            validators.NumberRange(0.0, 1.0, "Must be between 0.0 and 1.0")
        ])
    temperature = FloatField('temperature', default=60.0, 
        validators=[
            validators.NumberRange(-459.67 + settings.FLOAT_COMPARE_TOLERANCE, None, "Must be greater than -459.67")
        ])
    pressure = FloatField('pressure', default=14.696, 
        validators=[
            validators.NumberRange(settings.FLOAT_COMPARE_TOLERANCE, None, "Must be greater than 0.0")
        ])
    volume = FloatField('volume', 
        validators=[
            validators.NumberRange(settings.FLOAT_COMPARE_TOLERANCE, None, "Must be greater than 0.0")
        ])

class GasStreamResultsForm(FlaskForm):
    producer_name = StringField('producer_name')
    processor_name = StringField('processor_name')
    settlement_month = IntegerField('settlement_month')
    settlement_year = IntegerField('settlement_year')
    gas_volume = FloatField('gas_volume')
    gas_energy = FloatField('gas_energy')
    real_gas_heating_value = FloatField('real_gas_heating_value')
    compressibility_factor = FloatField('compressibility_factor')
    ethane_recovered_volume = FloatField('ethane_recovered_volume')
    ethane_shrink_energy = FloatField('ethane_shrink_energy')
    ethane_value = FloatField('ethane_value')
    propane_recovered_volume = FloatField('propane_recovered_volume')
    propane_shrink_energy = FloatField('propane_shrink_energy')
    propane_value = FloatField('propane_value')
    i_butane_recovered_volume = FloatField('i_butane_recovered_volume')
    i_butane_shrink_energy = FloatField('i_butane_shrink_energy')
    i_butane_value = FloatField('i_butane_value')
    n_butane_recovered_volume = FloatField('n_butane_recovered_volume')
    n_butane_shrink_energy = FloatField('n_butane_shrink_energy')
    n_butane_value = FloatField('n_butane_value')
    i_pentane_recovered_volume = FloatField('i_pentane_recovered_volume')
    i_pentane_shrink_energy = FloatField('i_pentane_shrink_energy')
    i_pentane_value = FloatField('i_pentane_value')
    n_pentane_recovered_volume = FloatField('n_pentane_recovered_volume')
    n_pentane_shrink_energy = FloatField('n_pentane_shrink_energy')
    n_pentane_value = FloatField('n_pentane_value')
    hexane_plus_recovered_volume = FloatField('hexane_plus_recovered_volume')
    hexane_plus_shrink_energy = FloatField('hexane_plus_shrink_energy')
    hexane_plus_value = FloatField('hexane_plus_value')
    residue_real_gas_heating_value = FloatField('residue_real_gas_heating_value')
    residue_gas_compressibility_factor = FloatField('residue_gas_compressibility_factor')
    residue_gas_volume = FloatField('residue_gas_volume')
    residue_gas_energy = FloatField('residue_gas_energy')
    residue_gas_value = FloatField('residue_gas_value')
