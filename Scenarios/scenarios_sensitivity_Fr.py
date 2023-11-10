import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

from data.Raw import tech_eco_data
from Scenarios.scenario_ref_Fr import scenarioFr

inputPath = "../data/Raw/"
areaList = ["France"]
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

t8760 = np.arange(1, oneYear + 1, 1)
tmoy = []
for i in np.arange(len(t)):
    tmoy += [t[i]] * timeStep
tmoy = tmoy[:8760]

scenarioGas1_Fr={k: v.copy() for (k, v) in scenarioFr.items()}

df_res_ref = pd.read_csv(inputPath + "/set2019_horaire_TIMExRES.csv", sep=",", decimal=".", skiprows=0, comment="#").set_index(["TIMESTAMP", "RESOURCES"])
biogasPrice = {2020: 120, 2030: 105, 2040:90 , 2050:75}
scenarioGas1_Fr["resourceImportPrices"] = pd.concat(
    (
        pd.DataFrame(
            data={
                "AREA": area,
                "YEAR": year,
                "TIMESTAMP": tmoy,
                "electricity": 100000 * np.ones(oneYear),
                "gazNat": df_res_ref.loc[(slice(None), "gazNat"), "importCost"].values,
                "gazBio": interpolate(biogasPrice, y_ref(year, y_act)) * np.ones(oneYear),
                "hydrogen": 100000 * np.ones(oneYear),
                "gaz": 100000 * np.ones(oneYear),
                "uranium": 3.3 * np.ones(oneYear),
            }
        )
        for k, year in enumerate(yearList[1:])
        for area in areaList
    )
)

scenarioGas1_Fr["resourceImportPrices"] = (
    scenarioGas1_Fr["resourceImportPrices"].groupby(["AREA", "YEAR", "TIMESTAMP"]).mean().reset_index()
)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


scenarioGas5_Fr={k: v.copy() for (k, v) in scenarioFr.items()}


df_res_ref = pd.read_csv(inputPath + "/set2019_horaire_TIMExRES.csv", sep=",", decimal=".", skiprows=0, comment="#").set_index(["TIMESTAMP", "RESOURCES"])
gasPriceFactor = 5
biogasPrice = {2020: 120, 2030: 105, 2040:90 , 2050:75}
scenarioGas5_Fr["resourceImportPrices"] = pd.concat(
    (
        pd.DataFrame(
            data={
                "AREA": area,
                "YEAR": year,
                "TIMESTAMP": tmoy,
                "electricity": 100000 * np.ones(oneYear),
                "gazNat": df_res_ref.loc[(slice(None), "gazNat"), "importCost"].values*(1 if year <= 2020 else gasPriceFactor),
                "gazBio": interpolate(biogasPrice, y_ref(year, y_act)) * np.ones(oneYear),
                "hydrogen": 100000 * np.ones(oneYear),
                "gaz": 100000 * np.ones(oneYear),
                "uranium": 3.3 * np.ones(oneYear),
            }
        )
        for k, year in enumerate(yearList[1:])
        for area in areaList
    )
)

scenarioGas5_Fr["resourceImportPrices"] = (
    scenarioGas5_Fr["resourceImportPrices"].groupby(["AREA", "YEAR", "TIMESTAMP"]).mean().reset_index()
)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#



scenarioBM60_Fr={k: v.copy() for (k, v) in scenarioFr.items()}


df_res_ref = pd.read_csv(inputPath + "/set2019_horaire_TIMExRES.csv", sep=",", decimal=".", skiprows=0, comment="#").set_index(["TIMESTAMP", "RESOURCES"])
biogasPrice = {2020: 120, 2030: 100, 2040:80, 2050:60}
scenarioBM60_Fr["resourceImportPrices"] = pd.concat(
    (
        pd.DataFrame(
            data={
                "AREA": area,
                "YEAR": year,
                "TIMESTAMP": tmoy,
                "electricity": 100000 * np.ones(oneYear),
                "gazNat": df_res_ref.loc[(slice(None), "gazNat"), "importCost"].values**(1 if year <= 2020 else 2),
                "gazBio": interpolate(biogasPrice, y_ref(year, y_act)) * np.ones(oneYear),
                "hydrogen": 100000 * np.ones(oneYear),
                "gaz": 100000 * np.ones(oneYear),
                "uranium": 3.3 * np.ones(oneYear),
            }
        )
        for k, year in enumerate(yearList[1:])
        for area in areaList
    )
)

scenarioBM60_Fr["resourceImportPrices"] = (
    scenarioBM60_Fr["resourceImportPrices"].groupby(["AREA", "YEAR", "TIMESTAMP"]).mean().reset_index()
)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


scenarioBM90_Fr={k: v.copy() for (k, v) in scenarioFr.items()}


df_res_ref = pd.read_csv(inputPath + "/set2019_horaire_TIMExRES.csv", sep=",", decimal=".", skiprows=0, comment="#").set_index(["TIMESTAMP", "RESOURCES"])
biogasPrice =  {2020: 120, 2030: 110, 2040: 100, 2050: 90}
scenarioBM90_Fr["resourceImportPrices"] = pd.concat(
    (
        pd.DataFrame(
            data={
                "AREA": area,
                "YEAR": year,
                "TIMESTAMP": tmoy,
                "electricity": 100000 * np.ones(oneYear),
                "gazNat": df_res_ref.loc[(slice(None), "gazNat"), "importCost"].values**(1 if year <= 2020 else 2),
                "gazBio": interpolate(biogasPrice, y_ref(year, y_act)) * np.ones(oneYear),
                "hydrogen": 100000 * np.ones(oneYear),
                "gaz": 100000 * np.ones(oneYear),
                "uranium": 3.3 * np.ones(oneYear),
            }
        )
        for k, year in enumerate(yearList[1:])
        for area in areaList
    )
)

scenarioBM90_Fr["resourceImportPrices"] = (
    scenarioBM90_Fr["resourceImportPrices"].groupby(["AREA", "YEAR", "TIMESTAMP"]).mean().reset_index()
)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
scenarioExpensiveRE_Fr={k: v.copy() for (k, v) in scenarioFr.items()}



scenarioExpensiveRE_Fr["conversionTechs"] = []
for area in areaList:
    for k, year in enumerate(yearList[:-1]):
        tech = "WindOffShore"
        max_cumul_capacity = {2010: 0, 2020: 5200, 2030: 20900, 2040: 45000}
        min_cumul_capacity = {2010: 0, 2020: 5200, 2030: 20900, 2040: 45000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="high", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
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
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": interpolate(min_cumul_capacity, y_ref(year, y_act)),
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "WindOnShore"

        max_cumul_capacity = {2010: 16570, 2020: 33200, 2030: 47200, 2040: 58000}
        min_cumul_capacity = {2010: 16570, 2020: 33200, 2030: 47200, 2040: 58000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="high", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
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
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": interpolate(min_cumul_capacity, y_ref(year, y_act)),
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "Solar"
        max_cumul_capacity = {2010: 9440, 2020: 35100, 2030: 79600, 2040: 118000}
        min_cumul_capacity = {2010: 9440, 2020: 35100, 2030: 79600, 2040: 118000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="high", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
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
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": interpolate(min_cumul_capacity, y_ref(year, y_act)),
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "HydroReservoir"

        max_cumul_capacity = {2010: 15000, 2020: 15000, 2030: 16000, 2040: 17000}
        min_cumul_capacity = {2010: 15000, 2020: 15000, 2030: 16000, 2040: 17000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="high", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
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
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "EnergyNbhourCap": 2100,  # used for hydroelectricity
                        "minCumulCapacity": interpolate(min_cumul_capacity, y_ref(year, y_act)),
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "HydroRiver"

        max_cumul_capacity = {2010: 11000, 2020: 11000, 2030: 12000, 2040: 13000}
        min_cumul_capacity = {2010: 11000, 2020: 11000, 2030: 12000, 2040: 13000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="high", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
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
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": interpolate(min_cumul_capacity, y_ref(year, y_act)),
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "OldNuke"
        max_cumul_capacity = {2010: 63100, 2020: 59400, 2030: 43100, 2040: 15500}
        min_cumul_capacity = {2010: 63100, 2020: 59400, 2030: 43100, 2040: 15500}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
                        "lifeSpan": lifespan,
                        "powerCost": 30,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1, "uranium": -3.03},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": interpolate(min_cumul_capacity, y_ref(year, y_act)),
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                        "RampConstraintPlus": 0.04,
                        "RampConstraintMoins": 0.04,
                    }
                }
            )
        )

        tech = "NewNuke"
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 6600, 2040: 13200}
        min_cumul_capacity = {2010: 0, 2020: 0, 2030: 6600, 2040: 13200}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
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
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1, "uranium": -3.03},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": interpolate(min_cumul_capacity, y_ref(year, y_act)),
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                        "RampConstraintPlus": 0.04,
                        "RampConstraintMoins": 0.04,
                    }
                }
            )
        )

        tech = "Coal_p"
        max_cumul_capacity = {2010: 6000, 2020: 1000, 2030: 0, 2040: 0}
        min_cumul_capacity = {2010: 6000, 2020: 1000, 2030: 0, 2040: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
                        "lifeSpan": lifespan,
                        "powerCost": 50,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 1000,
                        "Conversion": {"electricity": 1},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": interpolate(min_cumul_capacity, y_ref(year, y_act)),
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                        "RampConstraintPlus": 0.06,
                        "RampConstraintMoins": 0.06,
                    }
                }
            )
        )

        tech = "TAC"
        max_cumul_capacity = {2010: 7100, 2020: 6500, 2030: 0}
        min_cumul_capacity = {2010: 7100, 2020: 6500, 2030: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
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
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1, "gaz": -2.7},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": interpolate(min_cumul_capacity, y_ref(year, y_act)),
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "TAC_H2"
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 1000000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
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
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1, "hydrogen": -2.7},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "CCG"
        min_cumul_capacity = {2010: 5000, 2020: 0}
        max_cumul_capacity = {2010: 5000, 2020: 5000, 2030: 500}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
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
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1, "gaz": -1.72},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": interpolate(min_cumul_capacity, y_ref(year, y_act)),
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                        "RampConstraintPlus": 0.06,
                        "RampConstraintMoins": 0.06,
                    }
                }
            )
        )

        tech = "CCG_H2"
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 100000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
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
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1, "hydrogen": -1.72},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                        "RampConstraintPlus": 0.06,
                        "RampConstraintMoins": 0.06,
                    }
                }
            )
        )

        tech = "electrolysis_AEL"
        max_cumul_capacity = {2010: 0, 2020: 6500, 2030: 7500, 2040: 13400}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="high", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
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

        tech = "IntercoIn"
        max_install_capacity = {2010: 11000, 2020: 22300, 2030: 29700, 2040: 39400}
        max_cumul_capacity = {2010: 11000, 2020: 22300, 2030: 29700, 2040: 39400}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
                        "lifeSpan": lifespan,
                        "powerCost": 150,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": interpolate(max_install_capacity, y_ref(year, y_act)),
                        "EmissionCO2": 290,
                        "Conversion": {"electricity": 1},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "IntercoOut"
        max_cumul_capacity = {2010: 11000, 2020: 22300, 2030: 29700, 2040: 39400}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE_Fr["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
                        "lifeSpan": lifespan,
                        "powerCost": -50,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 0,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": -1},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
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
        scenarioExpensiveRE_Fr["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
                        "lifeSpan": lifespan,
                        "powerCost": 3000,
                        "investCost": capex,
                        "operationCost": opex,
                        "minInstallCapacity": 0,
                        "maxInstallCapacity": 100000,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "EnergyNbhourCap": 0,  # used for hydroelectricity
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": 1000000,
                    }
                }
            )
        )

scenarioExpensiveRE_Fr["conversionTechs"] = pd.concat(scenarioExpensiveRE_Fr["conversionTechs"], axis=1)