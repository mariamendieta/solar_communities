import pandas as pd


def import_data():
    google_sunroof=pd.read_csv('input/project-sunroof-google-08282017.csv')
    google_NY = google_sunroof[google_sunroof['state_name']=='New York']
    return google_NY
