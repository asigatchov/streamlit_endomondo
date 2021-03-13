import glob
import json
import pandas as pd
import streamlit as st
import numpy as np
from streamlit_folium import folium_static
import folium
import altair as alt

st.set_page_config(layout="wide")

st.sidebar.title('Endomondo workout')

# endomondo/Workouts/2013-05-04 03:57:07.0.json
# endomondo/Workouts/2013-05-07 10:07:41.0.json
# endomondo/Workouts/2013-07-06 06:47:14.0.json
# endomondo/Workouts/2013-05-18 07:13:52.0.json


JSON_DIR = 'endomondo/Workouts/'
files = sorted(glob.glob(F"{JSON_DIR}*.json"))
option= st.sidebar.selectbox('активность', files)
st.sidebar.write('You selected:', option)


FILE=option
f = open(FILE,  encoding="utf-8").read()
res = json.loads(f)
points = res[-1]['points']

data = []
for row in points:
    line = {}
    for col in row: 
        for el in col:
            if el == 'location':
                for i in col[el]:
                    line['latitude'] = i[0]['latitude']
                    line['longitude'] = i[1]['longitude']
            else:
                line[el] = col[el]
    data.append(line)
data = pd.DataFrame(data).dropna()
st.write(data)




points = data[['latitude', 'longitude']].to_numpy()
midpoint = [np.average(data["latitude"]), np.average(data["longitude"])]
m = folium.Map(location=midpoint, zoom_start=14)
folium.PolyLine(points, color='red', weight=4.5, opacity=.5).add_to(m)


row1_1, row1_2 = st.beta_columns((1, 1  ))
with row1_1:
    folium_static(m)
    

with row1_2:
    c = alt.Chart(data).mark_area().encode(x="distance_km:Q",y="speed_kmh:Q")
    st.altair_chart(c, use_container_width=True)

    c = alt.Chart(data).mark_area().encode(x="distance_km:Q", y="altitude:Q")
    st.altair_chart(c, use_container_width=True)


