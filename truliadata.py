from dataclasses import dataclass
from textwrap import indent
from bs4 import BeautifulSoup
import requests
import re
import csv
import json
from json.decoder import JSONDecodeError
import os

directory = '/Users/bhava/downloads/Austin'

def permissive_json_loads(text):
    while True:
        try:
            data = json.loads(text)
        except JSONDecodeError as exc:
            if exc.msg == 'Invalid \\escape':
                text = text[:exc.pos] + '\\' + text[exc.pos:]
            else:
                raise
        else:
            return data
j = 0
for filename in os.listdir("/Users/bhava/Desktop/DS4A/Austin/"):     
    if filename.endswith(".html"):         
        with open(os.path.join('/Users/bhava/Desktop/DS4A/Austin/', filename)) as f:
            contents = f.read()

            soup = BeautifulSoup(contents, 'lxml')
            
            pjson = soup.find('script', attrs={ 'id' : '__NEXT_DATA__'}).text
            
            pj = str(pjson)
            pj.encode('utf-8')
            
            with open('/Users/bhava/Desktop/DS4A/books.json', 'w', encoding='utf-8') as fi:
                json.dump(pj, fi)
            
            with open('/Users/bhava/Desktop/DS4A/books.json', 'r', encoding='utf-8') as conn_file:
                conn_doc = conn_file.read()
            conn = permissive_json_loads(conn_doc)
            tcc = json.loads(conn)
            
            with open('austindata.csv', 'a') as csvfile:
                field_names = ['ID', 'File', 'city', 'stateCode', 'zipCode', 'fullLocation', 'partialLocation','coordinates','price', 'floorSpace', 'bedrooms', 'bathrooms']
                
                writer = csv.DictWriter(csvfile, fieldnames = field_names)
                    
                if os.stat('austindata.csv').st_size == 0:
                    writer.writeheader()
                    
                i = 0
                while i<=39:
                    newdict={}
                    #newdict = tcc["props"]["searchData"]["homes"][i]["location"]
                    city = tcc["props"]["searchData"]["homes"][i]["location"]["city"]
                    stateCode = tcc["props"]["searchData"]["homes"][i]["location"]["stateCode"]
                    zipCode = tcc["props"]["searchData"]["homes"][i]["location"]["zipCode"]
                    fullLocation = tcc["props"]["searchData"]["homes"][i]["location"]["fullLocation"]
                    partialLocation = tcc["props"]["searchData"]["homes"][i]["location"]["partialLocation"]
                    coordinates = tcc["props"]["searchData"]["homes"][i]["location"]["coordinates"]
                    price = tcc["props"]["searchData"]["homes"][i]["price"]["formattedPrice"]
                    #currencyCode = tcc["props"]["searchData"]["homes"][i]["price"]["currencyCode"]
                    floorSpace = tcc["props"]["searchData"]["homes"][i]["floorSpace"]
                    bedrooms = tcc["props"]["searchData"]["homes"][i]["bedrooms"]
                    bathrooms = tcc["props"]["searchData"]["homes"][i]["bathrooms"]
                    
                    if city is None:
                        city = 'N/A'
                    if stateCode is None:
                        stateCode = 'N/A'
                    if zipCode is None:
                        zipCode = 'N/A'
                    if fullLocation is None:
                        fullLocation = 'N/A'
                    if partialLocation is None:
                        partialLocation = 'N/A'
                    if coordinates is None:
                        coordinates = 'N/A'
                    if price is None:
                        price = 'N/A'
                    #if currencyCode is None:
                    #    currencyCode = 'N/A'
                    if floorSpace is None:
                        floorSpace = 'N/A'
                    if bedrooms is None:
                        bedrooms = 'N/A'
                    if bathrooms is None:
                        bathrooms = 'N/A'
                    
                    j = j+i
                    newdict["ID"] = i
                    newdict["File"] = f #'austin'+str(x)+'.html'
                    newdict["city"] = city
                    newdict["stateCode"] = stateCode
                    newdict["zipCode"] = zipCode
                    newdict["fullLocation"] = fullLocation
                    newdict["partialLocation"] = partialLocation
                    newdict["coordinates"] = coordinates
                    newdict["price"] = price
                    #newdict["currencyCode"] = currencyCode
                    newdict["floorSpace"] = floorSpace
                    newdict["bedrooms"] = bedrooms
                    newdict["bathrooms"] = bathrooms
                    
                    #print(x)
                    print(newdict)
                    
                    writer.writerow(newdict)
                    
                    i =i+1
                    continue
    else:
        continue
    #f.close()
    #x = x-1