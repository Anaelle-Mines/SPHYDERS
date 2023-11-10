import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

from data.Raw import tech_eco_data
from Scenarios.scenario_ref_PACA import scenarioPACA_ref

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


scenarioWoSMR2030={k: v.copy() for (k, v) in scenarioPACA_ref.items()}


scenarioWoSMR2030["conversionTechs"] = []
for area in areaList:
    for k, year in enumerate(yearList[:-1]):
        tech = "WindOffShore"
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2030["conversionTechs"].append(
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
        scenarioWoSMR2030["conversionTechs"].append(
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
        scenarioWoSMR2030["conversionTechs"].append(
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
        scenarioWoSMR2030["conversionTechs"].append(
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
        max_install_capacity = {2010: 411, 2020: 411, 2021: 0}
        min_install_capacity = {2010: 411, 2020: 411, 2021: 0}
        max_cumul_capacity = {2010: 411, 2020: 411, 2021: 0}
        min_cumul_capacity = {2010: 411, 2020: 411, 2021: 0}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
            min_install_capacity = {2010: 0, 2050: 0}
            min_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2030["conversionTechs"].append(
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
        max_cumul_capacity = {2010: 0, 2020: 0}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2030["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
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
        max_cumul_capacity = {2010: 0, 2020: 0}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2030["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
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
        max_cumul_capacity = {2010: 0, 2020: 0}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2030["conversionTechs"].append(
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
                        "Conversion": {"hydrogen": 0},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "CCS2"
        max_cumul_capacity = {2010: 0, 2020: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2030["conversionTechs"].append(
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
        scenarioWoSMR2030["conversionTechs"].append(
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
        scenarioWoSMR2030["conversionTechs"].append(
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
        scenarioWoSMR2030["conversionTechs"].append(
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
        scenarioWoSMR2030["conversionTechs"].append(
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
        scenarioWoSMR2030["conversionTechs"].append(
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
                        "Conversion": {"hydrogen": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": 100000,
                    }
                }
            )
        )

scenarioWoSMR2030["conversionTechs"] = pd.concat(
    scenarioWoSMR2030["conversionTechs"], axis=1
)

scenarioWoSMR2030["transitionFactors"] =pd.DataFrame(
    {'TECHNO1':[],
    'TECHNO2':[],
    'TransFactor':[] }).set_index(['TECHNO1','TECHNO2'])


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


scenarioWoSMR2040={k: v.copy() for (k, v) in scenarioPACA_ref.items()}

scenarioWoSMR2040["conversionTechs"] = []
for area in areaList:
    for k, year in enumerate(yearList[:-1]):
        tech = "WindOffShore"
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2040["conversionTechs"].append(
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
        scenarioWoSMR2040["conversionTechs"].append(
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
        scenarioWoSMR2040["conversionTechs"].append(
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
        scenarioWoSMR2040["conversionTechs"].append(
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
        max_install_capacity = {2010: 411, 2020: 411, 2030:10000, 2031: 0}
        min_install_capacity = {2010: 411, 2020: 411, 2021: 0}
        max_cumul_capacity = {2010: 411, 2020: 411, 2030:10000, 2031: 0}
        min_cumul_capacity = {2010: 411, 2020: 411, 2021: 0}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
            min_install_capacity = {2010: 0, 2050: 0}
            min_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2040["conversionTechs"].append(
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
        max_cumul_capacity = {2010: 0, 2020:0, 2030:10000, 2031: 0}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2040["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
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
        max_cumul_capacity = {2010: 0, 2020:0, 2030:10000, 2031: 0}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2040["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
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
        max_cumul_capacity = {2010: 0, 2020:0, 2030:10000, 2031: 0}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2040["conversionTechs"].append(
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
                        "Conversion": {"hydrogen": 0},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "CCS2"
        max_cumul_capacity = {2010: 0, 2020:0, 2030:10000, 2031: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2040["conversionTechs"].append(
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
        scenarioWoSMR2040["conversionTechs"].append(
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
        scenarioWoSMR2040["conversionTechs"].append(
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
        scenarioWoSMR2040["conversionTechs"].append(
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
        scenarioWoSMR2040["conversionTechs"].append(
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
        scenarioWoSMR2040["conversionTechs"].append(
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
                        "Conversion": {"hydrogen": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": 100000,
                    }
                }
            )
        )

scenarioWoSMR2040["conversionTechs"] = pd.concat(
    scenarioWoSMR2040["conversionTechs"], axis=1
)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


scenarioWoSMR2050={k: v.copy() for (k, v) in scenarioPACA_ref.items()}


scenarioWoSMR2050["conversionTechs"] = []
for area in areaList:
    for k, year in enumerate(yearList[:-1]):
        tech = "WindOffShore"
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2050["conversionTechs"].append(
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
        scenarioWoSMR2050["conversionTechs"].append(
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
        scenarioWoSMR2050["conversionTechs"].append(
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
        scenarioWoSMR2050["conversionTechs"].append(
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
        max_install_capacity = {2010: 411, 2020: 411, 2030:10000, 2040:10000, 2041: 0}
        min_install_capacity = {2010: 411, 2020: 411, 2021: 0}
        max_cumul_capacity = {2010: 411, 2020: 411, 2030:10000, 2040:10000, 2041: 0}
        min_cumul_capacity = {2010: 411, 2020: 411, 2021: 0}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
            min_install_capacity = {2010: 0, 2050: 0}
            min_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2050["conversionTechs"].append(
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
        max_cumul_capacity = {2010: 0, 2020:0, 2030:10000, 2040:10000, 2041: 0}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2050["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
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
        max_cumul_capacity = {2010: 0, 2020:0, 2030:10000, 2040:10000, 2041: 0}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2050["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
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
        max_cumul_capacity = {2010: 0, 2020:0, 2030:10000, 2040:10000, 2041: 0}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2050["conversionTechs"].append(
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
                        "Conversion": {"hydrogen": 0},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act)),
                    }
                }
            )
        )

        tech = "CCS2"
        max_cumul_capacity = {2010: 0, 2020:0, 2030:10000, 2040:10000, 2041: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioWoSMR2050["conversionTechs"].append(
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
        scenarioWoSMR2050["conversionTechs"].append(
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
        scenarioWoSMR2050["conversionTechs"].append(
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
        scenarioWoSMR2050["conversionTechs"].append(
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
        scenarioWoSMR2050["conversionTechs"].append(
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
        scenarioWoSMR2050["conversionTechs"].append(
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
                        "Conversion": {"hydrogen": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": 100000,
                    }
                }
            )
        )

scenarioWoSMR2050["conversionTechs"] = pd.concat(
    scenarioWoSMR2050["conversionTechs"], axis=1
)
