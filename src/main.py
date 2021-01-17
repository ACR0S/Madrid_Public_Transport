import numpy as np
import pandas as pd
import scipy.spatial as spatial
import matplotlib.pyplot as plt
import matplotlib as mpl
import smopy

import pykml
import urllib.request
from pykml import parser

def unify_stations(df, stations, field='Estacion'):
    # This function receives a DataFrame and a list of stations with more than one line passing by them
    # And sets the coordinates for each station to be the same
    for station in stations:
        for i in range(len(df[df[field] == station])):
            df.iloc[df[df[field]==station].index[i],df.columns.get_loc('Latitud')] = df.iloc[df[df[field]==station].index[0],df.columns.get_loc('Latitud')]
            df.iloc[df[df[field]==station].index[i],df.columns.get_loc('Altitud')] = df.iloc[df[df[field]==station].index[0],df.columns.get_loc('Altitud')]
    return df


if '__name__' == '__main__':

    # Official data provided by Madrid council house
    # (source: https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=08055cde99be2410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default)

    filename = './data/Metro_2018_09.kml'
    with open(filename, encoding = "ISO-8859-1") as f:
        folder = parser.parse(f).getroot().Document.Folder

    stations = []
    coordinates = []
    for pm in folder.Placemark:
        plnm1 = pm.name
        plcs1 = pm.Point.coordinates
        stations.append(plnm1.text)
        coordinates.append(plcs1.text)

    df = pd.DataFrame()
    df['place_name'] = stations
    df['cordinates'] = coordinates

    # Basic modifications of the DataFrame
    df['Altitud'], df['Latitud'] = df['cordinates'].str.split('\n', 1).replace(',','').astype(float)
    df['Estacion'] = df['place_name'].str.split(' ',1).str[-1]
    df['Linea'] = df['place_name'].str.split(' ',1).str[0]
    df = df.drop(['cordinates', 'place_name'], 1)

    # Reorder columns
    cols = ['Linea', 'Estacion', 'Latitud','Altitud']
    df = df[cols]
    # Store different stations
    different_stations = df['Estacion'].unique()
    # Stores repeated stations in order to update their cordinates
    repeated_stations = set([x for x in df['Estacion'].tolist() if df['Estacion'].tolist().count(x) > 1])
    # Coordinates Update
    df = unify_stations(df, repeated_stations)
