import pandas as pd
import matplotlib.pyplot as mpl
import data_fetcher
import io
import base64

#DATA: dict = data_fetcher.prepare_data_to_current_hour()
#DATA['time'] = [x.split('T')[1] for x in DATA['time']]
#mpl.style.use('dark_background')
#
#def temperature() -> str:
#    df = pd.DataFrame(DATA)
#    mpl.plot(df['time'], df['temperature_2m'])
#    buffer = io.BytesIO()
#    mpl.savefig(buffer, format='png')
#    buffer.seek(0)
#    img = base64.b64encode(buffer.read()).decode('utf-8')
#    return img
