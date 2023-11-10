import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

os.sys.path.append(r"../")

from Scenarios.scenarios_gasAnalysis import scenarioDict_gasAnalysis_PACA
# from Scenarios.scenario_creation import scenarioDict
from Functions.f_extract_data import extract_energy

outputPath = "../data/output/gasAnalysis/"

priceList=[15,20,30,40,50,60,70,80,90,100]

dico={}
for k,p in enumerate(priceList):
    outputFolder=outputPath+'scenario_'+str(p)+'_PACA'
    scenarioName='scenario_'+str(p)+'_PACA'
    df1=extract_energy(scenarioDict_gasAnalysis_PACA[scenarioName],'Marseille',outputFolder)[["SMR w/o CCUS","SMR + CCUS 50%","SMR + CCUS 90%",'feedBiogas',"Alkaline electrolysis","PEM electrolysis","importsH2",'importBM','curtailment','totalProd','carbon','total_carbon','costs','total_costs']]
    df1['scenario']=scenarioName
    df1['order']=k
    dico[scenarioName]=df1

df=pd.concat([dico[s] for s in dico.keys()])
df.to_csv(outputPath+'results_gas.csv', index=True)


df=pd.read_csv(outputPath+'results_gas.csv').set_index(['order','scenario']).fillna(0)

df_mean1=(df.reset_index().groupby(['order','scenario']).sum()['total_costs']/(df.reset_index().groupby(['order','scenario']).sum()['totalProd']*30)/1000).sort_index(level=0) # €/kg
df_mean2=(df.reset_index().groupby(['order','scenario']).sum()['total_carbon']/(df.reset_index().groupby(['order','scenario']).sum()['totalProd']*30)/1000).sort_index(level=0) # kgCo2/kg
df_mean3=(df.reset_index().groupby(['order','scenario']).mean()['importsH2']/1000).sort_index(level=0) # TWh
df_mean4=(df.reset_index().groupby(['order','scenario']).mean()['importBM']/1000).sort_index(level=0) # TWh


col = plt.cm.tab20c

fig, ax = plt.subplots(2,1,sharex=True, figsize=(6.5,4))
ax2 = ax[0].twinx() 

ax[0].plot(df_mean1.values,color=col(0),label='LCOH')
ax2.plot(df_mean2.values,color=col(4),label='Carbon content')
ax[1].plot(df_mean3.values,color=col(8),label='Imports H2')
ax[1].plot(df_mean4.values,color=col(12),label='Imports biomethane')

ax[1].set_xticks(np.arange(len(priceList)),priceList)
ax[0].set_ylabel('LCOH (€/kgH$_2$)')
ax2.set_ylabel('Carbon content of H$_2$ \n (kgCO$_2$/kgH$_2$)')
ax[1].set_ylabel('Imported energy (TWh)')
ax[1].set_xlabel("Natural gas average price (€/MWh)")

ax[0].grid(axis='y',alpha=0.5)
ax[1].grid(axis='y',alpha=0.5)


handles, labels = ax[0].get_legend_handles_labels()
handles.append(ax2.get_legend_handles_labels()[0][0])
labels.append(ax2.get_legend_handles_labels()[1][0])
# Put a legend to the right of the current axis
ax[0].legend(handles,labels,loc='center right')
ax[1].legend()
plt.tight_layout()

plt.savefig(outputPath+'gasAnalysis_line.png',dpi=300)
plt.show(block=False)


#---------------------------------------------------------------------------------------------------------------------------------#

x=np.arange(1,len(priceList)+1)
df_sum=df.reset_index().groupby(['order','scenario']).sum()[['SMR w/o CCUS','SMR + CCUS 50%', 'SMR + CCUS 90%','Alkaline electrolysis','importsH2']].sort_index(level=0).rename(columns={'importsH2':'H2 importations'})
total=df_sum.sum(axis=1)
biogas=list(round(df.reset_index().groupby(['order','scenario']).sum()['feedBiogas']/total*100,2))

dic_col={'SMR w/o CCUS':col(16),'SMR + CCUS 50%':col(0),'SMR + CCUS 90%':col(1),'Alkaline electrolysis':col(8),'H2 importations':col(4)}

fig,ax=plt.subplots(figsize=(6.5,3))

l=[]
for k,tech in enumerate(df_sum.columns):
	if k==0:
		l.append(list(round(df_sum[tech]/total*100,2)))
		ax.bar(x,l[0],color=dic_col[tech],label=tech)
	else:
		new_l=list(round(df_sum[tech]/total*100,2))
		l.append([i+j for i,j in zip(l[k-1],new_l)])
		ax.bar(x,new_l,color=dic_col[tech],bottom=l[k-1],label=tech)

plt.rcParams["hatch.linewidth"] = 8
plt.rcParams["hatch.color"] = col(3)
ax.bar(x,biogas,color="none",hatch="/",linewidth=0.5,edgecolor=col(3),alpha=0.8,label="Biomethane feed")

ax.set_xticks(x,priceList)
box = ax.get_position()
ax.set_position([box.x0, box.y0+0.05, box.width * 0.7, box.height])
# get handles and labels
handles, labels = ax.get_legend_handles_labels()
# specify order of items in legend
order = [5,4, 3, 2, 1, 0]
# Put a legend to the right of the current axi
ax.legend(
    [handles[idx] for idx in order],
    [labels[idx] for idx in order],
    loc="center left",
    bbox_to_anchor=(1, 0.5),
)
plt.ylabel("Sahre of the hydrogen demand (%)")
plt.xlabel("Natural gas average price (€/MWh)")

plt.savefig(outputPath+'gasAnalysis_energy.png',dpi=300)
plt.show()