from botocore.vendored import requests

def get_countries_list():
    req = requests.get("https://raw.githubusercontent.com/Miguel-Frazao/world-data/master/countries.json").json()
    countries = (i['name'] for i in req)
    return list(country_uppercase(list(countries)))
    


def country_uppercase(countries):
    countries_uppercase = []
    for i in countries:
        countries_uppercase.append(i.upper())
    return countries_uppercase
