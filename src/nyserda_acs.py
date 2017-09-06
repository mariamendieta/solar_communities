from ast import literal_eval
import requests
import pandas as pd
import numpy as np
import acs5
import nyserda
import project_sunroof

def merging_data():
    #Merging the American Community Survey data with NYSERDA solar instalation data
    acs = acs5.get_acs_all()
    solar = nyserda.nyserda_tract_summary()
    google = project_sunroof.import_data()
    all_data = acs.merge(solar, left_on='GEOID10', right_on='GEOID10', how='left')
    all_data = all_data.merge(google, left_on='GEOID10', right_on='region_name', how='left')
    #Project precense dummy
    all_data['Project_yes'] = (all_data['Project_Number']>0)
    all_data['Project_yes']= all_data.Project_yes.astype(int)

    #New features from EDA
    all_data['less_35k_%'] = (all_data['Less_10k']+all_data['10k_15k']+all_data['15k_25k']+all_data['25k_35k'])/all_data['households']
    all_data['more_than_hs%'] = (all_data['Some_college']+all_data['Associate']+all_data['Bachelors']+all_data['Graduate'])/all_data['Pop_over_25']
    all_data['10+_units%'] = (all_data['10_19_units']+all_data['20+_units'])/all_data['Total_units_structure']
    all_data['1_unit%'] = (all_data['1_unit_detached']+all_data['20+_units'])/all_data['Total_units_structure']
    all_data['10+_units'] = all_data['10_19_units']+all_data['20+_units']
    all_data['more_than_hs%'] = (all_data['Some_college']+all_data['Associate']+all_data['Bachelors']+all_data['Graduate'])/all_data['Pop_over_25']
    return all_data
