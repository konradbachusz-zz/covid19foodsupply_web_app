import streamlit as st
import numpy as np 
import pandas as pd 
from PIL import Image
import streamlit as st
from bokeh.plotting import figure
import pydeck as pdk

#Logo
image=Image.open('logo-new-min.png')
st.sidebar.image(image,use_column_width=True)
st.title("Covid19 Food Supply: Demo App")

st.markdown("The data below is fictional and purely for demonstration purposes")

scenario=st.sidebar.selectbox("Social Distancing Measures",['Yes','No'])

airports_closed=st.sidebar.selectbox("Closed Airports",['No','Yes'])

county = st.sidebar.multiselect("Counties",('Oxfordshire', 'Berkshire', 'Wiltshire'))

#Map
st.markdown("\nReported Infections")
df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [51.5074, 0.1278],columns=['lat', 'lon'])
st.map(df)

#Map2
st.markdown("Food Shortage")
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [51.5074, 0.1278],
    columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=51.5074,
         longitude=0.1278,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
 ))

#Infections Chart
if scenario=="No" and airports_closed=="No":
    x = np.linspace(0, 3, 100)
    y = np.exp(x)
    p = figure(title='Number of infections',x_axis_label='Years since 1st infection',y_axis_label='Number of Infections')
    p.line(x, y, legend='Trend', line_width=2)
    st.bokeh_chart(p, use_container_width=True)
elif scenario=="Yes" and airports_closed=="No":
    x = np.linspace(0, 3, 100)
    y = x*2
    p = figure(title='Number of infections',x_axis_label='Years since 1st infection',y_axis_label='Number of Infections')
    p.line(x, y, legend='Trend', line_width=2)
    st.bokeh_chart(p, use_container_width=True)

elif scenario=="Yes" and airports_closed=="Yes":
    x = np.linspace(0, 3, 100)
    y = -np.exp(-x)
    p = figure(title='Number of infections',x_axis_label='Years since 1st infection',y_axis_label='Number of Infections')
    p.line(x, y, legend='Trend', line_width=2)
    st.bokeh_chart(p, use_container_width=True)