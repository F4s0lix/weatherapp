import data_fetcher
import create_charts
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index() -> None:
    ip = request.headers.get('X-Forwarded-For', request.remote_addr) # get user API, try to bypass proxy
    localization = data_fetcher.get_localization(ip)
    if localization[0] == False:
        city = 'CITY'
    else:
        city = localization[1]
    print(f'Error: HTML code {localization[1]}')
    data = data_fetcher.prepare_data_to_current_hour(ip)
    charts = create_charts.create_charts(ip)
    return render_template('index.html', city=city, weatherdata=data, units=data_fetcher.UNITS, chart_images=charts)

#TODO: sites with base64 images so I can load them better

@app.errorhandler(404)
def page_missing(e):
    return render_template('404.html')