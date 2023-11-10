import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd

from data.Raw import tech_eco_data
from Functions.f_getCapa_robustness import get_newScenario,get_newScenario_cavern2040,get_newScenario_woSMR2040
from Scenarios.scenarios_caverns_robustness import scenarioDict_Cavern_robustness
from Scenarios.scenario_creation import scenarioDict

scenarioDict_robustness={}

inputPath = "../data/Raw/"
outputPath="../data/output/"

areaList = ["Marseille"]
y_act = "middle"

# Liste des scenarios à garder pour analyse :

scenarioList=['ref','gas_x5','BM_60','CO2_100','import_H2','Re_inf','woSMR_2040','expensiveRE'] 
aleaList=['expensiveRE']#['ref','gas_x5','BM_60','CO2_100','import_H2','cheap_H2','expensiveRE']

for scenarioAlea in aleaList:
    for scenarioCapa in scenarioList:
        outputFolder_capa=outputPath+scenarioCapa+'_PACA'
        if scenarioCapa == scenarioAlea:
            scenarioDict_robustness[scenarioCapa]={k: v.copy() for (k, v) in scenarioDict[scenarioCapa].items()}
        else:
            scenarioNewName=scenarioCapa+'_'+scenarioAlea
            scenario_new={k: v.copy() for (k, v) in scenarioDict[scenarioAlea].items()}
            scenario_new['conversionTechs'],scenario_new['storageTechs']=get_newScenario(outputFolder_capa,scenarioAlea,y_act,scenarioDict)
            scenarioDict_robustness[scenarioNewName]=scenario_new
        if scenarioCapa not in aleaList :
            scenarioDict_robustness[scenarioCapa]={k: v.copy() for (k, v) in scenarioDict[scenarioCapa].items()}


# Alea 'woSMR_2040'

for scenarioCapa in scenarioList:
    if scenarioCapa == 'woSMR_2040':
        scenarioDict_robustness[scenarioCapa]={k: v.copy() for (k, v) in scenarioDict[scenarioCapa].items()}
    else:
        outputFolder_capa=outputPath+scenarioCapa+'_PACA'
        scenarioNewName=scenarioCapa+'_woSMR_2040'
        scenario_new={k: v.copy() for (k, v) in scenarioDict['woSMR_2040'].items()}
        scenario_new['conversionTechs'],scenario_new['storageTechs']=get_newScenario_woSMR2040(outputFolder_capa,y_act)
        scenarioDict_robustness[scenarioNewName]=scenario_new

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# # # With caverns


scenarioList=['Cavern','gas_x5Cavern', 'BM_60Cavern', 'CO2_100Cavern', 'import_H2Cavern', 'Re_infCavern', 'woSMR_2040Cavern', 'expensiveRECavern']
aleaList=['Cavern', 'gas_x5Cavern', 'BM_60Cavern', 'CO2_100Cavern', 'import_H2Cavern','cheap_H2Cavern','expensiveRECavern']


for scenarioAlea in aleaList:
    for scenarioCapa in scenarioList:
        outputFolder_capa=outputPath+scenarioCapa+'_PACA'
        if scenarioCapa == scenarioAlea:
            scenarioDict_robustness[scenarioCapa]={k: v.copy() for (k, v) in scenarioDict_Cavern_robustness[scenarioCapa].items()}
        else:
            scenarioNewName=scenarioCapa+'_'+scenarioAlea
            scenario_new={k: v.copy() for (k, v) in scenarioDict_Cavern_robustness[scenarioAlea].items()}
            scenario_new['conversionTechs'],scenario_new['storageTechs']=get_newScenario(outputFolder_capa,scenarioAlea,y_act,scenarioDict_Cavern_robustness)
            scenarioDict_robustness[scenarioNewName]=scenario_new
        if scenarioCapa not in aleaList :
            scenarioDict_robustness[scenarioCapa]={k: v.copy() for (k, v) in scenarioDict_Cavern_robustness[scenarioCapa].items()}


# Alea 'Cavern2040'

# for scenarioCapa in scenarioList:
#     outputFolder_capa=outputPath+scenarioCapa+'_PACA'
#     scenarioNewName=scenarioCapa+'_Cavern2040'
#     scenario_new={k: v.copy() for (k, v) in scenarioDict_Cavern_robustness['Cavern2040'].items()}
#     scenario_new['conversionTechs'],scenario_new['storageTechs']=get_newScenario_cavern2040(outputFolder_capa,y_act)
#     scenarioDict_robustness[scenarioNewName]=scenario_new

# Alea 'woSMR_2040'

for scenarioCapa in scenarioList:
    if scenarioCapa == 'woSMR_2040Cavern':
        scenarioDict_robustness[scenarioCapa]={k: v.copy() for (k, v) in scenarioDict_Cavern_robustness[scenarioCapa].items()}
    else:
        outputFolder_capa=outputPath+scenarioCapa+'_PACA'
        scenarioNewName=scenarioCapa+'_woSMR_2040Cavern'
        scenario_new={k: v.copy() for (k, v) in scenarioDict_Cavern_robustness['woSMR_2040Cavern'].items()}
        scenario_new['conversionTechs'],scenario_new['storageTechs']=get_newScenario_woSMR2040(outputFolder_capa,y_act)
        scenarioDict_robustness[scenarioNewName]=scenario_new

