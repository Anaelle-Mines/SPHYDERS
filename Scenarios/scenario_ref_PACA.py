import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

from data.Raw import tech_eco_data

inputPath = "../data/Raw/"
outputFolderFr = "../data/output/ref_Fr_1h"
areaList = ["Marseille"]
y_act = "middle"

oneYear = 8760

timeStep = 1  # Only integers work
t = np.arange(1, oneYear + 1, timeStep)
nHours = len(t)

yearZero = 2010
yearFinal = 2050
yearStep = 10
yearList = [yr for yr in range(yearZero, yearFinal + yearStep, yearStep)]  # +1 to include the final year
nYears = len(yearList)

ctechs = [
    "WindOnShore",
    "WindOffShore_flot",
    "Solar",
    "SMR",
    "SMR + CCS1",
    "SMR + CCS2",
    "CCS1",
    "CCS2",
    "electrolysis_PEMEL",
    "electrolysis_AEL",
    "curtailment",
]

#------------------------------------------------------------------------------------------------------------------#

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


scenarioPACA_ref = {}

scenarioPACA_ref["areaList"] = areaList
scenarioPACA_ref["yearList"] = yearList
scenarioPACA_ref["lastTime"] = t[-1]
scenarioPACA_ref["timeStep"] = pd.DataFrame({"timeStep": [timeStep]})
scenarioPACA_ref["convTechList"] = ctechs


scenarioPACA_ref["economicParameters"] = pd.DataFrame(
    {
        "discountRate": [0.04],
        "financeRate": [0.04],
        "y_act": y_act,  # Moment of the period chosen for investments and actualisation. Possible values : 'beginning', 'middle', 'end'
    }
)


hourlyDemand_H2 = interp1d(
    yearList[1:],
    [360 * (1 + 0.025) ** (k * yearStep) for k in np.arange(len(yearList[1:]))],
    fill_value=(360, 755),
    bounds_error=False,
)


def demande_h2_area(area, year):
    """returns hydrogen yearly demand of an area in MWh"""
    if area == "Fos":
        return np.zeros(nHours)
    else:
        return hourlyDemand_H2(y_ref(year, y_act)) * np.ones(nHours) * timeStep


scenarioPACA_ref["resourceDemand"] = pd.concat(
    (
        pd.DataFrame(
            data={
                "AREA": area,
                "YEAR": year,
                "TIMESTAMP": t,  # We add the TIMESTAMP so that it can be used as an index later.
                "electricity": np.zeros(nHours),  # Only considering H2 final demand
                "hydrogen": demande_h2_area(area, year),
                "gaz": np.zeros(nHours),
            }
        )
        for k, year in enumerate(yearList[1:])
        for area in areaList
    )
)


scenarioPACA_ref["conversionTechs"] = []
for area in areaList:
    for k, year in enumerate(yearList[:-1]):
        tech = "WindOffShore"
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
                        "lifeSpan": lifespan,
                        "powerCost": 0,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 0,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": 0,
                    }
                }
            )
        )

        tech = "WindOffShore_flot"
        max_install_capacity = {2010: 0, 2020: 0, 2021:500, 2030: 1000}
        max_cumul_capacity = {2010: 0, 2020: 0, 2021:500, 2030: 1000}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
                        "lifeSpan": lifespan,
                        "powerCost": 0,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": interpolate(max_install_capacity, y_ref(year, y_act)),
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "WindOnShore"
        max_install_capacity = {2010: 0, 2020: 0, 2021:100}
        max_cumul_capacity = {2010: 0, 2020: 0, 2021:150}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
                        "lifeSpan": lifespan,
                        "powerCost": 0,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": interpolate(max_install_capacity, y_ref(year, y_act)),
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "Solar"
        max_install_capacity = {2010: 0, 2020: 0, 2021:100}
        max_cumul_capacity = {2010: 0, 2020: 0, 2021:150}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
                        "lifeSpan": lifespan,
                        "powerCost": 0,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": interpolate(max_install_capacity, y_ref(year, y_act)),
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "SMR"
        max_install_capacity = {2010: 411, 2020: 411, 2021:1000, 2030: 10000}
        min_install_capacity = {2010: 411, 2020: 411, 2021:0}
        max_cumul_capacity = {2010: 411, 2020: 411, 2021:1000, 2030: 10000}
        min_cumul_capacity = {2010: 411, 2020: 411, 2021:0}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
            min_install_capacity = {2010: 0, 2050: 0}
            min_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Hydrogen production",
                        "lifeSpan": lifespan,
                        "powerCost": 0.21,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": interpolate(min_install_capacity, y_ref(year, y_act)),
                        "maxInstallCapacity": interpolate(max_install_capacity, y_ref(year, y_act)),
                        "EmissionCO2": 0,
                        "Conversion": {"hydrogen": 1, "gaz": -1.28},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": interpolate(min_cumul_capacity, y_ref(year, y_act)),
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                        "RampConstraintPlus": 0.3,
                    }
                }
            )
        )

        tech = "SMR + CCS1"
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Hydrogen production",
                        "lifeSpan": lifespan,
                        "powerCost": 7.71,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": -150,
                        "Conversion": {"hydrogen": 1, "gaz": -1.32},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                        "RampConstraintPlus": 0.3,
                    }
                }
            )
        )

        tech = "SMR + CCS2"
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Hydrogen production",
                        "lifeSpan": lifespan,
                        "powerCost": 13.7,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": -270,
                        "Conversion": {"hydrogen": 1, "gaz": -1.45},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                        "RampConstraintPlus": 0.3,
                    }
                }
            )
        )

        tech = "CCS1"
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Hydrogen support",
                        "lifeSpan": lifespan,
                        "powerCost": 0,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"hydrogen": 0},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "CCS2"
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Hydrogen support",
                        "lifeSpan": lifespan,
                        "powerCost": 0,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"hydrogen": 0},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "SMR_elec"
        max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Hydrogen production",
                        "lifeSpan": lifespan,
                        "powerCost": 0,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 0,
                        "EmissionCO2": 0,
                        "Conversion": {"hydrogen": 1, "gaz": -0.91, "electricity": -0.4},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                        "RampConstraintPlus": 0.3,
                    }
                }
            )
        )

        tech = "SMR_elecCCS1"
        max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Hydrogen production",
                        "lifeSpan": lifespan,
                        "powerCost": 0,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 0,
                        "EmissionCO2": -156,
                        "Conversion": {"hydrogen": 1, "gaz": -0.91, "electricity": -0.57},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                        "RampConstraintPlus": 0.3,
                    }
                }
            )
        )

        tech = "electrolysis_AEL"
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Hydrogen production",
                        "lifeSpan": lifespan,
                        "powerCost": 0,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"hydrogen": 1, "electricity": -1.54},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "electrolysis_PEMEL"
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Hydrogen production",
                        "lifeSpan": lifespan,
                        "powerCost": 0,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"hydrogen": 1, "electricity": -1.67},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "curtailment"
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Hydrogen production",
                        "lifeSpan": lifespan,
                        "powerCost": 3000,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"hydrogen": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": 100000,
                    }
                }
            )
        )

scenarioPACA_ref["conversionTechs"] = pd.concat(
    scenarioPACA_ref["conversionTechs"], axis=1
)

scenarioPACA_ref["storageTechs"] = []
for area in areaList:
    for k, year in enumerate(yearList[:-1]):
        tech = "Battery"
        max_install_capacity = {2010: 0, 2020: 500, 2030: 1000, 2040: 7700}
        max_install_power = {2010: 0, 2020: 50, 2030: 100, 2040: 770}
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

        scenarioPACA_ref["storageTechs"].append(
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
        scenarioPACA_ref["storageTechs"].append(
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
        max_install_capacity = {2010: 0, 2050: 0}
        max_install_power = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioPACA_ref["storageTechs"].append(
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

scenarioPACA_ref["storageTechs"] = pd.concat(scenarioPACA_ref["storageTechs"], axis=1)

scenarioPACA_ref["carbonTax"] = pd.DataFrame(
    data=np.linspace(0.0675, 0.165, nYears), index=yearList, columns=("carbonTax",)
)

scenarioPACA_ref["carbonGoals"] = pd.DataFrame(
    data=np.linspace(974e6, 205e6, nYears), index=yearList, columns=("carbonGoals",)
)

impBiogasCap = np.linspace(0, 5e6, nYears)
# impH2Cap=np.linspace(0, 30e6, nYears)
scenarioPACA_ref["maxImportCap"] = pd.concat(
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

# expH2Cap=np.linspace(0, 30e6, nYears)
scenarioPACA_ref["maxExportCap"] = pd.concat(
    (
        pd.DataFrame(
            index=[year],
            data={"electricity": 0, "gazNat": 0, "gazBio": 0, "hydrogen": 0, "gaz": 0},  # 10e6,
        )
        for k, year in enumerate(yearList[1:])
    )
)


df_res_ref = pd.read_csv(
    inputPath + "/set2019_horaire_TIMExRES.csv", sep=",", decimal=".", skiprows=0, comment="#"
).set_index(["TIMESTAMP", "RESOURCES"])
df_elecPrice = pd.read_csv(outputFolderFr + "/marketPrice.csv").set_index(["YEAR_op", "TIMESTAMP"])
df_elecCarbon = pd.read_csv(outputFolderFr + "/carbon.csv").set_index(["YEAR_op", "TIMESTAMP"])
gridConnection = pd.read_csv(
    inputPath + "CalendrierHTB_TIME.csv", sep=",", decimal=".", skiprows=0, comment="#"
).set_index(["TIMESTAMP"])

t8760 = df_res_ref.index.get_level_values("TIMESTAMP").unique().values
tmoy = []
for i in np.arange(len(t)):
    tmoy += [t[i]] * timeStep

tmoy = tmoy[:8760]
calendar = gridConnection["Calendrier"].loc[t]
gridConnection["TIME"] = tmoy
scenarioPACA_ref["gridConnection"] = (
    gridConnection[["HTB", "TIME"]]
    .groupby(["TIME"])
    .mean()
    .reset_index()
    .rename(columns={"TIME": "TIMESTAMP"})
)
scenarioPACA_ref["gridConnection"]["Calendrier"] = calendar.values
scenarioPACA_ref["gridConnection"].set_index("TIMESTAMP", inplace=True)
scenarioPACA_ref["turpeFactorsHTB"] = pd.DataFrame(
    columns=["HORAIRE", "fixeTurpeHTB"],
    data={"P": 5880, "HPH": 5640, "HCH": 5640, "HPE": 5280, "HCE": 4920}.items(),
).set_index(
    "HORAIRE"
)  # en €/MW/an part abonnement


biogasPrice = {2020: 120, 2030: 105, 2040:90 , 2050:75} # €/MWh
hdyrogenPrice = {2020: 6, 2030: 6, 2040:6, 2050:6} # €/kg

scenarioPACA_ref["resourceImportPrices"] = pd.concat(
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
                "hydrogen": interpolate(hdyrogenPrice, y_ref(year, y_act)) * 30 * np.ones(oneYear),
                "gaz": 100000 * np.ones(oneYear),
            }
        )
        for k, year in enumerate(yearList[1:])
        for area in areaList
    )
)


scenarioPACA_ref["resourceImportPrices"] = (
    scenarioPACA_ref["resourceImportPrices"]
    .groupby(["AREA", "YEAR", "TIMESTAMP"])
    .mean()
    .reset_index()
)

scenarioPACA_ref["resourceImportCO2eq"] = pd.concat(
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

scenarioPACA_ref["resourceImportCO2eq"] = (
    scenarioPACA_ref["resourceImportCO2eq"]
    .groupby(["AREA", "YEAR", "TIMESTAMP"])
    .mean()
    .reset_index()
)


availabilityFactor = pd.read_csv(
    inputPath + "/availabilityFactor2019_PACA_TIMExTECH.csv", sep=",", decimal=".", skiprows=0
).set_index(["TIMESTAMP", "TECHNOLOGIES"])
techs = list(availabilityFactor.index.get_level_values("TECHNOLOGIES").unique())

scenarioPACA_ref["availability"] = []
for year in yearList[1:]:
    for tech in techs:
        scenarioPACA_ref["availability"].append(
            pd.DataFrame(
                data={
                    "YEAR": year,
                    "TIMESTAMP": tmoy,
                    "TECHNOLOGIES": tech,
                    "availabilityFactor": availabilityFactor.loc[
                        (slice(None), tech), "availabilityFactor"
                    ].values,
                }
            )
        )

scenarioPACA_ref["availability"] = pd.concat(scenarioPACA_ref["availability"], axis=0)
scenarioPACA_ref["availability"] = (
    scenarioPACA_ref["availability"]
    .reset_index()
    .groupby(["YEAR", "TIMESTAMP", "TECHNOLOGIES"])
    .mean()
    .drop(columns="index")
)
itechs = scenarioPACA_ref["availability"].index.isin(ctechs, level=2)
scenarioPACA_ref["availability"] = scenarioPACA_ref["availability"].loc[
    (slice(None), slice(None), itechs)
]

scenarioPACA_ref["transitionFactors"] = pd.DataFrame(
    {"TECHNO1": ["SMR", "SMR"], "TECHNO2": ["SMR + CCS1", "SMR + CCS2"], "TransFactor": 1}
).set_index(["TECHNO1", "TECHNO2"])

