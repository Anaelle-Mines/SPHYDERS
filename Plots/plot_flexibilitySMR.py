import os
import pandas as pd
os.sys.path.append(r"../")
from Functions.f_extract_data import extract_costs,extract_energy
from Functions.f_graphicTools_manuscript import plot_total_co2_emissions_and_flexSMR,plot_energy_new
from Scenarios.scenarios_sensitivity_valueSMR import scenarioDict_sensitivity_valueSMR
from Scenarios.scenario_creation import scenarioDict

outputPath = "../data/output/SMRAnalysis/"

scenarioList =list(scenarioDict_sensitivity_valueSMR.keys())
scenarioNames = [
    "Re_inf",
    "Re_inf_TC200",
    "Re_inf_CCS10",
    "Caverns",
    "Caverns_TC200",
    "Caverns_CCS10",
    "CavernREinf",
    "CavernREinf_TC200",
    "CavernREinf_CCS10",
    "gas_x5",
    "gas_x5_TC200",
    "gas_x5_CCS10",
    "BM_90",
    "BM_90_TC200",
    "BM_90_CCS10",
]
labels = [
    "Unlimited RE potential",
    "Unlimited RE potential TC=200€/t",
    "Unlimited RE potential CCS=10€/t",
    "Geological storage",
    "Geological storage TC=200€/t",
    "Geological storage CCS=10€/t",
    "Unlimited + storage",
    "Unlimited + storage TC=200€/t",
    "unlimited + storage CCS=10€/t",
    "Expensive natural gas",
    "Expensive gas TC=200€/t",
    "Expensive gas CCS=10€/t",
    "Expensive biomethane",
    "Expensive biomethane TC=200€/t",
    "Expensive biomethane CCS=10€/t",
]

dico_ener = {}
for s in scenarioList:
    outputFolder = outputPath + s + "_PACA"
    dico_ener[s] = extract_energy(scenarioDict_sensitivity_valueSMR[s],'Marseille',outputFolder)[['totalProd','total_carbon','total_costs']]
    dico_ener[s]['scenario']=s
    outputFolder = "../data/output/ref_PACA"
    dico_ener['ref']=extract_energy(scenarioDict['ref'],'Marseille',outputFolder)[['totalProd','total_carbon','total_costs']]
    dico_ener['ref']['scenario']='ref'
    outputFolder = "../data/output/woSMR_2030_PACA"
    dico_ener['ref_woSMR']=extract_energy(scenarioDict['woSMR_2030'],'Marseille',outputFolder)[['totalProd','total_carbon','total_costs']]
    dico_ener['ref_woSMR']['scenario']='ref_woSMR'

df=pd.concat([dico_ener[s] for s in dico_ener.keys()])
df.to_csv(outputPath+'results_valueSMR.csv', index=True)

flex = plot_total_co2_emissions_and_flexSMR(dico_ener, scenarioNames, labels,area='Marseille', outputPath=outputPath)
