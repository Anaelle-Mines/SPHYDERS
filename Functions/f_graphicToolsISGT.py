import os

os.sys.path.append(r"../")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

from Functions.loadScenario import loadScenario
from Scenarios.scenario_ref_Fr import scenarioFr

def plot_capacity(outputFolder='data/output/'):
    v_list = ['capacityInvest_Dvar', 'transInvest_Dvar', 'capacity_Pvar', 'capacityDel_Pvar', 'capacityDem_Dvar',
              'energy_Pvar', 'power_Dvar', 'storageConsumption_Pvar', 'storageIn_Pvar', 'storageOut_Pvar',
              'stockLevel_Pvar', 'importation_Dvar', 'Cmax_Pvar', 'carbon_Pvar', 'powerCosts_Pvar', 'capacityCosts_Pvar',
              'importCosts_Pvar', 'storageCosts_Pvar', 'turpeCosts_Pvar', 'Pmax_Pvar', 'max_PS_Dvar', 'carbonCosts_Pvar']
    Variables = {v: pd.read_csv(outputFolder + '/' + v + '.csv').drop(columns='Unnamed: 0') for v in v_list}

    YEAR=Variables['power_Dvar'].set_index('YEAR_op').index.unique().values
    TECHNO = Variables['power_Dvar'].set_index('TECHNOLOGIES').index.unique().values
    TIMESTAMP=Variables['power_Dvar'].set_index('TIMESTAMP').index.unique().values
    YEAR.sort()

    #region Tracé mix prod H2 et EnR
    df=Variables['capacity_Pvar']
    df=df.pivot(columns='TECHNOLOGIES',values='capacity_Pvar', index='YEAR_op').rename(columns={
        "electrolysis_AEL": "Alkaline electrolysis",
        "electrolysis_PEMEL": "PEM electrolysis",
        'SMR': "SMR w/o CCUS",
        'SMR + CCS1':  'SMR + CCUS 50%',
        'SMR + CCS2':  'SMR + CCUS 90%',
        'SMR_elec': 'eSMR w/o CCUS',
        'SMR_elecCCS1': 'eSMR + CCUS 50%',
        'cracking': 'Methane cracking'
    }).fillna(0)

    capa=Variables['capacity_Pvar'].set_index(['YEAR_op','TECHNOLOGIES'])

    #LoadFactors
    EnR_loadFactor={y : (Variables['power_Dvar'].groupby(['YEAR_op','TECHNOLOGIES']).sum().drop(columns='TIMESTAMP')['power_Dvar']/(Variables['capacity_Pvar'].set_index(['YEAR_op','TECHNOLOGIES'])['capacity_Pvar']*8760)).reset_index().pivot(index='YEAR_op',columns='TECHNOLOGIES',values=0).loc[y,['WindOnShore','Solar','WindOffShore_flot','WindOnShorePPA','SolarPPA','WindOffShorePPA']].fillna(0)  for y in YEAR}
    H2_loadFactor={y : (Variables['power_Dvar'].groupby(['YEAR_op','TECHNOLOGIES']).sum().drop(columns='TIMESTAMP')['power_Dvar']/(Variables['capacity_Pvar'].set_index(['YEAR_op','TECHNOLOGIES'])['capacity_Pvar']*8760)).reset_index().pivot(index='YEAR_op',columns='TECHNOLOGIES',values=0).loc[y,['electrolysis_PEMEL','electrolysis_AEL','SMR','SMR + CCS1','SMR + CCS2','SMR_elec','SMR_elecCCS1']].fillna(0) for y in YEAR}
    for y in YEAR : H2_loadFactor[y].loc[H2_loadFactor[y]<-0.0001]=0
    for y in YEAR : H2_loadFactor[y].loc[H2_loadFactor[y]>1.0001]=0
    for y in YEAR : EnR_loadFactor[y].loc[EnR_loadFactor[y]<-0.0001]=0
    for y in YEAR : EnR_loadFactor[y].loc[EnR_loadFactor[y]>1.0001]=0

    fig, ax = plt.subplots(2,1,sharex=True,figsize=(6.2,4))
    width= 0.40
    labels=list(df.index)
    x = np.arange(len(labels))
    col = plt.cm.tab20c

    # Create dark grey Bar
    l1=list(df['SMR w/o CCUS'])
    ax[0].bar(x, l1,width, color=col(17), label="SMR w/o CCUS",zorder=2)
    # Create dark bleu Bar
     # Create green Bars
    l7=list(df['Alkaline electrolysis']+df['PEM electrolysis'])
    ax[0].bar(x,l7,width, color=col(9),label="Water electrolysis",zorder=2)

    # Create red bar
    l8=list(df['Solar'])
    ax[1].bar(x ,l8,width, color=col(5),label="Solar local",zorder=2)
    l9=list(df['SolarPPA'])
    ax[1].bar(x ,l9,width,bottom=l8, color=col(6),label="Solar delocalised",zorder=2)
    # Create violet bar
    l10=list(df['WindOnShore'])
    ax[1].bar(x,l10,width,  bottom=[i+j for i,j in zip(l8,l9)],color=col(13),label="Wind local",zorder=2)
    # Create pink bar
    l11=list(df['WindOnShorePPA'])
    ax[1].bar(x,l11,width,  bottom=[i+j+k for i,j,k in zip(l8,l9,l10)],color=col(14),label="Wind delocalised",zorder=2)
    #
    # # Create grey line
    # ax[2].plot(x,list((round(H2_loadFactor[y]['SMR']*100)for y in YEAR)),color=col(17),label='SMR w/o CCUS',zorder=2)
    # # Create dark blue line
    # ax[2].plot(x, list((round(H2_loadFactor[y]['SMR + CCS1'] * 100) for y in YEAR)), color=col(0), label='SMR + CCUS 50%',zorder=2)
    # # Create light blue line
    # ax[2].plot(x, list((round(H2_loadFactor[y]['electrolysis_AEL'] * 100)) for y in YEAR), color=col(9), label='Water electrolysis',zorder=2)
    # Create green line
    # ax[2].plot(x, list((round(H2_loadFactor[y]['SMR + CCS2'] * 100)) for y in YEAR), color=col(1), label='SMR + CCUS 90%',zorder=2)
    # Create WindOnshore line
    # ax[2].plot(x, list((round(EnR_loadFactor[y]['WindOnShore'] * 100)) for y in YEAR),linestyle='--' ,color=col(13), label='Wind Onshore',zorder=2)
    # # Create Solar line
    # ax[2].plot(x, list((round(EnR_loadFactor[y]['Solar'] * 100) for y in YEAR)),linestyle='--',color=col(5), label='Solar',zorder=2)

    #add Load factors
    # for i,y in enumerate(YEAR):
    #     if capa.loc[(y,'electrolysis_AEL'),'capacity_Pvar'] > 100:
    #         ax[0].text((x + width/2)[i], l7[i]/2, str(round(H2_loadFactor[y]['electrolysis_AEL']*100)) +'%',ha='center')
    #     if capa.loc[(y,'SMR'),'capacity_Pvar'] > 100:
    #         ax[0].text((x - width / 2)[i], l1[i] / 2, str(round(H2_loadFactor[y]['SMR'] * 100)) + '%',ha='center',color='white')
    #     if capa.loc[(y,'SMR + CCS1'),'capacity_Pvar'] > 100:
    #         ax[0].text((x - width / 2)[i], l1[i]+l2[i] / 2, str(round(H2_loadFactor[y]['SMR + CCS1'] * 100)) + '%',ha='center',color='white')
    #     if capa.loc[(y, 'Solar'), 'capacity_Pvar'] > 10:
    #         ax[1].text((x)[i], l8[i] / 2, str(round(EnR_loadFactor[y]['Solar'] * 100)) + '%', ha='center')
    #     if capa.loc[(y,'Solar'),'capacity_Pvar'] > 100:
    #         ax[1].text((x)[i], l8[i]/2, str(round(EnR_loadFactor[y]['Solar'] * 100)) + '%', ha='center',color='white')
    #     if capa.loc[(y,'WindOnShore'),'capacity_Pvar'] > 100:
    #         ax[1].text((x)[i], l8[i]+l9[i]/2, str(round(EnR_loadFactor[y]['WindOnShore'] * 100)) + '%', ha='center',color='white')
    #     if capa.loc[(y,'WindOffShore_flot'),'capacity_Pvar'] > 100:
    #         ax[1].text((x)[i], l8[i]+l9[i]+l10[i]/2, str(round(EnR_loadFactor[y]['WindOffShore_flot'] * 100)) + '%', ha='center',color='white')

    ax[0].set_ylim([0,max(l7)+100])
    ax[0].grid(axis='y',alpha=0.5,zorder=1)
    ax[1].set_ylim([0,max([i+j+k+l for i,j,k,l in zip(l8,l9,l10,l11)])+100])
    ax[1].grid(axis='y',alpha=0.5,zorder=1)
    # ax[2].grid(axis='y', alpha=0.5,zorder=1)
    ax[0].set_ylabel('Installed capacity (MW)')
    ax[1].set_ylabel('Installed capacity (MW)')
    # ax[2].set_ylabel('Load factors (%)')
    ax[0].set_title("Evolution of H2 production assets")
    ax[1].set_title("Evolution of EnR assets")
    # ax[2].set_title("Evolution of load factors")
    plt.xticks(x, ['2020','2030'])#['2010-2020','2020-2030','2030-2040', '2040-2050']'2050-2060'])
    # Shrink current axis by 20%
    box = ax[0].get_position()
    ax[0].set_position([box.x0, box.y0, box.width * 0.73, box.height*0.95])
    # Put a legend to the right of the current axis
    ax[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # Shrink current axis by 20%
    box = ax[1].get_position()
    ax[1].set_position([box.x0, box.y0, box.width * 0.73, box.height*0.95])
    # Put a legend to the right of the current axis
    ax[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # Shrink current axis by 20%
    # box = ax[2].get_position()
    # ax[2].set_position([box.x0, box.y0, box.width * 0.73, box.height*0.95])
    # Put a legend to the right of the current axis
    # ax[2].legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputFolder+'/Evolution mix prod.png')
    plt.show()

    def monthly_average(df):
        df['month'] = df.index // 730 + 1
        df.loc[8760,'month']=12
        return df.groupby('month').mean()

    loadFactors_df=Variables['power_Dvar'].copy().pivot(index=['YEAR_op','TIMESTAMP'],columns='TECHNOLOGIES',values='power_Dvar')
    for y in YEAR :
        for tech in TECHNO:
            loadFactors_df.loc[y,slice(None)][tech]=(Variables['power_Dvar'].set_index(['YEAR_op','TIMESTAMP','TECHNOLOGIES']).loc[(y,slice(None),tech),'power_Dvar']/Variables['capacity_Pvar'].set_index(['YEAR_op','TECHNOLOGIES']).loc[(y,tech),'capacity_Pvar']).reset_index().drop(columns=['TECHNOLOGIES','YEAR_op']).set_index('TIMESTAMP')['power_Dvar']

    month=np.unique(TIMESTAMP//730+1)[:-1]

    fig, ax = plt.subplots()

    for k,y in enumerate(YEAR):
        #Create electrolysis graph
        l1=list(monthly_average(loadFactors_df.loc[(y,slice(None))])['electrolysis_AEL']*100)
        plt.plot(month,l1,color=col(8+k),label=y,zorder=2)

    plt.grid(axis='y',alpha=0.5,zorder=1)
    plt.ylabel('Load factor (%)')
    plt.xlabel('Months')
    plt.xticks(month,['January','February','March','April','May','June','July','August','September','October','November','December'],rotation=45)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0+0.1, box.width * 0.90, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputFolder+'/elec_LoadFactor.png')
    plt.show()

    return df

def plot_energy(outputFolder='data/output/'):
    v_list = ['capacityInvest_Dvar', 'transInvest_Dvar', 'capacity_Pvar', 'capacityDel_Pvar', 'capacityDem_Dvar',
              'energy_Pvar', 'power_Dvar', 'storageConsumption_Pvar', 'storageIn_Pvar', 'storageOut_Pvar',
              'stockLevel_Pvar', 'importation_Dvar', 'Cmax_Pvar', 'carbon_Pvar', 'powerCosts_Pvar', 'capacityCosts_Pvar',
              'importCosts_Pvar', 'storageCosts_Pvar', 'turpeCosts_Pvar', 'Pmax_Pvar', 'max_PS_Dvar', 'carbonCosts_Pvar','exportation_Dvar']
    Variables = {v: pd.read_csv(outputFolder + '/' + v + '.csv').drop(columns='Unnamed: 0') for v in v_list}

    YEAR=Variables['power_Dvar'].set_index('YEAR_op').index.unique().values
    YEAR.sort()

    df = Variables['power_Dvar'].groupby(['YEAR_op', 'TECHNOLOGIES']).sum().drop(columns='TIMESTAMP').reset_index()
    df = df.pivot(columns='TECHNOLOGIES', values='power_Dvar', index='YEAR_op').rename(columns={
        "electrolysis_AEL": "Alkaline electrolysis",
        "electrolysis_PEMEL": "PEM electrolysis",
        'SMR': "SMR w/o CCUS",
        'SMR + CCS1': 'SMR + CCUS 50%',
        'SMR + CCS2': 'SMR + CCUS 90%',
        'SMR_elec': 'eSMR w/o CCUS',
        'SMR_elecCCS1': 'eSMR + CCUS 50%',
        'cracking': 'Methane cracking'
    }).fillna(0)

    df = df / 1000000

    df_renewables=Variables['power_Dvar'].pivot(index=['YEAR_op','TIMESTAMP'],columns='TECHNOLOGIES',values='power_Dvar')[['WindOnShore','WindOffShore_flot','Solar','WindOnShorePPA','WindOffShorePPA','SolarPPA']].reset_index().groupby('YEAR_op').sum().drop(columns='TIMESTAMP').sum(axis=1)
    df_export=Variables['exportation_Dvar'].groupby(['YEAR_op','RESOURCES']).sum().loc[(slice(None),'electricity'),'exportation_Dvar'].reset_index().drop(columns='RESOURCES').set_index('YEAR_op')
    df_feedRE=(df_renewables-df_export['exportation_Dvar'])/1.54/1000000#

    df_biogas=Variables['importation_Dvar'].groupby(['YEAR_op','RESOURCES']).sum().loc[(slice(None),'gazBio'),'importation_Dvar'].reset_index().set_index('YEAR_op').drop(columns='RESOURCES')
    for y in YEAR:
        fugitives = 0.03 * (1 - (y - YEAR[0]) / (2050 - YEAR[0]))*df_biogas.loc[y]['importation_Dvar']
        temp=df_biogas.loc[y]['importation_Dvar']-fugitives
        if temp/1.28/1000000<df.loc[y]['SMR w/o CCUS']:
            df_biogas.loc[y]['importation_Dvar']=temp/1.28/1000000
        else:
            temp2=temp-df.loc[y]['SMR w/o CCUS']*1.28*1000000
            if temp2/1.32/1000000<df.loc[y]['SMR + CCUS 50%']:
                df_biogas.loc[y]['importation_Dvar']=df.loc[y]['SMR w/o CCUS']+temp2/1.32/1000000
            else:
                temp3=temp-df.loc[y]['SMR w/o CCUS']*1.28*1000000-df.loc[y]['SMR + CCUS 50%']*1.32*1000000
                if temp3/1.45/1000000<df.loc[y]['SMR + CCUS 90%']:
                    df_biogas.loc[y]['importation_Dvar']=df.loc[y]['SMR w/o CCUS']+df.loc[y]['SMR + CCUS 50%']+temp3/1.45/1000000
                else :
                    df_biogas.loc[y]['importation_Dvar'] = df.loc[y]['SMR w/o CCUS']+df.loc[y]['SMR + CCUS 50%']+df.loc[y]['SMR + CCUS 90%']

    fig, ax = plt.subplots(figsize=(6,4))
    width = 0.35
    col=plt.cm.tab20c
    labels = list(df.index)
    x = np.arange(len(labels))

    # Create dark grey Bar
    l1 = list(df['SMR w/o CCUS'])
    ax.bar(x, l1, width, color=col(17), label="SMR w/o CCUS",zorder=2)
    # Create dark bleu Bar
    l2 = list(df['SMR + CCUS 50%'])
    ax.bar(x, l2, width, bottom=l1, color=col(0), label="SMR + CCUS 50%",zorder=2)
    # Create turquoise bleu Bar
    l3 = list(df['SMR + CCUS 90%'])
    ax.bar(x , l3, width, bottom=[i + j for i, j in zip(l1, l2)], color=col(1), label="SMR + CCUS 90%",zorder=2)
    # Create biogas Bars
    l8=list(df_biogas['importation_Dvar'])
    plt.rcParams['hatch.linewidth']=8
    plt.rcParams['hatch.color'] = col(3)
    ax.bar(x ,l8,width,color='none',hatch='/',edgecolor=col(3),linewidth=0.5,label="Biomethane feed",alpha=0.8,zorder=3)
    # Create light green Bars
    l7 = list(df['Alkaline electrolysis']+ df['PEM electrolysis'])
    ax.bar(x , l7, width, color=col(8), label="AEL grid feed",zorder=2)
    # Create dark green bar
    l9=list(df_feedRE)
    ax.bar(x,l9,width,color=col(9),label="AEL RE feed",zorder=3)

    plt.grid(axis='y',alpha=0.5,zorder=1)
    ax.set_ylabel('H2 production (TWh/yr)')
    # ax.set_title("Use of assets")
    plt.xticks(x,['2020','2030']) #['2020-2030', '2030-2040', '2040-2050', '2050-2060'])#,'2060'])
    m=max(max(l7),max([l1[i]+l2[i]+l3[i] for i in np.arange(len(l1))]))
    ax.set_ylim([0,int(m)+0.5])
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.72, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputFolder+'/H2 production.png')
    plt.show()

    return df

def plot_stock(outputFolder='data/output/'):

    v_list = ['capacityInvest_Dvar', 'transInvest_Dvar', 'capacity_Pvar', 'capacityDel_Pvar', 'capacityDem_Dvar',
              'energy_Pvar', 'power_Dvar', 'storageConsumption_Pvar', 'storageIn_Pvar', 'storageOut_Pvar',
              'stockLevel_Pvar', 'importation_Dvar', 'Cmax_Pvar', 'carbon_Pvar', 'powerCosts_Pvar', 'capacityCosts_Pvar',
              'importCosts_Pvar', 'storageCosts_Pvar', 'turpeCosts_Pvar', 'Pmax_Pvar', 'max_PS_Dvar', 'carbonCosts_Pvar']
    Variables = {v: pd.read_csv(outputFolder + '/' + v + '.csv').drop(columns='Unnamed: 0') for v in v_list}

    YEAR=Variables['power_Dvar'].set_index('YEAR_op').index.unique().values
    YEAR.sort()

    stock={y:Variables['stockLevel_Pvar'].loc[Variables['stockLevel_Pvar']['YEAR_op']==y].pivot(index='TIMESTAMP',columns='STOCK_TECHNO',values='stockLevel_Pvar') for y in YEAR}

    # hourly
    fig, ax = plt.subplots(4, 1, figsize=(6, 10), sharex=True,sharey=True)
    col=plt.cm.tab20c
    colBis=plt.cm.tab20b
    for k,yr in enumerate(YEAR):
        ax.plot(stock[yr].index,stock[yr]['tankH2_G']/1000,color=colBis(6),label='Stock hydrogen tank')
        ax.plot(stock[yr].index, stock[yr]['saltCavernH2_G'] / 1000,color=colBis(17), label='Stock hydrogen cavern')
        # ax.plot(stock[yr].index, stock[yr]['Battery']/1000, color=colBis(8),label='Stock electricity')
        ax.set_ylabel('Stock level (GWh)')
        # Shrink all axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.74, box.height])
    ax[0].legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax[-1].set_xlabel('Hour')
    plt.savefig(outputFolder+'/Gestion stockage.png')
    plt.show()

    fig, ax = plt.subplots(figsize=(6,4))
    ax1=ax.twinx()
    l1=ax.plot(stock[2050].index,stock[2050]['tankH2_G']/1000,color=colBis(6),label='Stock tank')
    # l2=ax1.plot(stock[2050].index, stock[2050]['saltCavernH2_G'] / 1000,color=colBis(17), label='Stock cavern')
    l3=ax1.plot(stock[yr].index, stock[yr]['Battery']/1000, color=colBis(8),label='Stock battery')
    legendLabels=[l.get_label() for l in l1+l3]
    ax.set_ylabel('Tank stock level (GWh)')
    ax1.set_ylabel('Battery stock level (GWh)')
    # Shrink all axis by 20%
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0, box.width * 0.72, box.height])
    plt.legend(l1+l3,legendLabels,loc='upper left', bbox_to_anchor=(1.1, 1))
    ax.set_xlabel('Hour')
    plt.savefig(outputFolder+'/Stock 2050.png')
    plt.show()

    return

def extract_costs(scenario,area,outputFolder='data/output/'):

    v_list = ['capacityInvest_Dvar', 'transInvest_Dvar', 'capacity_Pvar', 'capacityDel_Pvar', 'capacityDem_Dvar',
              'energy_Pvar', 'power_Dvar', 'storageConsumption_Pvar', 'storageIn_Pvar', 'storageOut_Pvar',
              'stockLevel_Pvar', 'importation_Dvar', 'Cmax_Pvar', 'carbon_Pvar', 'powerCosts_Pvar', 'capacityCosts_Pvar',
              'importCosts_Pvar', 'storageCosts_Pvar', 'turpeCosts_Pvar','pipeCosts_Pvar', 'Pmax_Pvar', 'max_PS_Dvar', 'carbonCosts_Pvar']
    Variables = {v: pd.read_csv(outputFolder + '/' + v + '.csv').drop(columns='Unnamed: 0') for v in v_list}

    inputDict = loadScenario(scenario)

    YEAR=Variables['power_Dvar'].set_index('YEAR_op').index.unique().values
    YEAR.sort()
    dy=YEAR[1]-YEAR[0]
    y0=YEAR[0]-dy

    convFac=inputDict['conversionFactor']
    Tech=inputDict['techParameters'].rename(index={2010:2020,2020:2030,2030:2040,2040:2050,2050:2060})
    Tech.sort_index(inplace=True)
    TaxC=inputDict['carbonTax']


    Grid_car=inputDict['resourceImportCO2eq'].set_index(['YEAR','TIMESTAMP'])['electricity'].reset_index().rename(columns={'electricity':'carbonContent'}).set_index(['YEAR','TIMESTAMP'])
    df1=Variables['powerCosts_Pvar'].rename(columns={'YEAR_op':'YEAR','powerCosts_Pvar':'powerCosts'}).set_index(['AREA','YEAR','TECHNOLOGIES']).loc[(area,slice(None),slice(None))]
    df1['capacityCosts']=Variables['capacityCosts_Pvar'].rename(columns={'YEAR_op':'YEAR'}).set_index(['AREA','YEAR','TECHNOLOGIES']).loc[(area,slice(None),slice(None))]
    df1['Prod']=Variables['power_Dvar'].rename(columns={'YEAR_op':'YEAR'}).groupby(['AREA','YEAR','TECHNOLOGIES']).sum().drop(columns=['TIMESTAMP']).loc[(area,slice(None),slice(None))]
    df2=Variables['importCosts_Pvar'].rename(columns={'YEAR_op':'YEAR','importCosts_Pvar':'importCosts'}).set_index(['AREA','YEAR','RESOURCES']).loc[(area,slice(None),slice(None))]
    df2['TURPE']=Variables['turpeCosts_Pvar'].rename(columns={'YEAR_op':'YEAR'}).set_index(['AREA','YEAR','RESOURCES']).loc[(area,slice(None),slice(None))]
    df3=Variables['capacityCosts_Pvar'].rename(columns={'YEAR_op':'YEAR'}).set_index(['AREA','YEAR','TECHNOLOGIES']).loc[(area,slice(None),slice(None))]
    df4=Variables['storageCosts_Pvar'].rename(columns={'YEAR_op':'YEAR','storageCosts_Pvar':'storageCosts'}).set_index(['AREA','YEAR','STOCK_TECHNO']).loc[(area,slice(None),slice(None))]
    df5=Variables['carbonCosts_Pvar'].rename(columns={'YEAR_op':'YEAR','carbonCosts_Pvar':'carbon'}).set_index(['AREA','YEAR']).loc[(area,slice(None))]
    df6=Variables['pipeCosts_Pvar'].rename(columns={'YEAR_op':'YEAR','pipeCosts_Pvar':'pipelineH2'}).set_index(['YEAR'])

    df1.sort_index(inplace=True)
    df2.sort_index(inplace=True)
    df3.sort_index(inplace=True)
    df4.sort_index(inplace=True)
    df5.sort_index(inplace=True)
    df6.sort_index(inplace=True)



    for y in YEAR:
        for tech in ['WindOnShore','WindOffShore_flot','Solar','WindOnShorePPA','WindOffShorePPA','SolarPPA']: #'CCS1','CCS2',
            df1.drop((y,tech),inplace=True)

    # Energy use
    TECHNO = list(df1.index.get_level_values('TECHNOLOGIES').unique())
    TIMESTAMP=list(Variables['power_Dvar'].set_index('TIMESTAMP').index.get_level_values('TIMESTAMP').unique())

    df1['elecUse'] = 0
    df1['gasUse'] = 0
    df1['carbon'] = 0

    for tech in TECHNO:
        df1.loc[(slice(None),tech),'elecUse']=df1.loc[(slice(None),tech),'Prod']*(-convFac.loc[('electricity',tech),'conversionFactor'])
        df1.loc[(slice(None), tech), 'gasUse'] = df1.loc[(slice(None), tech), 'Prod'] * (-convFac.loc[('gaz', tech), 'conversionFactor'])

    Elecfac=pd.DataFrame(YEAR,columns=['YEAR']).set_index('YEAR')
    imp=Variables['importation_Dvar'].rename(columns={'YEAR_op':'YEAR'}).set_index(['AREA','YEAR','TIMESTAMP','RESOURCES']).loc[(area,slice(None),slice(None),'electricity')].groupby('YEAR').sum()

    for y in YEAR:
        if df1['elecUse'].groupby('YEAR').sum().loc[y]==0:
            Elecfac.loc[y, 'ElecFac'] =0
        else :
            Elecfac.loc[y,'ElecFac']=imp.loc[y,'importation_Dvar']/df1['elecUse'].groupby('YEAR').sum().loc[y]

    df_biogas=Variables['importation_Dvar'].groupby(['AREA','YEAR_op','RESOURCES']).sum().loc[(area,slice(None),'gazBio'),'importation_Dvar'].reset_index().rename(columns={'YEAR_op':'YEAR'}).set_index('YEAR').drop(columns='RESOURCES')
    df_natgas=Variables['importation_Dvar'].groupby(['AREA','YEAR_op','RESOURCES']).sum().loc[(area,slice(None),'gazNat'),'importation_Dvar'].reset_index().rename(columns={'YEAR_op':'YEAR'}).set_index('YEAR').drop(columns='RESOURCES')
    natgasFac=df_natgas['importation_Dvar']/(df_natgas['importation_Dvar']+df_biogas['importation_Dvar'])
    natgasFac=natgasFac.fillna(0)

    for tech in TECHNO:
        Grid_car[tech]=Variables['power_Dvar'].rename(columns={'YEAR_op':'YEAR'}).set_index(['AREA','YEAR','TIMESTAMP','TECHNOLOGIES']).loc[(area,slice(None),slice(None),tech)]*(-convFac.loc[('electricity',tech),'conversionFactor'])
        Grid_car[tech]=Grid_car[tech]*Grid_car['carbonContent']
        df1.loc[(slice(None), tech), 'carbon'] = (df1.loc[(slice(None), tech), 'Prod'] * ((-convFac.loc[('gaz', tech), 'conversionFactor']) * 203.5 * natgasFac + Tech.loc[(area,slice(None),tech),'EmissionCO2'].reset_index().drop(columns='TECHNOLOGIES').set_index('YEAR')['EmissionCO2']) + Grid_car[tech].groupby('YEAR').sum()*Elecfac['ElecFac'])*TaxC['carbonTax']

    df1['prodPercent']=0
    for y in YEAR:
        if df1['elecUse'].groupby('YEAR').sum().loc[y] == 0 : df1.loc[(y, slice(None)), 'elecPercent']=0
        else : df1.loc[(y,slice(None)),'elecPercent']=df1.loc[(y,slice(None)),'elecUse']/df1['elecUse'].groupby('YEAR').sum().loc[y]
        if df1['gasUse'].groupby('YEAR').sum().loc[y]==0 : df1.loc[(y, slice(None)), 'gasPercent']=0
        else : df1.loc[(y, slice(None)), 'gasPercent'] = df1.loc[(y, slice(None)), 'gasUse']/df1['gasUse'].groupby('YEAR').sum().loc[y]
        if df1.loc[(y, 'electrolysis_AEL'), 'Prod']==0 : df1.loc[(y, 'electrolysis_AEL'), 'prodPercent'] =0
        else : df1.loc[(y, 'electrolysis_AEL'), 'prodPercent'] = df1.loc[(y, 'electrolysis_AEL'), 'Prod'] / (df1.loc[(y, 'electrolysis_AEL'), 'Prod'])


    #regroupement
    df1['type'] = 'None'
    df1.loc[(slice(None), 'SMR'), 'type']='SMR'
    df1.loc[(slice(None), 'electrolysis_AEL'), 'type']='AEL'

    # Repartition coût and Removing actualisation
    def actualisationFactor(r,y):
        return (1 + r) ** (-(y+dy/2 - y0))

    r=inputDict['economics'].loc['discountRate'].value

    

    for y in YEAR:
        df1.loc[(y,slice(None)),'importElec']=df1.loc[(y,slice(None)),'elecPercent']*df2.loc[(y,'electricity')]['importCosts']/actualisationFactor(r,y)
        df1.loc[(y, slice(None)), 'TURPE'] = df1.loc[(y, slice(None)), 'elecPercent'] * df2.loc[(y, 'electricity')]['TURPE']/actualisationFactor(r,y)
        df1.loc[(y,slice(None)),'capexElec']=df1.loc[(y,slice(None)),'elecPercent']*(df3.loc[(y,'WindOnShore')]['capacityCosts_Pvar']+df3.loc[(y,'WindOffShore_flot')]['capacityCosts_Pvar']+df3.loc[(y,'Solar')]['capacityCosts_Pvar']+df3.loc[(y,'SolarPPA')]['capacityCosts_Pvar']+df3.loc[(y,'WindOnShorePPA')]['capacityCosts_Pvar']+df3.loc[(y,'WindOffShorePPA')]['capacityCosts_Pvar'])/actualisationFactor(r,y)
        df1.loc[(y, slice(None)), 'importGas'] = df1.loc[(y,slice(None)),'gasPercent']*(df2.loc[(y, 'gazNat')]['importCosts']+df2.loc[(y, 'gazBio')]['importCosts'])/actualisationFactor(r,y)
        df1.loc[(y,slice(None)),'storageElec']=df1.loc[(y,slice(None)),'elecPercent']*df4.loc[(y,'Battery')]['storageCosts']/actualisationFactor(r,y)
        df1.loc[(y, slice(None)), 'storageH2'] = df1.loc[(y, slice(None)), 'prodPercent'] *( df4.loc[(y, 'tankH2_G')]['storageCosts']+ df4.loc[(y, 'saltCavernH2_G')]['storageCosts'])/actualisationFactor(r,y)
        df1.loc[(y,slice(None)),'carbon']=df1.loc[(y,slice(None)),'carbon']
        df1.loc[(y, slice(None)), 'powerCosts'] = df1.loc[(y, slice(None)), 'powerCosts'] / actualisationFactor(r, y)
        df1.loc[(y, slice(None)), 'capacityCosts'] = df1.loc[(y, slice(None)), 'capacityCosts'] / actualisationFactor(r, y)
        df1.loc[(y, slice(None)), 'pipelineH2'] = df6.loc[y, 'pipelineH2']*df1.loc[(y,slice(None)),'prodPercent'] / actualisationFactor(r,y)
        df1.loc[(y,'electrolysis_AEL'),'importH2']=df2.loc[(y, 'hydrogen')]['importCosts']/actualisationFactor(r,y)

    df1['Prod'].loc[df1['Prod']<0.0001]=0


    TECH=['AEL','SMR','eSMR']
    df={tech:df1.loc[df1['type']==tech].groupby('YEAR').sum() for tech in TECH}
    df_cocon=pd.DataFrame(index=YEAR)

    for tech in TECH:
        if df[tech]['Prod'].sum()==0:
            df.pop(tech)
        # else :
        #     for y in YEAR:
        #         if df[tech].loc[y]['Prod']==0:
        #             df_cocon.loc[y,tech] = df[tech]['capacityCosts'].loc[y]+df[tech]['storageElec'].loc[y]+df[tech]['storageH2'].loc[y]+df[tech]['capexElec'].loc[y]
        #             df[tech].loc[y]=0
        #             df[tech].loc[y]['Prod']=1

    importH2=Variables['importation_Dvar'].rename(columns={'YEAR_op':'YEAR'}).set_index(['AREA','YEAR','TIMESTAMP','RESOURCES']).loc[(area,slice(None),slice(None),'hydrogen')].groupby('YEAR').sum()
    df['AEL']['Prod']=df['AEL']['Prod']+importH2['importation_Dvar']

    return df

def plot_costs(df,outputPath='data/output/ISGT/'):

    YEAR=df[list(df.keys())[0]].index.values
    YEAR.sort()
    dy=YEAR[1]-YEAR[0]
    y0=YEAR[0]-dy

    fig, ax = plt.subplots(figsize=(7,3))
    width= 0.5
    B=list(df.keys())
    B_nb=len(B)
    x = np.arange(B_nb)
    col=plt.cm.tab20

    parameters={'axes.labelsize': 12,
                'xtick.labelsize': 12,
                'ytick.labelsize': 12,
              'figure.titlesize': 15,
                'legend.fontsize':12}
    plt.rcParams.update(parameters)

    # Create blue Bars
    a=[]
    for i in np.arange(B_nb):
        a.append(df[B[i]].loc[2030,'capacityCosts']/(df[B[i]].loc[2030,'Prod']*30))
    plt.bar(x, a, width, color=col(0),label="Electrolysis capacity",zorder=2)

    # Create light blue Bars
    aa=[]
    for i in np.arange(B_nb):
        aa.append(df[B[i]].loc[2030,'powerCosts']/(df[B[i]].loc[2030,'Prod']*30))
    plt.bar(x, aa, width,bottom=a, color=col(1),label="",zorder=2)

    # Create green Bars
    b=[]
    for i in np.arange(B_nb):
        b.append(df[B[i]].loc[2030,'capexElec']/(df[B[i]].loc[2030,'Prod']*30))
    plt.bar(x , b, width, bottom=[i+j for i,j in zip(a,aa)], color=col(4),label="Renewables capacity",zorder=2)

    # Create dark red Bars
    c=[]
    for i in np.arange(B_nb):
        c.append(df[B[i]].loc[2030,'importElec']/(df[B[i]].loc[2030,'Prod']*30))
    plt.bar(x , c, width, bottom=[i+j+k for i,j,k in zip(a,aa,b)], color=col(6),label="Grid electricity" ,zorder=2)

    # Create light red Bars
    d=[]
    for i in np.arange(B_nb):
        d.append(df[B[i]].loc[2030,'TURPE']/(df[B[i]].loc[2030,'Prod']*30))
    plt.bar(x , d, width, bottom=[i+j+k+l for i,j,k,l in zip(a,aa,b,c)], color=col(7),label="Network taxes" ,zorder=2)

    # Create purple Bars
    e=[]
    for i in np.arange(B_nb):
        e.append(df[B[i]].loc[2030,'storageH2']/(df[B[i]].loc[2030,'Prod']*30))
    plt.bar(x , e, width, bottom=[i+j+k+l+m for i,j,k,l,m in zip(a,aa,b,c,d)], color=col(8),label="H2 storage capacity" ,zorder=2)


    # Create light purple Bars
    f=[]
    for i in np.arange(B_nb):
        f.append(df[B[i]].loc[2030,'pipelineH2']/(df[B[i]].loc[2030,'Prod']*30))
    plt.bar(x, f, width, bottom=[i+j+k+l+m+n for i,j,k,l,m,n in zip(a,aa,b,c,d,e)], color=col(9),label="H2 transportation" ,zorder=2)

    # Create orange bars
    h=[]
    for i in np.arange(B_nb):
        h.append(df[B[i]].loc[2030,'importH2']/(df[B[i]].loc[2030,'Prod']*30))
    plt.bar(x, h, width, bottom=[i+j+k+l+m+n+o for i,j,k,l,m,n,o in zip(a,aa,b,c,d,e,f)], color=col(2),label="H2 importations" ,zorder=2)


    # Create grey Bars
    v=[]
    for i in np.arange(B_nb):
        v.append(df[B[i]].loc[2030,'carbon']/(df[B[i]].loc[2030,'Prod']*30))
    plt.bar(x, v, width,  bottom=[i+j+k+l+m+n+o+p for i,j,k,l,m,n,o,p in zip(a,aa,b,c,d,e,f,h)], color=col(15),label="Carbon tax" ,zorder=2)

    s= []
    maxi=[]
    for i in np.arange(B_nb):
        s.append(a[i]+aa[i]+b[i]+c[i]+d[i]+e[i]+f[i]+h[i]+v[i])
        print (B[i],'=',s[i])
        maxi.append(np.max(s[i]))

    for i,j in enumerate(maxi) :
        if j == np.inf: maxi.pop(i)


    ax.set_ylabel('Levelised cost of hydrogen (€/kgH$_2$)')
    x=list(x)
    plt.xticks(x,B)

    ax.set_ylim([0,np.max(maxi)+0.5])
    # ax.set_title("Hydrogen production costs")
    plt.grid(axis='y',alpha=0.5,zorder=1)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.65, box.height])
    # get handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # specify order of items in legend
    order = [7,6,5,4,3, 2, 1, 0]
    # Put a legend to the right of the current axis
    ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputPath+'/H2 costs.png')
    plt.show()

    return

def plot_Costs2030(df,outputFolder='data/output/'):

    fig, ax = plt.subplots(figsize=(7.5,5))
    width= 0.3
    labels=[2030]
    x = np.arange(len(labels))
    col=plt.cm.tab20c
    colBis=plt.cm.tab20b

    parameters={'axes.labelsize': 13,
                'xtick.labelsize': 13,
                'ytick.labelsize': 13,
                'legend.fontsize':13}
    plt.rcParams.update(parameters)

    # Create light blue Bars
    a=df['capacityCosts']/(df['Prod']*30)
    plt.bar(x, a, width, color=col(1),label="Fixed Costs",zorder=2)

    # Create dark blue Bars
    aa=df['powerCosts']/(df['Prod']*30)
    plt.bar(x, aa, width,bottom=a, color=col(0),label="Variable Costs" ,zorder=2)

    # Create brown Bars
    b=df['importGas']/(df['Prod']*30)
    plt.bar(x, b, width, bottom=a+aa, color=colBis(9),label="Gas" ,zorder=2)

    # Create green Bars
    c=df['capexElec']/(df['Prod']*30)
    plt.bar(x, c, width, bottom=a+aa+b, color=col(9),label="Local RE capa" ,zorder=2)

    # Create dark red Bars
    d=df['importElec']/(df['Prod']*30)
    plt.bar(x, d, width, bottom=a+aa+b+c, color=colBis(14),label="Grid electricity" ,zorder=2)

    # Create light red Bars
    e=df['TURPE']/(df['Prod']*30)
    plt.bar(x, e, width,  bottom=a+aa+b+c+d, color=colBis(15),label="Network taxes" ,zorder=2)

    # Create purple Bars
    f=df['storageH2']/(df['Prod']*30)
    plt.bar(x, f, width, bottom=a+aa+b+c+d+e, color=colBis(17),label="H2 storage capa" ,zorder=2)

    # Create light purple Bars
    ff=df['pipelineH2']/(df['Prod']*30)
    plt.bar(x, f, width, bottom=a+aa+b+c+d+e, color=colBis(18),label="H2 transportation" ,zorder=2)

    # Create yellow Bars
    g=df['storageElec']/(df['Prod']*30)
    plt.bar(x, g, width,   bottom=a+aa+b+c+d+e+f+ff, color=col(5),label="Elec storage capa" ,zorder=2)

    # Create grey Bars
    h=df['carbon']/(df['Prod']*30)
    plt.bar(x, h, width,   bottom=a+aa+b+c+d+e+f+ff+g, color=col(18),label="Carbon tax" ,zorder=2)

    ax.set_ylabel('Costs (€/kgH$_2$)')
    plt.xticks(x, ['2030'])
    m=a+aa+b+c+d+e+f+ff+g+h
    ax.set_ylim([0,np.round(m)+1])
    # ax.set_title("Hydrogen production costs")
    plt.grid(axis='y',alpha=0.5,zorder=1)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.68 , box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputFolder+'/H2 costs.png')
    plt.show()

    return

def plot_carbon(outputFolder='data/output/'):

    carbon=pd.read_csv(outputFolder+'/carbon_Pvar.csv').groupby('YEAR_op').sum().drop(columns=['TIMESTAMP','Unnamed: 0'])/1000000
    carbon=carbon.sort_index()
    Prod=pd.read_csv(outputFolder+'/energy_Pvar.csv').groupby(['YEAR_op','RESOURCES']).sum().drop(columns=['TIMESTAMP','Unnamed: 0']).loc[(slice(None),'hydrogen'),'energy_Pvar'].reset_index().set_index('YEAR_op').drop(columns='RESOURCES')
    carbonContent=carbon['carbon_Pvar']*1000000/(Prod['energy_Pvar']*30)

    # carbon_ref=pd.read_csv('data/output\SmrOnly_var4bis_PACA/carbon_Pvar.csv').groupby('YEAR_op').sum().drop(columns=['TIMESTAMP','Unnamed: 0'])/1000000
    # carbon_ref=carbon_ref.sort_index()
    # Prod_ref=pd.read_csv('data/output\SmrOnly_var4bis_PACA/energy_Pvar.csv').groupby(['YEAR_op','RESOURCES']).sum().drop(columns=['TIMESTAMP','Unnamed: 0']).loc[(slice(None),'hydrogen'),'energy_Pvar'].reset_index().set_index('YEAR_op').drop(columns='RESOURCES')
    # carbonContent_ref = carbon_ref['carbon_Pvar'] * 1000000 / (Prod_ref['energy_Pvar'] * 30)

    # test=pd.read_csv('data/output\Ref_Base_PACA/carbon_Pvar.csv').groupby('YEAR_op').sum().drop(columns=['TIMESTAMP','Unnamed: 0'])/1000000
    # test=test.sort_index()
    # Prod_test=pd.read_csv('data/output\Ref_Base_PACA/energy_Pvar.csv').groupby(['YEAR_op','RESOURCES']).sum().drop(columns=['TIMESTAMP','Unnamed: 0']).loc[(slice(None),'hydrogen'),'energy_Pvar'].reset_index().set_index('YEAR_op').drop(columns='RESOURCES')
    # carbonContent_test= test['carbon_Pvar'] * 1000000 / (Prod_test['energy_Pvar'] * 30)

    # avoided=[carbon_ref.carbon_Pvar.loc[2020]-carbon.carbon_Pvar.loc[2050],carbon_ref.carbon_Pvar.loc[2050]-carbon.carbon_Pvar.loc[2050]]

    YEAR=carbon.index.unique().values

    # plt.plot(YEAR,carbon_ref.carbon_Pvar,label='Reference CO2 emission')
    plt.plot(YEAR,carbon.carbon_Pvar,label='CO2 emissions',color='g')
    # plt.plot(YEAR, test.carbon_Pvar,linestyle='--',label='Base CO2 emissions',color='g')

    # plt.fill_between(YEAR,carbon_ref.carbon_Pvar,carbon.carbon_Pvar,color='none',edgecolor='#cccccc',hatch='//')
    plt.title('CO2 Avoided emissions')
    plt.legend()
    plt.ylabel('kt/yr')
    plt.xlabel('year')
    plt.savefig(outputFolder+'/Emissions.png')
    plt.show()

    # plt.plot(YEAR,carbonContent_ref,label='Reference CO2 content')
    plt.plot(YEAR,carbonContent,label='CO2 content',color='g')
    # plt.plot(YEAR, carbonContent_test,linestyle='--',label='Base CO2 content',color='g')

    # plt.fill_between(YEAR,carbonContent_ref,carbonContent,color='none',edgecolor='#cccccc',hatch='//')
    plt.title('Carbon content of hydrogen')
    plt.legend()
    plt.ylabel('kgCO2/kgH2')
    plt.xlabel('year')
    plt.savefig(outputFolder+'/Carbon content.png')
    plt.show()

    return

def plot_carbonCosts(dico,scenarioNames,outputPath='data/output/'):

    YEAR=list(list(dico.items())[0][1].items())[0][1].index.values
    YEAR.sort()

    carbonContent = {}
    meanPrice = {}
    horizonMean={}
    horizonContent={}
    for s in list(dico.keys()):
        meanPrice[s]=sum(dico[s][k][['powerCosts','capacityCosts','capexElec','importElec','importGas','storageElec','storageH2','carbon','TURPE']].sum(axis=1) for k in list(dico[s].keys()))/(sum((dico[s][k]['Prod']*30) for k in list(dico[s].keys())))
        horizonMean[s]=sum(dico[s][k][['powerCosts','capacityCosts','capexElec','importElec','importGas','storageElec','storageH2','carbon','TURPE']].sum(axis=1) for k in list(dico[s].keys())).sum()/(sum((dico[s][k]['Prod']*30) for k in list(dico[s].keys())).sum())
        carbon=pd.read_csv(outputPath+s+'_PACA/carbon_Pvar.csv').groupby('YEAR_op').sum().drop(columns=['TIMESTAMP','Unnamed: 0'])
        carbon=carbon.sort_index()
        carbonContent[s]=carbon['carbon_Pvar']/(sum((dico[s][k]['Prod']*30) for k in list(dico[s].keys())))
        horizonContent[s]=carbon['carbon_Pvar'].sum()/(sum((dico[s][k]['Prod']*30) for k in list(dico[s].keys())).sum())
        # plt.scatter(horizonContent[s],horizonMean[s],label=s)

    # plt.title('Cost and carbon content of hydrogen horizon mean')
    # plt.legend()
    # plt.ylabel('€/kgH2')
    # plt.xlabel('kgCo2/kgH2')
    # plt.savefig(outputPath + '/Comparaison carbon horizon mean.png')
    # plt.show()
    #
    # fig,ax=plt.subplots(1,3,sharey=True,sharex=True)
    # for k,y in enumerate(YEAR[1:]):
    #     for s in list(dico.keys()):
    #         ax.scatter(carbonContent[s].loc[y],meanPrice[s].loc[y],label=s)
    #         ax.set_title(str(y))
    #
    # ax[0].set_ylabel('€/kgH2')
    # ax[1].set_xlabel('kgCo2/kgH2')
    # ax[-1].legend()
    # plt.savefig(outputPath + '/Comparaison carbon subplot.png')
    # plt.show()

    fig,ax=plt.subplots()
    col = plt.cm.tab20c
    colBis = plt.cm.tab20b
    dico_color={'Ref':(colBis,0),'BM_':(col,0),'woSMR_':(colBis,16),'CO2_':(colBis,8),'Re_':(col,8)}
    colNumber=[]
    variable=[]
    n=0
    for l,s in enumerate(list(dico.keys())):
        for var in list(dico_color.keys()):
            if var in s:
                variable.append(var)
                if variable[l-1]==variable[l]:
                    n=n+1
                else :
                    n=0
                colNumber.append((dico_color[var][0],dico_color[var][1]+n))
    mark=['s','D','o']

    n=0
    for k,y in enumerate(YEAR[1:]):
        for l,s in enumerate(list(dico.keys())):
            ax.scatter(carbonContent[s].loc[y],meanPrice[s].loc[y],marker=mark[k],color=col(l*4),zorder=2) #colNumber[l][0+l*4](colNumber[l][1])
        ax.plot([],[],marker=mark[k],linestyle='',color='grey',label=str(y+5))
    for l,s in enumerate(list(dico.keys())):
        ax.plot(carbonContent[s].iloc[1:].values,meanPrice[s].iloc[1:].values,marker='',color=col(l*4),label=scenarioNames[n],linestyle='--',alpha=0.5,zorder=2)
        n+=1

    plt.title('')
    plt.ylabel('€/kgH$_2$')
    plt.xlabel('kgCO$_2$/kgH$_2$')
    # plt.title('LCOH and carbon content evolution')
    plt.grid(axis='y',alpha=0.5,zorder=1)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.72, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputPath + '/Comparaison carbon.png')
    plt.show()

    return

def plot_carbonCosts2050(dico,scenarioNames,outputPath='data/output/'):

    YEAR=list(list(dico.items())[0][1].items())[0][1].index.values
    YEAR.sort()

    carbonContent = {}
    meanPrice = {}
    horizonMean={}
    horizonContent={}
    for s in list(dico.keys()):
        meanPrice[s]=sum(dico[s][k][['powerCosts','capacityCosts','capexElec','importElec','importGas','storageElec','storageH2','carbon','TURPE']].sum(axis=1) for k in list(dico[s].keys()))/(sum((dico[s][k]['Prod']*30) for k in list(dico[s].keys())))
        horizonMean[s]=sum(dico[s][k][['powerCosts','capacityCosts','capexElec','importElec','importGas','storageElec','storageH2','carbon','TURPE']].sum(axis=1) for k in list(dico[s].keys())).sum()/(sum((dico[s][k]['Prod']*30) for k in list(dico[s].keys())).sum())
        carbon=pd.read_csv(outputPath+s+'_PACA/carbon_Pvar.csv').groupby('YEAR_op').sum().drop(columns=['TIMESTAMP','Unnamed: 0'])
        carbon=carbon.sort_index()
        carbonContent[s]=carbon['carbon_Pvar']/(sum((dico[s][k]['Prod']*30) for k in list(dico[s].keys())))
        horizonContent[s]=carbon['carbon_Pvar'].sum()/(sum((dico[s][k]['Prod']*30) for k in list(dico[s].keys())).sum())


    fig,ax=plt.subplots(figsize=(6,4))
    col = plt.cm.tab20c
    colBis = plt.cm.tab20b
    dico_color={'Ref':(colBis,0),'BM_':(col,0),'woSMR_':(colBis,16),'CO2_':(colBis,8),'Re_':(col,8)}
    dico_mark=['o','D','s','v','^']
    colNumber=[]
    markNumber=[]
    variable=[]
    n=0
    c=0
    for l,s in enumerate(list(dico.keys())):
        for var in list(dico_color.keys()):
            if var in s:
                variable.append(var)
                if variable[l-1]==variable[l]:
                    n=n+1
                else :
                    n=0
                    c=c+1
                colNumber.append((dico_color[var][0],dico_color[var][1]+n))
                markNumber.append(dico_mark[c])


    # n=0
    y=2050
    for l,s in enumerate(list(dico.keys())):
        ax.scatter(carbonContent[s].loc[y],meanPrice[s].loc[y],marker=markNumber[l],markersize=4,color=colNumber[l][0](colNumber[l][1]),zorder=2,label=scenarioNames[l])
    # for l,s in enumerate(list(dico.keys())):
    #     ax.plot(carbonContent[s].iloc[1:].values,meanPrice[s].iloc[1:].values,marker='',color=colNumber[l][0](colNumber[l][1]),label=scenarioNames[n],linestyle='--',alpha=0.5,zorder=2)
    #     n+=1

    plt.title('')
    plt.ylabel('€/kgH$_2$')
    plt.xlabel('kgCO$_2$/kgH$_2$')
    # plt.title('LCOH and carbon content evolution')
    plt.grid(axis='y',alpha=0.5,zorder=1)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0+0.05, box.width * 0.7, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputPath + '/Comparaison carbon 2050.png')
    plt.show()

    return

def extract_energy(scenario,area,outputFolder='data/output'):
    v_list = [ 'capacity_Pvar','energy_Pvar', 'power_Dvar', 'storageConsumption_Pvar', 'storageIn_Pvar', 'storageOut_Pvar','importation_Dvar','carbon_Pvar',
             'powerCosts_Pvar', 'capacityCosts_Pvar','importCosts_Pvar', 'storageCosts_Pvar', 'turpeCosts_Pvar','carbonCosts_Pvar','pipeCosts_Pvar']#, 'exportation_Dvar']
    Variables = {v: pd.read_csv(outputFolder + '/' + v + '.csv').drop(columns='Unnamed: 0') for v in v_list}

    inputDict = loadScenario(scenario)

    YEAR = Variables['power_Dvar'].set_index('YEAR_op').index.unique().values
    YEAR.sort()
    dy=YEAR[1]-YEAR[0]
    y0=YEAR[0]-dy

    df = Variables['power_Dvar'].groupby(['AREA','YEAR_op', 'TECHNOLOGIES']).sum().drop(columns='TIMESTAMP').loc[(area,slice(None),slice(None))].reset_index()
    df = df.pivot(columns='TECHNOLOGIES', values='power_Dvar', index='YEAR_op').rename(columns={
        "electrolysis_AEL": "Alkaline electrolysis",
        "electrolysis_PEMEL": "PEM electrolysis",
        'SMR': "SMR w/o CCUS",
        'SMR + CCS1': 'SMR + CCUS 50%',
        'SMR + CCS2': 'SMR + CCUS 90%',
        'SMR_elec': 'eSMR w/o CCUS',
        'SMR_elecCCS1': 'eSMR + CCUS 50%',
        'cracking': 'Methane cracking'
    }).fillna(0)

    df = df / 1000

    df_capa = Variables['capacity_Pvar'].set_index('AREA').loc[area].reset_index()
    df_capa = df_capa.pivot(columns='TECHNOLOGIES', values='capacity_Pvar', index='YEAR_op').rename(columns={
        "electrolysis_AEL": "Alkaline electrolysis",
        "electrolysis_PEMEL": "PEM electrolysis",
        'SMR': "SMR w/o CCUS",
        'SMR + CCS1': 'SMR + CCUS 50%',
        'SMR + CCS2': 'SMR + CCUS 90%',
        'SMR_elec': 'eSMR w/o CCUS',
        'SMR_elecCCS1': 'eSMR + CCUS 50%',
        'cracking': 'Methane cracking'
    }).fillna(0)

    df_capa=df_capa*8760/1000

    df_carbon = Variables['carbon_Pvar'].groupby(['AREA','YEAR_op']).sum().drop(columns='TIMESTAMP').loc[(area,slice(None))]
    df_costs=Variables['powerCosts_Pvar'].groupby(['AREA','YEAR_op']).sum().rename(columns={'powerCosts_Pvar':'power'}).loc[(area,slice(None))]
    df_costs['capacity']=Variables['capacityCosts_Pvar'].groupby(['AREA','YEAR_op']).sum().loc[(area,slice(None))]
    df_costs['TURPE']=Variables['turpeCosts_Pvar'].groupby(['AREA','YEAR_op']).sum().loc[(area,slice(None))]
    df_costs['import'] = Variables['importCosts_Pvar'].groupby(['AREA','YEAR_op']).sum().loc[(area,slice(None))]
    df_costs['storage'] = Variables['storageCosts_Pvar'].groupby(['AREA','YEAR_op']).sum().loc[(area,slice(None))]
    df_costs['carbon'] = Variables['carbonCosts_Pvar'].groupby(['AREA','YEAR_op']).sum().loc[(area,slice(None))]
    df_costs['H2pipeline'] = Variables['pipeCosts_Pvar'].groupby('YEAR_op').sum()
    df_costs['total']=df_costs.sum(axis=1)


    df_loadFac=(df/df_capa).fillna(0)
    for l in df_loadFac.columns:df_loadFac[l]=df_loadFac[l].apply(lambda x:0 if x<0 else x)
    for l in df_loadFac.columns: df_loadFac[l] = df_loadFac[l].apply(lambda x: 0 if x > 1 else x)

    df_renewables = Variables['power_Dvar'].pivot(index=['AREA','YEAR_op', 'TIMESTAMP'], columns='TECHNOLOGIES', values='power_Dvar')[
        ['WindOnShore', 'WindOffShore_flot', 'Solar','WindOnShorePPA', 'WindOffShorePPA', 'SolarPPA']].reset_index().groupby(['AREA','YEAR_op']).sum().drop(
        columns='TIMESTAMP').sum(axis=1).loc[(area,slice(None))]
    # df_export = Variables['exportation_Dvar'].groupby(['YEAR_op', 'RESOURCES']).sum().loc[
    #     (slice(None), 'electricity'), 'exportation_Dvar'].reset_index().drop(columns='RESOURCES').set_index('YEAR_op')
    df_feedRE = (df_renewables) / 1.54 / 1000 #- df_export['exportation_Dvar']
    df_imports=Variables['importation_Dvar'].pivot(index=['AREA','YEAR_op', 'TIMESTAMP'], columns='RESOURCES', values='importation_Dvar')['hydrogen'].reset_index().groupby(['AREA','YEAR_op']).sum().drop(
        columns='TIMESTAMP').sum(axis=1).loc[(area,slice(None))]/1000

    df['importsH2']=df_imports

    df['totalProd']=df[['SMR w/o CCUS','Alkaline electrolysis','importsH2']].sum(axis=1)*30*1000

    df['feedRE']=df_feedRE
    df['loadFac_elec'] = df_loadFac['Alkaline electrolysis']
    df['total_carbon']=df_carbon['carbon_Pvar']
    df['carbon']=df_carbon['carbon_Pvar']/df['totalProd']
    df['carbon'].loc[df['carbon']<0]=0

    # print(df_loadFac[['WindOnShore', 'WindOffShore_flot', 'Solar']])

    def actualisationFactor(r,y):
        return (1 + r) ** (-(y+dy/2 - y0))

    r=inputDict['economics'].loc['discountRate'].value
    for y in YEAR:
        df_costs.loc[y,'total_nonAct']=df_costs.loc[y,'total']/actualisationFactor(r,y)

    df['costs']=df_costs['total_nonAct']/df['totalProd']
    df['total_costs']=df_costs['total_nonAct']

    return df

def extract_capa(area,outputFolder='data/output'):
    v_list = [ 'capacity_Pvar', 'power_Dvar','Cmax_Pvar','Pmax_Pvar','max_PS_Dvar']#, 'exportation_Dvar']
    Variables = {v: pd.read_csv(outputFolder + '/' + v + '.csv').drop(columns='Unnamed: 0') for v in v_list}

    YEAR = Variables['power_Dvar'].set_index('YEAR_op').index.unique().values
    YEAR.sort()
    dy=YEAR[1]-YEAR[0]
    y0=YEAR[0]-dy

    df = Variables['capacity_Pvar']
    df = df.pivot(columns='TECHNOLOGIES', values='capacity_Pvar', index='YEAR_op').rename(columns={
        "electrolysis_AEL": "Alkaline electrolysis",
        "electrolysis_PEMEL": "PEM electrolysis",
        'SMR': "SMR w/o CCUS",
        'SMR + CCS1': 'SMR + CCUS 50%',
        'SMR + CCS2': 'SMR + CCUS 90%',
        'SMR_elec': 'eSMR w/o CCUS',
        'SMR_elecCCS1': 'eSMR + CCUS 50%',
        'cracking': 'Methane cracking'
    }).fillna(0)
    df1=Variables['Cmax_Pvar'].pivot(columns='STOCK_TECHNO',values='Cmax_Pvar',index='YEAR_op').rename(columns={'tankH2_G': 'H2 tank','saltCavernH2_G' : 'Salt cavern'}).fillna(0)
    df2=Variables['Pmax_Pvar'].pivot(columns='STOCK_TECHNO',values='Pmax_Pvar',index='YEAR_op').rename(columns={'tankH2_G': 'H2 tank','saltCavernH2_G' : 'Salt cavern'}).fillna(0)
    df3=Variables['max_PS_Dvar'].pivot(columns='HORAIRE',values='max_PS_Dvar',index='YEAR_op').fillna(0)
    for stech in list(df1.columns):
        df[stech+'_Capa']=df1[stech]
        df[stech + '_Power']=df2[stech]
        df['Raccord pointe']=df3['P']
        df['Raccord creuses été'] = df3['HCE']

    return df

def plot_compare_energy(dico_ener, scenarioNames, outputPath='data/output/'):
    YEAR = list(list(dico_ener.items())[0][1].items())[0][1].index.values
    YEAR.sort()
    L = list(dico_ener.keys())

    for l in L:
        dico_ener[l] = dico_ener[l].loc[2030:2050]

    # fig=plt.figure(figsize=(8,6))
    # F = GridSpec(2,3,figure=fig)
    fig,ax=plt.subplots(1,3,sharey=True,figsize=(10,3))
    # ax1 = fig.add_subplot(F[0,0])
    # ax2 = fig.add_subplot(F[0,1],sharey=ax1)
    # ax3 = fig.add_subplot(F[0,2],sharey=ax1)
    # ax = [ax1, ax2, ax3]
    # ay = fig.add_subplot(F[1,:])
    width = 0.35
    col = plt.cm.tab20c
    labels = list(YEAR[1:])
    x = np.arange(len(labels))

    for k, l in enumerate(L):
        ax.grid(axis='y',alpha=0.5,color=col(19),zorder=1)

    for k, l in enumerate(L):
        # Create grey Bars
        l1 = list(dico_ener[l]['SMR w/o CCUS'] / 1000)
        ax.bar(x - width/2, l1, width, color=col(17),label="SMR w/o CCUS" if k == 2 else '',zorder=2)
        # Create blue Bars
        l2 = list((dico_ener[l]['SMR + CCUS 50%'] + dico_ener[l]['SMR + CCUS 90%']) / 1000)
        ax.bar(x - width/2 , l2, width, bottom=l1, color=col(0),label="SMR + CCUS" if k == 2 else '',zorder=2)
        # Create biogas Bars
        plt.rcParams['hatch.linewidth'] = 8
        plt.rcParams['hatch.color'] = col(3)
        l8 = list(dico_ener[l]['feedBiogas'] / 1000)
        ax.bar(x - width/2, l8, width, color='none', hatch='/',linewidth=0.5, edgecolor=col(3),alpha=0.8,label="Biomethane feed" if k == 2 else '',zorder=3)
        # Create green Bars
        l7 = list((dico_ener[l]['Alkaline electrolysis']+ dico_ener[l]['PEM electrolysis']) / 1000)
        ax.bar(x + width/2, l7, width, color=col(8),label="AEL grid feed" if k == 2 else '',zorder=2)
        # Create Local renewables bars
        l9 = list(dico_ener[l]['feedRE'] / 1000)
        ax.bar(x + width/2, l9, width,color=col(9),label="AEL local feed" if k == 2 else '',zorder=3)

    ax[0].set_ylabel('H$_2$ production (TWh/an)')
    for k,l in enumerate(L):
        ax.set_title(scenarioNames[k])
        ax.set_xticks(x)
        ax.set_xticklabels(['2035', '2045', '2055'])# ,'2060'])
    # ay.set_xticks(x)
    # ay.set_xticklabels(['2030', '2040', '2050'])  # ,'2060'])
    # ay.set_ylabel('kgCO2/kgH2')
    # ay.set_title('Carbon content')
    # Shrink current axis by 20%
    box = ax[0].get_position()
    ax[0].set_position([box.x0, box.y0, box.width * 0.9, box.height])
    box = ax[1].get_position()
    ax[1].set_position([box.x0-0.05, box.y0, box.width * 0.9, box.height])
    box = ax[2].get_position()
    ax[2].set_position([box.x0-0.1, box.y0, box.width * 0.9, box.height])
    # Put a legend to the right of the current axis
    ax[2].legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # box = ay.get_position()
    # ay.set_position([box.x0, box.y0, box.width * 0.815, box.height*0.8])
    # Put a legend to the right of the current axis
    # ay.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputPath + '/Comparison energy.png')
    plt.show()

    return

def plot_total_co2_emissions_and_costs(dico_costs, dico_ener,labels, legend_title=None, outputPath='data/output/'):

    col = plt.cm.tab20c
    colBis = plt.cm.tab20b

    dico_color={'scenario1':(col,8),'scenario2':(colBis,16),'scenario3':(col,0),'scenario4':(col,4)}
    dico_mark= {'scenario1':'d', 'scenario2':'s', 'scenario3':'^','scenario4':'o'}

    colNumber=[]
    markNumber=[]
    variable=[]
    n=0
    for l,s in enumerate(list(dico_costs.keys())):
        for var in list(dico_color.keys()):
            if var == s:
                variable.append(var)
                if variable[l-1]==variable[l]:
                    n=n+1
                else :
                    n=0
                colNumber.append((dico_color[var][0],dico_color[var][1]+n))
                markNumber.append(dico_mark[var])

    carbonCumul = {}
    horizonMean={}

    for s in list(dico_costs.keys()):

        horizonMean[s]=dico_ener[s]['costs']
        carbonCumul[s]=dico_ener[s]['total_carbon']

    fig, ax = plt.subplots(figsize=(7,4))
    for k,s in enumerate(list(dico_costs.keys())):
        ax.plot(carbonCumul[s]/1e6,horizonMean[s], linestyle='',marker=markNumber[k],markersize=12, label=labels[k], color=colNumber[k][0](colNumber[k][1]),zorder=2)

    ax.set_ylabel('Levelised cost of hydrogen (€/kgH$_2$)')
    ax.set_xlabel('$CO_2$ emissions (ktCO$_2$/yr)')
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0+0.05, box.width * 0.6, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
    plt.grid(axis='y',alpha=0.5, zorder=1)

    plt.savefig(outputPath+'/Cumul carbon and costs.png')
    plt.show()

    return

def plot_compare_capacity(dico,outputPath='data/output/ISGT/'):

    fig, ax = plt.subplots(figsize=(6,4))
    width= 0.40
    labels=list(dico.keys())
    x = np.arange(len(labels))
    col = plt.cm.tab20c

    # Create green Bars
    l7=[dico[s]['Alkaline electrolysis'].loc[2030] for s in labels]
    ax.bar(x + width/2,l7,width, color=col(9),label="Water electrolysis",zorder=2)

    # Create red bar
    l8=[dico[s]['Solar'].loc[2030] for s in labels]
    ax.bar(x -width/2 ,l8,width, color=col(5),label="Solar direct connection",zorder=2)
    # Create light bar
    l9=[dico[s]['SolarPPA'].loc[2030] for s in labels]
    ax.bar(x -width/2,l9,width,bottom=l8, color=col(6),label="Solar via the grid",zorder=2)
    # Create purple bar
    l10=[dico[s]['WindOnShore'].loc[2030] for s in labels]
    ax.bar(x-width/2,l10,width,  bottom=[i+j for i,j in zip(l8,l9)],color=col(13),label="Wind direct connection",zorder=2)
    # Create light purple bar
    l11=[dico[s]['WindOnShorePPA'].loc[2030] for s in labels]
    ax.bar(x-width/2,l11,width,  bottom=[i+j+k for i,j,k in zip(l8,l9,l10)],color=col(14),label="Wind via the grid",zorder=2)

    #add Load factor electrolysis

    for i in x:
        ax.text(x[i] + width / 2, l7[i] / 2 , [str(round(dico[s]['loadFac_elec'].loc[2030] * 100)) + '%' for s in list(dico.keys())][i], ha='center')

    ax.set_ylim([0,max(i+j+k+l for i,j,k,l in zip(l8,l9,l10,l11))+100])
    ax.grid(axis='y',alpha=0.5,zorder=1)
    ax.set_ylabel('Installed capacity (MW)')
    # ax.set_title("Evolution of production assets")
    plt.xticks(x, labels)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.66, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.savefig(outputPath+'/Evolution capa.png',dpi=300)
    plt.show()

    return

def plot_sensibility_costs(df1,df2,costsS1,costsS2,outputPath='data/output/ISGT/'):

    fig, ax = plt.subplots(figsize=(6.2,3))
    width= 0.40
    labels=['d=10km','d=50km','d=150km','d=250km','d=500km']
    x = np.arange(len(labels))
    col = plt.cm.tab20c

    ax.plot(x, costsS1,'--', color=col(0),label="scenario 1", zorder=2)
    ax.plot(x, costsS2,'--', color=col(4),label="scenario 2", zorder=2)
    ax.plot(x,list(df1.values()), color=col(8),label="scenario 3",zorder=2)
    ax.plot(x, list(df2.values()), color=col(12), label="scenario 4", zorder=2)

    ax.grid(axis='y',alpha=0.5,zorder=1)
    ax.set_ylabel('Average LCOH (€/kgH$_2$)')
    # ax.set_title("Sensibility to distance")
    plt.xticks(x, labels)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.83, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.savefig(outputPath+'/Sensibility distance.png',dpi=300)
    plt.show()

    return

def plot_sensibility_costsT(df1,df2,df3,df4,outputPath='data/output/ISGT/'):

    fig, ax = plt.subplots(figsize=(6.2,3))
    width= 0.40
    labels=['costs x 0.5','costs x 1','costs x 2']
    x = np.arange(len(labels))
    col = plt.cm.tab20c

    ax.plot(x,list(df1.values()),'-s', color=col(0),label="scenario 1",zorder=2)
    ax.plot(x, list(df2.values()),'-s', color=col(4), label="scenario 2", zorder=2)
    ax.plot(x,list(df3.values()),'-s', color=col(8),label="scenario 3",zorder=2)
    ax.plot(x, list(df4.values()),'-s', color=col(12), label="scenario 4", zorder=2)

    ax.grid(axis='y',alpha=0.5,zorder=1)
    ax.set_ylabel('Average LCOH (€/kgH$_2$)')
    # ax.set_title("Sensibility to network taxes")
    plt.xticks(x, labels)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.83, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.savefig(outputPath+'/Sensibility TURPE.png',dpi=300)
    plt.show()

    return

def plot_compare_energy(dico_ener,outputPath='data/output/ISGT/'):

    fig, ax = plt.subplots()

    width = 0.5
    labels = list(dico_ener.keys())
    x = np.arange(len(labels))
    col = plt.cm.tab20c

    # Create green Bars
    l1 = [dico_ener[s]["Alkaline electrolysis"].loc[2030] / 1000 for s in dico_ener.keys()]
    ax.bar(x ,l1, width,color=col(8),label="AEL grid feed" ,zorder=2)

    # Create Local renewables bars
    l2 = [dico_ener[s]["feedRE"].loc[2030] / 1000 for s in dico_ener.keys()]
    ax.bar(x,l2,width,color=col(9),label="AEL local feed" ,zorder=3)

    # Create orange Bars
    l3 = [dico_ener[s]["importsH2"].loc[2030] / 1000 for s in dico_ener.keys()]
    ax.bar(x, l3, width, bottom=l1, color=col(4), label="Imports H2", zorder=2)

    # Add load factors

    place={'AEL local feed':[0]*len(x),'Alkaline electrolysis':l2,'Imports H2':l1}
    dico_fig_L={'Alkaline electrolysis':[i-j for i,j in zip(l1,l2)],'AEL local feed':l2,'Imports H2':l3}

    

    prod_sum=[i+j for i,j in zip(l1,l3)]
  
    load_factors={}
    load_factors['Alkaline electrolysis']=[round((i-j)/k*100) for i,j,k in zip(l1,l2,prod_sum)]
    load_factors['AEL local feed']=[round(i/j*100) for i,j in zip(l2,prod_sum)]
    load_factors['Imports H2']=[round(i/j*100) for i,j in zip(l3,prod_sum)]
    for k in x:
        for tech in load_factors.keys():
            if load_factors[tech][k]>5:
                ax.text(x[k],place[tech][k]+dico_fig_L[tech][k]/2,str(load_factors[tech][k])+'%',ha='center')

    ax.grid(axis="y", alpha=0.5, color=col(19), zorder=1)

    ax.set_ylabel("H$_2$ production  (TWh H$_2$/yr)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)  # ,'2060'])

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.78, box.height])
    box = ax.get_position()
    # get handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # specify order of items in legend
    order = [1, 0, 2]
    # Put a legend to the right of the current axis
    ax.legend(
        [handles[idx] for idx in order],
        [labels[idx] for idx in order],
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )

    plt.savefig(outputPath + "/Comparison energy.png",dpi=300)
    plt.show(block=False)

    return

def plot_sensitivity_energy(dico_ener,outputPath='data/output/ISGT/'):

    fig, ax = plt.subplots()

    width = 0.5
    labels = ['1/2','1','2']*4
    x = np.arange(len(labels))
    col = plt.cm.tab20c

    # Create green Bars
    l1 = [dico_ener[s]["Alkaline electrolysis"].loc[2030] / 1000 for s in dico_ener.keys()]
    ax.bar(x ,l1, width,color=col(8),label="AEL grid feed" ,zorder=2)

    # Create Local renewables bars
    l2 = [dico_ener[s]["feedRE"].loc[2030] / 1000 for s in dico_ener.keys()]
    ax.bar(x,l2,width,color=col(9),label="AEL local feed" ,zorder=3)

    # Create orange Bars
    l3 = [dico_ener[s]["importsH2"].loc[2030] / 1000 for s in dico_ener.keys()]
    ax.bar(x, l3, width, bottom=l1, color=col(4), label="Imports H2", zorder=2)


    # Add vertical lines

    line_list=[(x[2]+[3])/2,(x[5]+[6])/2,(x[8]+[9])/2]

    for k in range(3):
        ax.axvline(line_list[k],color='grey',linestyle='--')

    # # Add load factors

    # place={'AEL local feed':[0]*len(x),'Alkaline electrolysis':l2,'Imports H2':l1}
    # dico_fig_L={'Alkaline electrolysis':[i-j for i,j in zip(l1,l2)],'AEL local feed':l2,'Imports H2':l3}

    prod_sum=[i+j for i,j in zip(l1,l3)]
  
    # load_factors={}
    # load_factors['Alkaline electrolysis']=[round((i-j)/k*100) for i,j,k in zip(l1,l2,prod_sum)]
    # load_factors['AEL local feed']=[round(i/j*100) for i,j in zip(l2,prod_sum)]
    # load_factors['Imports H2']=[round(i/j*100) for i,j in zip(l3,prod_sum)]
    # for k in x:
    #     for tech in load_factors.keys():
    #         if load_factors[tech][k]>5:
    #             ax.text(x[k],place[tech][k]+dico_fig_L[tech][k]/2,str(load_factors[tech][k])+'%',ha='center')

    ax.grid(axis="y", alpha=0.5, color=col(19), zorder=1)
    # ax.set_ylim(prod_sum[0]+1)

    ax.set_ylabel("H$_2$ production  (TWh H$_2$/yr)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.78, box.height])
    box = ax.get_position()
    # get handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # specify order of items in legend
    order = [1, 0, 2]
    # Put a legend to the right of the current axis
    ax.legend(
        [handles[idx] for idx in order],
        [labels[idx] for idx in order],
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )

    plt.savefig(outputPath + "/Sensitivity energy.png",dpi=300)
    plt.show(block=True)

    return
