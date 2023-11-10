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


scenarioREx2={k: v.copy() for (k, v) in scenarioPACA_ref.items()}


scenarioREx2["conversionTechs"] = []
for area in areaList:
    for k, year in enumerate(yearList[:-1]):
        tech = "WindOffShore"
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREx2["conversionTechs"].append(
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
        max_install_capacity = {2010: 0, 2020: 0, 2030: 500}
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 500}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREx2["conversionTechs"].append(
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
                        "maxInstallCapacity": interpolate(max_install_capacity, y_ref(year, y_act))*2,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act))*2,
                    }
                }
            )
        )

        tech = "WindOnShore"
        max_install_capacity = {2010: 0, 2020: 0, 2030: 100}
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 150}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREx2["conversionTechs"].append(
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
                        "maxInstallCapacity": interpolate(max_install_capacity, y_ref(year, y_act))*2,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act))*2,
                    }
                }
            )
        )

        tech = "Solar"
        max_install_capacity = {2010: 0, 2020: 0, 2030: 100}
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 150}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREx2["conversionTechs"].append(
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
                        "maxInstallCapacity": interpolate(max_install_capacity, y_ref(year, y_act))*2,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act))*2,
                    }
                }
            )
        )

        tech = "SMR"
        max_install_capacity = {2010: 411, 2020: 411, 2021:1000, 2030: 10000}
        min_install_capacity = {2010: 411, 2020: 411, 2021:0, 2030: 0}
        max_cumul_capacity = {2010: 411, 2020: 411, 2021:1000, 2030: 10000}
        min_cumul_capacity = {2010: 411, 2020: 411, 2021:0, 2030: 0}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
            min_install_capacity = {2010: 0, 2050: 0}
            min_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREx2["conversionTechs"].append(
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
        scenarioREx2["conversionTechs"].append(
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
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREx2["conversionTechs"].append(
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
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREx2["conversionTechs"].append(
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
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREx2["conversionTechs"].append(
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
        scenarioREx2["conversionTechs"].append(
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
        scenarioREx2["conversionTechs"].append(
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
        scenarioREx2["conversionTechs"].append(
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
        scenarioREx2["conversionTechs"].append(
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
        scenarioREx2["conversionTechs"].append(
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

scenarioREx2["conversionTechs"] = pd.concat(
    scenarioREx2["conversionTechs"], axis=1)



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


scenarioREinf={k: v.copy() for (k, v) in scenarioPACA_ref.items()}


scenarioREinf["conversionTechs"] = []
for area in areaList:
    for k, year in enumerate(yearList[:-1]):
        tech = "WindOffShore"
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREinf["conversionTechs"].append(
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
        max_install_capacity = {2010: 0, 2020: 0, 2030: 10000}
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREinf["conversionTechs"].append(
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
                        "maxInstallCapacity": interpolate(max_install_capacity, y_ref(year, y_act))*2,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act))*2,
                    }
                }
            )
        )

        tech = "WindOnShore"
        max_install_capacity = {2010: 0, 2020: 0, 2030: 10000}
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREinf["conversionTechs"].append(
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
                        "maxInstallCapacity": interpolate(max_install_capacity, y_ref(year, y_act))*2,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act))*2,
                    }
                }
            )
        )

        tech = "Solar"
        max_install_capacity = {2010: 0, 2020: 0, 2030: 10000}
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREinf["conversionTechs"].append(
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
                        "maxInstallCapacity": interpolate(max_install_capacity, y_ref(year, y_act))*2,
                        "EmissionCO2": 0,
                        "Conversion": {"electricity": 1},
                        "minCumulCapacity": 0,
                        "maxCumulCapacity": interpolate(max_cumul_capacity, y_ref(year, y_act))*2,
                    }
                }
            )
        )

        tech = "SMR"
        max_install_capacity = {2010: 411, 2020: 411, 2021:1000, 2030: 10000}
        min_install_capacity = {2010: 411, 2020: 411, 2021:0, 2030: 0}
        max_cumul_capacity = {2010: 411, 2020: 411, 2021:1000, 2030: 10000}
        min_cumul_capacity = {2010: 411, 2020: 411, 2021:0, 2030: 0}
        if area != "Marseille":
            max_install_capacity = {2010: 0, 2050: 0}
            max_cumul_capacity = {2010: 0, 2050: 0}
            min_install_capacity = {2010: 0, 2050: 0}
            min_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREinf["conversionTechs"].append(
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
        scenarioREinf["conversionTechs"].append(
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
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREinf["conversionTechs"].append(
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
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        if area != "Marseille":
            max_cumul_capacity = {2010: 0, 2050: 0}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREinf["conversionTechs"].append(
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
        max_cumul_capacity = {2010: 0, 2020: 0, 2030: 10000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioREinf["conversionTechs"].append(
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
        scenarioREinf["conversionTechs"].append(
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
        scenarioREinf["conversionTechs"].append(
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
        scenarioREinf["conversionTechs"].append(
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
        scenarioREinf["conversionTechs"].append(
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
        scenarioREinf["conversionTechs"].append(
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

scenarioREinf["conversionTechs"] = pd.concat(
    scenarioREinf["conversionTechs"], axis=1)


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


scenarioExpensiveRE={k: v.copy() for (k, v) in scenarioPACA_ref.items()}

outputFolderFr='../data/output/expensiveRE_Fr_1h'

scenarioExpensiveRE["conversionTechs"] = []
for area in areaList:
    for k, year in enumerate(yearList[:-1]):
        tech = "WindOffShore"
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="high", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE["conversionTechs"].append(
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
            tech, hyp="high", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE["conversionTechs"].append(
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
            tech, hyp="high", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE["conversionTechs"].append(
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
            tech, hyp="high", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE["conversionTechs"].append(
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
        scenarioExpensiveRE["conversionTechs"].append(
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
        scenarioExpensiveRE["conversionTechs"].append(
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
        scenarioExpensiveRE["conversionTechs"].append(
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
        scenarioExpensiveRE["conversionTechs"].append(
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
        scenarioExpensiveRE["conversionTechs"].append(
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
        scenarioExpensiveRE["conversionTechs"].append(
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
        scenarioExpensiveRE["conversionTechs"].append(
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
            tech, hyp="high", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE["conversionTechs"].append(
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
            tech, hyp="high", year=y_ref(year, y_act)
        )
        scenarioExpensiveRE["conversionTechs"].append(
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
        scenarioExpensiveRE["conversionTechs"].append(
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

scenarioExpensiveRE["conversionTechs"] = pd.concat(
    scenarioExpensiveRE["conversionTechs"], axis=1
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
scenarioExpensiveRE["gridConnection"] = (
    gridConnection[["HTB", "TIME"]]
    .groupby(["TIME"])
    .mean()
    .reset_index()
    .rename(columns={"TIME": "TIMESTAMP"})
)
scenarioExpensiveRE["gridConnection"]["Calendrier"] = calendar.values
scenarioExpensiveRE["gridConnection"].set_index("TIMESTAMP", inplace=True)
scenarioExpensiveRE["turpeFactorsHTB"] = pd.DataFrame(
    columns=["HORAIRE", "fixeTurpeHTB"],
    data={"P": 5880, "HPH": 5640, "HCH": 5640, "HPE": 5280, "HCE": 4920}.items(),
).set_index(
    "HORAIRE"
)  # en €/MW/an part abonnement


biogasPrice = {2020: 120, 2030: 105, 2040:90 , 2050:75} # €/MWh
hdyrogenPrice = {2020: 6, 2030: 6, 2040:6, 2050:6} # €/kg

scenarioExpensiveRE["resourceImportPrices"] = pd.concat(
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


scenarioExpensiveRE["resourceImportPrices"] = (
    scenarioExpensiveRE["resourceImportPrices"]
    .groupby(["AREA", "YEAR", "TIMESTAMP"])
    .mean()
    .reset_index()
)

scenarioExpensiveRE["resourceImportCO2eq"] = pd.concat(
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

scenarioExpensiveRE["resourceImportCO2eq"] = (
    scenarioExpensiveRE["resourceImportCO2eq"]
    .groupby(["AREA", "YEAR", "TIMESTAMP"])
    .mean()
    .reset_index()
)
