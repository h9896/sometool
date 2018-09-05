import requests
import xmltodict
import json
from math import radians, cos, sin, asin, sqrt
#825ce0780e7949e7b08d4b242d5e23ec22ef04d3f30e90b55beb0afe60be9791
#---------------------------------class function type----------------------------------------#
class weather_query():
    def __init__(self, latp, lonp):
        self.latp = latp
        self.lonp = lonp
        self.authorizationkey = "authorizationkey"
        self.dataid = "O-A0001-001"
        self.url = "http://opendata.cwb.gov.tw/opendataapi?dataid={0}&authorizationkey={1}".format(self.dataid, self.authorizationkey)
        self.response = requests.get(self.url)
        self.datadic = xmltodict.parse(self.response.text)
        self.location_list = self.datadic['cwbopendata']['location']
    def update(self):
        self.response = requests.get(self.url)
        self.datadic = xmltodict.parse(self.response.text)
        self.location_list = self.datadic['cwbopendata']['location']
        
    def distance(self, lat1, lon1):
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, self.lonp, self.latp])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        return c * 6371 * 1000
        #take latitude and longitude as x and y coordinate in x-y plane
        #d = (lat1-self.latp)**2 + (lon1-self.lonp)**2
        #return d
    
    def query(self):
        placeweather={}
        if self.response.ok:
            dis = []
            for i in self.location_list:
                dis.append([self.distance(float(i['lat']),float(i['lon'])), i["stationId"]])
            dis.sort()
            
            for i in self.location_list:
                if i["stationId"] == dis[0][1]:
                    loca = i
            for i in loca['weatherElement']:
                if i['elementName'] == 'WDSD':
                    placeweather['WDSD'] = i['elementValue']['value']
                elif i['elementName'] == 'TEMP':
                    placeweather['TEMP'] = i['elementValue']['value']
                elif i['elementName'] == 'HUMD':
                    placeweather['HUMD'] = i['elementValue']['value']
                elif i['elementName'] == 'H_24R':
                    placeweather['H_24R'] = i['elementValue']['value']
            print("{} {}".format(loca['parameter'][0]['parameterValue'], loca['parameter'][2]['parameterValue']))
            print("溫度:{} \n風速:{} \n濕度:{} \n累積雨量:{}".format(placeweather['TEMP'], placeweather['WDSD'], placeweather['HUMD'], placeweather['H_24R']))
        else:
            print("{} {}".format( response.status_code ,response.reason))
        return placeweather
#---------------------------------function type----------------------------------------#
def distance(lat1, lon1, latp, lngp):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lonp, latp])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return c * 6371 * 1000
    #take latitude and longitude as x and y coordinate in x-y plane
    #d = (lat1-latp)**2 + (lng1-lngp)**2
    #return d
def getdata():
    authorizationkey = "authorizationkey"
    dataid = "O-A0001-001"
    url = "http://opendata.cwb.gov.tw/opendataapi?dataid={0}&authorizationkey={1}".format(dataid, authorizationkey)
    response = requests.get(url)
    if response.ok:
        datadic = xmltodict.parse(response.text)
        location_list = datadic['cwbopendata']['location']
    else:
        location_list = None
    return response, location_list
def query(response, location_list):
    if response.ok:
        #datadic = xmltodict.parse(response.text)
        #location_list = datadic['cwbopendata']['location']
        placeweather={}
        latp = float(input("Latitude: "))
        lonp = float(input("Longitude: "))
        dis = []
        for i in location_list:
            dis.append([distance(float(i['lat']),float(i['lon']), latp, lonp), i["stationId"]])
        dis.sort()
        
        for i in location_list:
            if i["stationId"] == dis[0][1]:
                loca = i
        for i in loca['weatherElement']:
            if i['elementName'] == 'WDSD':
                placeweather['WDSD'] = i['elementValue']['value']
            elif i['elementName'] == 'TEMP':
                placeweather['TEMP'] = i['elementValue']['value']
            elif i['elementName'] == 'HUMD':
                placeweather['HUMD'] = i['elementValue']['value']
            elif i['elementName'] == 'H_24R':
                placeweather['H_24R'] = i['elementValue']['value']
        print("{} {}".format(loca['parameter'][0]['parameterValue'], loca['parameter'][2]['parameterValue']))
        print("溫度:{} \n風速:{} \n濕度:{} \n累積雨量:{}".format(placeweather['TEMP'], placeweather['WDSD'], placeweather['HUMD'], placeweather['H_24R']))
    else:
        print("{} {}".format( response.status_code ,response.reason))

if __name__ == '__main__':
    response, location_list = getdata()
    while True:
        act = input("Query/Update/Exit:")
        if act.upper() == "QUERY":
            query(response, location_list)
        elif act.upper() == "UPDATE":
            response, location_list = getdata()
            query(response, location_list)
        elif act.upper() == "EXIT":
            break
        else:
            print("ERR, Try Again!")