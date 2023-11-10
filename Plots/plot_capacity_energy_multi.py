# region Importation of modules
import os
import pandas as pd

os.sys.path.append(r"../")
from Functions.f_graphicTools_manuscript import plot_capacity, plot_energy,plot_energy_new,plot_stockLevel
from Scenarios.scenarios_sensitivity_valueSMR import scenarioDict_sensitivity_valueSMR
from Scenarios.scenarios_LRAnalysis import scenarioDict_LRAnalysis_PACA
from Scenarios.scenario_creation import scenarioDict

from Functions.f_extract_data import extract_energy
# endregion

# First : execute runPACA.py Ref

outputPath = "../data/output/"
scenarioList =['ref']

for scenarioName in scenarioList:
	outputFolder = outputPath + scenarioName +'_PACA'
	TIMESTAMP = (pd.read_csv(outputFolder + "/power_Dvar.csv").set_index("TIMESTAMP").index.unique().values)
	timeStep = TIMESTAMP[2] - TIMESTAMP[1]


	# plot_capacity("Marseille", timeStep, outputFolder, LoadFac=True)
	# plot_energy_new("Marseille", timeStep, outputFolder)
	plot_stockLevel("Marseille", timeStep, outputFolder)

