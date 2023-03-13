from geopy.geocoders import Nominatim
import pandas as pd
import folium


geolocator = Nominatim(user_agent="my_application")
angeles = pd.read_csv(r'\Users\usuario\entorno\master-ua\Trabajo\moondi\Tripadvisor_Los_Angeles - Hoja 1 (1).csv', na_values = None)
#addresses = angeles['address']
addresses = angeles['Dirección']

for i, address in enumerate(addresses): 
  if address != None: 
    try: 
      location = geolocator.geocode(str(address))
      #print(location.latitude, location.longitude)
      angeles.loc[i, 'latitude'] = str(location.latitude) 
      angeles.loc[i, 'longitude'] = str(location.longitude)
    except: 
      angeles.loc[i, 'latitude'] = "None"
      angeles.loc[i, 'longitude'] = "None"

angeles.to_csv('archivo.csv')