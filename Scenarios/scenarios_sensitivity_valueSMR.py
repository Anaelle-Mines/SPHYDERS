import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

from data.Raw import tech_eco_data
from Functions.f_getCapa_woSMR import get_capa_woSMR_REinf,get_capa_woSMR
from Scenarios.scenario_creation import scenarioDict


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

yearZero = 2010
yearFinal = 2050
yearStep = 10
yearList = [
    yr for yr in range(yearZero, yearFinal + yearStep, yearStep)
]  # +1 to include the final year
nYears = len(yearList)

scenarioDict_sensitivity_valueSMR={'Re_inf':scenarioDict['Re_inf'],'Caverns':scenarioDict['Cavern'],'CavernREinf':scenarioDict['CavernREinf'],'gas_x5':scenarioDict['gas_x5'],'BM_90':scenarioDict['BM_90']}

#-------------------------------------------------------------------------------------------------------------------------------#

scenarioRe_inf_woSMR={k: v.copy() for (k, v) in scenarioDict['Re_inf'].items()}
scenarioRe_inf_woSMR['conversionTechs']=get_capa_woSMR_REinf(areaList,yearList,y_act,CCS=50)
scenarioDict_sensitivity_valueSMR['Re_inf_woSMR']=scenarioRe_inf_woSMR

scenarioRe_inf_TC200={k: v.copy() for (k, v) in scenarioDict['Re_inf'].items()}
scenarioRe_inf_TC200["carbonTax"] = pd.DataFrame(data=np.linspace(0.0675, 0.2, nYears), index=yearList, columns=("carbonTax",))
scenarioDict_sensitivity_valueSMR['Re_inf_TC200']=scenarioRe_inf_TC200

scenarioRe_inf_TC200_woSMR={k: v.copy() for (k, v) in scenarioRe_inf_TC200.items()}
scenarioRe_inf_TC200_woSMR['conversionTechs']=get_capa_woSMR_REinf(areaList,yearList,y_act,CCS=50)
scenarioDict_sensitivity_valueSMR['Re_inf_TC200_woSMR']=scenarioRe_inf_TC200_woSMR

scenarioRe_inf_CCS10={k: v.copy() for (k, v) in scenarioDict['Re_inf'].items()}
scenarioRe_inf_CCS10["conversionTechs"] = []
for area in areaList:
    for k, year in enumerate(yearList[:-1]):
        tech = "WindOffShore"
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioRe_inf_CCS10["conversionTechs"].append(
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
                        "lifeSpan": lifespan,
                        "powerCost": 1.71,
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "Category": "Electricity production",
                        "lifeSpan": lifespan,
                        "powerCost": 2.9,
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
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
        scenarioRe_inf_CCS10["conversionTechs"].append(
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

scenarioRe_inf_CCS10["conversionTechs"] = pd.concat(
    scenarioRe_inf_CCS10["conversionTechs"], axis=1)
scenarioDict_sensitivity_valueSMR['Re_inf_CCS10']=scenarioRe_inf_CCS10

scenarioRe_inf_CCS10_woSMR={k: v.copy() for (k, v) in scenarioRe_inf_CCS10.items()}
scenarioRe_inf_CCS10_woSMR['conversionTechs']=get_capa_woSMR_REinf(areaList,yearList,y_act,CCS=10)
scenarioDict_sensitivity_valueSMR['Re_inf_CCS10_woSMR']=scenarioRe_inf_CCS10_woSMR


# -------------------------------------------------------------------------------------------------------------------------------#

scenarioCaverns_woSMR={k: v.copy() for (k, v) in scenarioDict['Cavern'].items()}
scenarioCaverns_woSMR['conversionTechs']=get_capa_woSMR(areaList,yearList,y_act,CCS=50)
scenarioDict_sensitivity_valueSMR['Caverns_woSMR']=scenarioCaverns_woSMR

scenarioCaverns_TC200={k: v.copy() for (k, v) in scenarioDict['Cavern'].items()}
scenarioCaverns_TC200['carbonTax']=pd.DataFrame(data=np.linspace(0.0675, 0.2, nYears), index=yearList, columns=("carbonTax",))
scenarioDict_sensitivity_valueSMR['Caverns_TC200']=scenarioCaverns_TC200

scenarioCaverns_TC200_woSMR={k: v.copy() for (k, v) in scenarioCaverns_TC200.items()}
scenarioCaverns_TC200_woSMR['conversionTechs']=get_capa_woSMR(areaList,yearList,y_act,CCS=50)
scenarioDict_sensitivity_valueSMR['Caverns_TC200_woSMR']=scenarioCaverns_TC200_woSMR

scenarioCaverns_CCS10={k: v.copy() for (k, v) in scenarioDict['Cavern'].items()}
scenarioCaverns_CCS10["conversionTechs"] = scenarioDict['CO2_10']['conversionTechs'].copy()
scenarioDict_sensitivity_valueSMR['Caverns_CCS10']=scenarioCaverns_CCS10

scenarioCaverns_CCS10_woSMR={k: v.copy() for (k, v) in scenarioCaverns_CCS10.items()}
scenarioCaverns_CCS10_woSMR['conversionTechs']=get_capa_woSMR(areaList,yearList,y_act,CCS=10)
scenarioDict_sensitivity_valueSMR['Caverns_CCS10_woSMR']=scenarioCaverns_CCS10_woSMR


#-------------------------------------------------------------------------------------------------------------------------------#

scenarioCavernREinf_woSMR={k: v.copy() for (k, v) in scenarioDict['CavernREinf'].items()}
scenarioCavernREinf_woSMR['conversionTechs']=get_capa_woSMR_REinf(areaList,yearList,y_act,CCS=50)
scenarioDict_sensitivity_valueSMR['CavernREinf_woSMR']=scenarioCavernREinf_woSMR

scenarioCavernREinf_TC200={k: v.copy() for (k, v) in scenarioDict['CavernREinf'].items()}
scenarioCavernREinf_TC200['carbonTax']=pd.DataFrame(data=np.linspace(0.0675, 0.2, nYears), index=yearList, columns=("carbonTax",))
scenarioDict_sensitivity_valueSMR['CavernREinf_TC200']=scenarioCavernREinf_TC200

scenarioCavernREinf_TC200_woSMR={k: v.copy() for (k, v) in scenarioCavernREinf_TC200.items()}
scenarioCavernREinf_TC200_woSMR['conversionTechs']=get_capa_woSMR_REinf(areaList,yearList,y_act,CCS=50)
scenarioDict_sensitivity_valueSMR['CavernREinf_TC200_woSMR']=scenarioCavernREinf_TC200_woSMR

scenarioCavernREinf_CCS10={k: v.copy() for (k, v) in scenarioDict['CavernREinf'].items()}
scenarioCavernREinf_CCS10["conversionTechs"] = scenarioRe_inf_CCS10['conversionTechs'].copy()
scenarioDict_sensitivity_valueSMR['CavernREinf_CCS10']=scenarioCavernREinf_CCS10

scenarioCavernREinf_CCS10_woSMR={k: v.copy() for (k, v) in scenarioCavernREinf_CCS10.items()}
scenarioCavernREinf_CCS10_woSMR['conversionTechs']=get_capa_woSMR_REinf(areaList,yearList,y_act,CCS=10)
scenarioDict_sensitivity_valueSMR['CavernREinf_CCS10_woSMR']=scenarioCavernREinf_CCS10_woSMR


#-------------------------------------------------------------------------------------------------------------------------------#

scenarioGas5_woSMR={k: v.copy() for (k, v) in scenarioDict['gas_x5'].items()}
scenarioGas5_woSMR['conversionTechs']=get_capa_woSMR(areaList,yearList,y_act,CCS=50)
scenarioDict_sensitivity_valueSMR['gas_x5_woSMR']=scenarioGas5_woSMR

scenarioGas5_TC200={k: v.copy() for (k, v) in scenarioDict['gas_x5'].items()}
scenarioGas5_TC200['carbonTax']=pd.DataFrame(data=np.linspace(0.0675, 0.2, nYears), index=yearList, columns=("carbonTax",))
scenarioDict_sensitivity_valueSMR['gas_x5_TC200']=scenarioGas5_TC200

scenarioGas5_TC200_woSMR={k: v.copy() for (k, v) in scenarioGas5_TC200.items()}
scenarioGas5_TC200_woSMR['conversionTechs']=get_capa_woSMR(areaList,yearList,y_act,CCS=50)
scenarioDict_sensitivity_valueSMR['gas_x5_TC200_woSMR']=scenarioGas5_TC200_woSMR

scenarioGas5_CCS10={k: v.copy() for (k, v) in scenarioDict['gas_x5'].items()}
scenarioGas5_CCS10["conversionTechs"] = scenarioDict['CO2_10']['conversionTechs'].copy()
scenarioDict_sensitivity_valueSMR['gas_x5_CCS10']=scenarioGas5_CCS10

scenarioGas5_CCS10_woSMR={k: v.copy() for (k, v) in scenarioGas5_CCS10.items()}
scenarioGas5_CCS10_woSMR['conversionTechs']=get_capa_woSMR(areaList,yearList,y_act,CCS=10)
scenarioDict_sensitivity_valueSMR['gas_x5_CCS10_woSMR']=scenarioGas5_CCS10_woSMR


#-------------------------------------------------------------------------------------------------------------------------------#

scenarioBM90_woSMR={k: v.copy() for (k, v) in scenarioDict['BM_90'].items()}
scenarioBM90_woSMR['conversionTechs']=get_capa_woSMR(areaList,yearList,y_act,CCS=50)
scenarioDict_sensitivity_valueSMR['BM_90_woSMR']=scenarioBM90_woSMR

scenarioBM90_TC200={k: v.copy() for (k, v) in scenarioDict['BM_90'].items()}
scenarioBM90_TC200['carbonTax']=pd.DataFrame(data=np.linspace(0.0675, 0.2, nYears), index=yearList, columns=("carbonTax",))
scenarioDict_sensitivity_valueSMR['BM_90_TC200']=scenarioBM90_TC200

scenarioBM90_TC200_woSMR={k: v.copy() for (k, v) in scenarioBM90_TC200.items()}
scenarioBM90_TC200_woSMR['conversionTechs']=get_capa_woSMR(areaList,yearList,y_act,CCS=50)
scenarioDict_sensitivity_valueSMR['BM_90_TC200_woSMR']=scenarioBM90_TC200_woSMR

scenarioBM90_CCS10={k: v.copy() for (k, v) in scenarioDict['BM_90'].items()}
scenarioBM90_CCS10["conversionTechs"] = scenarioDict['CO2_10']['conversionTechs'].copy()
scenarioDict_sensitivity_valueSMR['BM_90_CCS10']=scenarioBM90_CCS10

scenarioBM90_CCS10_woSMR={k: v.copy() for (k, v) in scenarioBM90_CCS10.items()}
scenarioBM90_CCS10_woSMR['conversionTechs']=get_capa_woSMR(areaList,yearList,y_act,CCS=10)
scenarioDict_sensitivity_valueSMR['BM_90_CCS10_woSMR']=scenarioBM90_CCS10_woSMR

