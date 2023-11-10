# region Importation of modules
import os
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np



os.sys.path.append(r"../")
import pandas as pd

from Scenarios.scenario_creationFr import scenarioDictFr
# from Functions.f_graphicTools_Fr import plot_mixProdElec, plot_monotone

# endregion


def plot_mixProdElec(outputFolder='Data/output/'):

    v_list = ['capacityInvest_Dvar','transInvest_Dvar','capacity_Pvar','capacityDel_Pvar','capacityDem_Dvar', 'energy_Pvar', 'power_Dvar', 'storageConsumption_Pvar', 'storageIn_Pvar', 'storageOut_Pvar',
              'stockLevel_Pvar', 'importation_Dvar', 'Cmax_Pvar','carbon_Pvar','powerCosts_Pvar','capacityCosts_Pvar','importCosts_Pvar','storageCosts_Pvar','turpeCosts_Pvar','Pmax_Pvar','max_PS_Dvar','carbonCosts_Pvar']
    Variables = {v : pd.read_csv(outputFolder+'/'+v+'.csv').drop(columns='Unnamed: 0') for v in v_list}

    YEAR=list(Variables['power_Dvar'].set_index('YEAR_op').index.unique())
    elecProd=Variables['power_Dvar'].set_index(['YEAR_op','TIMESTAMP','TECHNOLOGIES'])

    Prod=elecProd.groupby(['YEAR_op','TECHNOLOGIES']).sum()
    Prod.loc[(slice(None),'IntercoOut'),'power_Dvar']=-Prod.loc[(slice(None),'IntercoOut'),'power_Dvar']
    Capa=Variables['capacity_Pvar'].set_index(['YEAR_op','TECHNOLOGIES'])
    Capa.sort_index(axis = 0,inplace=True)

    TECHNO=list(elecProd.index.get_level_values('TECHNOLOGIES').unique())
    l_tech=len(TECHNO)
    l_year=len(YEAR)

    Interco={y:(Prod.loc[(y,'IntercoIn')]+Prod.loc[(y,'IntercoOut')]) for y in YEAR}
    Fossils={y:(Prod.loc[(y,'CCG')]+Prod.loc[(y,'Coal_p')]+Prod.loc[(y,'NewNuke')]+Prod.loc[(y,'OldNuke')]+Prod.loc[(y,'TAC')])['power_Dvar']/(Prod.loc[(y,slice(None))].sum()['power_Dvar']-Interco[y]['power_Dvar']) for y in YEAR}
    EnR={y:(Prod.loc[(y,'Solar')]+Prod.loc[(y,'WindOnShore')]+Prod.loc[(y,'WindOffShore')]+Prod.loc[(y,'HydroRiver')]+Prod.loc[(y,'HydroReservoir')])['power_Dvar']/(Prod.loc[(y,slice(None))].sum()['power_Dvar']-Interco[y]['power_Dvar']) for y in YEAR}
    Nuke={y:(Prod.loc[(y,'OldNuke')]+Prod.loc[(y,'NewNuke')])['power_Dvar']/(Prod.loc[(y,slice(None))].sum()['power_Dvar']-Interco[y]['power_Dvar']) for y in YEAR}
    test={y:Fossils[y]+EnR[y] for y in YEAR}
    print('EnR+Fossils = ',test)

    sb.set_palette('muted')

    fig, ax = plt.subplots()
    width= 0.60
    x = np.arange(l_year)
    cpt=1
    for tech in TECHNO :
        l=list(Prod.loc[(slice(None),tech),'power_Dvar']/1000000)
        ax.bar(x + cpt*width/l_tech, l, width/l_tech, label=tech)
        cpt=cpt+1

    plt.xticks(x,['2020','2030','2040','2050'])#,'2060'])
    plt.title('Electricity production')
    plt.ylabel('TWh/an')
    plt.legend()

    plt.savefig(outputFolder+'/Electricity production.png')

    plt.show()

    fig, ax = plt.subplots()
    width = 0.60
    x = np.arange(l_year)
    cpt = 1
    for tech in TECHNO:
        l = list(Capa.loc[(slice(None), tech), 'capacity_Pvar'] / 1000)
        ax.bar(x + cpt * width / l_tech, l, width / l_tech, label=tech)
        cpt = cpt + 1

    plt.xticks(x, ['2020', '2030', '2040', '2050'])#,'2060'])
    plt.title('Installed capacity')
    plt.ylabel('GW')
    plt.legend()

    plt.savefig(outputFolder+'/Installed capacity.png')

    plt.show()

    return EnR, Fossils, Nuke

# First : execute ModelFrance.py

outputPath = "../data/output/"

scenarioName='Ref_wH2_Fr'
# timeStep=scenarioDictFr[scenarioName]['timeStep'].loc[0,'timeStep']
timeStep=1
outputFolderFr = outputPath + scenarioName


# plot_monotone(outputFolderFr)

EnR, Fossils, Nuke = plot_mixProdElec(outputFolderFr)#(timeStep, outputFolderFr, "France")
print("EnR = ", EnR, "\nFossils = ", Fossils, "\nNuke = ", Nuke)
