import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd

from data.Raw import tech_eco_data
from Scenarios.scenario_creation import scenarioDict
from Scenarios.scenarios_caverns_robustness import scenarioDict_Cavern_robustness


def get_capaTech(area,tech,outputFolder_origin):
    df_capa=pd.read_csv(outputFolder_origin + "/capacity_Pvar.csv").drop(columns="Unnamed: 0")
    df_capa = df_capa.pivot(columns="TECHNOLOGIES", values="capacity_Pvar", index=["AREA","YEAR_op"]).fillna(0)
    YEAR=df_capa.index.get_level_values('YEAR_op').unique()
    dy=YEAR[1]-YEAR[0]
    TECH=list(df_capa.columns)
    if tech not in TECH: 
        capa={y-dy:0 for y in YEAR}
    else:
        capa={y-dy:df_capa.loc[(area,y),tech] for y in YEAR}
    return capa

def get_powerCost(area,tech,scenario,scenarioDict_run=scenarioDict):
    scenario=scenarioDict_run[scenario]
    convTech=scenario['conversionTechs'].loc[['YEAR','powerCost']][tech].transpose()
    YEAR=scenario['yearList']
    dy=YEAR[1]-YEAR[0]
    TECH=list(scenario['conversionTechs'].columns.unique())
    if tech not in TECH: 
        powerCost={y:0 for y in YEAR[:-1]}
    else:
        powerCost={y:convTech.loc[convTech['YEAR']==y]['powerCost'].loc[tech] for y in YEAR[:-1]}
    return powerCost

def get_capaStech(area,stech,outputFolder_origin):


    df_powerStorage=pd.read_csv(outputFolder_origin + "/Pmax_Pvar.csv").drop(columns="Unnamed: 0")
    df_capaStorage=pd.read_csv(outputFolder_origin + "/Cmax_Pvar.csv").drop(columns="Unnamed: 0")

    df_powerStorage = df_powerStorage.pivot(columns="STOCK_TECHNO", values="Pmax_Pvar", index=["AREA","YEAR_op"]).fillna(0)
    df_capaStorage = df_capaStorage.pivot(columns="STOCK_TECHNO", values="Cmax_Pvar", index=["AREA","YEAR_op"]).fillna(0)

    YEAR=df_powerStorage.index.get_level_values('YEAR_op').unique()
    dy=YEAR[1]-YEAR[0]
    powerStorage={y-dy:df_powerStorage.loc[(area,y),stech] for y in YEAR}
    capaStorage={y-dy:df_capaStorage.loc[(area,y),stech] for y in YEAR}

    return powerStorage,capaStorage

def get_newScenario(outputFolder_origin,scenario_alea,y_act,dict_run):
    df_origin=pd.read_csv(outputFolder_origin + "/capacity_Pvar.csv").drop(columns="Unnamed: 0")
    year_invest=pd.read_csv(outputFolder_origin + "/capacityInvest_Dvar.csv").drop(columns="Unnamed: 0").set_index('YEAR_invest').index.unique()
    year_op=df_origin.set_index('YEAR_op').index.unique()
    yearList=year_invest.append(year_op).unique()
    dy=yearList[1]-yearList[0]
    TECH=df_origin.set_index('TECHNOLOGIES').index.unique()
    areaList=df_origin.set_index('AREA').index.unique()

    def y_ref(y, y_act="middle"):
        if y_act == "beginning":
            return y
        elif y_act == "middle":
            return y + dy / 2
        elif y_act == "end":
            return y + dy

    conversionTechs = []
    for area in areaList:
        for k, year in enumerate(yearList[:-1]):
            tech = "WindOffShore"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Electricity production",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 0,
                            "EmissionCO2": 0,
                            "Conversion": {"electricity": 1},
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                        }
                    }
                )
            )

            tech = "WindOffShore_flot"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Electricity production",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 10000,
                            "EmissionCO2": 0,
                            "Conversion": {"electricity": 1},
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                        }
                    }
                )
            )

            tech = "WindOnShore"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Electricity production",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity":10000,
                            "EmissionCO2": 0,
                            "Conversion": {"electricity": 1},
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                        }
                    }
                )
            )

            tech = "Solar"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Electricity production",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity":10000,
                            "EmissionCO2": 0,
                            "Conversion": {"electricity": 1},
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                        }
                    }
                )
            )

            tech = "SMR"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Hydrogen production",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity":10000,
                            "EmissionCO2": 0,
                            "Conversion": {"hydrogen": 1, "gaz": -1.28},
                            "EnergyNbhourCap": 0,  # used for hydroelectricity
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "SMR + CCS1"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Hydrogen production",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 100000,
                            "EmissionCO2": -150,
                            "Conversion": {"hydrogen": 1, "gaz": -1.32},
                            "EnergyNbhourCap": 0,  # used for hydroelectricity
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "SMR + CCS2"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Hydrogen production",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 100000,
                            "EmissionCO2": -270,
                            "Conversion": {"hydrogen": 1, "gaz": -1.45},
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "CCS1"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Hydrogen suport",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 100000,
                            "EmissionCO2": 0,
                            "Conversion": {"hydrogen": 0},
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                        }
                    }
                )
            )

            tech = "CCS2"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Hydrogen support",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 100000,
                            "EmissionCO2": 0,
                            "Conversion": {"hydrogen": 0},
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                        }
                    }
                )
            )

            tech = "SMR_elec"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Hydrogen production",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 0,
                            "EmissionCO2": 0,
                            "Conversion": {"hydrogen": 1, "gaz": -0.91, "electricity": -0.4},
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "SMR_elecCCS1"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Hydrogen production",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 0,
                            "EmissionCO2": -156,
                            "Conversion": {"hydrogen": 1, "gaz": -0.91, "electricity": -0.57},
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "electrolysis_AEL"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Hydrogen production",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 100000,
                            "EmissionCO2": 0,
                            "Conversion": {"hydrogen": 1, "electricity": -1.54},
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                        }
                    }
                )
            )

            tech = "electrolysis_PEMEL"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Hydrogen production",
                            "lifeSpan": lifespan,
                            "powerCost": get_powerCost(area,tech, scenario_alea,dict_run)[year],
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 100000,
                            "EmissionCO2": 0,
                            "Conversion": {"hydrogen": 1, "electricity": -1.67},
                            "minCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                            "maxCumulCapacity": get_capaTech(area,tech,outputFolder_origin)[year],
                        }
                    }
                )
            )

            tech = "curtailment"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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

    conversionTechs = pd.concat(
        conversionTechs, axis=1
    )


    storageTechs = []
    for area in areaList:
        for k, year in enumerate(yearList[:-1]):
            tech = "Battery"
            capex1, opex1, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech + " - 1h", hyp="ref", year=y_ref(year, y_act)
            )
            capex4, opex4, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech + " - 4h", hyp="ref", year=y_ref(year, y_act)
            )
            capex_per_kWh = (capex4 - capex1) / 3
            capex_per_kW = capex1 - capex_per_kWh

            storageTechs.append(
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
                            "p_max": get_capaStech(area,tech,outputFolder_origin)[0][year],
                            "c_max":get_capaStech(area,tech,outputFolder_origin)[1][year],
                            "chargeFactors": {"electricity": 0.9200},
                            "dischargeFactors": {"electricity": 1.09},
                            "dissipation": 0.0085,
                        },
                    }
                )
            )

            tech = "tankH2_G"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            storageTechs.append(
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
                            "p_max": get_capaStech(area,tech,outputFolder_origin)[0][year],
                            "c_max":get_capaStech(area,tech,outputFolder_origin)[1][year],
                            "chargeFactors": {"electricity": 0.0168, "hydrogen": 1},
                            "dischargeFactors": {"hydrogen": 1},
                            "dissipation": 0,
                        },
                    }
                )
            )

            tech = "saltCavernH2_G"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            storageTechs.append(
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
                            "p_max": get_capaStech(area,tech,outputFolder_origin)[0][year],
                            "c_max":get_capaStech(area,tech,outputFolder_origin)[1][year],
                            "chargeFactors": {"electricity": 0.0168, "hydrogen": 1},
                            "dischargeFactors": {"hydrogen": 1},
                            "dissipation": 0,
                        },
                    }
                )
            )

    storageTechs = pd.concat(storageTechs, axis=1)

    return conversionTechs,storageTechs

def get_newScenario_woSMR2040(outputFolder_origin,y_act):
    df_origin=pd.read_csv(outputFolder_origin + "/capacity_Pvar.csv").drop(columns="Unnamed: 0")
    year_invest=pd.read_csv(outputFolder_origin + "/capacityInvest_Dvar.csv").drop(columns="Unnamed: 0").set_index('YEAR_invest').index.unique()
    year_op=df_origin.set_index('YEAR_op').index.unique()
    yearList=year_invest.append(year_op).unique()
    dy=yearList[1]-yearList[0]
    TECH=df_origin.set_index('TECHNOLOGIES').index.unique()
    areaList=df_origin.set_index('AREA').index.unique()

    def y_ref(y, y_act="middle"):
        if y_act == "beginning":
            return y
        elif y_act == "middle":
            return y + dy / 2
        elif y_act == "end":
            return y + dy

    conversionTechs = []
    for area in areaList:
        for k, year in enumerate(yearList[:-1]):
            tech = "WindOffShore"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "WindOffShore_flot"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:1000,2040:1000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Electricity production",
                            "lifeSpan": lifespan,
                            "powerCost":0,
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 10000,
                            "EmissionCO2": 0,
                            "Conversion": {"electricity": 1},
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "WindOnShore"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:150,2040:150}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "maxInstallCapacity":10000,
                            "EmissionCO2": 0,
                            "Conversion": {"electricity": 1},
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "Solar"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:150,2040:150}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "maxInstallCapacity":10000,
                            "EmissionCO2": 0,
                            "Conversion": {"electricity": 1},
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "SMR"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minInstallCapacity": 0,
                            "maxInstallCapacity":10000,
                            "EmissionCO2": 0,
                            "Conversion": {"hydrogen": 1, "gaz": -1.28},
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "SMR + CCS1"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "SMR + CCS2"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "CCS1"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Hydrogen suport",
                            "lifeSpan": lifespan,
                            "powerCost": 0,
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 100000,
                            "EmissionCO2": 0,
                            "Conversion": {"hydrogen": 0},
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "CCS2"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "SMR_elec"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "maxCumulCapacity": 0,
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "SMR_elecCCS1"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "maxCumulCapacity": 0,
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "electrolysis_AEL"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:10000,2040:10000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "electrolysis_PEMEL"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:10000,2040:10000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "curtailment"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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

    conversionTechs = pd.concat(
        conversionTechs, axis=1
    )


    storageTechs = []
    for area in areaList:
        for k, year in enumerate(yearList[:-1]):
            tech = "Battery"
            capex1, opex1, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech + " - 1h", hyp="ref", year=y_ref(year, y_act)
            )
            capex4, opex4, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech + " - 4h", hyp="ref", year=y_ref(year, y_act)
            )
            capex_per_kWh = (capex4 - capex1) / 3
            capex_per_kW = capex1 - capex_per_kWh

            storageTechs.append(
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
                            "p_max":get_capaStech(area,tech,outputFolder_origin)[0][year],
                            "c_max": get_capaStech(area,tech,outputFolder_origin)[1][year],
                            "chargeFactors": {"electricity": 0.9200},
                            "dischargeFactors": {"electricity": 1.09},
                            "dissipation": 0.0085,
                        },
                    }
                )
            )

            tech = "tankH2_G"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            storageTechs.append(
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
                            "p_max":get_capaStech(area,tech,outputFolder_origin)[0][year],
                            "c_max": get_capaStech(area,tech,outputFolder_origin)[1][year],
                            "chargeFactors": {"electricity": 0.0168, "hydrogen": 1},
                            "dischargeFactors": {"hydrogen": 1},
                            "dissipation": 0,
                        },
                    }
                )
            )

            tech = "saltCavernH2_G"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            storageTechs.append(
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
                            "p_max":get_capaStech(area,tech,outputFolder_origin)[0][year],
                            "c_max": get_capaStech(area,tech,outputFolder_origin)[1][year],
                            "chargeFactors": {"electricity": 0.0168, "hydrogen": 1},
                            "dischargeFactors": {"hydrogen": 1},
                            "dissipation": 0,
                        },
                    }
                )
            )

    storageTechs = pd.concat(storageTechs, axis=1)

    return conversionTechs,storageTechs

def get_newScenario_cavern2040(outputFolder_origin,y_act):
    df_origin=pd.read_csv(outputFolder_origin + "/capacity_Pvar.csv").drop(columns="Unnamed: 0")
    year_invest=pd.read_csv(outputFolder_origin + "/capacityInvest_Dvar.csv").drop(columns="Unnamed: 0").set_index('YEAR_invest').index.unique()
    year_op=df_origin.set_index('YEAR_op').index.unique()
    yearList=year_invest.append(year_op).unique()
    dy=yearList[1]-yearList[0]
    TECH=df_origin.set_index('TECHNOLOGIES').index.unique()
    areaList=df_origin.set_index('AREA').index.unique()

    def y_ref(y, y_act="middle"):
        if y_act == "beginning":
            return y
        elif y_act == "middle":
            return y + dy / 2
        elif y_act == "end":
            return y + dy

    conversionTechs = []
    for area in areaList:
        for k, year in enumerate(yearList[:-1]):
            tech = "WindOffShore"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "WindOffShore_flot"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:1000,2040:1000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Electricity production",
                            "lifeSpan": lifespan,
                            "powerCost":0,
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 10000,
                            "EmissionCO2": 0,
                            "Conversion": {"electricity": 1},
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "WindOnShore"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:150,2040:150}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "maxInstallCapacity":10000,
                            "EmissionCO2": 0,
                            "Conversion": {"electricity": 1},
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "Solar"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:150,2040:150}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "maxInstallCapacity":10000,
                            "EmissionCO2": 0,
                            "Conversion": {"electricity": 1},
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "SMR"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:10000,2040:10000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minInstallCapacity": 0,
                            "maxInstallCapacity":10000,
                            "EmissionCO2": 0,
                            "Conversion": {"hydrogen": 1, "gaz": -1.28},
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "SMR + CCS1"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:10000,2040:10000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "SMR + CCS2"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:10000,2040:10000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "CCS1"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:10000,2040:10000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
                pd.DataFrame(
                    data={
                        tech: {
                            "AREA": area,
                            "YEAR": year,
                            "Category": "Hydrogen suport",
                            "lifeSpan": lifespan,
                            "powerCost": 0,
                            "investCost": capex,
                            "operationCost": opex,
                            "minInstallCapacity": 0,
                            "maxInstallCapacity": 100000,
                            "EmissionCO2": 0,
                            "Conversion": {"hydrogen": 0},
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "CCS2"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:10000,2040:10000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "SMR_elec"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "maxCumulCapacity": 0,
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "SMR_elecCCS1"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "maxCumulCapacity": 0,
                            "RampConstraintPlus": 0.3,
                        }
                    }
                )
            )

            tech = "electrolysis_AEL"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:10000,2040:10000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "electrolysis_PEMEL"
            min_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:0,2040:0}
            max_capacity={2010:get_capaTech(area,tech,outputFolder_origin)[2010],2020:get_capaTech(area,tech,outputFolder_origin)[2020],2030:10000,2040:10000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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
                            "minCumulCapacity": min_capacity[year],
                            "maxCumulCapacity": max_capacity[year],
                        }
                    }
                )
            )

            tech = "curtailment"
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            conversionTechs.append(
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

    conversionTechs = pd.concat(
        conversionTechs, axis=1
    )


    storageTechs = []
    for area in areaList:
        for k, year in enumerate(yearList[:-1]):
            tech = "Battery"
            max_power={2010:get_capaStech(area,tech,outputFolder_origin)[0][2010],2020:get_capaStech(area,tech,outputFolder_origin)[0][2020],2030:1000,2040:7700}
            max_capacity={2010:get_capaStech(area,tech,outputFolder_origin)[1][2010],2020:get_capaStech(area,tech,outputFolder_origin)[1][2020],2030:100,2040:770}
            capex1, opex1, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech + " - 1h", hyp="ref", year=y_ref(year, y_act)
            )
            capex4, opex4, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech + " - 4h", hyp="ref", year=y_ref(year, y_act)
            )
            capex_per_kWh = (capex4 - capex1) / 3
            capex_per_kW = capex1 - capex_per_kWh

            storageTechs.append(
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
                            "p_max": max_power[year],
                            "c_max": max_capacity[year],
                            "chargeFactors": {"electricity": 0.9200},
                            "dischargeFactors": {"electricity": 1.09},
                            "dissipation": 0.0085,
                        },
                    }
                )
            )

            tech = "tankH2_G"
            max_power={2010:get_capaStech(area,tech,outputFolder_origin)[0][2010],2020:get_capaStech(area,tech,outputFolder_origin)[0][2020],2030:20000,2040:30000}
            max_capacity={2010:get_capaStech(area,tech,outputFolder_origin)[1][2010],2020:get_capaStech(area,tech,outputFolder_origin)[1][2020],2030:2000,2040:3000}
            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            storageTechs.append(
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
                            "p_max": max_power[year],
                            "c_max": max_capacity[year],
                            "chargeFactors": {"electricity": 0.0168, "hydrogen": 1},
                            "dischargeFactors": {"hydrogen": 1},
                            "dissipation": 0,
                        },
                    }
                )
            )

            tech = "saltCavernH2_G"
            max_power={2010:get_capaStech(area,tech,outputFolder_origin)[0][2010],2020:get_capaStech(area,tech,outputFolder_origin)[0][2010],2030:130000,2040:130000}
            max_capacity={2010:get_capaStech(area,tech,outputFolder_origin)[1][2010],2020:get_capaStech(area,tech,outputFolder_origin)[1][2010],2030:13000,2040:13000}
            # charge_factor={2010:{"electricity": 0.0168, "hydrogen": 0},2020:{"electricity": 0.0168, "hydrogen": 0},2030:{"electricity": 0.0168, "hydrogen": 1},2040:{"electricity": 0.0168, "hydrogen": 1}}

            capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
                tech, hyp="ref", year=y_ref(year, y_act)
            )
            storageTechs.append(
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
                            "p_max": max_power[year],
                            "c_max": max_capacity[year],
                            "chargeFactors": {"electricity": 0.0168, "hydrogen": 1},
                            "dischargeFactors": {"hydrogen": 1},
                            "dissipation": 0,
                        },
                    }
                )
            )

    storageTechs = pd.concat(storageTechs, axis=1)

    return conversionTechs,storageTechs