import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy.types as types
import numpy as np
import datetime
import here_api get_coordinate

my_db_info = {
    'host': '',
    'user': '',
    'password': '',
    'port': , # four-digit number, not a string 
    'dbname': ''
}

def get_travel_pattern(origin_left_top, origin_right_bottom, destination_left_top, destination_right_bottom, input_year = 2016, input_uw = False, input_db_info = my_db_info):
    origin_lat_lower, origin_lon_upper = getLatLon(origin_right_bottom)
    origin_lat_upper, origin_lon_lower = getLatLon(origin_left_top)
    destination_lat_lower, destination_lon_upper = getLatLon(destination_right_bottom)
    destination_lat_upper, destination_lon_lower = getLatLon(destination_left_top)
   
    print (origin_lat_lower, 'origin lat' , origin_lat_upper)
    print (origin_lon_lower, 'origin lon' , origin_lon_upper)
    print (destination_lat_lower, 'destination lat' , destination_lat_upper)
    print (destination_lon_lower, 'destination lon' , destination_lon_upper)    
    
    db_info = input_db_info
    sql_str = 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'.format 
    engine = create_engine(sql_str(**db_info))

    query = '' 
    query = "SELECT origin, first_route_taken, first_service_provider,  destination, last_route_taken, last_service_provider, number_of_transfers, count(*) as abs_frequency from "
        

    if year == 2016:
        query = query + "orca2016"     
    if year == 2015:
        query = query + "orca"     
    
    query = query + \
        ".`od-trip` where origin_lat<= " +str(origin_lat_upper)+ " and origin_lat >= " + str(origin_lat_lower) + \
        " and origin_lon >= " + str(origin_lon_lower) + " and origin_lon <= " + str(origin_lon_upper) + \
        " and destination_lat <= " + str(destination_lat_upper) + " and destination_lat >= " + str(destination_lat_lower) + \
        " and destination_lon >= " + str(destination_lon_lower) + " and destination_lon <= " + str(destination_lon_upper) + \
        " group by origin, first_route_taken, first_service_provider, destination, last_route_taken, last_service_provider, number_of_transfers order by abs_frequency DESC "

    print('''
      /\_/|
     ( o.o )
      > ^ <    Reading Table now...''')
    data = pd.read_sql(query, engine)
    
    # print (query)

    return data

def get_count(origin_left_top, origin_right_bottom, destination_left_top, destination_right_bottom, year = 2016, input_db_info = my_db_info):
    origin_lat_lower, origin_lon_upper = here_api.get_coordinate(origin_right_bottom)
    origin_lat_upper, origin_lon_lower = here_api.get_coordinate(origin_left_top)
    destination_lat_lower, destination_lon_upper = here_api.get_coordinate(destination_right_bottom)
    destination_lat_upper, destination_lon_lower = here_api.get_coordinate(destination_left_top)
    
    db_info = input_db_info
    sql_str = 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'.format 
    engine = create_engine(sql_str(**db_info))

    query = '' # initiate an empty string 

    query = "SELECT count(*) as total from "

    if year == 2016:
        query = query + "orca2016."

    if year == 2015:
         query = query + "orca."

    query = query + "`od-trip` where origin_lat<= " +str(origin_lat_upper)+ " and origin_lat >= " + str(origin_lat_lower) + \
        " and origin_lon >= " + str(origin_lon_lower) + " and origin_lon <= " + str(origin_lon_upper) + \
        " and destination_lat <= " + str(destination_lat_upper) + " and destination_lat >= " + str(destination_lat_lower) + \
        " and destination_lon >= " + str(destination_lon_lower) + " and destination_lon <= " + str(destination_lon_upper) 

    data = pd.read_sql(query, engine)

    # print(data['total'][0])

    return data['total'][0]


def get_count_matrix(origin, destination, input_year = 2016, input_uw = False):

    h, w = len(origin),len(destination)
    count_matrix = [[0 for x in range(w)] for y in range(h)]

    for i in range(h):
        for j in range(w):
            count_matrix[i][j] = get_count(origin[i][0], origin[i][1], destination[j][0], destination[j][1], year = input_year, uw = input_uw)

    print(DataFrame(count_matrix))


## U District and Capitol Hill 
ud_1 = ['7th Ave NE and NE 50th St, Seattle', 'NE 45th St and Union Bay PI NE, Seattle']
ud_2 = ['7th Ave NE and NE 45th St, Seattle', 'Walla Walla Rd and Snohomish Ln N, Seattle']
ud_3 = ['NE Pacific St and NE Boat St, Seattle', '2802 E Park Dr E, Seattle']

ch_1 = ['Bellevue Ave E and E Mercer St, Seattle', '15th Ave and E Olive St, Seattle']
ch_2 = ['Bellevue Ave and E Olive St, Seattle', '15th Ave and E Union St, Seattle']
ch_3 = ['Pike St and Boren Ave, Seattle', '15th Ave and E Jefferson St, Seattle']

origin = [ud_1, ud_2, ud_3]
destination = [ch_1, ch_2, ch_3]
