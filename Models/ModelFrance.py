import os

os.sys.path.append(r"../")
import time

import pandas as pd
from pyomo.environ import SolverFactory

from Functions.f_multiResourceModels_multiNodes import (
    ElecPrice_optim,
    systemModel_multiResource_multiNodes,
)
from Functions.f_optimization import getConstraintsDual_panda, getVariables_panda
from Functions.loadScenario import loadScenario
from Scenarios.scenario_creationFr import scenarioDictFr

# pd.set_option("display.max_columns", 500)

outputPath = "../data/output/"

solver = "mosek"
# solver = "appsi_highs"

if solver == "appsi_highs":
    solverpath_folder = "C:\\Users\\anaelle.jodry\\Documents\\highs.mswin64.20230531"
    os.sys.path.append(solverpath_folder)

scenarioName='expensiveRE_Fr'
inputDict = loadScenario(scenarioDictFr[scenarioName], False)
timeStep=scenarioDictFr[scenarioName]['timeStep'].loc[0,'timeStep']

outputFolder = outputPath + scenarioName + '_' + str(timeStep) + 'h'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

### Calculation

print("Building model France...")
model = systemModel_multiResource_multiNodes(inputDict, isAbstract=False)
start_clock = time.time()
print("Calculating model France...")
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
year_results = 2030
area = "France"
production_df = (
    res["variables"]["energy_Pvar"]
    .set_index(["AREA", "YEAR_op"])
    .loc[area, year_results]
    .pivot(index="TIMESTAMP", columns="RESOURCES", values="energy_Pvar")
)
areaConsumption_df = inputDict["resourceDemand"].set_index(["AREA", "YEAR"]).loc[area, year_results]
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


elecPrice = round(
    res["constraints"]["energyCtr"]
    .set_index(["AREA", "RESOURCES"])
    .loc[("France", "electricity")]
    .set_index(["YEAR_op", "TIMESTAMP"]),
    2,
)

Carbon = res["variables"]["carbon_Pvar"].set_index(["YEAR_op", "TIMESTAMP"])
Carbon.loc[Carbon["carbon_Pvar"] < 0.01] = 0
Prod_elec = (
    res["variables"]["energy_Pvar"]
    .loc[res["variables"]["energy_Pvar"]["RESOURCES"] == "electricity"]
    .groupby(["AREA", "YEAR_op", "TIMESTAMP"])
    .sum()
    .loc[("France", slice(None), slice(None))]
)
Carbon_content = Carbon["carbon_Pvar"] / Prod_elec["energy_Pvar"]
Carbon_content = round(
    Carbon_content.reset_index()
    .set_index("YEAR_op")
    .rename(columns={0: "carbonContent"})
    .set_index("TIMESTAMP", append=True)
)

elecPrice.to_csv(outputFolder + "/elecPrice.csv", index=True)
Carbon_content.to_csv(outputFolder + "/carbon.csv", index=True)

marketPrice, elec_prod = ElecPrice_optim(
    inputDict, area="France", IntercoOut=50, solver="mosek", outputFolder=outputFolder
)

# endregion
