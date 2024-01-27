import pandas as pd
import matplotlib.pyplot as mpl
import data_fetcher
import io
import base64

DATA: dict = data_fetcher.prepare_data_to_current_hour()
mpl.style.use('Solarize_Light2')

def temperature() -> str:
    """function return base64 image with temperature chart"""
    df = pd.DataFrame(DATA)
    _, ax = mpl.subplots()

    #creating chart
    ax.plot(df['time'], df['temperature_2m'], marker='o', linestyle='-')
    ax.set_xticks(DATA['time'][::8])
    ax.set_title('temperature')
    ax.set_ylabel(data_fetcher.UNITS['temperature_2m'], rotation=0)
    ax.set_xlabel('date')

    #saving image as base64
    buffer = io.BytesIO()
    mpl.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    img = base64.b64encode(buffer.read()).decode('utf-8')
    return img