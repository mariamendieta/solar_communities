import pandas as pd
import numpy as np

# Getting raw data from NYSERDA.

def raw_data():
    '''This Data Frame  Data has been downloaded from NY SERDA and modified
    to add tract numbers using QGIS and Census Tract Shapefiles
    '''
    #Includes Tract Numbers from NY Census Geo
    solar_instal = pd.read_csv('input/serda_tract.csv')

    #Making project cost a number
    solar_instal['Project_Cost'] = solar_instal['Project_Cost'].str.replace('$', '')
    solar_instal['Project_Cost'] = solar_instal['Project_Cost'].str.replace(' ', '')
    solar_instal['Project_Cost'] = solar_instal['Project_Cost'].str.replace(',', '')
    solar_instal['Project_Cost'] = pd.to_numeric(solar_instal['Project_Cost'])
    # Cost per KW
    solar_instal['cost_Kw']=solar_instal['Project_Cost']/solar_instal['Total_Nameplate_kW_DC']
    #Date completed to Date Type
    solar_instal['Date_Completed1']= pd.to_datetime(solar_instal['Date_Completed'])
    #Converting yes/no in dummies
    solar_instal['Affordable_Solar'] = solar_instal.Affordable_Solar.map(dict(Yes=1, No=0))
    solar_instal['Remote_Net_Metering']=solar_instal.Remote_Net_Metering.map(dict(Yes=1, No=0))
    solar_instal['Community_Distributed_Generation'] =solar_instal.Community_Distributed_Generation.map(dict(Yes=1, No=0))
    return solar_instal

def nyserda_tract_summary():
    '''Creating a new dataframe: Groupby Tract, Only Residentail/Small Commercial ,
    Number of projects(count), TotalCapacity(sum), Meantotal_cost(mean), CostperKw (mean),
    Affordablesolar (sum), community (sum), expected prod (sum), net_metering (sum)'''
    solar_instal = raw_data()
    temp = solar_instal[solar_instal['Program_Type']=='Residential/Small Commercial']

    temp1 = pd.pivot_table(temp, values=['Total_Nameplate_kW_DC','Affordable_Solar','Expected_KWh_Annual_Production',
                                         'Community_Distributed_Generation','Remote_Net_Metering'], index=['GEOID10'],
                                         aggfunc=np.sum)
    temp2 = pd.pivot_table(temp, values=['Project_Cost','cost_Kw'], index=['GEOID10'], aggfunc=np.mean)
    temp3 = pd.pivot_table(temp, values=['Project_Number'], index=['GEOID10'], aggfunc=len)
    nyserda_tract = pd.concat((temp1, temp2, temp3), axis=1)
    nyserda_tract['GEOID10'] = nyserda_tract.index
    #Alternatively read this file
    #nyserda_tract = pd.read_csv('input/solar_tract.csv')
    return nyserda_tract
