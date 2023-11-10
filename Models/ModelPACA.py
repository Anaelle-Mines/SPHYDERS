import os

os.sys.path.append(r"../")
import time

import pandas as pd
import numpy as np
from pyomo.environ import SolverFactory

from Functions.f_multiResourceModels_multiNodes import systemModel_multiResource_multiNodes
from Functions.f_optimization import getConstraintsDual_panda, getVariables_panda
from Functions.loadScenario import loadScenario
# from Scenarios.scenario_creation import scenarioDict
# from Scenarios.scenarios_ISGT import scenarioDict_ISGT
# from Scenarios.scenarios_caverns_robustness import scenarioDict_Cavern_robustness
from Scenarios.scenarios_sensitivity_valueSMR import scenarioDict_sensitivity_valueSMR

scenarioDict_run={k: v.copy() for (k, v) in scenarioDict_sensitivity_valueSMR.items()}
scenarioList=['gas_x5_CCS10','BM_90_CCS10']
year_results = 2030
area_results = "Marseille"

#----------------------------------------------------------------------------------------------------------------------------#

pd.set_option("display.max_columns", 500)

outputPath = "../data/output/SMRAnalysis/"

solver = "mosek"
# solver= 'appsi_highs'

if solver == "appsi_highs":
    solverpath_folder = "C:\\Users\\anaelle.jodry\\Documents\\highs.mswin64.20230531"
    os.sys.path.append(solverpath_folder)

for scenarioName in scenarioList:

    timeStep=scenarioDict_run[scenarioName]['timeStep'].loc[0,'timeStep']

    inputDict = loadScenario(scenarioDict_run[scenarioName], False)

    outputFolder = outputPath + scenarioName + '_PACA'
    outputFolderScenario=outputFolder+'/scenario'

    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    ### Calculation

    print("Building model PACA " + scenarioName + "...")
    model = systemModel_multiResource_multiNodes(inputDict, isAbstract=False)
    start_clock = time.time()
    print("Calculating model PACA " + scenarioName + "...")
    opt = SolverFactory(solver)
    results = opt.solve(model)
    end_clock = time.time()
    print("Computational time: {:.0f} s".format(end_clock - start_clock))


    res = {
        "variables": getVariables_panda(model),
        "constraints": getConstraintsDual_panda(model),
    }

    clock = pd.DataFrame(["time", end_clock - start_clock])
    res["variables"].update({"Computational time (s)": clock})

    print(str(results.Problem))
    print(
        "Valeur de la fonction objectif = ", res["variables"]["objective_Pvar"].sum()["objective_Pvar"]
    )


    ### Check sum Prod = Consumption
    production_df = (
        res["variables"]["energy_Pvar"]
        .set_index(["AREA", "YEAR_op"])
        .loc[area_results, year_results]
        .pivot(index="TIMESTAMP", columns="RESOURCES", values="energy_Pvar")
    )
    areaConsumption_df = inputDict["resourceDemand"].set_index(["AREA", "YEAR"]).loc[area_results, year_results]
    Delta = production_df.sum(axis=0) - areaConsumption_df.sum(axis=0)
    abs(Delta).max()
    print("Vérification équilibre O/D : \n", Delta)
    print(
        "Production par énergie (TWh) : \n", production_df.sum(axis=0) / 10**6
    )  ### energies produites TWh (ne comprends pas ce qui est consommé par le système)


    ### save results
    var_name = list(res["variables"].keys())
    cons_name = list(res["constraints"].keys())


    try:
        os.mkdir(outputFolder)
    except:
        pass

    for k, v in res["variables"].items():
        v.to_csv(outputFolder + "/" + k + ".csv", index=True)


    if not os.path.exists(outputFolderScenario):
        os.makedirs(outputFolderScenario)


    for k, v in scenarioDict_run[scenarioName].items():
        if type(v) is list:
            v=pd.DataFrame(data={k:v})
            v.to_csv(outputFolderScenario + "/" + k + ".csv")
        elif type(v) is np.int32:
            v=pd.DataFrame(data={k:[v]})
            v.to_csv(outputFolderScenario + "/" + k + ".csv")
        else:
            v.to_csv(outputFolderScenario + "/" + k + ".csv", index=True)
