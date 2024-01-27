import data_fetcher
import data_validator
import create_charts
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index() -> None:
    data_fetcher.get_localization()
    city: str = data_fetcher.CITY.upper()
    data = data_fetcher.prepare_data_to_current_hour()
    temperature = data_validator.get_userfriendly_data(data['time'], data['temperature_2m'], data_fetcher.UNITS['temperature_2m'])
    
    return render_template('index.html', city=city, temp_data=temperature, units=data_fetcher.UNITS)