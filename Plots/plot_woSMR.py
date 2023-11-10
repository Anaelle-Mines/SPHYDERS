import os

os.sys.path.append(r"../")
from Functions.f_extract_data import extract_costs,extract_energy
from Functions.f_graphicTools_manuscript import plot_carbonCosts,plot_compare_carbon_woSMR
from Scenarios.scenario_creation import scenarioDict

# First : execute runPACA.py Ref woSMR_2030 woSMR_2040 woSMR_2050

outputPath = "../data/output/"
area='Marseille'

dico_ener = {}
scenarioList = ["ref", "woSMR_2030", "woSMR_2040", "woSMR_2050"]
scenarioNames = ["Reference", "Ban on SMR from 2030", "Ban on SMR from 2040", "Ban on SMR from 2050"]
for s in scenarioList:
    outputFolder = outputPath + s + "_PACA"
    # dico_costs[s] = extract_costs(scenarioDict[s],area, outputFolder)
    dico_ener[s] = extract_energy(scenarioDict[s],area, outputFolder)[['totalProd','total_carbon','total_costs','carbon']]


plot_carbonCosts(dico_ener,area, scenarioNames)
# plot_compare_carbon_woSMR(dico_ener, scenarioNames, outputPath="../data/output/",name='woSMR')

