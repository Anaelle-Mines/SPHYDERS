import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd

from data.Raw import tech_eco_data
from Functions.loadScenario import loadScenario
from Scenarios.scenario_creation import scenarioDict

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


scenarioList=['gas_x5','BM_60','CO2_100','import_H2','Re_inf','woSMR_2040','expensiveRE','cheap_H2','expensiveRE']

scenarioDict_Cavern_robustness={'Cavern':scenarioDict['Cavern']}

for s in scenarioList:
    scenarioName=s+'Cavern'
    scenario={k: v.copy() for (k, v) in scenarioDict[s].items()}

    scenario["storageTechs"] = []
    for area in areaList:
        for k, year in enumerate(yearList[:-1]):
            tech = "Battery"
            max_install_capacity = {2010: 0, 2020: 0}
            max_install_power = {2010: 0, 2020: 0}
            if area != "Marseille":
                max_install_capacity = {2010: 0, 2050: 0}
            capex1, opex1, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech + " - 1h", hyp="ref", year=y_ref(year, y_act)
            )
            capex4, opex4, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech + " - 4h", hyp="ref", year=y_ref(year, y_act)
            )
            capex_per_kWh = (capex4 - capex1) / 3
            capex_per_kW = capex1 - capex_per_kWh

            scenario["storageTechs"].append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "resource": "electricity",
                            "storagelifeSpan": lifespan,
                            "storagePowerCost": capex_per_kW,
                            "storageEnergyCost": capex_per_kWh,
                            "storageOperationCost": opex1,
                            "p_max": interpolate(max_install_power, y_ref(year, y_act)),
                            "c_max": interpolate(max_install_capacity, y_ref(year, y_act)),
                            "chargeFactors": {"electricity": 0.9200},
                            "dischargeFactors": {"electricity": 1.09},
                            "dissipation": 0.0085,
                        },
                    }
                )
            )

            tech = "tankH2_G"
            max_install_capacity = {2010: 0, 2020: 10000, 2030: 20000, 2040: 30000}
            max_install_power = {2010: 0, 2020: 1000, 2030: 2000, 2040: 3000}
            if area != "Marseille":
                max_install_capacity = {2010: 0, 2050: 0}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            scenario["storageTechs"].append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "resource": "hydrogen",
                            "storagelifeSpan": lifespan,
                            "storagePowerCost": capex * 0.7,
                            "storageEnergyCost": capex * 0.3,
                            "storageOperationCost": opex,
                            "p_max": interpolate(max_install_power, y_ref(year, y_act)),
                            "c_max": interpolate(max_install_capacity, y_ref(year, y_act)),
                            "chargeFactors": {"electricity": 0.0168, "hydrogen": 1},
                            "dischargeFactors": {"hydrogen": 1},
                            "dissipation": 0,
                        },
                    }
                )
            )

            tech = "saltCavernH2_G"
            max_install_capacity = {2010: 0, 2020: 0, 2021 : 130000, 2030:130000}
            max_install_power = {2010: 0, 2020: 0, 2021:13000, 2030:13000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            scenario["storageTechs"].append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "resource": "hydrogen",
                            "storagelifeSpan": lifespan,
                            "storagePowerCost": capex,
                            "storageEnergyCost": 280,
                            "storageOperationCost": opex,
                            "p_max": interpolate(max_install_power, y_ref(year, y_act)),
                            "c_max": interpolate(max_install_capacity, y_ref(year, y_act)),
                            "chargeFactors": {"electricity": 0.0168, "hydrogen": 1},
                            "dischargeFactors": {"hydrogen": 1},
                            "dissipation": 0,
                        },
                    }
                )
            )

    scenario["storageTechs"] = pd.concat(scenario["storageTechs"], axis=1)

    scenarioDict_Cavern_robustness[scenarioName]=scenario
