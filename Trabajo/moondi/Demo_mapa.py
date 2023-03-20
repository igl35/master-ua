#importa streamlit
import streamlit as st
#importa pandas
import pandas as pd
#parte del mapa que se va a añadir a streamlit
import folium
from folium.plugins import Search
import geopandas as gpd
from shapely.geometry import Point
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit_folium 



if st.button('Filtrar'):
    import pandas as pd
    #df = pd.read_csv(r'\Users\usuario\entorno\master-ua\Trabajo\moondi\archivo (4).csv', na_values=None)

    #ahora lo leemos desde github
    df = pd.read_csv('https://raw.githubusercontent.com/igl35/master-ua/main/Trabajo/moondi/archivo%20(4).csv', na_values=None)

    #mostramos el head del dataframe
    original_filtro_nombre = df

    #dont reload the page 
    #st.set_page_config(page_title='Restaurante', page_icon=':smile:', layout='wide', initial_sidebar_state='auto')

    # #filtro de categoria por defecto a None el selectbox
    categoria = st.selectbox('Categoría', df['Categoría'].unique())

    ciudad = st.selectbox('Ciudad', df['Ciudad'].unique())

    # #filtro de precio
    precio = st.selectbox('Precio', df['Precio_Conver'].unique())

    # #filtro de valoración
    valoracion = st.selectbox('Valoración', df['Valoración'].unique())

    #ahora añadimois un buscardor para cada filtro y lo guardamos en una variable
    # #buscador de nombre
    nombre = st.text_input('Restaurante', 'Restaurante')

    if nombre == '' or nombre == 'Restaurante':
        df = df[(df['Categoría'] == categoria) & (df['Precio_Conver'] == precio) & (df['Valoración'] == valoracion) & (df['Ciudad'] == ciudad)] #& (df['Restaurante'] == nombre)]
        refres = True
    else:
        df = original_filtro_nombre[(original_filtro_nombre['Restaurante'] == nombre)]

    st.write(df)

    #ahora añadimos el mapa

    #eliminamos las filas que tienen la longitud y latitud igual a 'None'
    df = df[df['longitude'] != 'None']
    df = df[df['latitude'] != 'None']

    mymap = folium.Map(
        location=[34.1097092,	-118.29135709054987], 
        zoom_strat=5
    )

    points = [] 
    for index, row in df.iterrows():
            try: 
                points.append(Point(float(row.longitude), float(row.latitude)))
            except: 
                points.append(None) 


    df = gpd.GeoDataFrame(df, geometry=points)

    #geoson 
    df.to_file('Restaurant.geojson', driver = 'GeoJSON')
    comunidadesGeojson = gpd.read_file('Restaurant.geojson', driver = "GeoJSON",)

    # comunidadesFolium = folium.GeoJson(
    #     comunidadesGeojson, 
    #     name = "TODAS LAS CATEGORÍAS",
    # ).add_to(mymap)

    # comunidadesearch = Search(
    #     layer = comunidadesFolium, 
    #     geom_type = "Point", 
    #     placeholder= "Buscar Restaurante", 
    #     collapsed=False, 
    #     search_label ="Restaurante",
    #     search_zoom=20,
    # ).add_to(mymap)

    features = {}
    prices = {}
    ciudades = {}

    for row in pd.unique(df["Categoría"]):
        features[row] = folium.FeatureGroup(name=row)

    for row in pd.unique(df["Precio_Conver"]):
        prices[row] = folium.FeatureGroup(name=row)

    for row in pd.unique(df["Ciudad"]):
        ciudades[row] = folium.FeatureGroup(name=row)

    for index, row in df.iterrows():
            text = f"""
            {row.Restaurante} 
            {row.Web}   

            Image Courtesy of Kyle Neiber
            
                """

            if row.Imagen != 'No disponible': 
                url = row.Imagen
            else:
                url = "https://cdn.pixabay.com/photo/2014/09/17/20/26/restaurant-449952__340.jpg"

            try: 

                link_restaurante = "<a href={}>web</a>".format(row.Web)
                htmlcode = """<div>
                <img src={} alt="Descripción" width="230" height="172">
                <br /><span>{}</span><br /><span>{}</span><br /><span>{}</span><br /><span>{}</span><br /><span>{}</span><br /><span>{}</span>
                </div>""".format(url, "<b>Restaurante: </b>" + row['Restaurante'], "<b>Web: </b>" + row.Web, "<b>Categoría: </b>" + row['Categoría'], "<b>Precio: </b>" + row.Precio_Conver, "<b>Teléfono: </b>" + str(row.Teléfono), "<b>Reseñas: </b>" + row.Reseñas.replace('reviews', ''))
                tooltip = row['Restaurante']


                folium.Marker(
                    [row['latitude'],row['longitude']], popup=htmlcode, tooltip=tooltip
                ).add_to(features[row['Categoría']])

            except: 
                continue

    for row in pd.unique(df["Categoría"]):
        features[row].add_to(mymap)

    # folium.LayerControl().add_to(mymap)

    mymap.save('my_map_search.html')

    #añadir este html a streamlit
    from streamlit_folium import st_folium, folium_static

    folium_static(mymap, width=1000, height=500)

else: 

    import pandas as pd
    #df = pd.read_csv(r'\Users\usuario\entorno\master-ua\Trabajo\moondi\archivo (4).csv', na_values=None)
    df = pd.read_csv('https://raw.githubusercontent.com/igl35/master-ua/main/Trabajo/moondi/archivo%20(4).csv', na_values=None)

    #mostramos el head del dataframe
    original_filtro_nombre = df

    #dont reload the page 
    #st.set_page_config(page_title='Restaurante', page_icon=':smile:', layout='wide', initial_sidebar_state='auto')

    # #filtro de categoria por defecto a None el selectbox
    categoria = st.selectbox('Categoría', df['Categoría'].unique())

    ciudad = st.selectbox('Ciudad', df['Ciudad'].unique())

    # #filtro de precio
    precio = st.selectbox('Precio', df['Precio_Conver'].unique())

    # #filtro de valoración
    valoracion = st.selectbox('Valoración', df['Valoración'].unique())

    #ahora añadimois un buscardor para cada filtro y lo guardamos en una variable
    # #buscador de nombre
    nombre = st.text_input('Restaurante', 'Restaurante')

    st.write(df)

    #ahora añadimos el mapa

    #eliminamos las filas que tienen la longitud y latitud igual a 'None'
    df = df[df['longitude'] != 'None']
    df = df[df['latitude'] != 'None']

    mymap = folium.Map(
        location=[34.1097092,	-118.29135709054987], 
        zoom_strat=5
    )

    points = [] 
    for index, row in df.iterrows():
            try: 
                points.append(Point(float(row.longitude), float(row.latitude)))
            except: 
                points.append(None) 


    df = gpd.GeoDataFrame(df, geometry=points)

    #geoson 
    df.to_file('Restaurant.geojson', driver = 'GeoJSON')
    comunidadesGeojson = gpd.read_file('Restaurant.geojson', driver = "GeoJSON",)

    # comunidadesFolium = folium.GeoJson(
    #     comunidadesGeojson, 
    #     name = "TODAS LAS CATEGORÍAS",
    # ).add_to(mymap)

    # comunidadesearch = Search(
    #     layer = comunidadesFolium, 
    #     geom_type = "Point", 
    #     placeholder= "Buscar Restaurante", 
    #     collapsed=False, 
    #     search_label ="Restaurante",
    #     search_zoom=20,
    # ).add_to(mymap)

    features = {}
    prices = {}
    ciudades = {}

    for row in pd.unique(df["Categoría"]):
        features[row] = folium.FeatureGroup(name=row)

    for row in pd.unique(df["Precio_Conver"]):
        prices[row] = folium.FeatureGroup(name=row)

    for row in pd.unique(df["Ciudad"]):
        ciudades[row] = folium.FeatureGroup(name=row)

    for index, row in df.iterrows():
            text = f"""
            {row.Restaurante} 
            {row.Web}   

            Image Courtesy of Kyle Neiber
            
                """

            if row.Imagen != 'No disponible': 
                url = row.Imagen
            else:
                url = "https://cdn.pixabay.com/photo/2014/09/17/20/26/restaurant-449952__340.jpg"

            try: 

                link_restaurante = "<a href={}>web</a>".format(row.Web)
                htmlcode = """<div>
                <img src={} alt="Descripción" width="230" height="172">
                <br /><span>{}</span><br /><span>{}</span><br /><span>{}</span><br /><span>{}</span><br /><span>{}</span><br /><span>{}</span>
                </div>""".format(url, "<b>Restaurante: </b>" + row['Restaurante'], "<b>Web: </b>" + row.Web, "<b>Categoría: </b>" + row['Categoría'], "<b>Precio: </b>" + row.Precio_Conver, "<b>Teléfono: </b>" + str(row.Teléfono), "<b>Reseñas: </b>" + row.Reseñas.replace('reviews', ''))
                tooltip = row['Restaurante']


                folium.Marker(
                    [row['latitude'],row['longitude']], popup=htmlcode, tooltip=tooltip
                ).add_to(features[row['Categoría']])

            except: 
                continue

    for row in pd.unique(df["Categoría"]):
        features[row].add_to(mymap)

    # folium.LayerControl().add_to(mymap)

    mymap.save('my_map_search.html')

    #añadir este html a streamlit
    from streamlit_folium import st_folium, folium_static

    folium_static(mymap, width=1000, height=500)





