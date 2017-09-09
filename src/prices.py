from ast import literal_eval
import requests
import pandas as pd
import numpy as np

def prices_data():
    county_names = {'001': 'Albany', '003': 'Allegany', '005': 'Bronx', '007': 'Broome' , '009':'Cattaraugus',
                    '011': 'Gayuga', '013': 'Chautauqua', '015':'Chemung' , '017': 'Chenango',
                    '019': 'Clinton', '021': 'Columbia', '023': 'Cortland' , '025':'Delaware',
                    '027': 'Dutchess', '029': 'Erie' , '031': 'Essex', '033': 'Franklin', '035':'Fulton' ,
                    '037':'Genesee', '039':'Greene', '041': 'Hamilton', '043': 'Herkimer' ,
                    '045':'Jefferson', '047': 'Kings', '049':'Lewis', '051':'Livingston', '053':'Madison',
                    '055':'Monroe', '057':'Montgomery','059':'Nassau', '061':'New York', '063':'Niagara',
                    '065':'Oneida', '067':'Onondaga', '069':'Ontario', '071':'Orange', '073':'Orleans',
                    '075':'Oswego', '077': 'Otsego', '079':'Putnam', '081':'Queens', '083':'Rensselaer',
                    '085':'Richmond', '087':'Rockland', '089':'St. Lawrence','091':'Saratoga',
                    '093':'Schenectady', '095':'Schoharie' , '097':'Schuyler', '099':'Seneca', '101':'Steuben',
                    '103':'Suffolk', '105':'Sullivan', '107':'Tioga','109':'Tompkins', '111':'Ulster',
                    '113':'Warren', '115':'Washington', '117':'Wayne', '119':'Westchester',
                    '121':'Wyoming', '123':'Yates'}

    zones = {'WEST': ['Chautauqua', 'Cattaraugus', 'Erie', 'Niagara', 'Orleans', 'Genesee', 'Wyoming', 'Livingston'],
            'GENESE': ['Allegany', 'Monroe', 'Wayne', 'Ontario'],
            'CENTRL': ['Steuben', 'Yates', 'Seneca', 'Gayuga', 'Schuyler', 'Chemung','Tioga', 'Tompkins', 'Cortland',
                   'Broome','Onondaga','Oswego'],
            'NORTH': ['Clinton'],
            'MHK VL': ['Jefferson', 'St. Lawrence', 'Franklin', 'Lewis', 'Oneida', 'Herkimer', 'Madison', 'Otsego',
                 'Chenango', 'Delaware', 'Sullivan'],
            'CAPITL': ['Essex', 'Hamilton', 'Warren', 'Washington', 'Saratoga', 'Fulton', 'Montgomery', 'Schenectady',
                 'Schoharie', 'Albany', 'Rensselaer', 'Columbia'],
             'HUD VL': ['Greene', 'Dutchess', 'Ulster', 'Orange', 'Putnam', 'Rockland'],
             'DUNWOD': ['Westchester'],
             'N.Y.C.': ['Bronx', 'Kings', 'Queens', 'New York','Richmond'],
             'LONGIL': ['Nassau', 'Suffolk'] }

    prices = pd.read_csv('input/2016-todate.csv')
    prices['Mean_price'] = 'Mean_price'
    prices['Var_price'] = 'Var_price'

    mean_prices = pd.crosstab(index=prices['Zone Name'], columns= prices['Mean_price'],
                                 values = prices['DAM Zonal LBMP'], aggfunc=np.mean)
    var_prices = pd.crosstab(index=prices['Zone Name'], columns= prices['Var_price'],
                                 values = prices['DAM Zonal LBMP'], aggfunc=np.var)
    zone_prices = pd.concat([mean_prices,var_prices], axis=1)

    df_zones = pd.DataFrame([{'Region': k , 'County': value} for k, v in zones.items() for value in v])
    df_county_names =pd.DataFrame(county_names.items(), columns=['county', 'county_name'])
    prices = df_zones.merge(zone_prices, left_on='Region', right_index=True, how='left')
    prices_with_codes = prices.merge(df_county_names, left_on='County', right_on='county_name', how='outer')
    prices_with_codes.drop('County',axis=1, inplace=True)

    return prices_with_codes
