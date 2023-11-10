import pandas as pd

from Functions.loadScenario import loadScenario



def extract_data_Fr(scenario, area, outputFolder="../data/output"):
    elec_price=pd.read_csv(outputFolder+'/marketPrice.csv').drop(columns='LastCalled').groupby(['YEAR_op']).mean()
    print(elec_price)
        

    return

