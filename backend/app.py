import data_fetcher
import create_charts
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index() -> None:
    ip = request.headers.get('X-Forwarded-For', request.remote_addr) # get user API
    city = data_fetcher.get_localization(ip)[1].upper()
    data = data_fetcher.prepare_data_to_current_hour(ip)
    charts = create_charts.create_charts()
    return render_template('index.html', city=city, weatherdata=data, units=data_fetcher.UNITS, chart_images=charts)

#TODO: sites with base64 images so I can load them better