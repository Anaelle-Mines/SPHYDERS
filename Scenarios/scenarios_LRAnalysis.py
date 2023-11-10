import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

from data.Raw import tech_eco_data
import pandas as pd
from Scenarios.scenario_ref_Fr import scenarioFr
from Scenarios.scenario_ref_PACA import scenarioPACA_ref

inputPath='../data/Raw/'
outputPath='../data/output/LRAnalysis/'

listLR=[0.1,0.12,0.14,0.16,0.18,0.2,0.22,0.24,0.26,0.28]

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
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def elecPrice(LR,y): # LR = learning rate = cost reduction when capacity is doubled
    X={2020:20,2030:100,2040:650,2050:1200} # Planned installed capacity of electrolysis
    Xi=interpolate(X,y)
    alpha=-np.log(1-LR)/np.log(2)
    C=750*np.power(Xi/20,-alpha)*1.54*0.88*1000
    return C


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


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


areaList=['France']
scenarioDict_LRAnalysis_Fr={}
for LR in listLR:
    scenarioName='scenario_'+str(LR)
    scenario_Fr={k: v.copy() for (k, v) in scenarioFr.items()}

    scenario_Fr["conversionTechs"] = []
    for area in areaList:
        for k, year in enumerate(yearList[:-1]):
            tech = "WindOffShore"
            max_cumul_capacity = {2010: 0, 2020: 5200, 2030: 20900, 2040: 45000}
            min_cumul_capacity = {2010: 0, 2020: 5200, 2030: 20900, 2040: 45000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            scenario_Fr["conversionTechs"].append(
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
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            scenario_Fr["conversionTechs"].append(
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
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            scenario_Fr["conversionTechs"].append(
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
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            scenario_Fr["conversionTechs"].append(
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
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            scenario_Fr["conversionTechs"].append(
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
            scenario_Fr["conversionTechs"].append(
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
            scenario_Fr["conversionTechs"].append(
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
            scenario_Fr["conversionTechs"].append(
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
            scenario_Fr["conversionTechs"].append(
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
            scenario_Fr["conversionTechs"].append(
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
            scenario_Fr["conversionTechs"].append(
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
            scenario_Fr["conversionTechs"].append(
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
            capex=elecPrice(LR,y_ref(year, y_act))
            opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(tech, hyp="ref", year=y_ref(year, y_act))[1:3]
            scenario_Fr["conversionTechs"].append(
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
            scenario_Fr["conversionTechs"].append(
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
            scenario_Fr["conversionTechs"].append(
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
            scenario_Fr["conversionTechs"].append(
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

    scenario_Fr["conversionTechs"] = pd.concat(scenario_Fr["conversionTechs"], axis=1)

    scenarioDict_LRAnalysis_Fr[scenarioName+'_Fr']=scenario_Fr


# #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

areaList=['Marseille']
scenarioDict_LRAnalysis_PACA={}
for LR in listLR:
    scenarioName='scenario_'+str(LR)
    outputFolderFr=outputPath+scenarioName+'_Fr'

    scenario_PACA={k: v.copy() for (k, v) in scenarioPACA_ref.items()}

    scenario_PACA["conversionTechs"] = []
    for area in areaList:
        for k, year in enumerate(yearList[:-1]):
            tech = "WindOffShore"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            scenario_PACA["conversionTechs"].append(
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
            scenario_PACA["conversionTechs"].append(
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
            scenario_PACA["conversionTechs"].append(
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
            scenario_PACA["conversionTechs"].append(
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
            scenario_PACA["conversionTechs"].append(
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
            scenario_PACA["conversionTechs"].append(
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
            scenario_PACA["conversionTechs"].append(
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
            scenario_PACA["conversionTechs"].append(
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
            scenario_PACA["conversionTechs"].append(
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
            scenario_PACA["conversionTechs"].append(
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
            scenario_PACA["conversionTechs"].append(
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
            capex=elecPrice(LR,y_ref(year, y_act))
            opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(tech, hyp="ref", year=y_ref(year, y_act))[1:3]
            scenario_PACA["conversionTechs"].append(
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
            scenario_PACA["conversionTechs"].append(
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
            scenario_PACA["conversionTechs"].append(
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

    scenario_PACA["conversionTechs"] = pd.concat(scenario_PACA["conversionTechs"], axis=1)


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


    scenarioDict_LRAnalysis_PACA[scenarioName+'_PACA']=scenario_PACA

