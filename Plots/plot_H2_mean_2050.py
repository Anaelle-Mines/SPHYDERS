import os

os.sys.path.append(r"../")
from Functions.f_graphicTools_manuscript import plot_H2Mean2050
from Functions.loadScenario import loadScenario
from Scenarios.scenario_creation import scenarioDict

# First : execute runPACA.py Re_inf

outputPath = "../data/output/"
scenario = "ref"
outputFolder = outputPath + scenario + "_PACA"
area='Marseille'

inputDict = loadScenario(scenarioDict[scenario])

plot_H2Mean2050(inputDict,area, outputFolder)
