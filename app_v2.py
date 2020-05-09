import streamlit as st
import numpy as np 
import pandas as pd 
from PIL import Image
import streamlit as st
from bokeh.plotting import figure
import pydeck as pdk

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
#st.markdown(df.columns)

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
#st.dataframe(df)

#Risk Factor
if scenario=="Full lockdown":
    df['Risk Factor']=df.intercept+df.resilience_coefficient*resilience+df.recovery_coefficient*recovery+df.food_safety_stock_coefficient*food_safety_stock-10
elif scenario=="Partial lockdown":
    df['Risk Factor']=df.intercept+df.resilience_coefficient*resilience+df.recovery_coefficient*recovery+df.food_safety_stock_coefficient*food_safety_stock+20
elif scenario=="Full re-opening":
    df['Risk Factor']=df.intercept+df.resilience_coefficient*resilience+df.recovery_coefficient*recovery+df.food_safety_stock_coefficient*food_safety_stock+30

st.markdown("Average Risk Factor: "+str(round(df['Risk Factor'].mean(),2)))

#Bar chart
df['Resilience']=resilience
st.bar_chart(df.groupby('region')[['Risk Factor','Resilience']].mean(),height=550)



#Infections Chart
if scenario=="No" and airports_closed=="No":
    x = np.linspace(0, 3, 100)
    y = np.exp(x)
    p = figure(title="Food Shortage per household in 1000s kcal",x_axis_label="Years since 1st infection",y_axis_label="Food Shortage per household in 1000s kcal")
    p.line(x, y, legend="Trend", line_width=2)
    st.bokeh_chart(p, use_container_width=True)
elif scenario=="Yes" and airports_closed=="No": 
    x = np.linspace(0, 3, 100)
    y = x*2
    p = figure(title="Food Shortage per household in 1000s kcal",x_axis_label="Years since 1st infection",y_axis_label="Food Shortage per household in 1000s kcal")
    p.line(x, y, legend="Trend", line_width=2)
    st.bokeh_chart(p, use_container_width=True)

elif scenario=="Yes" and airports_closed=="Yes":
    x = np.linspace(0, 3, 100)
    y = -np.exp(-x)
    p = figure(title="Food Shortage per household in 1000s kcal",x_axis_label="Years since 1st infection",y_axis_label="Food Shortage per household in 1000s kcal")
    p.line(x, y, legend="Trend", line_width=2)
    st.bokeh_chart(p, use_container_width=True)
#test map

#Map
st.markdown("\nFood Banks and Supermarkets")
cities=pd.read_csv("cities.csv")
#st.map(cities[['lat','lon']]) #simple map

midpoint = (np.average(cities["lat"]), np.average(cities["lon"]))

st.deck_gl_chart(
            viewport={
                "latitude": midpoint[0],
                "longitude":  midpoint[1],
                "zoom": 4
            },
            layers=[{
                "type": "ScatterplotLayer",
                "data": cities,
                "radiusScale": 250,
   "radiusMinPixels": 5
                
            }]
        )


#Map2
st.markdown("Food Shortage")
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [51.5074, 0.1278],
    columns=["lat", "lon"])

st.pydeck_chart(pdk.Deck(
     map_style="mapbox://styles/mapbox/light-v9",
     initial_view_state=pdk.ViewState(
         latitude=51.5074,
         longitude=0.1278,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            "HexagonLayer",
            data=df,
            get_position="[lon, lat]",
            auto_highlight=True,
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
            coverage=1
         ),
         pdk.Layer(
             "ScatterplotLayer",
             data=df,
             get_position="[lon, lat]",
             get_color="[200, 30, 0, 160]",
             get_radius=200,
         ),
     ],
 ))





