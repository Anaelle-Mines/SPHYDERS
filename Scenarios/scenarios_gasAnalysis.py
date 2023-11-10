import os

os.sys.path.append(r"../")
import time

import pandas as pd
import numpy as np
from pyomo.environ import SolverFactory
from data.Raw import tech_eco_data
from Functions.f_multiResourceModels_multiNodes import systemModel_multiResource_multiNodes,ElecPrice_optim
from Functions.f_optimization import getConstraintsDual_panda, getVariables_panda
from Functions.f_extract_data import extract_energy
from Functions.loadScenario import loadScenario
from Scenarios.scenario_ref_Fr import scenarioFr
from Scenarios.scenario_ref_PACA import scenarioPACA_ref

inputPath="../data/Raw/"
outputPath = "../data/output/gasAnalysis/"
solver = "mosek"

#----------------------------------------------------------------------------------------------------------------------------#

priceList=[15,20,30,40,50,60,70,80,90,100]
y_act = "middle"

def interpolate(dic, y):
    years = np.sort(list(dic.keys()))
    val = [dic[y] for y in years]
    return float(np.interp(y, years, val))


def y_ref(y, y_act="middle"):
    if y_act == "beginning":
        return y
    elif y_act == "middle":
        return y + yearStep / 2
    elif y_act == "end":
        return y + yearStep

oneYear = 8760

timeStep = 1  # Only integers work
t = np.arange(1, oneYear + 1, timeStep)
nHours = len(t)

t8760 = np.arange(1, oneYear + 1, 1)
tmoy = []
for i in np.arange(len(t)):
    tmoy += [t[i]] * timeStep
tmoy = tmoy[:8760]

yearZero = 2010
yearFinal = 2050
yearStep = 10
yearList = [
    yr for yr in range(yearZero, yearFinal + yearStep, yearStep)
]  # +1 to include the final year
nYears = len(yearList)

df_res_ref = pd.read_csv(inputPath + "/set2019_horaire_TIMExRES.csv", sep=",", decimal=".", skiprows=0, comment="#").set_index(["TIMESTAMP", "RESOURCES"])
gasPrice_mean=np.mean(df_res_ref.loc[(slice(None), "gazNat"), "importCost"].values)
biogasPrice = {2020: 120, 2030: 105, 2040:90 , 2050:75}

scenarioDict_gasAnalysis_Fr={}
for price in priceList:
    scenarioName='scenario_'+str(price)
    scenario_Fr={k: v.copy() for (k, v) in scenarioFr.items()}
    scenario_Fr["resourceImportPrices"] = pd.concat(
        (
            pd.DataFrame(
                data={
                    "AREA": area,
                    "YEAR": year,
                    "TIMESTAMP": tmoy,
                    "electricity": 100000 * np.ones(oneYear),
                    "gazNat": df_res_ref.loc[(slice(None), "gazNat"), "importCost"].values*(1 if year <= 2020 else price/gasPrice_mean),
                    "gazBio": interpolate(biogasPrice, y_ref(year, y_act)) * np.ones(oneYear),
                    "hydrogen": 100000 * np.ones(oneYear),
                    "gaz": 100000 * np.ones(oneYear),
                    "uranium": 3.3 * np.ones(oneYear),
                }
            )
            for k, year in enumerate(yearList[1:])
            for area in ["France"]
        )
    )
    scenario_Fr["resourceImportPrices"] = (scenario_Fr["resourceImportPrices"].groupby(["AREA", "YEAR", "TIMESTAMP"]).mean().reset_index())

    scenarioDict_gasAnalysis_Fr[scenarioName+'_Fr']=scenario_Fr


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

scenarioDict_gasAnalysis_PACA={}

areaList=['Marseille']
hdyrogenPrice = {2020: 6, 2030: 6, 2040:6, 2050:6} # €/kg
for price in priceList: 
    scenarioName='scenario_'+str(price)
    outputFolderFr=outputPath+'scenario_'+str(price)+'_Fr'
    scenario_PACA={k: v.copy() for (k, v) in scenarioPACA_ref.items()}

    df_elecPrice = pd.read_csv(outputFolderFr + "/marketPrice.csv").set_index(["YEAR_op", "TIMESTAMP"])
    df_elecCarbon = pd.read_csv(outputFolderFr + "/carbon.csv").set_index(["YEAR_op", "TIMESTAMP"])

    scenario_PACA["resourceImportPrices"] = pd.concat(
        (
            pd.DataFrame(
                data={
                    "AREA": area,
                    "YEAR": year,
                    "TIMESTAMP": tmoy,
                    "electricity": df_elecPrice.xs(year, level="YEAR_op")["OldPrice_NonAct"]
                    .reindex(pd.Index(tmoy, name="TIMESTAMP"), method="nearest")
                    .values,  # This is needed to resample electricity prices to tmoy length (8760), even for timeSteps in the FR model higher than 1
                    "gazNat": df_res_ref.loc[(slice(None), "gazNat"), "importCost"].values*(1 if year <= 2020 else price/gasPrice_mean),
                    "gazBio": interpolate(biogasPrice, y_ref(year, y_act)) * np.ones(oneYear),
                    "hydrogen": interpolate(hdyrogenPrice, y_ref(year, y_act)) * 30 * np.ones(oneYear),
                    "gaz": 100000 * np.ones(oneYear),
                }
            )
            for k, year in enumerate(yearList[1:])
            for area in areaList
        )
    )

    scenario_PACA["resourceImportPrices"] = (
        scenario_PACA["resourceImportPrices"]
        .groupby(["AREA", "YEAR", "TIMESTAMP"])
        .mean()
        .reset_index()
    )

    scenario_PACA["resourceImportCO2eq"] = pd.concat(
        (
            pd.DataFrame(
                data={
                    "AREA": area,
                    "YEAR": year,
                    "TIMESTAMP": tmoy,
                    "electricity": df_elecCarbon.xs(year, level="YEAR_op")["carbonContent"]
                    .reindex(pd.Index(tmoy, name="TIMESTAMP"), method="nearest")
                    .values,  # This is needed to resample carbon content to tmoy length (8760), even for timeSteps in the FR model higher than 1
                    "gaz": max(0, 0.03 * (1 - (y_ref(year, y_act) - yearZero) / (2050 - yearZero)))
                    * 29
                    / 13.1
                    + 203.5
                    * (
                        1 - tech_eco_data.get_biogas_share_in_network_RTE(y_ref(year, y_act))
                    ),  # Taking 100 yr GWP of methane and 3% losses due to upstream leaks. Losses drop to zero in 2050.
                    "gazNat": max(0, 0.03 * (1 - (y_ref(year, y_act) - yearZero) / (2050 - yearZero)))
                    * 29
                    / 13.1
                    + 203.5
                    * (
                        1 - tech_eco_data.get_biogas_share_in_network_RTE(y_ref(year, y_act))
                    ),  # Taking 100 yr GWP of methane and 3% losses due to upstream leaks. Losses drop to zero in 2050.
                    "gazBio": max(0, 0.03 * (1 - (y_ref(year, y_act) - yearZero) / (2050 - yearZero)))
                    * 29
                    / 13.1,
                    "hydrogen": max(
                        0, 0.05 - 0.03 * (y_ref(year, y_act) - yearZero) / (2050 - yearZero)
                    )
                    * 11
                    / 33,  # Taking 100 yr GWP of H2 and 5% losses due to upstream leaks. Leaks fall to 2% in 2050 See: https://www.energypolicy.columbia.edu/research/commentary/hydrogen-leakage-potential-risk-hydrogen-economy
                }
            )
            for k, year in enumerate(yearList[1:])
            for area in areaList
        )
    )

    scenario_PACA["resourceImportCO2eq"] = (
        scenario_PACA["resourceImportCO2eq"]
        .groupby(["AREA", "YEAR", "TIMESTAMP"])
        .mean()
        .reset_index()
    )

    scenarioDict_gasAnalysis_PACA[scenarioName+'_PACA'] = scenario_PACA


