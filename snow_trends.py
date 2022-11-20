import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import datetime
from shapely.geometry import Point, Polygon
import ipywidgets

#Read the geopandas shape file for continental US states
states = gpd.read_file('data/shapefile-data/usa-states-census-2014.shp')

#Load the two csvs with (1) date of first snow for each station, and (2) the details of each station
# Merge them into one dataframe with an inner join.
def generate_merged_dataframe(year):
    firstSnowDF = pd.read_csv(f"data/Snow_Trends_Data/First-Snow-Dates/{year}.csv").set_index("id")
    stationsDF = pd.read_csv("data/Snow_Trends_Data/stations.csv").set_index("id")
    mergedDF = pd.merge(firstSnowDF, stationsDF, left_index=True, right_index=True)[['date', 'latitude', 'longitude', 'name']]
    mergedDF['date'] = pd.to_datetime(mergedDF.date)
    return mergedDF

def generate_geodataframe(mergedDF):    
    #defined coordinate reference system. Use the same as the states shapefile.
    crs='epsg:4326'
    #define a geometry consisting of Points, to use as the GDF geometry
    geometry=[Point(longlat_tuple) for longlat_tuple in zip(mergedDF['longitude'], mergedDF['latitude'])]
    #create the GDF using the data and the geometry
    mergedGeoDF = gpd.GeoDataFrame(mergedDF[['date', 'name']], crs=crs, geometry=geometry)
    return mergedGeoDF

def points_per_day(mergedDF, datetime_input):
    ''' 
    Provide a datetime_object and return a geodataframe of of all snow events occuring before and up to then
    '''
    selected_data = mergedDF[mergedDF['date'] <= datetime_input]
    geometry=[Point(longlat_tuple) for longlat_tuple in zip(selected_data['longitude'], selected_data['latitude'])]
    selectGeoDF = gpd.GeoDataFrame(selected_data[['date', 'name']], crs="epsg:4326", geometry=geometry)
    return selectGeoDF

def generate_map(datetime_string, mergedDF, year):
    datetime_obj = datetime.datetime.strptime(datetime_string, "%b %d, %Y")
    pointMap = points_per_day(mergedDF, datetime_obj)
    continentalUS = states.boundary.plot(figsize=(13,10), color='grey', linewidth=1)
    plt.title(f"Stations Having Observed Snow in {year}-{year+1} Season", fontsize=24)
    plt.text(-125, 25, f"Up to:\n{datetime_string}", fontsize=15)
    plt.ylabel("Geodetic latitude, north (degree)", fontsize=15)
    plt.xlabel("Geodetic longitude, east (degree)", fontsize=15)
    pointMap.plot(ax=continentalUS, markersize=15, color='blue')

def generate_interactive_map(mergedDF, year):
    #Use this dictionary to make an interactive slider.
    # The key to be the string formatted date (), the value is the datetime object
    start_datetime = mergedDF['date'].min()
    end_datetime = mergedDF['date'].max()
    string_datetime_mapping = {}
    current_datetime = start_datetime
    while current_datetime < end_datetime:
        string_datetime_mapping[datetime.datetime.strftime(current_datetime, "%b %d, %Y")] = current_datetime
        current_datetime += datetime.timedelta(days=1)
    list_of_string_dates = list(string_datetime_mapping.keys())
    print(f"Select a Date Between {list_of_string_dates[0]} and {list_of_string_dates[-1]}.\n(The map will take a few seconds to update.")
    dateSlider = ipywidgets.SelectionSlider(options=list_of_string_dates, \
                                   value=list_of_string_dates[0], \
                                   description="Date:", \
                                   layout=ipywidgets.Layout(width='80%'))
    ipywidgets.widgets.interact(generate_map, datetime_string=dateSlider, mergedDF=ipywidgets.fixed(mergedDF), year=ipywidgets.fixed(year))
    
def prompt_for_year():
    #This function returns an interactive widget object, which has already been rendered.
    # After calling this function, you just need to access the result of the widget
    # using dropdownWidget.result
    from ipywidgets.widgets import Dropdown
    from ipywidgets import interactive
    import os
    from IPython.display import display
    directory_list = os.listdir("data/Snow_Trends_Data/First-Snow-Dates")
    available_years = [int(filename.rstrip(".csv")) for filename in directory_list]
    available_years.sort(reverse=True) #Sort the list from most recent to most distant year
    dropdownWidget = interactive(lambda Year: Year, Year = available_years)
    display(dropdownWidget)
    return dropdownWidget #this is an interactive widget object