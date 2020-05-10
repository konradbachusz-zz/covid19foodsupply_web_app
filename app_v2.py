import streamlit as st
import numpy as np 
import pandas as pd 
from PIL import Image
import streamlit as st
from bokeh.plotting import figure
import pydeck as pdk
import math
import geojson
import plotly.express as px

#Load UK Map
with open('UK.geojson') as f:
    geojson_map = geojson.load(f)

#Logo
image=Image.open("logo-new-min.png")
st.sidebar.image(image,use_column_width=True)

#Title and text
st.title("Covid19 Food Supply: Demo App")

st.markdown("The data below is fictional and purely for demonstration purposes")

#Parameters
scenario=st.sidebar.selectbox("Social Distancing Scenario",["Full lockdown","Partial lockdown","Full re-opening"])
interventions=st.sidebar.multiselect("Interventions",("Closed Airports","Closed Ports","Add another route to distribution channel","Add another route to the processing centre"))

resilience = st.sidebar.slider("Resilience %",0.0, 100.0, (25.0))
recovery = st.sidebar.slider("Recovery %",0.0, 100.0, (25.0))
food_safety_stock=st.sidebar.slider("Change food safety stock by x%",-100.0, 100.0, (0.00))

regions = st.sidebar.multiselect("Select regions",("All","Scotland","Northern Ireland","Wales",
    "North East","North West","Yorkshire and the Humber","West Midlands","East Midlands","South West", "South East", "East of England","Greater London"))

#Dataframe
df=pd.read_csv("dummy_data.csv")


#scenario filtering
if scenario=="Full lockdown":
    df=df[df.scenario_Full_lockdown==1]
elif scenario=="Partial lockdown":
    df=df[df.scenario_Partial_lockdown==1]
elif scenario=="Full re-opening":
    df=df[df.scenario_Full_reopening==1]

#regions filtering
if len(regions)>0:
    if "All" in regions:
        df=df
    else:
        df=df
        df=df[df.region.isin(regions)]


#Risk Factor
#scenario criteria
if scenario=="Full lockdown":
    df['Risk Factor']=df.intercept+df.resilience_coefficient*resilience+df.recovery_coefficient*recovery+df.food_safety_stock_coefficient*food_safety_stock
elif scenario=="Partial lockdown":
    df['Risk Factor']=df.intercept+df.resilience_coefficient*resilience+df.recovery_coefficient*recovery+df.food_safety_stock_coefficient*food_safety_stock+20
elif scenario=="Full re-opening":
    df['Risk Factor']=df.intercept+df.resilience_coefficient*resilience+df.recovery_coefficient*recovery+df.food_safety_stock_coefficient*food_safety_stock+30

#interventions criteria
if "Closed Airports" in interventions:
    df['Risk Factor']=df['Risk Factor']-5
elif "Closed Ports" in interventions:
    df['Risk Factor']=df['Risk Factor']-5
elif "Add another route to distribution channel" in interventions:
    df['Risk Factor']=df['Risk Factor']-5
elif "Add another route to the processing centre" in interventions:
    df['Risk Factor']=df['Risk Factor']-5

st.markdown("Average Risk Factor: "+str(round(df['Risk Factor'].mean(),2)))
st.markdown("Number of people impacted: "+str(round(df['Risk Factor'].mean()*98,0)))
st.markdown("Expected monetary impact: £"+str(round(df['Risk Factor'].mean()*98*9,0)))

#Bar chart
df['Resilience']=resilience
st.title("Risk Factor by region")
st.bar_chart(df.groupby('region')[['Risk Factor','Resilience']].mean(),height=550)

#Plotly choropleth
fig = px.choropleth(df, geojson=geojson_map , color="Risk Factor",
                    locations="region", featureidkey="properties.EER13NM",
                    projection="mercator"
                   )
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

#Map
st.title("\nFood Banks")
food_banks=pd.read_csv("foodbank_zw.csv")
food_banks['lat']=food_banks["Latitude"]
food_banks['lon']=food_banks["Longitude"]
food_banks=food_banks[['food_bank','lat','lon']].dropna()


midpoint = (np.average(food_banks["lat"]), np.average(food_banks["lon"]))

st.deck_gl_chart(
            viewport={
                "latitude": midpoint[0],
                "longitude":  midpoint[1],
                "zoom": 5
            },
            layers=[{
                "type": "ScatterplotLayer",
                "data": food_banks,
                "radiusScale": 100,
            "radiusMinPixels": 2,

                
            }]
        )
