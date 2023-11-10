import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

from data.Raw import tech_eco_data
from Scenarios.scenario_ref_PACA import scenarioPACA_ref

inputPath = "../data/Raw/"
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


outputFolderFr = "../data/output/ref_Fr_1h"
scenarioImportH2={k: v.copy() for (k, v) in scenarioPACA_ref.items()}


df_res_ref = pd.read_csv(
    inputPath + "/set2019_horaire_TIMExRES.csv", sep=",", decimal=".", skiprows=0, comment="#"
).set_index(["TIMESTAMP", "RESOURCES"])
df_elecPrice = pd.read_csv(outputFolderFr + "/marketPrice.csv").set_index(["YEAR_op", "TIMESTAMP"])


t8760 = df_res_ref.index.get_level_values("TIMESTAMP").unique().values
tmoy = []
for i in np.arange(len(t)):
    tmoy += [t[i]] * timeStep

tmoy = tmoy[:8760]


gasPriceFactor = {
    2020: 1,
    2050: 2,
}  # First term : factor for 2020 (price same as 2019) and second term : multiplicative factor in 2050 compare to 2019 prices
biogasPrice = {2020: 120, 2030: 105, 2040:90 , 2050:75} # €/MWh
hdyrogenPrice = {2020: 6, 2030: 4, 2040:3, 2050:2} # €/kg

scenarioImportH2["resourceImportPrices"] = pd.concat(
    (
        pd.DataFrame(
            data={
                "AREA": area,
                "YEAR": year,
                "TIMESTAMP": tmoy,
                "electricity": df_elecPrice.xs(year, level="YEAR_op")["OldPrice_NonAct"]
                .reindex(pd.Index(tmoy, name="TIMESTAMP"), method="nearest")
                .values,  # This is needed to resample electricity prices to tmoy length (8760), even for timeSteps in the FR model higher than 1
                "gazNat": df_res_ref.loc[(slice(None), "gazNat"), "importCost"].values
                * (1 if year <= 2020 else 2),
                "gazBio": interpolate(biogasPrice, y_ref(year, y_act)) * np.ones(oneYear),
                "hydrogen": interpolate(hdyrogenPrice, y_ref(year, y_act))* 30 * np.ones(oneYear),
                "gaz": 100000 * np.ones(oneYear),
            }
        )
        for k, year in enumerate(yearList[1:])
        for area in areaList
    )
)

scenarioImportH2["resourceImportPrices"] = (
    scenarioImportH2["resourceImportPrices"]
    .groupby(["AREA", "YEAR", "TIMESTAMP"])
    .mean()
    .reset_index()
)


impBiogasCap = np.linspace(0, 5e6, nYears)
# impH2Cap=np.linspace(0, 30e6, nYears)
scenarioImportH2["maxImportCap"] = pd.concat(
    (
        pd.DataFrame(
            index=[year],
            data={
                "electricity": 10e10,
                "gazNat": 10e10,
                "gazBio": impBiogasCap[k + 1],
                "hydrogen": 10e10,
                "gaz": 0,
            },
        )
        for k, year in enumerate(yearList[1:])
    )
)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

outputFolderFr = "../data/output/ref_Fr_1h"
scenarioCheapH2={k: v.copy() for (k, v) in scenarioPACA_ref.items()}


df_elecPrice = pd.read_csv(outputFolderFr + "/marketPrice.csv").set_index(["YEAR_op", "TIMESTAMP"])

t8760 = df_res_ref.index.get_level_values("TIMESTAMP").unique().values
tmoy = []
for i in np.arange(len(t)):
    tmoy += [t[i]] * timeStep

tmoy = tmoy[:8760]


gasPriceFactor = {
    2020: 1,
    2050: 2,
}  # First term : factor for 2020 (price same as 2019) and second term : multiplicative factor in 2050 compare to 2019 prices
biogasPrice = {2020: 120, 2030: 105, 2040:90 , 2050:75} # €/MWh
hdyrogenPrice = {2020: 6, 2030: 2, 2040:2, 2050:2} # €/kg

scenarioCheapH2["resourceImportPrices"] = pd.concat(
    (
        pd.DataFrame(
            data={
                "AREA": area,
                "YEAR": year,
                "TIMESTAMP": tmoy,
                "electricity": df_elecPrice.xs(year, level="YEAR_op")["OldPrice_NonAct"]
                .reindex(pd.Index(tmoy, name="TIMESTAMP"), method="nearest")
                .values,  # This is needed to resample electricity prices to tmoy length (8760), even for timeSteps in the FR model higher than 1
                "gazNat": df_res_ref.loc[(slice(None), "gazNat"), "importCost"].values
                * (1 if year <= 2020 else 2),
                "gazBio": interpolate(biogasPrice, y_ref(year, y_act)) * np.ones(oneYear),
                "hydrogen": interpolate(hdyrogenPrice, y_ref(year, y_act))* 30 * np.ones(oneYear),
                "gaz": 100000 * np.ones(oneYear),
            }
        )
        for k, year in enumerate(yearList[1:])
        for area in areaList
    )
)

scenarioCheapH2["resourceImportPrices"] = (
    scenarioCheapH2["resourceImportPrices"]
    .groupby(["AREA", "YEAR", "TIMESTAMP"])
    .mean()
    .reset_index()
)


impBiogasCap = np.linspace(0, 5e6, nYears)
# impH2Cap=np.linspace(0, 30e6, nYears)
scenarioCheapH2["maxImportCap"] = pd.concat(
    (
        pd.DataFrame(
            index=[year],
            data={
                "electricity": 10e10,
                "gazNat": 10e10,
                "gazBio": impBiogasCap[k + 1],
                "hydrogen": 10e10,
                "gaz": 0,
            },
        )
        for k, year in enumerate(yearList[1:])
    )
)
