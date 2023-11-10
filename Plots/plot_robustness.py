import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

os.sys.path.append(r"../")

# from Functions.f_graphicTools_manuscript import 
# from Scenarios.scenario_creation_robustness import scenarioDict_robustness
from Scenarios.scenario_creation import scenarioDict
from Functions.f_extract_data import extract_energy

outputPath = "../data/output/robustness/"

# scenarioList=['ref','gas_x5','BM_60','CO2_100','import_H2','Re_inf','woSMR_2040','expensiveRE'] 
# aleaList=['ref','gas_x5','BM_60','CO2_100','import_H2','cheap_H2','woSMR_2040','expensiveRE']

# dico={}
# for scenarioAlea in aleaList:
#     for scenarioCapa in scenarioList:
#         if scenarioCapa == scenarioAlea:
#             scenarioName=scenarioCapa
#         else:
#             scenarioName=scenarioCapa+'_'+scenarioAlea

#         outputFolder=outputPath+scenarioName+'_PACA'
#         df1=extract_energy(scenarioDict_robustness[scenarioName],'Marseille',outputFolder)[["SMR w/o CCUS","SMR + CCUS 50%","SMR + CCUS 90%","Alkaline electrolysis","PEM electrolysis","importsH2",'curtailment','totalProd','carbon','total_carbon','costs','total_costs']]
#         df1['scenario']=scenarioName
#         dico[scenarioName]=df1
#         if scenarioCapa not in aleaList:
#             scenarioName=scenarioCapa
#             outputFolder=outputPath+scenarioName+'_PACA'
#             df1=extract_energy(scenarioDict_robustness[scenarioName],'Marseille',outputFolder)[["SMR w/o CCUS","SMR + CCUS 50%","SMR + CCUS 90%","Alkaline electrolysis","PEM electrolysis","importsH2",'curtailment','totalProd','carbon','total_carbon','costs','total_costs']]
#             df1['scenario']=scenarioName
#             dico[scenarioName]=df1

# df=pd.concat([dico[s] for s in dico.keys()])
# df.to_csv(outputPath+'results_rob.csv', index=True)


# scenarioList=['Cavern','BM_60Cavern','expensiveRECavern','gas_x5Cavern','CO2_100Cavern','import_H2Cavern','Re_infCavern','woSMR_2040Cavern'] 
# aleaList=['Cavern','BM_60Cavern','expensiveRECavern','gas_x5Cavern','CO2_100Cavern','import_H2Cavern','cheap_H2Cavern','woSMR_2040Cavern',]


# dico={}
# for scenarioAlea in aleaList:
#     for scenarioCapa in scenarioList:
#         if scenarioCapa == scenarioAlea:
#             scenarioName=scenarioCapa
#         else:
#             scenarioName=scenarioCapa+'_'+scenarioAlea

#         outputFolder=outputPath+scenarioName+'_PACA'
#         df1=extract_energy(scenarioDict_robustness[scenarioName],'Marseille',outputFolder)[["SMR w/o CCUS","SMR + CCUS 50%","SMR + CCUS 90%","Alkaline electrolysis","PEM electrolysis","importsH2",'curtailment','totalProd','carbon','total_carbon','costs','total_costs']]
#         df1['scenario']=scenarioName
#         dico[scenarioName]=df1
#         if scenarioCapa not in aleaList:
#             scenarioName=scenarioCapa
#             outputFolder=outputPath+scenarioName+'_PACA'
#             df1=extract_energy(scenarioDict_robustness[scenarioName],'Marseille',outputFolder)[["SMR w/o CCUS","SMR + CCUS 50%","SMR + CCUS 90%","Alkaline electrolysis","PEM electrolysis","importsH2",'curtailment','totalProd','carbon','total_carbon','costs','total_costs']]
#             df1['scenario']=scenarioName
#             dico[scenarioName]=df1


# df=pd.concat([dico[s] for s in dico.keys()])
# df.to_csv(outputPath+'results_cavern.csv', index=True)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


dic_name={'ref':'Reference','gas_x5':'Expensive natural gas', 'BM_60':'Cheap biomethane', 'CO2_100':'Expensive carbon treatment', 'import_H2':'Hydrogen imports', 'cheap_H2':'Cheap hydrogen imports', 
 'Re_inf':'Unlimited renewable potential', 'woSMR_2040':'Ban on SMR from 2040','expensiveRE':'Expensive renewables'}

df=pd.read_csv(outputPath+'results_rob.csv').set_index('scenario').fillna(0)
df['scenarioCapa']="None"
df['scenarioAlea']="None"

scenarioList=['ref','BM_60','expensiveRE','CO2_100','Re_inf','import_H2','gas_x5','woSMR_2040'] 
aleaList=['ref','BM_60','expensiveRE','CO2_100','cheap_H2','import_H2','gas_x5','woSMR_2040']

c=0
for scenarioAlea in aleaList:
    for scenarioCapa in scenarioList:
        # print(scenarioCapa,scenarioAlea)
        if scenarioAlea == scenarioCapa:
            scenario=scenarioAlea
            df.loc[scenario,'scenarioCapa']=scenario
            df.loc[scenario,'scenarioAlea']=scenario
        else:
           scenario=scenarioCapa+'_'+scenarioAlea
           # print(scenario)
           df.loc[scenario,'scenarioCapa']=scenarioCapa
           df.loc[scenario,'scenarioAlea']=scenarioAlea

dico_opt={}
for s in df.loc[df['scenarioCapa']=='None'].index.unique():
	dico_opt[s]=(df.loc[s].reset_index().groupby('scenario').sum()['total_costs']/(df.loc[s].reset_index().groupby('scenario').sum()['totalProd']*30)/1000)[0]

df.drop(df.loc[df['scenarioCapa']=='None'].index,inplace=True)
df=df.set_index('YEAR_op',append=True)

df_mean1=df.reset_index().groupby(['scenarioCapa','scenarioAlea']).sum()['total_costs']/(df.reset_index().groupby(['scenarioCapa','scenarioAlea']).sum()['totalProd']*30)/1000
diff={}
for scenarioCapa in scenarioList:
	if scenarioCapa not in dico_opt.keys():
		dico_opt[scenarioCapa]=df_mean1.loc[(scenarioCapa,scenarioCapa)]
	diff[scenarioCapa]=df_mean1.loc[(scenarioCapa,slice(None))]-dico_opt[scenarioCapa]

df_costs_diff=pd.concat(diff[s] for s in diff.keys())

df_mean2=df.reset_index().groupby(['scenarioCapa','scenarioAlea']).sum()['total_carbon']/(df.reset_index().groupby(['scenarioCapa','scenarioAlea']).sum()['totalProd']*30)/1000
df_mean3=df.reset_index().groupby(['scenarioCapa','scenarioAlea']).mean()['importsH2']/1000



df_costs_mean=df_mean1.reset_index().pivot(index='scenarioCapa',columns='scenarioAlea',values=0).reindex(scenarioList).reindex(aleaList, axis=1)
df_costs_diff=df_costs_diff.reset_index().pivot(index='scenarioCapa',columns='scenarioAlea',values=0).reindex(scenarioList).reindex(aleaList, axis=1)
df_carbon_mean=df_mean2.reset_index().pivot(index='scenarioCapa',columns='scenarioAlea',values=0).reindex(scenarioList).reindex(aleaList, axis=1)
df_imports_mean=df_mean3.reset_index().pivot(index='scenarioCapa',columns='scenarioAlea',values='importsH2').reindex(scenarioList).reindex(aleaList, axis=1)

fig, ax = plt.subplots(figsize=(7,7))
im = ax.imshow(df_costs_mean,vmin=1.9, vmax=3.4)

# Show all ticks and label them with the respective list entries
plt.xticks(np.arange(len(aleaList)), labels=[dic_name[s] for s in list(df_costs_mean.columns)])
plt.yticks(np.arange(len(scenarioList)), labels=[dic_name[s] for s in list(df_costs_mean.index)])

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(scenarioList)):
    for j in range(len(aleaList)):
        text = ax.text(j, i, round(df_costs_mean.iloc[i,j],2),
                       ha="center", va="center", color="w")


# Add colorbar for legend
cbar = ax.figure.colorbar(im, ax=ax, shrink=0.64)
cbar.ax.set_ylabel('Average LCOH (€/kg)', rotation=-90, va="bottom")

plt.ylabel('Anticipated scenarios')
plt.xlabel('Actual scenarios')

plt.tight_layout()
plt.savefig(outputPath+'robustness_costs.png',dpi=300)

plt.show(block=True)

c = ["darkgreen","green", "palegreen","white","lightcoral","red","darkred"]
v = [0,.15,.4,.5,0.6,.9,1.]
l = list(zip(v,c))

cmap=LinearSegmentedColormap.from_list('rg',l, N=256)


fig, ax = plt.subplots(figsize=(7,7))
im = ax.imshow(df_costs_diff,cmap=cmap,vmin=-1.2, vmax=1.2)

# Show all ticks and label them with the respective list entries
plt.xticks(np.arange(len(aleaList)), labels=[dic_name[s] for s in list(df_costs_diff.columns)])
plt.yticks(np.arange(len(scenarioList)), labels=[dic_name[s] for s in list(df_costs_diff.index)])

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(scenarioList)):
    for j in range(len(aleaList)):
        text = ax.text(j, i, round(df_costs_diff.iloc[i,j],2),
                       ha="center", va="center")


# Add colorbar for legend
cbar = ax.figure.colorbar(im, ax=ax, shrink=0.64)
cbar.ax.set_ylabel('Average LCOH (€/kg)', rotation=-90, va="bottom")

plt.ylabel('Anticipated scenarios')
plt.xlabel('Actual scenarios')

plt.tight_layout()
plt.savefig(outputPath+'robustness_costsDifference.png',dpi=300)

plt.show(block=True)


# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# def kg_to_MWh(x):
#     y=x*30
#     return y

# def MWh_to_kg(x):
#     y=x/30
#     return y

# def t_to_TWh(x):
#     y=x*33.33/1e3
#     return y

# def TWh_to_t(x):
#     y=x/33.33*1e3
#     return y

# fig,ax=plt.subplots(3,1,figsize=(10,10),sharex=True)

# width=0.4
# col=plt.cm.tab20c
# x=np.arange(0,2*len(scenarioList),2)
# X=[x-1.5*width,x-0.5*width,x+0.5*width,x+1.5*width]
# YEAR=df.index.get_level_values('YEAR_op').unique()
# dic_costs={y: df.loc[(slice(None),y),['costs','scenarioAlea','scenarioCapa']].pivot(index='scenarioCapa',columns='scenarioAlea',values='costs') for y in YEAR}
# dic_carbon={y:df.loc[(slice(None),y),['carbon','scenarioAlea','scenarioCapa']].pivot(index='scenarioCapa',columns='scenarioAlea',values='carbon') for y in YEAR}
# dic_imports={y:df.loc[(slice(None),y),['importsH2','scenarioAlea','scenarioCapa']].pivot(index='scenarioCapa',columns='scenarioAlea',values='importsH2')/1000 for y in YEAR}
# H2demand={y:df.loc[(slice(None),y),'totalProd'].mean()/1000 for y in YEAR}

# for c,y in enumerate(YEAR[1:]):
# 	min_cost={}
# 	diff_cost={}
# 	avg_min_cost={}
# 	avg_diff_cost={}

# 	min_carbon={}
# 	diff_carbon={}
# 	avg_min_carbon={}
# 	avg_diff_carbon={}

# 	min_imports={}
# 	diff_imports={}
# 	avg_min_imports={}
# 	avg_diff_imports={}


# 	for k,scenario in enumerate(scenarioList) :
# 	    min_cost[scenario]=dic_costs[y].loc[scenario].min()
# 	    diff_cost[scenario]=dic_costs[y].loc[scenario].max()-dic_costs[y].loc[scenario].min()
# 	    ax[0].bar(X[c][k],diff_cost[scenario],width=width,bottom=min_cost[scenario],color=col(4*(c+1)),zorder=2)
# 	    ref_cost=pd.read_csv(outputPath+'results_rob.csv').set_index(['scenario','YEAR_op']).fillna(0).loc[(scenario,y),'costs']
# 	    ax[0].plot(X[c][k],ref_cost,marker='D',color='none',markerfacecolor='none',markeredgecolor='black',markeredgewidth=1,markersize=5,zorder=3)
	    
# 	    min_carbon[scenario]=dic_carbon[y].loc[scenario].min()
# 	    diff_carbon[scenario]=dic_carbon[y].loc[scenario].max()-dic_carbon[y].loc[scenario].min()	    
# 	    ax[1].bar(X[c][k],diff_carbon[scenario],width=width,bottom=min_carbon[scenario],color=col(4*(c+1)),zorder=2,label=str(y)+'-'+str(y+10) if k==0 else '')
# 	    ref_carbon=pd.read_csv(outputPath+'results_rob.csv').set_index(['scenario','YEAR_op']).fillna(0).loc[(scenario,y),'carbon']
# 	    ax[1].plot(X[c][k],ref_carbon,marker='D',color='none',markerfacecolor='none',markeredgecolor='black',markeredgewidth=1,markersize=5,zorder=3)
# 	    ax[1].bar(X[c][k],0,bottom=-2,width=width,color='none',edgecolor=col(16),label='Hydrogen demand' if k+c==0 else '' ,zorder=2)
	   
# 	    min_imports[scenario]=dic_imports[y].loc[scenario].min()
# 	    diff_imports[scenario]=dic_imports[y].loc[scenario].max()-dic_imports[y].loc[scenario].min()	    
# 	    ax[2].bar(X[c][k],diff_imports[scenario],width=width,bottom=min_imports[scenario],color=col(4*(c+1)),zorder=2)
# 	    ref_imports=pd.read_csv(outputPath+'results_rob.csv').set_index(['scenario','YEAR_op']).fillna(0).loc[(scenario,y),'importsH2']/1000
# 	    ax[2].plot(X[c][k],ref_imports,marker='D',color='none',markerfacecolor='none',markeredgecolor='black',markeredgewidth=1,markersize=5,zorder=3)   
# 	    ax[2].bar(X[c][k],H2demand[y],width=width,color='none',edgecolor=col(4*(c+1)),zorder=2)

# 	    if c==2:
# 	    	avg_min_cost[scenario]=df_costs_mean.loc[scenario].min()
# 	    	avg_diff_cost[scenario]=df_costs_mean.loc[scenario].max()-df_costs_mean.loc[scenario].min()
# 	    	ax[0].bar(X[3][k],avg_diff_cost[scenario],width=width,bottom=avg_min_cost[scenario],color=col(18),zorder=2)
# 	    	df_ref=pd.read_csv(outputPath+'results_rob.csv').set_index(['scenario','YEAR_op'])['total_costs'][scenario].sum()/(pd.read_csv(outputPath+'results_rob.csv').set_index(['scenario','YEAR_op'])['totalProd'][scenario].sum()*30)/1000
# 	    	ax[0].plot(X[3][k],df_ref,marker='D',color='none',markerfacecolor='none',markeredgecolor='black',markeredgewidth=1,markersize=5,zorder=3)
	    	
# 	    	avg_min_carbon[scenario]=df_carbon_mean.loc[scenario].min()
# 	    	avg_diff_carbon[scenario]=df_carbon_mean.loc[scenario].max()-df_carbon_mean.loc[scenario].min()
# 	    	ax[1].bar(X[3][k],avg_diff_carbon[scenario],width=width,bottom=avg_min_carbon[scenario],color=col(18),zorder=2,label='Avergage for 2020-2060' if k==0 else '')
# 	    	df_carbonRef=pd.read_csv(outputPath+'results_rob.csv').set_index(['scenario','YEAR_op'])['total_carbon'][scenario].sum()/(pd.read_csv(outputPath+'results_rob.csv').set_index(['scenario','YEAR_op'])['totalProd'][scenario].sum()*30)/1000
# 	    	ax[1].plot(X[3][k], df_carbonRef,marker='D',color='none',markerfacecolor='none',markeredgecolor='black',markeredgewidth=1,markersize=5,zorder=3,label='Perfect anticipation' if k==0 else '')

# 	    	avg_min_imports[scenario]=df_imports_mean.loc[scenario].min()
# 	    	avg_diff_imports[scenario]=df_imports_mean.loc[scenario].max()-df_imports_mean.loc[scenario].min()
# 	    	ax[2].bar(X[3][k],avg_diff_imports[scenario],width=width,bottom=avg_min_imports[scenario],color=col(18),zorder=2)
# 	    	ax[2].bar(X[3][k],np.mean(list(H2demand.values())),width=width,color='none',edgecolor=col(18),zorder=2)
# 	    	df_importsRef=pd.read_csv(outputPath+'results_rob.csv').set_index(['scenario','YEAR_op'])['importsH2'][scenario].mean()/1000
# 	    	ax[2].plot(X[3][k], df_importsRef,marker='D',color='none',markerfacecolor='none',markeredgecolor='black',markeredgewidth=1,markersize=5,zorder=3)



# cost2020=dic_costs[2020]['ref']['ref']
# carbon2020=dic_carbon[2020]['ref']['ref']
# import2020=dic_imports[2020]['ref']['ref']
# ax[0].axhline(cost2020,linestyle='--', color=col(0))
# ax[1].axhline(carbon2020,linestyle='--', color=col(0), label="2020-2030")
# ax[2].axhline(import2020,linestyle='--', color=col(0))


# ax[0].grid(axis='y',alpha=0.5,zorder=1)
# ax[1].grid(axis='y',alpha=0.5,zorder=1)
# ax[2].grid(axis='y',alpha=0.5,zorder=1)

# ax[0].set_ylim([1,5])
# ax[1].set_ylim([-1,10])
# ax[2].set_ylim([-1,7])
# plt.xticks(np.arange(0,2*len(scenarioList),2), labels=[dic_name[s] for s in scenarioList])
# plt.setp(ax[2].get_xticklabels(), rotation=30, ha="right",rotation_mode="anchor")
# plt.xlabel('Anticipated scenarios')
# ax[0].set_title('Levelized cost of hydrogen')
# ax[0].set_ylabel('(€/kg)')
# ax[1].set_title('Carbon emissions')
# ax[1].set_ylabel('(kgCO$_2$/kgH$_2$)')
# ax[2].set_title('H$_2$ importations')
# ax[2].set_ylabel('(TWh/year)')

# # Shrink axis by 20%
# box = ax[0].get_position()
# ax[0].set_position([box.x0, box.y0+0.08, box.width * 0.8, box.height])
# box = ax[1].get_position()
# ax[1].set_position([box.x0, box.y0+0.08, box.width * 0.8, box.height])
# box = ax[2].get_position()
# ax[2].set_position([box.x0, box.y0+0.08, box.width * 0.8, box.height])

# # get handles and labels
# handles, labels = ax[1].get_legend_handles_labels()
# # specify order of items in legend
# order = [0,1,2,4,5,6,3]
# # Put a legend to the right of the current axis
# ax[1].legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc="center left",bbox_to_anchor=(1.03, 0.5))

# secax0 = ax[0].secondary_yaxis("right", functions=(kg_to_MWh,MWh_to_kg))
# secax0.set_ylabel("(€/MWh)")

# secax2 = ax[2].secondary_yaxis("right", functions=(TWh_to_t,t_to_TWh))
# secax2.set_ylabel("(kt/year)")

# plt.savefig(outputPath+'/barChart_robustness_years.png',dpi=300)

# plt.show()
# plt.close()



# #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

dic_name={'Cavern':'With geological storage','gas_x5Cavern':'Expensive natural gas', 'BM_60Cavern':'Cheap biomethane', 'CO2_100Cavern':'Expensive carbon treatment', 'import_H2Cavern':'Hydrogen imports', 'cheap_H2Cavern':'Cheap hydrogen imports', 
 'Re_infCavern':'Unlimited renewable potential', 'woSMR_2040Cavern':'Ban on SMR from 2040','expensiveRECavern':'Expensive renewables','Cavern2040' : 'Geological storage from 2040'}


df=pd.read_csv(outputPath+'results_cavern.csv').set_index('scenario').fillna(0)
df['scenarioCapa']="None"
df['scenarioAlea']="None"

scenarioList=['Cavern','BM_60Cavern','expensiveRECavern','CO2_100Cavern','Re_infCavern','import_H2Cavern','gas_x5Cavern','woSMR_2040Cavern'] 
aleaList=['Cavern','BM_60Cavern','expensiveRECavern','CO2_100Cavern','cheap_H2Cavern','import_H2Cavern','gas_x5Cavern','woSMR_2040Cavern',]

c=0
for scenarioAlea in aleaList:
    for scenarioCapa in scenarioList:
        if scenarioAlea == scenarioCapa:
            scenario=scenarioAlea
            df.loc[scenario,'scenarioCapa']=scenario
            df.loc[scenario,'scenarioAlea']=scenario
        else:
           scenario=scenarioCapa+'_'+scenarioAlea
           # print(scenario)
           df.loc[scenario,'scenarioCapa']=scenarioCapa
           df.loc[scenario,'scenarioAlea']=scenarioAlea

df.drop(df.loc[df['scenarioCapa']=='None'].index,inplace=True)
df=df.set_index('YEAR_op',append=True)

df_mean1=df.reset_index().groupby(['scenarioCapa','scenarioAlea']).sum()['total_costs']/(df.reset_index().groupby(['scenarioCapa','scenarioAlea']).sum()['totalProd']*30)/1000
# df_mean2=df.reset_index().groupby(['scenarioCapa','scenarioAlea']).sum()['total_carbon']/(df.reset_index().groupby(['scenarioCapa','scenarioAlea']).sum()['totalProd']*30)/1000
# df_mean3=df.reset_index().groupby(['scenarioCapa','scenarioAlea']).mean()['importsH2']/1000

df_costs_mean=df_mean1.reset_index().pivot(index='scenarioCapa',columns='scenarioAlea',values=0).reindex(scenarioList).reindex(aleaList, axis=1)

# df_carbon_mean=df_mean2.reset_index().pivot(index='scenarioCapa',columns='scenarioAlea',values=0)
# df_imports_mean=df_mean3.reset_index().pivot(index='scenarioCapa',columns='scenarioAlea',values='importsH2')


fig, ax = plt.subplots(figsize=(7,7))
im = ax.imshow(df_costs_mean,vmin=1.9, vmax=3.4)

# Show all ticks and label them with the respective list entries
plt.xticks(np.arange(len(aleaList)), labels=[dic_name[s] for s in list(df_costs_mean.columns)])
plt.yticks(np.arange(len(scenarioList)), labels=[dic_name[s] for s in list(df_costs_mean.index)])

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(scenarioList)):
    for j in range(len(aleaList)):
        text = ax.text(j, i, round(df_costs_mean.iloc[i,j],2),
                       ha="center", va="center", color="w")


# Add colorbar for legend
cbar = ax.figure.colorbar(im, ax=ax, shrink=0.64)
cbar.ax.set_ylabel('Average LCOH (€/kg)', rotation=-90, va="bottom")

plt.ylabel('Anticipated scenarios')
plt.xlabel('Actual scenarios')

plt.tight_layout()
plt.savefig(outputPath+'robustness_costs_cavern.png',dpi=300)

plt.show(block=True)