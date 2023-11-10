import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

from data.Raw import tech_eco_data
from Scenarios.scenario_ref_PACA import scenarioPACA_ref
from Scenarios.scenarios_sensitivityRE import scenarioREinf

inputPath = "../data/Raw/"
outputFolderFr = "../data/output/ref_Fr_1h"
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


scenarioCavern={k: v.copy() for (k, v) in scenarioPACA_ref.items()}


scenarioCavern["storageTechs"] = []
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

        scenarioCavern["storageTechs"].append(
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
        scenarioCavern["storageTechs"].append(
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
        scenarioCavern["storageTechs"].append(
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

scenarioCavern["storageTechs"] = pd.concat(scenarioCavern["storageTechs"], axis=1)


#------------------------------------------------------------------------------------------------------------#



scenarioCavernREinf={k: v.copy() for (k, v) in scenarioREinf.items()}


scenarioCavernREinf["storageTechs"] = []
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

        scenarioCavernREinf["storageTechs"].append(
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
        scenarioCavernREinf["storageTechs"].append(
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
        max_install_capacity = {2010: 0, 2020: 0, 2030:130000}
        max_install_power = {2010: 0, 2020: 0, 2030:13000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioCavernREinf["storageTechs"].append(
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

scenarioCavernREinf["storageTechs"] = pd.concat(scenarioCavernREinf["storageTechs"], axis=1)


#------------------------------------------------------------------------------------------------------------------"


scenarioCavern2040={k: v.copy() for (k, v) in scenarioPACA_ref.items()}


scenarioCavern2040["storageTechs"] = []
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

        scenarioCavern2040["storageTechs"].append(
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
        scenarioCavern2040["storageTechs"].append(
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
        max_install_capacity = {2010: 0, 2020: 0, 2030:0, 2031: 130000, 2040:130000}
        max_install_power = {2010: 0, 2020: 0, 2030:0, 2031: 13000, 2040:13000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioCavern2040["storageTechs"].append(
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

scenarioCavern2040["storageTechs"] = pd.concat(scenarioCavern2040["storageTechs"], axis=1)


