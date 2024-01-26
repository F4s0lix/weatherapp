import data_fetcher
import create_charts
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index() -> None:
    data_fetcher.get_localization()
    city: str = data_fetcher.CITY.upper()
    return render_template('index.html', city=city)