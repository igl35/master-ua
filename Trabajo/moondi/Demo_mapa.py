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
#importamos base64
import streamlit_folium 
import base64


#definimos la funcion download_link que nos va a permitir descargar el csv
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

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
    #categoria = st.selectbox('Categoría', df['Categoría'].unique())
    categoria = st.multiselect('Categoría', df['Categoría'].unique(), df['Categoría'].unique())

    #ciudad = st.selectbox('Ciudad', df['Ciudad'].unique())
    ciudad = st.multiselect('Ciudad', df['Ciudad'].unique(), df['Ciudad'].unique())

    # #filtro de precio
    #precio = st.selectbox('Precio', df['Precio_Conver'].unique())
    precio = st.multiselect('Precio', df['Precio_Conver'].unique(), df['Precio_Conver'].unique())

    # #filtro de valoración
    #valoracion = st.selectbox('Valoración', df['Valoración'].unique())

    #creamos un filtro multiselect para valoración 
    valoracion = st.multiselect('Valoración', df['Valoración'].unique(), df['Valoración'].unique())

    #A esta opción le añadimos el "todos" y ya la tratamos como podamos

    #Ahora utilizamos st.text_input para que el usuario pueda introducir el nombre del restaurante con autocompletado
    #nombre = st.text_input('Restaurante', value='', max_chars=None, key=None, type='default')
    #opciones = [df['Restaurante'].unique()] # Aquí debe definir la lista de opciones que desea mostrar en el selectbox
    opciones = list(df['Restaurante'].unique())
    opciones.insert(0, "Todos")
    nombre = st.selectbox('Restaurante', opciones, index=0)
    #Por defecto el selectbox no tiene la opción de todos, por lo que la añadimos

    if nombre == '' or nombre == 'Restaurante':
        #df = df[(df['Categoría'] == categoria) & (df['Precio_Conver'] == precio) & (df['Valoración'] == valoracion) & (df['Ciudad'] == ciudad)] #& (df['Restaurante'] == nombre)]
        df = df[(df['Categoría'].isin(categoria)) & (df['Precio_Conver'].isin(precio)) & (df['Valoración'].isin(valoracion)) & (df['Ciudad'].isin(ciudad))] #& (df['Restaurante'] == nombre)]
    if nombre != '':
        if nombre == "Todos": 
             df = df[(df['Categoría'].isin(categoria)) & (df['Precio_Conver'].isin(precio)) & (df['Valoración'].isin(valoracion)) & (df['Ciudad'].isin(ciudad))]
        else:
            df = original_filtro_nombre[(original_filtro_nombre['Restaurante'] == nombre)]

    #quitamos de df la primera columna que es el index, la columna Precio, la columna Menú, la columna Imagen, la columna latitude y la columna longitude
    df_modified = df.drop(df.columns[[0, 5, 11, 13, 14, 15]], axis=1)
    df_modified = df_modified.rename(columns={'Precio_Conver': 'Precio'})
    st.write(df_modified)

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

    folium_static(mymap, width=700, height=700)

    #añadimos un boton para descargar df_modified en formato csv o excel
    #if st.button('Descargar CSV'):
    tmp_download_link = download_link(df_modified, 'data.csv', 'Click aquí para descargar los datos!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)

    

else: 

    import pandas as pd
    df = pd.read_csv('https://raw.githubusercontent.com/igl35/master-ua/main/Trabajo/moondi/archivo%20(4).csv', na_values=None)

    #mostramos el head del dataframe
    original_filtro_nombre = df

    #dont reload the page 
    #st.set_page_config(page_title='Restaurante', page_icon=':smile:', layout='wide', initial_sidebar_state='auto')

    # #filtro de categoria por defecto a None el selectbox
    #categoria = st.selectbox('Categoría', df['Categoría'].unique())
    categoria = st.multiselect('Categoría', df['Categoría'].unique(), df['Categoría'].unique())

    #ciudad = st.selectbox('Ciudad', df['Ciudad'].unique())
    ciudad = st.multiselect('Ciudad', df['Ciudad'].unique(), df['Ciudad'].unique())
    
    # #filtro de precio
    #precio = st.selectbox('Precio', df['Precio_Conver'].unique())
    precio = st.multiselect('Precio', df['Precio_Conver'].unique(), df['Precio_Conver'].unique())

    # #filtro de valoración
    #valoracion = st.selectbox('Valoración', df['Valoración'].unique())
    valoracion = st.multiselect('Valoración', df['Valoración'].unique(), df['Valoración'].unique())

    #ahora añadimois un buscardor para cada filtro y lo guardamos en una variable
    # #buscador de nombre
    #nombre = st.text_input('Restaurante', value='', max_chars=None, key=None, type='default')
    #opciones = [df['Restaurante'].unique()] # Aquí debe definir la lista de opciones que desea mostrar en el selectbox
    #creamos la variable opciones que es una lista con el formato [ ,  ,  , ] de todos los restaurantes 
    opciones = list(df['Restaurante'].unique())
    opciones.insert(0, "Todos")
    nombre = st.selectbox('Restaurante', opciones, index=0)

    df_modified = df.drop(df.columns[[0, 5, 11, 13, 14, 15]], axis=1)
    #ahora camiamos el combre de la columna Precio_Conver por Precio
    df_modified = df_modified.rename(columns={'Precio_Conver': 'Precio'})
    st.write(df_modified)

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

    #añade el mapa centrado 
    folium_static(mymap, width=700, height=700)

    #if st.button('Descargar CSV'):
    tmp_download_link = download_link(df_modified, 'data.csv', 'Click aquí para descargar los datos!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)






