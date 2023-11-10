import os

os.sys.path.append(r"../")
import time

import pandas as pd
import numpy as np
from pyomo.environ import SolverFactory
from Functions.f_multiResourceModels_multiNodes import systemModel_multiResource_multiNodes,ElecPrice_optim
from Functions.f_optimization import getConstraintsDual_panda, getVariables_panda
from Functions.f_extract_data import extract_energy
from Functions.loadScenario import loadScenario
from Scenarios.scenarios_WACCAnalysis import scenarioDict_WACCAnalysis_PACA, scenarioDict_WACCAnalysis_Fr

outputPath = "../data/output/WACCAnalysis/"
solver = "mosek"

#----------------------------------------------------------------------------------------------------------------------------#


# areaList=['France']

# for s in scenarioDict_WACCAnalysis_Fr.keys():

#     inputDict = loadScenario(scenarioDict_WACCAnalysis_Fr[s], False)
#     timeStep=scenarioDict_WACCAnalysis_Fr[s]['timeStep'].loc[0,'timeStep']

#     outputFolder = outputPath + s
#     if not os.path.exists(outputFolder):
#         os.makedirs(outputFolder)

#     ### Calculation

#     print("Building model France_"+s+"...")
#     model = systemModel_multiResource_multiNodes(inputDict, isAbstract=False)
#     start_clock = time.time()
#     print("Calculating model France_"+s+"...")
#     opt = SolverFactory(solver)
#     results = opt.solve(model)
#     end_clock = time.time()
#     print("Computational time: {:.0f} s".format(end_clock - start_clock))


#     res = {
#         "variables": getVariables_panda(model),
#         "constraints": getConstraintsDual_panda(model),
#     }

#     clock = pd.DataFrame(["time", end_clock - start_clock])
#     res["variables"].update({"Computational time (s)": clock})

#     ### save results
#     var_name = list(res["variables"].keys())
#     cons_name = list(res["constraints"].keys())

#     try:
#         os.mkdir(outputFolder)
#     except:
#         pass

#     for k, v in res["variables"].items():
#         v.to_csv(outputFolder + "/" + k + ".csv", index=True)


#     elecPrice = round(
#         res["constraints"]["energyCtr"]
#         .set_index(["AREA", "RESOURCES"])
#         .loc[("France", "electricity")]
#         .set_index(["YEAR_op", "TIMESTAMP"]),
#         2,
#     )

#     Carbon = res["variables"]["carbon_Pvar"].set_index(["YEAR_op", "TIMESTAMP"])
#     Carbon.loc[Carbon["carbon_Pvar"] < 0.01] = 0
#     Prod_elec = (
#         res["variables"]["energy_Pvar"]
#         .loc[res["variables"]["energy_Pvar"]["RESOURCES"] == "electricity"]
#         .groupby(["AREA", "YEAR_op", "TIMESTAMP"])
#         .sum()
#         .loc[("France", slice(None), slice(None))]
#     )
#     Carbon_content = Carbon["carbon_Pvar"] / Prod_elec["energy_Pvar"]
#     Carbon_content = round(
#         Carbon_content.reset_index()
#         .set_index("YEAR_op")
#         .rename(columns={0: "carbonContent"})
#         .set_index("TIMESTAMP", append=True)
#     )

#     elecPrice.to_csv(outputFolder + "/elecPrice.csv", index=True)
#     Carbon_content.to_csv(outputFolder + "/carbon.csv", index=True)

#     marketPrice, elec_prod = ElecPrice_optim(
#         inputDict, area="France", IntercoOut=50, solver="mosek", outputFolder=outputFolder
#     )


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

areaList=['Marseille']

dico={}
c=0
for scenar in scenarioDict_WACCAnalysis_PACA.keys() :

    inputDict = loadScenario(scenarioDict_WACCAnalysis_PACA[scenar], False)

    outputFolder = outputPath + scenar
    outputFolderScenario=outputPath + scenar + '/scenario'
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    ### Calculation

    print("Building model PACA_"+scenar+"...")
    model = systemModel_multiResource_multiNodes(inputDict, isAbstract=False)

    start_clock = time.time()
    print("Calculating model PACA_"+scenar+"...")
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


    for k, v in scenarioDict_WACCAnalysis_PACA[scenar].items():
        if type(v) is list:
            v=pd.DataFrame(data={k:v})
            v.to_csv(outputFolderScenario + "/" + k + ".csv")
        elif type(v) is np.int32:
            v=pd.DataFrame(data={k:[v]})
            v.to_csv(outputFolderScenario + "/" + k + ".csv")
        else:
            v.to_csv(outputFolderScenario + "/" + k + ".csv", index=True)

    df=extract_energy(scenarioDict_WACCAnalysis_PACA[scenar],'Marseille',outputFolder)[["SMR w/o CCUS","SMR + CCUS 50%","SMR + CCUS 90%","Alkaline electrolysis","PEM electrolysis","importsH2",'curtailment','totalProd','carbon','total_carbon','costs','total_costs']]
    df['scenario']=scenar
    df['order']=c
    c+=1
    dico[scenar]=df


df=pd.concat([dico[s] for s in dico.keys()])
df.to_csv(outputPath+'results_WACC.csv', index=True)




