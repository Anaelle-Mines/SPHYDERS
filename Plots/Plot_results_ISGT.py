import os
import numpy as np
import pandas as pd
import csv
os.sys.path.append(r"../")

from Functions.f_graphicToolsISGT import plot_costs,plot_total_co2_emissions_and_costs,plot_compare_capacity,plot_sensibility_costs,plot_sensibility_costsT,plot_compare_energy,plot_sensitivity_energy
from Functions.f_graphicToolsISGT import extract_costs,extract_capa,extract_energy
from Scenarios.scenarios_ISGT import scenarioDict_ISGT

outputPath='../data/output/ISGT/'
scenarioDict=scenarioDict_ISGT
area='Marseille'

# #region general results
# ScenarioList=['scenario1','scenario2','scenario3','scenario4']
# # ScenarioName='scenario3'
# for ScenarioName in ScenarioList :

#     outputFolder = outputPath + ScenarioName

#     # plot installed capacity by technologies
#     capacity=plot_capacity(outputFolder)

#     # plot H2 production by technologies
#     energy=plot_energy(outputFolder)

#     # calculation of charge factors
#     chargeFactors=(energy/(capacity*8.760)).fillna(0)

#     # plot stock level
#     # plot_stock(outputFolder)

#     # plot carbon emissions
#     plot_carbon(outputFolder)

#     # plot costs
#     plot_Costs2030(extract_costs(scenarioDict[ScenarioName],outputFolder)['AEL'].loc[2030], outputFolder)
# #endregion

#region create csv data
# ScenarioList=['scenario1','scenario2','scenario3','scenario4','scenario3_10', 'scenario4_10', 'scenario3_50', 'scenario4_50', 'scenario3_250', 'scenario4_250', 'scenario3_500', 'scenario4_500', 'scenario1_tdemi', 'scenario1_tdouble', 'scenario2_tdemi', 'scenario2_tdouble', 'scenario3_tdemi', 'scenario3_tdouble', 'scenario4_tdemi', 'scenario4_tdouble']

# allCosts=pd.DataFrame()
# allEnergy=pd.DataFrame()
# allCapa=pd.DataFrame()

# for ScenarioName in ScenarioList :
#     outputFolder = outputPath + ScenarioName+'_PACA'
#     scenario = ScenarioName
#     temp1=extract_costs(scenarioDict[ScenarioName],area,outputFolder)
#     temp2=extract_energy(scenarioDict[ScenarioName],area,outputFolder)
#     temp3=extract_capa(area,outputFolder)

#     for tech in temp1.keys():
#         temp1[tech]['SCENARIO']=ScenarioName
#         temp1[tech]['TECHNOLOGIE']=tech
#         temp1[tech]=temp1[tech].reset_index().set_index(['YEAR','SCENARIO','TECHNOLOGIE'])
#         allCosts=allCosts.append(temp1[tech])

#     temp2['SCENARIO']=ScenarioName
#     temp2=temp2.reset_index().set_index(['YEAR_op','SCENARIO'])
#     allEnergy=allEnergy.append(temp2)

#     temp3['SCENARIO']=ScenarioName
#     temp3=temp3.reset_index().set_index(['YEAR_op','SCENARIO'])
#     allCapa=allCapa.append(temp3)

# allCosts.to_csv(outputPath+'allCosts.csv')
# allEnergy.to_csv(outputPath+'allEnergy.csv')
# allCapa.to_csv(outputPath+'allCapa.csv')


#region comparaison structure de coût

# ScenarioList=['scenario1','scenario2','scenario3','scenario4']
# for ScenarioName in ScenarioList:
#     outputFolder = outputPath + ScenarioName+'_PACA'
#     print('obj = ', pd.read_csv(outputFolder+'/objective_Pvar.csv').sum()['objective_Pvar'])

# df={}
# for ScenarioName in ScenarioList:
#     outputFolder = outputPath + ScenarioName+'_PACA'
#     df1=extract_costs(scenarioDict[ScenarioName],area,outputFolder)
#     SMR=df1.pop('SMR')
#     df1[ScenarioName]=df1.pop('AEL')
#     df.update(df1)

# plot_costs(df,outputPath)

#endregion

#region comparaison coût + carbon

# scenarioList=['scenario1','scenario2','scenario3','scenario4']
# scenarioNames=['scenario1','scenario2','scenario3','scenario4']

# dico_costs={}
# dico_ener={}
# for s in scenarioList:
#     outputFolder=outputPath+s+'_PACA'
#     dico_costs[s]=extract_costs(scenarioDict[s],area,outputFolder)['AEL'].loc[2030]
#     dico_ener[s]=extract_energy(scenarioDict[s],area,outputFolder)[['costs','total_carbon']].loc[2030]

# plot_total_co2_emissions_and_costs(dico_costs,dico_ener,scenarioNames,outputPath=outputPath)

# endregion

# region comparaison capacité installées

# scenarioList=['scenario1','scenario2','scenario3','scenario4']
# scenarioNames=['scenario1','scenario2','scenario3','scenario4']

# dico_capa={}
# dico_ener={}
# for s in scenarioList:
#     outputFolder=outputPath+s+'_PACA'
#     dico_capa[s]=extract_capa(area,outputFolder)
#     dico_ener[s]=extract_energy(scenarioDict[s],area,outputFolder)
#     dico_capa[s]['loadFac_elec']=dico_ener[s]['loadFac_elec']

# plot_compare_capacity(dico_capa,outputPath)

#endregion

# region comparaison energy

# scenarioList=['scenario1','scenario2','scenario3','scenario4']
# scenarioNames=['scenario1','scenario2','scenario3','scenario4']

# dico_ener={}
# for s in scenarioList:
#     outputFolder=outputPath+s+'_PACA'
#     dico_ener[s]=extract_energy(scenarioDict[s],area,outputFolder)

# plot_compare_energy(dico_ener,outputPath)

#endregion

#region Sensibilité distance
scenarioList1=['scenario3_10', 'scenario3_50','scenario3', 'scenario3_250', 'scenario3_500']
costs1={}
for s in scenarioList1:
    outputFolder=outputPath+s+'_PACA'
    costs1[s]=extract_energy(scenarioDict_ISGT[s],area,outputFolder).loc[2030,'costs']

scenarioList2=[ 'scenario4_10', 'scenario4_50','scenario4', 'scenario4_250', 'scenario4_500']
costs2= {}
for s in scenarioList2:
    outputFolder=outputPath+s+'_PACA'
    costs2[s]=extract_energy(scenarioDict_ISGT[s],area,outputFolder).loc[2030,'costs']

outputFolder=outputPath+'scenario2_PACA'
costsS2=[extract_energy(scenarioDict_ISGT['scenario2'],area,outputFolder).loc[2030,'costs']]*5

outputFolder=outputPath+'scenario1_PACA'
costsS1=[extract_energy(scenarioDict_ISGT['scenario1'],area,outputFolder).loc[2030,'costs']]*5


plot_sensibility_costs(costs1,costs2,costsS1,costsS2,outputPath)

# #endregion

# region Sensibilité turpe

scenarioList1=['scenario1_tdemi',  'scenario1','scenario1_tdouble']
costs1={}
for s in scenarioList1:
    outputFolder=outputPath+s+'_PACA'
    costs1[s]=extract_energy(scenarioDict[s],area,outputFolder).loc[2030,'costs']

scenarioList2=['scenario2_tdemi',  'scenario2','scenario2_tdouble']
costs2= {}
for s in scenarioList2:
    outputFolder=outputPath+s+'_PACA'
    costs2[s]=extract_energy(scenarioDict[s],area,outputFolder).loc[2030,'costs']

scenarioList3 = ['scenario3_tdemi', 'scenario3', 'scenario3_tdouble']
costs3 = {}
for s in scenarioList3:
    outputFolder = outputPath + s+'_PACA'
    costs3[s] = extract_energy(scenarioDict[s],area, outputFolder).loc[2030, 'costs']

scenarioList4 = ['scenario4_tdemi', 'scenario4', 'scenario4_tdouble']
costs4 = {}
for s in scenarioList4:
    outputFolder = outputPath + s+'_PACA'
    costs4[s] = extract_energy(scenarioDict[s],area, outputFolder).loc[2030, 'costs']

plot_sensibility_costsT(costs1,costs2,costs3,costs4,outputPath)


# #endregion

# ScenarioList=['scenario1','scenario2','scenario3','scenario4']

# fix={}
# var={}
# tot_elec_kg={}
# tot_H2_kg={}
# tot_kg={}
# pipe={}
# PS={}
# percent={}
# fix_part={}
# var_part={}
# obj={}
# percent_elec={}
# percent_H2={}
# fix_percent = {}
# var_percent = {}
# H2_percent={}
# for s in ScenarioList:
#     outputFolder = outputPath + s+'_PACA'
#     fix[s]=pd.read_csv(outputFolder+'/turpeCostsFixe_Pvar.csv').groupby(['AREA','YEAR_op','RESOURCES']).sum().loc[(area,2030,'electricity'),'turpeCostsFixe_Pvar']
#     var[s] =pd.read_csv(outputFolder+'/turpeCostsVar_Pvar.csv').groupby(['AREA','YEAR_op','RESOURCES']).sum().loc[(area,2030,'electricity'),'turpeCostsVar_Pvar']
#     fix_part[s]=fix[s]/(fix[s]+var[s])*100
#     var_part[s] = var[s] / (fix[s] + var[s])*100
#     PS[s]=pd.read_csv(outputFolder+'/max_PS_Dvar.csv').groupby(['AREA','YEAR_op','HORAIRE']).sum().loc[(area,2030,'HCE'),'max_PS_Dvar']
#     obj[s]=pd.read_csv(outputFolder+'/objective_Pvar.csv').set_index(['YEAR_op']).loc[(2030),'objective_Pvar']
#     pipe[s]=pd.read_csv(outputFolder+'/pipeCosts_Pvar.csv').set_index(['YEAR_op']).loc[(2030),'pipeCosts_Pvar']
#     percent[s]=(fix[s]+var[s]+pipe[s])/obj[s]*100
#     percent_elec[s]=(fix[s]+var[s])/obj[s]*100
#     percent_H2[s]=(pipe[s])/obj[s]*100
#     tot_elec_kg[s] = (fix[s] + var[s]) / (
#                 pd.read_csv(outputFolder + '/power_Dvar.csv').groupby(['AREA','YEAR_op', 'TECHNOLOGIES']).sum().loc[
#                     (area,2030, 'electrolysis_AEL'), 'power_Dvar'] * 30)
#     tot_H2_kg[s] = (pipe[s]) / (
#                 pd.read_csv(outputFolder + '/power_Dvar.csv').groupby(['AREA','YEAR_op', 'TECHNOLOGIES']).sum().loc[
#                     (area,2030, 'electrolysis_AEL'), 'power_Dvar'] * 30)
#     tot_kg[s] = (fix[s] + var[s] + pipe[s]) / (
#                 pd.read_csv(outputFolder + '/power_Dvar.csv').groupby(['AREA','YEAR_op', 'TECHNOLOGIES']).sum().loc[
#                     (area,2030, 'electrolysis_AEL'), 'power_Dvar'] * 30)
#     fix_percent[s] = fix[s]/(fix[s]+var[s]+pipe[s])
#     var_percent[s] = var[s]/(fix[s]+var[s]+pipe[s])
#     H2_percent[s] =  pipe[s]/(fix[s]+var[s]+pipe[s])

# print(fix_percent,var_percent,H2_percent)

#region

# scenarioList=['scenario1_tdemi',  'scenario1','scenario1_tdouble',
# 'scenario2_tdemi',  'scenario2','scenario2_tdouble',
# 'scenario3_tdemi', 'scenario3', 'scenario3_tdouble',
# 'scenario4_tdemi', 'scenario4', 'scenario4_tdouble']
# ener={}
# for s in scenarioList:
#     outputFolder=outputPath+s+'_PACA'
#     ener[s]=extract_energy(scenarioDict[s],area,outputFolder)

# plot_sensitivity_energy(ener,outputPath)


#endregion