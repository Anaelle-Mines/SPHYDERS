import os

os.sys.path.append(r"../")
import time

import pandas as pd
from pyomo.environ import SolverFactory

from Functions.f_multiResourceModels_multiNodes import ElecPrice_optim, systemModel_multiResource_multiNodes
from Functions.f_optimization import getConstraintsDual_panda, getVariables_panda
from Functions.f_graphicTools_manuscript import plot_capacity, plot_energy_new, plot_costs_new
from Functions.f_extract_data import extract_costs
from Functions.f_graphicTools_Fr import plot_monotone
from Functions.loadScenario import loadScenario
from Scenarios.scenario_creationFr import scenarioDictFr
from Scenarios.scenario_creation import scenarioDict


solver = "mosek"
# solver = "appsi_highs"

outputPath = "../data/output/"

scenarioNameFr='ref_Fr'
scenarioNamePACA='ref'


#Run Model France

inputDict = loadScenario(scenarioDictFr[scenarioNameFr], False)

outputFolderFr = outputPath + scenarioNameFr + '_1h'
if not os.path.exists(outputFolderFr):
    os.makedirs(outputFolderFr)

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
print("Valeur de la fonction objectif = ", res["variables"]["objective_Pvar"].sum()["objective_Pvar"])


### save results
var_name = list(res["variables"].keys())
cons_name = list(res["constraints"].keys())

try:
    os.mkdir(outputFolderFr)
except:
    pass

for k, v in res["variables"].items():
    v.to_csv(outputFolderFr + "/" + k + ".csv", index=True)


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

elecPrice.to_csv(outputFolderFr + "/elecPrice.csv", index=True)
Carbon_content.to_csv(outputFolderFr + "/carbon.csv", index=True)

marketPrice, elec_prod = ElecPrice_optim(inputDict, area="France", IntercoOut=50, solver="mosek", outputFolder=outputFolderFr)

plot_monotone(outputFolderFr)

# Run model PACA

inputDict = loadScenario(scenarioDict[scenarioNamePACA], False)

outputFolderPACA = outputPath + scenarioNamePACA + '_PACA'
outputFolderScenario=outputFolderPACA+'/scenario'

if not os.path.exists(outputFolderPACA):
    os.makedirs(outputFolderPACA)

### Calculation

print("Building model PACA " + scenarioNamePACA + "...")
model = systemModel_multiResource_multiNodes(inputDict, isAbstract=False)
start_clock = time.time()
print("Calculating model PACA " + scenarioNamePACA + "...")
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
print("Valeur de la fonction objectif = ", res["variables"]["objective_Pvar"].sum()["objective_Pvar"])


### save results
var_name = list(res["variables"].keys())
cons_name = list(res["constraints"].keys())


try:
    os.mkdir(outputFolderPACA)
except:
    pass

for k, v in res["variables"].items():
    v.to_csv(outputFolderPACA + "/" + k + ".csv", index=True)


if not os.path.exists(outputFolderScenario):
    os.makedirs(outputFolderScenario)


for k, v in scenarioDict[scenarioNamePACA].items():
    if type(v) is list:
        v=pd.DataFrame(data={k:v})
        v.to_csv(outputFolderScenario + "/" + k + ".csv")
    elif type(v) is np.int32:
        v=pd.DataFrame(data={k:[v]})
        v.to_csv(outputFolderScenario + "/" + k + ".csv")
    else:
        v.to_csv(outputFolderScenario + "/" + k + ".csv", index=True)


plot_capacity("Marseille", 1, outputFolderPACA, LoadFac=True)
plot_energy_new("Marseille", 1, outputFolderPACA)

df = extract_costs(scenarioDict[scenarioNamePACA],"Marseille",outputFolderPACA)
plot_costs_new(df, outputFolderPACA)