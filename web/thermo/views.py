from flask import Blueprint

from thermo.api import GasStreamInputAPI, FractionationAPI

thermo_app = Blueprint('thermo_app', __name__)

gas_stream_input_view = GasStreamInputAPI.as_view('gas_stream_input_api')
thermo_app.add_url_rule('/input', view_func=gas_stream_input_view, methods=['GET','POST'])
fractionation_results_view = FractionationAPI.as_view('gas_stream_results_api')
thermo_app.add_url_rule('/results', view_func=fractionation_results_view, methods=['GET'])
