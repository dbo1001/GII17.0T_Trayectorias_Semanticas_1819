# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 22:17:45 2019

@author: Hector
"""

import requests
from time import time

def getNominatimIdOSM(lat,lon,zoom=18):
    # Creamos la petición HTTP con GET:
    r = requests.get("http://10.0.0.10/nominatim/reverse.php?format=geojson&lat="+str(lat)+"&lon="+str(lon)+"&zoom="+str(zoom)+"&accept-language=es-es&addressdetails=0")
    # Imprimimos el resultado si el código de estado HTTP es 200 (OK):
    try:
        if r.status_code == 200:
            return(r.json()['features'][0]['properties']['osm_id'])
    except:
        return -1

def getNominatimIdJson(lat,lon,zoom=18):
    # Creamos la petición HTTP con GET:
    r = requests.get("http://10.0.0.10/nominatim/reverse.php?format=geojson&lat="+str(lat)+"&lon="+str(lon)+"&zoom="+str(zoom)+"&accept-language=es-es")
    # Imprimimos el resultado si el código de estado HTTP es 200 (OK):
    try:
        if r.status_code == 200:
            r.json()['features'][0]['properties']['address']['neighbourhood']
            return(r.json())
            #['features'][0]['properties']['osm_id']
    except:
        return -1
    
def getNominatimforId(osmId):
    # Creamos la petición HTTP con GET:
    r = requests.get("http://10.0.0.10/nominatim/reverse.php?format=geojson&osm_type=N&osm_id="+str(osmId)+"&accept-language=es-es&addressdetails=1")
    # Imprimimos el resultado si el código de estado HTTP es 200 (OK):
    if r.status_code == 200:
        try:
            r.json()['features'][0]['properties']
            return(r.json())
            
        except:
            try:
                r = requests.get("http://10.0.0.10/nominatim/reverse.php?format=geojson&osm_type=W&osm_id="+str(osmId)+"&accept-language=es-es&addressdetails=1")
                r.json()['features'][0]['properties']
                return(r.json())
            
            except:
                return -1
