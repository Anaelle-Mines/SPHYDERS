import os

os.sys.path.append(r"../")
from Functions.f_extract_data import extract_energy
from Functions.f_graphicTools_manuscript import plot_carbon
from Scenarios.scenario_creation import scenarioDict


outputPath = "../data/output/"
scenario = "ref"
outputFolder = outputPath + scenario + "_PACA"
area='Marseille'

df=extract_energy(scenarioDict[scenario],area,outputFolder)[['totalProd','carbon','total_carbon','costs','total_costs']]
df_conv=extract_energy(scenarioDict['conv_SmrOnly'],area,outputFolder = outputPath + "conv_SmrOnly_PACA")[['totalProd','carbon','total_carbon','costs','total_costs']]

plot_carbon(df,df_conv,area,outputFolder)