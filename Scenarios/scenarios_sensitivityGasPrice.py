import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

from data.Raw import tech_eco_data
from Scenarios.scenario_ref_PACA import scenarioPACA_ref

inputPath = "../data/Raw/"
outputFolderFr = "../data/output/gas1_Fr_1h"
areaList = ["Marseille"]
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

yearZero = 2010
yearFinal = 2050
yearStep = 10
yearList = [
    yr for yr in range(yearZero, yearFinal + yearStep, yearStep)
]  # +1 to include the final year
nYears = len(yearList)


scenarioGas1={k: v.copy() for (k, v) in scenarioPACA_ref.items()}


df_res_ref = pd.read_csv(
    inputPath + "/set2019_horaire_TIMExRES.csv", sep=",", decimal=".", skiprows=0, comment="#"
).set_index(["TIMESTAMP", "RESOURCES"])
df_elecPrice = pd.read_csv(outputFolderFr + "/marketPrice.csv").set_index(["YEAR_op", "TIMESTAMP"])


t8760 = df_res_ref.index.get_level_values("TIMESTAMP").unique().values
tmoy = []
for i in np.arange(len(t)):
    tmoy += [t[i]] * timeStep

tmoy = tmoy[:8760]


biogasPrice = {2020: 120, 2030: 105, 2040:90 , 2050:75}
hdyrogenPrice = {2020: 6, 2030: 6, 2040:6, 2050:6} # €/kg

scenarioGas1["resourceImportPrices"] = pd.concat(
    (
        pd.DataFrame(
            data={
                "AREA": area,
                "YEAR": year,
                "TIMESTAMP": tmoy,
                "electricity": df_elecPrice.xs(year, level="YEAR_op")["OldPrice_NonAct"]
                .reindex(pd.Index(tmoy, name="TIMESTAMP"), method="nearest")
                .values,  # This is needed to resample electricity prices to tmoy length (8760), even for timeSteps in the FR model higher than 1
                "gazNat": df_res_ref.loc[(slice(None), "gazNat"), "importCost"].values,
                "gazBio": interpolate(biogasPrice, y_ref(year, y_act)) * np.ones(oneYear),
                "hydrogen": interpolate(hdyrogenPrice, y_ref(year, y_act)) * 30 * np.ones(oneYear),
                "gaz": 100000 * np.ones(oneYear),
            }
        )
        for k, year in enumerate(yearList[1:])
        for area in areaList
    )
)

scenarioGas1["resourceImportPrices"] = (
    scenarioGas1["resourceImportPrices"]
    .groupby(["AREA", "YEAR", "TIMESTAMP"])
    .mean()
    .reset_index()
)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

outputFolderFr =  "../data/output/gas5_Fr_1h"

scenarioGas5={k: v.copy() for (k, v) in scenarioPACA_ref.items()}

df_elecPrice = pd.read_csv(outputFolderFr + "/marketPrice.csv").set_index(["YEAR_op", "TIMESTAMP"])

biogasPrice = {2020: 120, 2030: 105, 2040:90 , 2050:75}
hdyrogenPrice = {2020: 6, 2030: 6, 2040:6, 2050:6} # €/kg
gasPriceFactor = 5

scenarioGas5["resourceImportPrices"] = pd.concat(
    (
        pd.DataFrame(
            data={
                "AREA": area,
                "YEAR": year,
                "TIMESTAMP": tmoy,
                "electricity": df_elecPrice.xs(year, level="YEAR_op")["OldPrice_NonAct"]
                .reindex(pd.Index(tmoy, name="TIMESTAMP"), method="nearest")
                .values,  # This is needed to resample electricity prices to tmoy length (8760), even for timeSteps in the FR model higher than 1
                "gazNat": df_res_ref.loc[(slice(None), "gazNat"), "importCost"].values*(1 if year <= 2020 else gasPriceFactor),
                "gazBio": interpolate(biogasPrice, y_ref(year, y_act)) * np.ones(oneYear),
                "hydrogen": interpolate(hdyrogenPrice, y_ref(year, y_act)) * 30 * np.ones(oneYear),
                "gaz": 100000 * np.ones(oneYear),
            }
        )
        for k, year in enumerate(yearList[1:])
        for area in areaList
    )
)

scenarioGas5["resourceImportPrices"] = (
    scenarioGas5["resourceImportPrices"]
    .groupby(["AREA", "YEAR", "TIMESTAMP"])
    .mean()
    .reset_index()
)
