import os

os.sys.path.append(r"../")
from Functions.f_extract_data import extract_costs
from Functions.f_graphicTools_manuscript import plot_costs2050
from Scenarios.scenario_creation import scenarioDict

# First : execute runPACA.py BM_60 Ref BM_90

outputPath = "../data/output/"
area='Marseille'

ScenarioName = "BM_60"
outputFolder = outputPath + ScenarioName + "_PACA"
df = extract_costs(scenarioDict[ScenarioName],area, outputFolder)
df["AEL BM=60€"] = df.pop("AEL")
df["SMR BM=60€"] = df.pop("SMR")
df.pop('Imports')


for l in df.keys():
    df[l] = df[l].reset_index().loc[df[l].reset_index().YEAR == 2050].set_index("YEAR")

ScenarioName = "ref"
outputFolder = outputPath + ScenarioName + "_PACA"
df2 = extract_costs(scenarioDict[ScenarioName],area, outputFolder)
df2["AEL BM=75€"] = df2.pop("AEL")
df2["SMR BM=75€"] = df2.pop("SMR")
df2.pop('Imports')


for l in df2.keys():
    df2[l] = df2[l].reset_index().loc[df2[l].reset_index().YEAR == 2050].set_index("YEAR")

df.update(df2)

ScenarioName = "BM_90"
outputFolder = outputPath + ScenarioName + "_PACA"
df3 = extract_costs(scenarioDict[ScenarioName],area, outputFolder)
df3["AEL BM=90€"] = df3.pop("AEL")
df3["SMR BM=90€"] = df3.pop("SMR")
df3.pop('Imports')

for l in df3.keys():
    df3[l] = df3[l].reset_index().loc[df3[l].reset_index().YEAR == 2050].set_index("YEAR")

df.update(df3)

plot_costs2050(df, outputPath, comparaison=True)

print(df['SMR BM=90€']['carbon'])