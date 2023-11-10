import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

os.sys.path.append(r"../")

# from Functions.f_graphicTools_manuscript import 
from Scenarios.scenarios_LRAnalysis import scenarioDict_LRAnalysis_PACA
from Functions.f_extract_data import extract_energy,extract_capa

outputPath = "../data/output/LRAnalysis/"

LRList=[0.1,0.12,0.14,0.16,0.18,0.2,0.22,0.24,0.26,0.28]
LRName=['10%','12%','14%','16%','18%','20%','22%','24%','26%','28%']

# dico1={}
# dico2={}
# for k,LR in enumerate(LRList):
#     outputFolder=outputPath+'scenario_'+str(LR)+'_PACA'
#     scenarioName='scenario_'+str(LR)+'_PACA'
#     df1=extract_energy(scenarioDict_LRAnalysis_PACA[scenarioName],'Marseille',outputFolder)[["SMR w/o CCUS","SMR + CCUS 50%","SMR + CCUS 90%",'feedBiogas',"Alkaline electrolysis","PEM electrolysis","importsH2",'importBM','curtailment','totalProd','carbon','total_carbon','costs','total_costs']]
#     df1['scenario']=scenarioName
#     df1['order']=k
#     dico1[scenarioName]=df1
#     df2=extract_capa(scenarioDict_LRAnalysis_PACA[scenarioName],'Marseille',outputFolder)[["SMR w/o CCUS","SMR + CCUS 50%","SMR + CCUS 90%","Alkaline electrolysis","PEM electrolysis"]]
#     df2['scenario']=scenarioName
#     df2['order']=k
#     dico2[scenarioName]=df2

# df1=pd.concat([dico1[s] for s in dico1.keys()])
# df1.to_csv(outputPath+'results_LR.csv', index=True)
# df2=pd.concat([dico2[s] for s in dico2.keys()])
# df2.to_csv(outputPath+'results_LR_capa.csv', index=True)


dico_price={}
for k,LR in enumerate(LRList):
    scenarioName='scenario_'+str(LR)+'_PACA'
    df=scenarioDict_LRAnalysis_PACA[scenarioName]['conversionTechs']['electrolysis_AEL'].loc[['investCost','YEAR']].transpose()
    df['scenario']=scenarioName
    df['order']=k
    df.set_index(['order','scenario','YEAR'],inplace=True)
    dico_price[scenarioName]=df/1000 # Prix en €/kW PCI

df_price=pd.concat(dico_price[s] for s in dico_price.keys())

YEAR=df_price.index.get_level_values('YEAR').unique()

df=pd.read_csv(outputPath+'results_LR.csv').set_index(['YEAR_op','order','scenario']).fillna(0)
df_capa=pd.read_csv(outputPath+'results_LR_capa.csv').set_index(['YEAR_op','order','scenario']).fillna(0)

load=(df[["SMR w/o CCUS","SMR + CCUS 50%","SMR + CCUS 90%","Alkaline electrolysis"]]*1000/(df_capa[["SMR w/o CCUS","SMR + CCUS 50%","SMR + CCUS 90%","Alkaline electrolysis"]]*8760)*100).fillna(0)

df_mean1=(df.reset_index().groupby(['order','scenario']).sum()['total_costs']/(df.reset_index().groupby(['order','scenario']).sum()['totalProd']*30)/1000).sort_index(level=0) # €/kg
df_mean2=(df.reset_index().groupby(['order','scenario']).sum()['total_carbon']/(df.reset_index().groupby(['order','scenario']).sum()['totalProd']*30)/1000).sort_index(level=0) # kgCo2/kg
df_capa_elec=df_capa['Alkaline electrolysis']
# df_mean3=(df.reset_index().groupby(['order','scenario']).mean()['importsH2']).sort_index(level=0) # GWh
# df_mean4=(df.reset_index().groupby(['order','scenario']).mean()['importBM']).sort_index(level=0) # GWh


col = plt.cm.tab20c

def kW_to_kWel(x):
    return x*0.65

def kWel_to_kW(x):
    return x/0.65

fig, ax = plt.subplots(3,1,sharex=True,figsize=(6.5,7))
ax2 = ax[0].twinx() 

ax[0].plot(round(df_mean1,2).values,color=col(0),label='LCOH')
ax2.plot(round(df_mean2,2).values,color=col(4),label='Carbon content')
# ax[1].plot(df_mean3.values,color=col(8),label='Imports H2')
# ax[1].plot(df_mean4.values,color=col(12),label='Imports biomethane')

for i,y in enumerate(YEAR):
    ax[1].plot(df_price.loc[slice(None),slice(None),y].values,color=col(4*i),label=y+10)
    ax[2].plot(df_capa_elec.loc[y+10,slice(None),slice(None)].values,color=col(4*i))


ax[0].set_ylim(2.2,2.36)
ax[1].set_xticks(np.arange(len(LRList)),LRName)
ax[0].set_ylabel('LCOH (€/kgH$_2$)')
ax2.set_ylabel('Carbon content of H$_2$ \n (kgCO$_2$/kgH$_2$)')
ax[1].set_ylabel('Electroyser CAPEX (€/kW$_{PCI}$)')
ax[2].set_ylabel('Electroysis capacity (MW)')
ax[2].set_xlabel('Learning Rate (%)')

ax[0].grid(axis='y',alpha=0.5)
ax[1].grid(axis='y',alpha=0.5)
ax[2].grid(axis='y',alpha=0.5)

box = ax[0].get_position()
ax[0].set_position([box.x0, box.y0+0.05, box.width * 0.88, box.height])
box = ax[1].get_position()
ax[1].set_position([box.x0, box.y0+0.025, box.width * 0.88, box.height])
box = ax[2].get_position()
ax[2].set_position([box.x0, box.y0, box.width * 0.88, box.height])

handles, labels = ax[0].get_legend_handles_labels()
handles.append(ax2.get_legend_handles_labels()[0][0])
labels.append(ax2.get_legend_handles_labels()[1][0])
# Put a legend to the right of the current axis
ax[0].legend(handles,labels,loc='upper right')
legend1=ax[1].legend(loc="center left",bbox_to_anchor=(1.01, -0.2))

secax = ax[1].secondary_yaxis("right", functions=(kW_to_kWel,kWel_to_kW))
secax.set_ylabel("(€/kW$_{el}$)")
# plt.tight_layout()

plt.savefig(outputPath+'LRAnalysis_line.png',dpi=300)
plt.show()




fig, ax = plt.subplots(3,1,sharex=True,figsize=(6.5,7))

for i,y in enumerate([2020,2030,2040,2050]):
    ax[0].plot(load.loc[(y,slice(None),slice(None)),'SMR w/o CCUS'].values,color=col(4*i),label=y)
    ax[1].plot(load.loc[(y,slice(None),slice(None)),'SMR + CCUS 50%'].values,color=col(4*i),label=y)
    # plt.plot(load.loc[(y,slice(None),slice(None)),'SMR + CCUS 90%'].values,color=col(4*i),label='SMR + CCUS 90% ' + str(y))
    ax[2].plot(load.loc[(y,slice(None),slice(None)),'Alkaline electrolysis'].values,color=col(4*i),label=y)


box = ax[0].get_position()
ax[0].set_position([box.x0, box.y0+0.05, box.width * 0.9, box.height])
box = ax[1].get_position()
ax[1].set_position([box.x0, box.y0+0.025, box.width * 0.9, box.height])
box = ax[2].get_position()
ax[2].set_position([box.x0, box.y0, box.width * 0.9, box.height])

ax[0].grid(axis='y',alpha=0.5)
ax[1].grid(axis='y',alpha=0.5)
ax[2].grid(axis='y',alpha=0.5)

fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
yticks = mtick.FormatStrFormatter(fmt)
ax[0].yaxis.set_major_formatter(yticks)
ax[1].yaxis.set_major_formatter(yticks)
ax[2].yaxis.set_major_formatter(yticks)
ax[2].set_xticks(np.arange(len(LRList)),LRName)

ax[0].set_ylabel('Load factor (%)')
ax[1].set_ylabel('Load factor (%)')
ax[2].set_ylabel('Load factor (%)')
ax[2].set_xlabel('LR (%)')
ax[0].set_title('SMR w/o CCUS')
ax[1].set_title('SMR + CCUS 50%')
ax[2].set_title('Alkaline electroolysis')


ax[1].legend(loc="center left",bbox_to_anchor=(1, 0.5))
plt.savefig(outputPath+'LRAnalysis_load.png',dpi=300)
plt.show()

# #---------------------------------------------------------------------------------------------------------------------------------#

x=np.arange(1,len(LRList)+1)
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

ax.set_xticks(x,LRName)
box = ax.get_position()
ax.set_position([box.x0, box.y0+0.05, box.width * 0.7, box.height])
# get handles and labels
handles, labels = ax.get_legend_handles_labels()
# specify order of items in legend
order = [4,3, 2, 1, 0, 5]
# Put a legend to the right of the current axis
ax.legend(
    [handles[idx] for idx in order],
    [labels[idx] for idx in order],
    loc="center left",
    bbox_to_anchor=(1, 0.5),
)
plt.ylabel("Share of the hydrogen demand (%)")
plt.xlabel("Learning rate (%) ")

plt.savefig(outputPath+'LRAnalysis_energy.png',dpi=300)
plt.show()