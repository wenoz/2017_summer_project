import requests
import bs4
import html
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy.types as types
import numpy as np
import datetime
import numpy as np
from pandas import *
from locations_lib import *
import webbrowser

my_db_info = {
    'host': '',
    'user': ',
    'password': '',
    'port': ,
    'dbname': ''
}

def display_map_box(location_array):
    lat_lower, lon_upper = getLatLon(location_array[0])
    lat_upper, lon_lower = getLatLon(location_array[1])

    app_id = ''
    app_code = ''
    location = str(lat_lower)+"%2C"+ str(lon_lower)+"%2C"+ \
               str(lat_upper)+"%2C"+ str(lon_lower)+"%2C"+ \
               str(lat_lower)+"%2C"+ str(lon_upper)+"%2C"+ \
               str(lat_upper)+"%2C"+ str(lon_upper)
    # get the bouding box but sometime does not show the one passed in 
    # URL = "https://image.maps.cit.api.here.com/mia/1.6/mapview?bbox="+location+"&app_id="+app_id+"&app_code="+app_code
    
    # get four points indicating the bounding box
    URL = "https://image.maps.cit.api.here.com/mia/1.6/mapview?poi=" +location+"&app_id="+app_id+"&app_code="+app_code
    
    r = requests.get(url=URL)
    try:
        print( URL)
        webbrowser.open_new(URL)

    except:
        print("Fail to get the image")
        
    
def getLatLon(location):
   app_id = ''
   app_code = ''
   location = location.replace(" ", "+")
   URL = "https://geocoder.cit.api.here.com/6.2/geocode.xml?app_id="+app_id+"&app_code="+app_code+"&searchtext="+location
   r = requests.get(url=URL)
   try:
       soup = bs4.BeautifulSoup(r.text, 'lxml')
       soup = soup.body.response.navigationposition.contents
       lat = soup[0].contents[0]
       lon = soup[1].contents[0]
       return lat, lon
   except:
       print("Here Map fails to fine "+location)
       return None, None


def get_od_table( origin_lon_upper, origin_lat_upper, origin_lon_lower, origin_lat_lower, destination_lat_lower, destination_lon_upper, destination_lat_upper, destination_lon_lower, year = 2016, uw = False, input_db_info = my_db_info ) :
    db_info = input_db_info
    sql_str = 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'.format 
    engine = create_engine(sql_str(**db_info))

    query = '' 

    if year == 2016 and uw == False:
        query = "SELECT origin, first_route_taken, first_service_provider,  destination, last_route_taken, last_service_provider, number_of_transfers, count(*) as abs_frequency from orca2016.`od-trip` where origin_lat<= " +str(origin_lat_upper)+ " and origin_lat >= " + str(origin_lat_lower) + \
        " and origin_lon >= " + str(origin_lon_lower) + " and origin_lon <= " + str(origin_lon_upper) + \
        " and destination_lat <= " + str(destination_lat_upper) + " and destination_lat >= " + str(destination_lat_lower) + \
        " and destination_lon >= " + str(destination_lon_lower) + " and destination_lon <= " + str(destination_lon_upper) + \
        " group by origin, first_route_taken, first_service_provider, destination, last_route_taken, last_service_provider, number_of_transfers order by abs_frequency DESC "
    if year == 2015 and uw == False:
        query = "SELECT origin, first_route_taken, first_service_provider,  destination, last_route_taken, last_service_provider, number_of_transfers, count(*) as abs_frequency  from orca.`od-trip` where origin_lat<= " +str(origin_lat_upper)+ " and origin_lat >= " + str(origin_lat_lower) + \
        " and origin_lon >= " + str(origin_lon_lower) + " and origin_lon <= " + str(origin_lon_upper) + \
        " and destination_lat <= " + str(destination_lat_upper) + " and destination_lat >= " + str(destination_lat_lower) + \
        " and destination_lon >= " + str(destination_lon_lower) + " and destination_lon <= " + str(destination_lon_upper) + \
        " group by origin, first_route_taken, first_service_provider, destination, last_route_taken, last_service_provider, number_of_transfers order by abs_frequency DESC "
    
    if year == 2016 and uw == True:
        query = "SELECT origin, first_route_taken, first_service_provider,  destination, last_route_taken, last_service_provider, number_of_transfers, count(*) as abs_frequency from orca2016.`od-trip` where origin_lat<= " +str(origin_lat_upper)+ " and origin_lat >= " + str(origin_lat_lower) + \
        " and origin_lon >= " + str(origin_lon_lower) + " and origin_lon <= " + str(origin_lon_upper) + \
        " and destination_lat <= " + str(destination_lat_upper) + " and destination_lat >= " + str(destination_lat_lower) + \
        " and destination_lon >= " + str(destination_lon_lower) + " and destination_lon <= " + str(destination_lon_upper) + \
        " and bid = '0ad41765045007f9' group by origin, first_route_taken, first_service_provider, destination, last_route_taken, last_service_provider, number_of_transfers order by abs_frequency DESC "
    
    if year == 2015 and uw == True:
        query = "SELECT origin, first_route_taken, first_service_provider,  destination, last_route_taken, last_service_provider, number_of_transfers, count(*) as abs_frequency from orca.`od-trip` where origin_lat<= " +str(origin_lat_upper)+ " and origin_lat >= " + str(origin_lat_lower) + \
        " and origin_lon >= " + str(origin_lon_lower) + " and origin_lon <= " + str(origin_lon_upper) + \
        " and destination_lat <= " + str(destination_lat_upper) + " and destination_lat >= " + str(destination_lat_lower) + \
        " and destination_lon >= " + str(destination_lon_lower) + " and destination_lon <= " + str(destination_lon_upper) + \
        " and bid = '0ad41765045007f9' group by origin, first_route_taken, first_service_provider, destination, last_route_taken, last_service_provider, number_of_transfers order by abs_frequency DESC "
    
    
    print('''
      /\_/|
     ( o.o )
      > ^ < ''')
    data = pd.read_sql(query, engine)
    
    print (query)

    return data



def get_count(origin_left_top, origin_right_bottom, destination_left_top, destination_right_bottom, year = 2016, uw = False, weekday_average = False, input_db_info = my_db_info):
    origin_lat_lower, origin_lon_upper = getLatLon(origin_right_bottom)
    origin_lat_upper, origin_lon_lower = getLatLon(origin_left_top)
    destination_lat_lower, destination_lon_upper = getLatLon(destination_right_bottom)
    destination_lat_upper, destination_lon_lower = getLatLon(destination_left_top)
    
    db_info = input_db_info
    sql_str = 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'.format 
    engine = create_engine(sql_str(**db_info))

    query = '' 
    query = "SELECT count(*) as total from "

    if year == 2016:
        query = query+"orca2016"    
    
    if year == 2015 :
        query = query+"orca"

    query = query + ".`od-trip` where origin_lat<= " +str(origin_lat_upper)+ " and origin_lat >= " + str(origin_lat_lower) + \
        " and origin_lon >= " + str(origin_lon_lower) + " and origin_lon <= " + str(origin_lon_upper) + \
        " and destination_lat <= " + str(destination_lat_upper) + " and destination_lat >= " + str(destination_lat_lower) + \
        " and destination_lon >= " + str(destination_lon_lower) + " and destination_lon <= " + str(destination_lon_upper) 
    
    if uw == True:
        query = query + " and bid = '0ad41765045007f9' "

    if weekday_average ==True:
        query = query + " and dayofweek(trip_start_date) in(2,3,4,5,6)"

    '''
    if year == 2016 and uw == True:
        query = "SELECT count(*) as total from orca2016.`od-trip` where origin_lat<= " +str(origin_lat_upper)+ " and origin_lat >= " + str(origin_lat_lower) + \
        " and origin_lon >= " + str(origin_lon_lower) + " and origin_lon <= " + str(origin_lon_upper) + \
        " and destination_lat <= " + str(destination_lat_upper) + " and destination_lat >= " + str(destination_lat_lower) + \
        " and destination_lon >= " + str(destination_lon_lower) + " and destination_lon <= " + str(destination_lon_upper) + \
        " and bid = '0ad41765045007f9' "   '''
        
    data = pd.read_sql(query, engine)
    # print(data['total'][0])
    # print(query)
    print('''
 /\-/\  
(=^Y^=) ''')
    return data['total'][0]

    
    

def get_travel_pattern(origin_left_top, origin_right_bottom, destination_left_top, destination_right_bottom, input_year = 2016, input_uw = False):
    origin_lat_lower, origin_lon_upper = getLatLon(origin_right_bottom)
    origin_lat_upper, origin_lon_lower = getLatLon(origin_left_top)
    destination_lat_lower, destination_lon_upper = getLatLon(destination_right_bottom)
    destination_lat_upper, destination_lon_lower = getLatLon(destination_left_top)
    print (origin_lat_lower, 'origin lat' , origin_lat_upper)
    print (origin_lon_lower, 'origin lon' , origin_lon_upper)
    print (destination_lat_lower, 'destination lat' , destination_lat_upper)
    print (destination_lon_lower, 'destination lon' , destination_lon_upper)


    result = get_od_table(origin_lon_upper,origin_lat_upper, origin_lon_lower, origin_lat_lower, destination_lat_lower, destination_lon_upper, destination_lat_upper, destination_lon_lower, year = input_year, uw = input_uw)
    print(result.head(10))

    total = result['abs_frequency'].sum()
    print(total)

    result.to_csv('travel_pattern_result.csv') 

    return result


def get_count_matrix(origin, destination, input_year = 2016, input_uw = False, input_weekday_average = False):

    h, w = len(origin),len(destination)
    count_matrix = [[0 for x in range(w)] for y in range(h)]

    for i in range(h):
        for j in range(w):
            count_matrix[i][j] = get_count(origin[i][0], origin[i][1], destination[j][0], destination[j][1], year = input_year, uw = input_uw, weekday_average =input_weekday_average )/(45*input_weekday_average + 1*(1-input_weekday_average))

    print(DataFrame(count_matrix))


