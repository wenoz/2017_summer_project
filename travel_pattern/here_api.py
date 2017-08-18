import requests
import bs4
import html
import pandas as pd
import webbrowser


def get_coordinate(location):
    ''' input : location, a String, text to indicate the crosssection of the two roads 
                                    example: NE 42nd St and 15th Ave, Seattle
        output: two float, latitute and longtitute of the location
    '''

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
        print("Here Map fails to fine "+ location)
        return None, None

def display_a_location_on_map(location):
    ''' input : location, a String, text to indicate the crosssection of the two roads 
                                    example: NE 42nd St and 15th Ave, Seattle
        output: pop out browser window 
    '''

    lat, lon = getLatLon(location_array)

    app_id = ''
    app_code = ''
    location = str(lat)+"%2C"+ str(lon_lower)
    URL = "https://image.maps.cit.api.here.com/mia/1.6/mapview?poi=" +location+"&app_id="+app_id+"&app_code="+app_code
    try:
        print( URL) # print the url in console 
        webbrowser.open_new(URL)
    except:
        print("Fail to get the image")


def display_bourding_box(location_array):
    ''' input : location_array, a length of 2 array of strings, 
                two location address to indidate the bounding box left top corner and right bottom corner
                example: ['NE 50nd St and 5th Ave, Seattle', 'NE 42nd St and 15th Ave, Seattle']
        output: pop out browser window 
    '''
    lat_lower, lon_upper = getLatLon(location_array[0])
    lat_upper, lon_lower = getLatLon(location_array[1])

    app_id = '6hOQhDogstGXM1cPpsJH'
    app_code = 'fBI5vpKhsRRyZS1-ahfHEg'
    location = str(lat_lower)+"%2C"+ str(lon_lower)+"%2C"+ \
               str(lat_upper)+"%2C"+ str(lon_upper)+"%2C"+ \
    
    URL = "https://image.maps.cit.api.here.com/mia/1.6/mapview?bbox="+location+"&app_id="+app_id+"&app_code="+app_code

    try:
        print( URL)
        webbrowser.open_new(URL)

    except:
        print("Fail to get the image")