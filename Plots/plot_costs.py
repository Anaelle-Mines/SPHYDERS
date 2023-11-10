import os

os.sys.path.append(r"../")

from Functions.f_extract_data import extract_costs
from Functions.f_graphicTools_manuscript import plot_costs, plot_costs_detailed, plot_costs_new
from Scenarios.scenario_creation import scenarioDict

# First : execute runPACA.py

outputPath = "../data/output/"

scenarioList = ['ref']

for scenarioName in scenarioList:

	timeStep=scenarioDict[scenarioName]['timeStep'].loc[0,'timeStep']
	outputFolder = outputPath + scenarioName + '_PACA'
	scenario = scenarioDict[scenarioName]

	area='Marseille'

	df = extract_costs(scenario,area,outputFolder)

	# plot_costs(df, outputFolder)
	# plot_costs_detailed(df, outputFolder)
	plot_costs_new(df, outputFolder)
