import os

os.sys.path.append(r"../")
import time

import pandas as pd
import numpy as np
from pyomo.environ import SolverFactory

from Functions.f_multiResourceModels_multiNodes import systemModel_multiResource_multiNodes
from Functions.f_optimization import getConstraintsDual_panda, getVariables_panda
from Functions.f_extract_data import extract_energy
from Functions.loadScenario import loadScenario
from Scenarios.scenario_creation_robustness import scenarioDict_robustness


scenarioList=scenarioDict_robustness.keys()
print(scenarioList)

outputPath = "../data/output/robustness/"
solver = "mosek"

#----------------------------------------------------------------------------------------------------------------------------#

dico={}
for scenarioName in scenarioList :

    inputDict = loadScenario(scenarioDict_robustness[scenarioName], False)

    outputFolder = outputPath + scenarioName + '_PACA'
    outputFolderScenario=outputPath + scenarioName + '_PACA/scenario'
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    ### Calculation

    print("Building model PACA..."+scenarioName)
    model = systemModel_multiResource_multiNodes(inputDict, isAbstract=False)

    start_clock = time.time()
    print("Calculating model PACA..."+scenarioName)
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


    for k, v in scenarioDict_robustness[scenarioName].items():
        if type(v) is list:
            v=pd.DataFrame(data={k:v})
            v.to_csv(outputFolderScenario + "/" + k + ".csv")
        elif type(v) is np.int32:
            v=pd.DataFrame(data={k:[v]})
            v.to_csv(outputFolderScenario + "/" + k + ".csv")
        else:
            v.to_csv(outputFolderScenario + "/" + k + ".csv", index=True)

    df=extract_energy(scenarioDict_robustness[scenarioName],'Marseille',outputFolder)[["SMR w/o CCUS","SMR + CCUS 50%","SMR + CCUS 90%","Alkaline electrolysis","PEM electrolysis","importsH2",'curtailment','totalProd','carbon','total_carbon','costs','total_costs']]
    df['scenario']=scenarioName
    dico[scenarioName]=df


df=pd.concat([dico[s] for s in dico.keys()])
df.to_csv(outputPath+'results.csv', index=True)




