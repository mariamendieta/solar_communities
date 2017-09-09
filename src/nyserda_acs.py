from ast import literal_eval
import requests
import pandas as pd
import numpy as np
import acs5
import nyserda
import project_sunroof
import prices

def merging_data():
    #Merging the American Community Survey data with NYSERDA solar instalation data
    d = acs5.Get_census_data()
    acs = d.get_acs_all()
    solar = nyserda.nyserda_tract_summary()
    google = project_sunroof.import_data()
    prices_with_codes=prices.prices_data()
    acs_solar = acs.merge(solar, left_on='GEOID10', right_on='GEOID10', how='left')
    acs_solar_google = acs_solar.merge(google, left_on='GEOID10', right_on='region_name', how='left')
    all_data= acs_solar_google.merge(prices_with_codes, left_on='county', right_on='county', how='left')
    #Project precense dummy
    all_data['Project_yes'] = (all_data['Project_Number']>0)
    all_data['Project_yes']= all_data.Project_yes.astype(int)

    return all_data
