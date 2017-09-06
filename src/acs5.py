from ast import literal_eval
import requests
import pandas as pd
import numpy as np

''' Getting data from the American Community Survey API
Find list of variables to get:
http://api.census.gov/data/2015/acs5/profile/variables.html
'''

def get_acs_demo():
    # List of selected variables to get.
    dct = {'DP03_0051E': 'households',
    'DP03_0052E': 'Less_10k', #Income variables
    'DP03_0053E': '10k_15k',
    'DP03_0054E': '15k_25k',
    'DP03_0055E': '25k_35k',
    'DP03_0056E': '35k_50k',
    'DP03_0057E': '50k_75k',
    'DP03_0058E': '75k_100k',
    'DP03_0059E': '100k_150k',
    'DP03_0060E': '150k_200k',
    'DP03_0061E': '200k_more',
    'DP03_0062E': 'Median_income',
    'DP03_0063E': 'Mean_income',
    'DP05_0001E': 'Total_population',
    'DP05_0004E': 'Under_5_years', #Population under 5
    'DP05_0017E': 'Median_age', #Median age
    'DP02_0001E': 'Total_households_by_type',
    'DP02_0003E': 'Hh_w_children', #Family
    'DP02_0015E': 'Avg_hh_size',
    'DP02_0058E': 'Pop_over_25',
    'DP02_0059E': 'Less_9th', #Education
    'DP02_0060E': '12th_no_dip',
    'DP02_0061E': 'HighSchool',
    'DP02_0062E': 'Some_college',
    'DP02_0063E': 'Associate',
    'DP02_0064E': 'Bachelors',
    'DP02_0065E': 'Graduate'
    }
    lst = dct.keys()
    var = ','.join(lst)
    lst_names = dct.values()
    #URL  http://api.census.gov/data/2015/acs5/profile?  State = 36 (New York), Level = Tract
    key = 'ff3aee5f79063ffd4c2fa0b7912d2b83f974b2f8'
    acs_url = 'http://api.census.gov/data/2015/acs5/profile?get={},NAME&for=tract:*&in=state:36&key={}'.format(var, key)
    response = requests.get(acs_url)
    request_content_list = literal_eval(response.text)
    headers = request_content_list.pop(0)
    acs_demo = pd.DataFrame(request_content_list, columns=headers)
    #Renaming features
    acs_demo.rename(columns=dct,inplace=True)
    # Creating full tract number
    acs_demo["GEOID10"] = acs_demo["state"].map(str) + acs_demo["county"].map(str) + acs_demo["tract"].map(str)
    # Changing type to numeric
    for fea  in lst_names:
        acs_demo[fea] = pd.to_numeric(acs_demo[fea], errors='coerce')
    acs_demo["GEOID10"] = pd.to_numeric(acs_demo['GEOID10'], errors='coerce')

    return acs_demo


def get_acs_hous():
    dct = {'DP04_0001E': 'Housing_Units',
    #'DP04_0001PE':'Percent_Housing',
    'DP04_0002E':'Occupied_units',
    #'DP04_0002PE':'Occupied_units_percent',
    'DP04_0005E':'Rental_vacancy_rate',
    'DP04_0006E':'Total_units_structure',
    'DP04_0007E':'1_unit_detached',
    #'DP04_0007PE':'1_unit_detached_percent',
    'DP04_0008E':'1_unit_attached',
    'DP04_0009E':'2_units',
    'DP04_0010E':'3_4_units',
    'DP04_0011E':'5_9_units',
    'DP04_0012E':'10_19_units',
    'DP04_0013E':'20+_units',
    'DP04_0027E':'Total_housing_units_Rooms',
    'DP04_0028E':'1_room',
    'DP04_0029E':'2_rooms',
    'DP04_0030E':'3_rooms',
    'DP04_0031E':'4_rooms',
    'DP04_0032E':'5_rooms',
    'DP04_0033E':'6_rooms',
    'DP04_0034E':'7_rooms',
    'DP04_0035E':'8_rooms',
    'DP04_0036E':'9_more_rooms',
    'DP04_0037E':'median_rooms',
    'DP04_0062E':'Occupied_units_heating',
    'DP04_0063E':'Heating_gas',
    'DP04_0064E':'Heating_gas_tank',
    'DP04_0065E':'Heating_electricity',
    'DP04_0066E':'Heating_fuelkero',
    'DP04_0067E':'Heating_coal_coke',
    'DP04_0068E':'Heating_wood',
    'DP04_0069E':'Heating_solar',
    'DP04_0070E':'Heating_other',
    'DP04_0071E':'Heating_no',
    'DP04_0089E':'Median_unit_values',
    }
    lst = dct.keys()
    var = ','.join(lst)
    lst_names = dct.values()
    #URL  http://api.census.gov/data/2015/acs5/profile?  State = 36 (New York), Level = Tract
    key = 'ff3aee5f79063ffd4c2fa0b7912d2b83f974b2f8'
    acs_url = 'http://api.census.gov/data/2015/acs5/profile?get={},NAME&for=tract:*&in=state:36&key={}'.format(var, key)
    response = requests.get(acs_url)
    request_content_list = literal_eval(response.text)
    headers = request_content_list.pop(0)
    acs_hous = pd.DataFrame(request_content_list, columns=headers)
    #Renaming features
    acs_hous.rename(columns=dct,inplace=True)
    # Creating full tract number
    acs_hous["GEOID10"] = acs_hous["state"].map(str) + acs_hous["county"].map(str) + acs_hous["tract"].map(str)
    # Changing type to numeric
    for fea  in lst_names:
        acs_hous[fea] = pd.to_numeric(acs_hous[fea], errors='coerce')
    acs_hous["GEOID10"] = pd.to_numeric(acs_hous['GEOID10'], errors='coerce')

    return acs_hous

def get_acs_all():
    acs_demo=get_acs_demo()
    acs_demo.drop(['NAME','state', 'county', 'tract'], axis=1, inplace=True)
    acs_hous=get_acs_hous()
    return acs_demo.merge(acs_hous, left_on='GEOID10', right_on='GEOID10', how='left')
