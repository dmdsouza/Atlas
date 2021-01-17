from botocore.vendored import requests
import random
import json


def change_correct_name(str):
        loc=str.find('(')
        if loc < 1:
            return str
        newstr=str[0:loc-1]
        return newstr
        
def country_info(country):
    req = requests.get("https://restcountries.eu/rest/v2/all").json()
    info = []
   
    for d in req:
        time = d['name']
       
        if(change_correct_name(d['name'].upper())==country.upper()):
            
            info.append(d['capital'])
            info.append(d['subregion'])
            info.append(d['population'])
            
    return info
