import data_fetcher
import create_charts
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index() -> None:
    data_fetcher.get_localization()
    city: str = data_fetcher.CITY.upper()
    data = data_fetcher.prepare_data_to_current_hour()
    print(data_fetcher.UNITS)
    return render_template('index.html', city=city, weatherdata=data, units=data_fetcher.UNITS)