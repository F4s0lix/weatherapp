import data_fetcher
import create_charts
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index() -> None:
    data_fetcher.get_localization()
    city: str = data_fetcher.CITY.upper()
    data = data_fetcher.prepare_data_to_current_hour()
    temperature_chart = create_charts.temperature()
    return render_template('index.html', city=city, weatherdata=data, units=data_fetcher.UNITS, temperature_img=temperature_chart)