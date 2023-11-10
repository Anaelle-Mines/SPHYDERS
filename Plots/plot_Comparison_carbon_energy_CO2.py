import os

import pandas as pd

os.sys.path.append(r"../")
from Functions.f_extract_data import extract_energy, extract_capa
from Functions.f_graphicTools_manuscript import plot_compare_energy_and_carbon,plot_compare_capacity_and_costs
from Scenarios.scenario_creation import scenarioDict

# First : execute runPACA.py CO2_10 Ref CO2_100

outputPath = "../data/output/"

dico_ener = {}
area='Marseille'
scenarioList = ["CO2_10", "ref", "CO2_100"]
scenarioNames = [
    "CO$_2$=10€/t$_{captured}$",
    "CO$_2$=50€/t$_{captured}$",
    "CO$_2$=100€/t$_{captured}$",
]

for s in scenarioList:
    outputFolder = outputPath + s + "_PACA"
    dico_ener[s] = extract_energy(scenarioDict[s],area ,outputFolder)

plot_compare_energy_and_carbon(dico_ener, scenarioNames, outputPath)


# First : execute runPACA.py Cavern Ref CavernREinf

outputPath = "../data/output/"

dico_ener = {}
dico_capa = {}
area='Marseille'
scenarioList = ["ref", "Cavern", "CavernREinf"]
scenarioNames = [
    "Without geological storage",
    "With geological storage",
    "With geological storage \n + unlimited renewables",
]

for s in scenarioList:
    outputFolder = outputPath + s + "_PACA"
    dico_ener[s] = extract_energy(scenarioDict[s],area ,outputFolder)
    dico_capa[s] = extract_capa(scenarioDict[s],area ,outputFolder)

plot_compare_energy_and_carbon(dico_ener, scenarioNames, outputPath,name='Cavern')
plot_compare_capacity_and_costs(dico_capa, dico_ener, scenarioNames, outputPath,name='Cavern')


# First : execute runPACA.py  Ref Re_x2 Re_inf

outputPath = "../data/output/"

dico_ener = {}
dico_capa = {}
area='Marseille'
scenarioList = ["ref", "Re_x2", "Re_inf"]
scenarioNames = [
    "Reference",
    "Doubled renewables",
    "Unlimited renewables",
]

for s in scenarioList:
    outputFolder = outputPath + s + "_PACA"
    dico_ener[s] = extract_energy(scenarioDict[s],area ,outputFolder)
    dico_capa[s] = extract_capa(scenarioDict[s],area ,outputFolder)

plot_compare_energy_and_carbon(dico_ener, scenarioNames, outputPath,name='Re')
plot_compare_capacity_and_costs(dico_capa, dico_ener, scenarioNames, outputPath,name='Re')


# First : execute runPACA.py  Ref BM_60 BM_90

outputPath = "../data/output/"

dico_ener = {}
area='Marseille'
scenarioList = ["BM_60","ref",  "BM_90"]
scenarioNames = [
    "Cheap biomethane",
    "Reference",
    "Expensive biomethane",
]

for s in scenarioList:
    outputFolder = outputPath + s + "_PACA"
    dico_ener[s] = extract_energy(scenarioDict[s],area ,outputFolder)

plot_compare_energy_and_carbon(dico_ener, scenarioNames, outputPath,name='BM')


# First : execute runPACA.py  Ref cheap_H2 import_H2


outputPath = "../data/output/"

dico_ener = {}
area='Marseille'
scenarioList = ["ref", "import_H2", "cheap_H2"]
scenarioNames = [
    "Reference",
    "Hydrogen imports",
    "Cheap hydrogen imports",
]

for s in scenarioList:
    outputFolder = outputPath + s + "_PACA"
    dico_ener[s] = extract_energy(scenarioDict[s],area ,outputFolder)

plot_compare_energy_and_carbon(dico_ener, scenarioNames, outputPath,name='Imports')

