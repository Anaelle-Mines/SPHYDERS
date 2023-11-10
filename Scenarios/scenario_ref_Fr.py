import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd

from data.Raw import tech_eco_data

inputPath = "../data/Raw/"

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

ctechs = [
    "WindOnShore",
    "WindOffShore",
    "Solar",
    "CCG",
    "TAC",
    "Coal_p",
    "OldNuke",
    "NewNuke",
    "IntercoIn",
    "IntercoOut",
    "curtailment",
    "HydroReservoir",
    "HydroRiver",
    "CCG_H2",
    "TAC_H2",
    "electrolysis_AEL",
]
areaList = ["France"]


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


scenarioFr = {}

scenarioFr["areaList"] = areaList
scenarioFr["yearList"] = yearList
scenarioFr["timeStep"] = pd.DataFrame({"timeStep": [timeStep]})
scenarioFr["lastTime"] = t[-1]
scenarioFr["convTechList"] = ctechs
y_act = "middle"

scenarioFr["economicParameters"] = pd.DataFrame(
    {
        "discountRate": [0.04],
        "financeRate": [0.04],
        "y_act": y_act,  # Moment of the period chosen for investments and actualisation. Possible values : 'beginning', 'middle', 'end'
    }
)


elec_demand = pd.read_csv(inputPath + "areaConsumption2019_Fr_TIMExRES.csv").set_index(
    ["TIMESTAMP", "RESOURCES"]
)
anualElec = {2020: 470.5e6, 2030: 562.4e6, 2040: 619.8e6, 2050: 659.2e6}
hourlyH2 = {2020: 0, 2030: 1825, 2040: 2400, 2050: 3710}
scenarioFr["resourceDemand"] = pd.concat(
    (
        pd.DataFrame(
            data={
                "AREA": area,
                "YEAR": year,
                "TIMESTAMP": tmoy,
                "electricity": np.array(
                    elec_demand.loc[(slice(None), "electricity"), "areaConsumption"]
                    * interpolate(anualElec, y_ref(year, y_act))
                    / anualElec[2020]
                ),  # incrising demand of electricity (hypothesis : ADEME)
                "hydrogen": interpolate(hourlyH2, y_ref(year, y_act))
                * np.ones(oneYear),  # base-load consumption of H2 (hypothesis : ADEME)
                "gaz": np.zeros(oneYear),
                "uranium": np.zeros(oneYear),
            }
        )
        for k, year in enumerate(yearList[1:])
        for area in areaList
    )
)

scenarioFr["resourceDemand"] = (
    scenarioFr["resourceDemand"].groupby(["AREA", "YEAR", "TIMESTAMP"]).sum().reset_index()
)

scenarioFr["conversionTechs"] = []
for area in areaList:
    for k, year in enumerate(yearList[:-1]):
        tech = "WindOffShore"
        max_cumul_capacity = {2010: 0, 2020: 5200, 2030: 20900, 2040: 45000}
        min_cumul_capacity = {2010: 0, 2020: 5200, 2030: 20900, 2040: 45000}
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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
        scenarioFr["conversionTechs"].append(
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

scenarioFr["conversionTechs"] = pd.concat(scenarioFr["conversionTechs"], axis=1)

scenarioFr["storageTechs"] = []
for area in areaList:
    for k, year in enumerate(yearList[:-1]):
        tech = "Battery"
        max_install_capacity = {2010: 0, 2020: 5000, 2030: 10000, 2040: 77000}
        max_install_power = {2010: 0, 2020: 500, 2030: 1000, 2040: 7700}
        capex1, opex1, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech + " - 1h", hyp="ref", year=y_ref(year, y_act)
        )
        capex4, opex4, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech + " - 4h", hyp="ref", year=y_ref(year, y_act)
        )
        capex_per_kWh = (capex4 - capex1) / 3
        capex_per_kW = capex1 - capex_per_kWh

        scenarioFr["storageTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "resource": "electricity",
                        "storagelifeSpan": lifespan,
                        "storagePowerCost": capex_per_kW,
                        "storageEnergyCost": capex_per_kWh,
                        "storageOperationCost": opex1,  # TODO: according to RTE OPEX seems to vary with energy rather than power
                        "p_max": interpolate(max_install_power, year),
                        "c_max": interpolate(max_install_capacity, y_ref(year, y_act)),
                        "chargeFactors": {"electricity": 0.9200},
                        "dischargeFactors": {"electricity": 1.09},
                        "dissipation": 0.0085,
                    },
                }
            )
        )


        tech = "saltCavernH2_G"
        capex, opex, lifespan = tech_eco_data.get_capex_new_tech_RTE(
            tech, hyp="ref", year=y_ref(year, y_act)
        )
        scenarioFr["storageTechs"].append(
            pd.DataFrame(
                data={
                    tech: {
                        "AREA": area,
                        "YEAR": year,
                        "resource": "hydrogen",
                        "storagelifeSpan": lifespan,
                        "storagePowerCost": 1000,
                        "storageEnergyCost": capex,
                        "storageOperationCost": opex,
                        "p_max": 100000,
                        "c_max": 1000000,
                        "chargeFactors": {"electricity": 0.0168, "hydrogen": 1},
                        "dischargeFactors": {"hydrogen": 1},
                        "dissipation": 0,
                    },
                }
            )
        )

scenarioFr["storageTechs"] = pd.concat(scenarioFr["storageTechs"], axis=1)

scenarioFr["carbonTax"] = pd.DataFrame(
    data=np.linspace(0.0675, 0.165, nYears), index=yearList, columns=("carbonTax",)
)

scenarioFr["carbonGoals"] = pd.DataFrame(
    data=np.linspace(974e6, 205e6, nYears), index=yearList, columns=("carbonGoals",)
)


scenarioFr["turpeFactorsHTB"] = pd.DataFrame(
    columns=["HORAIRE", "fixeTurpeHTB"],
    data={"P": 5880, "HPH": 5640, "HCH": 5640, "HPE": 5280, "HCE": 4920}.items(),
).set_index(
    "HORAIRE"
)  # en €/MW/an part abonnement


scenarioFr["gridConnection"] = pd.read_csv(
    inputPath + "CalendrierHTB_TIME.csv", sep=",", decimal=".", skiprows=0, comment="#"
).set_index(["TIMESTAMP"])


scenarioFr["maxImportCap"] = pd.concat(
    (
        pd.DataFrame(
            index=[year],
            data={
                "electricity": 0,
                "gazNat": 10e10,
                "gazBio": 310e6,
                "hydrogen": 0,
                "gaz": 0,
                "uranium": 10e10,
            },
        )
        for k, year in enumerate(yearList[1:])
    )
)

scenarioFr["maxExportCap"] = pd.concat(
    (
        pd.DataFrame(
            index=[year],
            data={
                "electricity": 0,
                "gazNat": 0,
                "gazBio": 0,
                "hydrogen": 0,
                "gaz": 0,
                "uranium": 0,
            },
        )
        for k, year in enumerate(yearList[1:])
    )
)


df_res_ref = pd.read_csv(
    inputPath + "/set2019_horaire_TIMExRES.csv", sep=",", decimal=".", skiprows=0, comment="#"
).set_index(["TIMESTAMP", "RESOURCES"])

gridConnection = pd.read_csv(
    inputPath + "CalendrierHTB_TIME.csv", sep=",", decimal=".", skiprows=0, comment="#"
).set_index(["TIMESTAMP"])
calendar = gridConnection["Calendrier"].loc[t]
gridConnection["TIME"] = tmoy
scenarioFr["gridConnection"] = (
    gridConnection[["HTB", "TIME"]]
    .groupby(["TIME"])
    .mean()
    .reset_index()
    .rename(columns={"TIME": "TIMESTAMP"})
)
scenarioFr["gridConnection"]["Calendrier"] = calendar.values
scenarioFr["gridConnection"].set_index("TIMESTAMP", inplace=True)
scenarioFr["turpeFactorsHTB"] = pd.DataFrame(
    columns=["HORAIRE", "fixeTurpeHTB"],
    data={"P": 5880, "HPH": 5640, "HCH": 5640, "HPE": 5280, "HCE": 4920}.items(),
).set_index(
    "HORAIRE"
)  # en €/MW/an part abonnement

biogasPrice = {2020: 120, 2030: 105, 2040:90 , 2050:75}
scenarioFr["resourceImportPrices"] = pd.concat(
    (
        pd.DataFrame(
            data={
                "AREA": area,
                "YEAR": year,
                "TIMESTAMP": tmoy,
                "electricity": 100000 * np.ones(oneYear),
                "gazNat": df_res_ref.loc[(slice(None), "gazNat"), "importCost"].values
                * (1 if year <= 2020 else 2),
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

scenarioFr["resourceImportPrices"] = (
    scenarioFr["resourceImportPrices"].groupby(["AREA", "YEAR", "TIMESTAMP"]).mean().reset_index()
)

scenarioFr["resourceImportCO2eq"] = pd.concat(
    (
        pd.DataFrame(
            data={
                "AREA": area,
                "YEAR": year,
                "TIMESTAMP": tmoy,
                "electricity": 0 * np.ones(oneYear),
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
                "uranium": 0 * np.ones(oneYear),
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

scenarioFr["resourceImportCO2eq"] = (
    scenarioFr["resourceImportCO2eq"].groupby(["AREA", "YEAR", "TIMESTAMP"]).mean().reset_index()
)

availabilityFactor = pd.read_csv(
    inputPath + "availabilityFactor2019_Fr_TIMExTECH.csv", sep=",", decimal=".", skiprows=0
).set_index(["TIMESTAMP", "TECHNOLOGIES"])
techs = list(availabilityFactor.index.get_level_values("TECHNOLOGIES").unique())

scenarioFr["availability"] = []
for year in yearList[1:]:
    for tech in techs:
        scenarioFr["availability"].append(
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


scenarioFr["availability"] = pd.concat(scenarioFr["availability"], axis=0)
scenarioFr["availability"] = (
    scenarioFr["availability"]
    .reset_index()
    .groupby(["YEAR", "TIMESTAMP", "TECHNOLOGIES"])
    .mean()
    .drop(columns="index")
)
itechs = scenarioFr["availability"].index.isin(ctechs, level=2)
scenarioFr["availability"] = scenarioFr["availability"].loc[(slice(None), slice(None), itechs)]

scenarioFr["transitionFactors"] = pd.DataFrame(
    {"TECHNO1": [], "TECHNO2": [], "TransFactor": 1}
).set_index(["TECHNO1", "TECHNO2"])


# print(scenarioFr.keys())
# print(scenarioFr['conversionTechs'])
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.max_rows', 500)
