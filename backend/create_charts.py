import pandas as pd
import matplotlib.pyplot as mpl
import data_fetcher
import io
import base64

mpl.style.use('Solarize_Light2')

chart_data: list = [
    'temperature_2m', 
    'precipitation_probability', 
    'surface_pressure', 
#    'wind_speed_10m', NOTE: may be user in future
]
#its easier to just store titles in dict
chart_title: dict = {
    'temperature_2m': 'temperature', 
    'precipitation_probability': 'precipitation', 
    'surface_pressure': 'pressure', 
#    'wind_speed_10m': 'wind speed', NOTE: may be used in future
}

def create_charts() -> str:
    """function creates base64 images with temperature, precipitation, pressure and wind speed charts"""
    DATA: dict = data_fetcher.prepare_data_to_current_hour()
    chart_images: dict = {}
    df = pd.DataFrame(DATA)
    for chart in chart_data:
        _, ax = mpl.subplots()
        #creating chart
        ax.plot(df['time'], df[chart], marker='o', linestyle='-')
        ax.set_xticks(DATA['time'][::8]) # date labels every 8 hours
        ax.set_title(chart_title[chart])
        ax.set_ylabel(data_fetcher.UNITS[chart], rotation=0) # y label horizontal
        ax.set_xlabel('date')

        #saving image as base64
        buffer = io.BytesIO()
        mpl.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        chart_images[chart] = base64.b64encode(buffer.read()).decode('utf-8') 
    return chart_images