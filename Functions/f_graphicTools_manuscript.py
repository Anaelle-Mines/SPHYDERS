import os

os.sys.path.append(r"../")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd


def plot_capacity(area, timeStep, outputFolder="../data/output/", LoadFac=False):
    v_list = [
        "transInvest_Dvar",
        "capacity_Pvar",
        "energy_Pvar",
        "power_Dvar",
        "storageConsumption_Pvar",
        "storageIn_Pvar",
        "storageOut_Pvar",
        "stockLevel_Pvar",
        "importation_Dvar",
        "carbon_Pvar",
        "powerCosts_Pvar",
        "capacityCosts_Pvar",
        "importCosts_Pvar",
        "storageCosts_Pvar",
        "turpeCosts_Pvar",
        "carbonCosts_Pvar",
    ]
    Variables = {
        v: pd.read_csv(outputFolder + "/" + v + ".csv").drop(columns="Unnamed: 0") for v in v_list
    }

    YEAR = Variables["power_Dvar"].set_index("YEAR_op").index.unique().values
    TECHNO = Variables["power_Dvar"].set_index("TECHNOLOGIES").index.unique().values
    TIMESTAMP = Variables["power_Dvar"].set_index("TIMESTAMP").index.unique().values
    YEAR.sort()

    # region Tracé mix prod H2 et EnR
    df = Variables["capacity_Pvar"].set_index('AREA').loc[area]

    renameDict={
                "electrolysis_AEL": "Alkaline electrolysis",
                "electrolysis_PEMEL": "PEM electrolysis",
                "SMR": "SMR w/o CCUS",
                "SMR + CCS1": "SMR + CCUS 50%",
                "SMR + CCS2": "SMR + CCUS 90%",
                "SMR_elec": "eSMR w/o CCUS",
                "SMR_elecCCS1": "eSMR + CCUS 50%",
                "cracking": "Methane cracking",
                "WindOnShore": "WindOnShore",
                "WindOffShore_flot": "WindOffShore_flot",
                "Solar": "Solar",
                "curtailment": "curtailment"
            }

    df = (
        df.pivot(columns="TECHNOLOGIES", values="capacity_Pvar", index="YEAR_op")
        .rename(
            columns=renameDict
        )
        .fillna(0)
    )


    listTech= ["WindOnShore","WindOffShore_flot","Solar","SMR","SMR + CCS1","SMR + CCS2","electrolysis_PEMEL","electrolysis_AEL","curtailment"]
    for tech in listTech:
        if tech not in TECHNO:
            df[renameDict[tech]]=0

    list_renamed=[renameDict[tech] for tech in listTech]
    capa = pd.melt(df.reset_index(),id_vars="YEAR_op",value_vars=list_renamed,value_name='capacity_Pvar').set_index(['YEAR_op','TECHNOLOGIES'])

    power = (
        Variables["power_Dvar"]
        .set_index("AREA")
        .loc[area]
        .groupby(["YEAR_op", "TECHNOLOGIES"])
        .sum()
        .drop(columns="TIMESTAMP")
        .rename(index=renameDict,level=1)

    )

    power.loc[power["power_Dvar"] < 1e-6] = 0

    # LoadFactors

    df_factor=(power["power_Dvar"] * timeStep / (capa["capacity_Pvar"] * 8760)).reset_index().pivot(index="YEAR_op", columns="TECHNOLOGIES", values=0).fillna(0)
    for tech in listTech:
        if tech not in TECHNO:
            df_factor[tech]=0


    EnR_loadFactor = {
        y: df_factor.loc[y, ["WindOnShore", "Solar", "WindOffShore_flot"]]
        for y in YEAR}

    H2_loadFactor = {
        y: df_factor.loc[y,["PEM electrolysis","Alkaline electrolysis","SMR w/o CCUS","SMR + CCUS 50%","SMR + CCUS 90%",]]
        for y in YEAR}

    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(6.2, 4))
    width = 0.40
    labels = list(df.index)
    x = np.arange(len(labels))
    col = plt.cm.tab20c

    # Create dark grey Bar
    l1 = list(df["SMR w/o CCUS"])
    ax[0].bar(x - width / 2, l1, width, color=col(17), label="SMR w/o CCUS", zorder=2)
    # Create dark bleu Bar
    l2 = list(df["SMR + CCUS 50%"])
    ax[0].bar(x - width / 2, l2, width, bottom=l1, color=col(0), label="SMR + CCUS 50%", zorder=2)
    # Create turquoise bleu Bar
    l3 = list(df["SMR + CCUS 90%"])
    ax[0].bar(
        x - width / 2,
        l3,
        width,
        bottom=[i + j for i, j in zip(l1, l2)],
        color=col(1),
        label="SMR + CCUS 90%",
        zorder=2,
    )
    #Create green Bars
    l7 = list(df["Alkaline electrolysis"] + df["PEM electrolysis"])
    ax[0].bar(x + width / 2, l7, width, color=col(9), label="Water electrolysis", zorder=2)

    # Create red bar
    l8 = list(df["Solar"])
    ax[1].bar(x, l8, width, color=col(5), label="Solar", zorder=2)
    # Create violet bar
    l9 = list(df["WindOnShore"])
    ax[1].bar(x, l9, width, bottom=l8, color=col(13), label="Onshore wind", zorder=2)
    # Create pink bar
    l10 = list(df["WindOffShore_flot"])
    ax[1].bar(
        x,
        l10,
        width,
        bottom=[i + j for i, j in zip(l8, l9)],
        color=col(14),
        label="Offshore wind",
        zorder=2,
    )


    # add Load factors
    if LoadFac == True:
        for i, y in enumerate(YEAR):
            if capa.loc[(y, renameDict["electrolysis_AEL"]), "capacity_Pvar"] > 50:
                ax[0].text(
                    (x + width / 2)[i],
                    l7[i] / 2,
                    str(round(H2_loadFactor[y][renameDict["electrolysis_AEL"]] * 100)) + "%",
                    ha="center",
                )
            if capa.loc[(y, renameDict["SMR"]), "capacity_Pvar"] > 50:
                ax[0].text(
                    (x - width / 2)[i],
                    l1[i] / 2,
                    str(round(H2_loadFactor[y][renameDict["SMR"]] * 100)) + "%",
                    ha="center",
                )
            if capa.loc[(y, renameDict["SMR + CCS1"]), "capacity_Pvar"] > 50:
                ax[0].text(
                    (x - width / 2)[i],
                    l1[i] + l2[i] / 2,
                    str(round(H2_loadFactor[y][renameDict["SMR + CCS1"]] * 100)) + "%",
                    ha="center",
                )
            if capa.loc[(y, renameDict["SMR + CCS2"]), "capacity_Pvar"] > 10:
                ax[1].text(
                    (x)[i],
                    l1[i] + l2[i] + l3[i]/ 2,
                    str(round(H2_loadFactor[y][renameDict["SMR + CCS2"]] * 100)) + "%",
                    ha="center",
                )
            if capa.loc[(y, "Solar"), "capacity_Pvar"] > 50:
                ax[1].text(
                    (x)[i],
                    l8[i] / 2,
                    str(round(EnR_loadFactor[y]["Solar"] * 100)) + "%",
                    ha="center",
                )
            if capa.loc[(y, "WindOnShore"), "capacity_Pvar"] > 50:
                ax[1].text(
                    (x)[i],
                    l8[i] + l9[i] / 2,
                    str(round(EnR_loadFactor[y]["WindOnShore"] * 100)) + "%",
                    ha="center",
                )
            if capa.loc[(y, "WindOffShore_flot"), "capacity_Pvar"] > 50:
                ax[1].text(
                    (x)[i],
                    l8[i] + l9[i] + l10[i] / 2,
                    str(round(EnR_loadFactor[y]["WindOffShore_flot"] * 100)) + "%",
                    ha="center",
                )



    ax[0].set_ylim(
        [
            0,
            max(max([i + j + k for i, j, k in zip(l1, l2, l3)]), max(l7))
            + 200,
        ]
    )
    ax[0].grid(axis="y", alpha=0.5, zorder=1)
    ax[1].set_ylim([0, max([i + j + k for i, j, k in zip(l8, l9, l10)]) + 100])
    ax[1].grid(axis="y", alpha=0.5, zorder=1)
    # ax[2].grid(axis='y', alpha=0.5,zorder=1)
    ax[0].set_ylabel("Installed capacity (MW)")
    ax[1].set_ylabel("Installed capacity (MW)")
    # ax[2].set_ylabel('Load factors (%)')
    ax[0].set_title("Evolution of H2 production assets")
    ax[1].set_title("Evolution of local RE assets")
    # ax[2].set_title("Evolution of load factors")
    plt.xticks(x, ["2010-2020", "2020-2030", "2030-2040", "2040-2050"])
    # Shrink current axis by 20%
    box = ax[0].get_position()
    ax[0].set_position([box.x0, box.y0, box.width * 0.73, box.height * 0.95])
    # get handles and labels
    handles, labels = ax[0].get_legend_handles_labels()
    # specify order of items in legend
    order = [3, 2, 1, 0]
    # Put a legend to the right of the current axis
    ax[0].legend(
        [handles[idx] for idx in order],
        [labels[idx] for idx in order],
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )
    # Shrink current axis by 20%
    box = ax[1].get_position()
    ax[1].set_position([box.x0, box.y0, box.width * 0.73, box.height * 0.95])
    # get handles and labels
    handles, labels = ax[1].get_legend_handles_labels()
    # specify order of items in legend
    order = [2, 1, 0]
    # Put a legend to the right of the current axis
    ax[1].legend(
        [handles[idx] for idx in order],
        [labels[idx] for idx in order],
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )

    plt.savefig(outputFolder + "/Capacity.png",dpi=300)
    plt.show(block=True)
    plt.close()

    # def monthly_average(df):
    #     df['month'] = df.index // 730 + 1
    #     df.loc[8760,'month']=12
    #     return df.groupby('month').mean()

    # loadFactors_df=power.copy().pivot(index=['YEAR_op','TIMESTAMP'],columns='TECHNOLOGIES',values='power_Dvar')
    # for y in YEAR :
    #     for tech in TECHNO:
    #         loadFactors_df.loc[y,slice(None)][tech]=(power.set_index(['YEAR_op','TIMESTAMP','TECHNOLOGIES']).loc[(y,slice(None),tech),'power_Dvar']/capa.loc[(y,tech),'capacity_Pvar']).reset_index().drop(columns=['TECHNOLOGIES','YEAR_op']).set_index('TIMESTAMP')['power_Dvar']

    # month=np.unique(TIMESTAMP//730+1)[:-1]

    # fig, ax = plt.subplots()

    # for k,y in enumerate(YEAR):
    #     #Create electrolysis graph
    #     l1=list(monthly_average(loadFactors_df.loc[(y,slice(None))])['electrolysis_AEL']*100)
    #     plt.plot(month,l1,color=col(8+k),label=y,zorder=2)

    # plt.grid(axis='y',alpha=0.5,zorder=1)
    # plt.ylabel('Load factor (%)')
    # plt.xlabel('Months')
    # plt.xticks(month,['January','February','March','April','May','June','July','August','September','October','November','December'],rotation=45)
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0+0.1, box.width * 0.90, box.height])
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.savefig(outputFolder+'/elec_LoadFactor.png')
    # plt.show(block=False)

    return df


def plot_energy(area, timeStep, outputFolder="../data/output/"):
    v_list = [
        "capacityInvest_Dvar",
        "transInvest_Dvar",
        "capacity_Pvar",
        "capacityDel_Pvar",
        "capacityDem_Dvar",
        "energy_Pvar",
        "power_Dvar",
        "storageConsumption_Pvar",
        "storageIn_Pvar",
        "storageOut_Pvar",
        "stockLevel_Pvar",
        "importation_Dvar",
        "Cmax_Pvar",
        "carbon_Pvar",
        "powerCosts_Pvar",
        "capacityCosts_Pvar",
        "importCosts_Pvar",
        "storageCosts_Pvar",
        "turpeCosts_Pvar",
        "Pmax_Pvar",
        "max_PS_Dvar",
        "carbonCosts_Pvar",
        "exportation_Dvar",
    ]
    Variables = {
        v: pd.read_csv(outputFolder + "/" + v + ".csv").drop(columns="Unnamed: 0") for v in v_list
    }

    def t_to_TWh(x):
        y=x*8760*33.33/1e6
        return y

    def t_to_kg(x):
        y=x/(8760*33.33)*1e6
        return y

    YEAR = Variables["power_Dvar"].set_index("YEAR_op").index.unique().values
    YEAR.sort()
    TECHNO=Variables["power_Dvar"].set_index("TECHNOLOGIES").index.unique().values

    capa = Variables["capacity_Pvar"].set_index("AREA").loc[area]
    power = Variables["power_Dvar"].set_index("AREA").loc[area]
    export = Variables["exportation_Dvar"].set_index("AREA").loc[area]

    renameDict={
                "electrolysis_AEL": "Alkaline electrolysis",
                "electrolysis_PEMEL": "PEM electrolysis",
                "SMR": "SMR w/o CCUS",
                "SMR + CCS1": "SMR + CCUS 50%",
                "SMR + CCS2": "SMR + CCUS 90%",
                "SMR_elec": "eSMR w/o CCUS",
                "SMR_elecCCS1": "eSMR + CCUS 50%",
                "cracking": "Methane cracking",
            }

    df = power.groupby(["YEAR_op", "TECHNOLOGIES"]).sum().drop(columns="TIMESTAMP").reset_index()
    df = (
        df.pivot(columns="TECHNOLOGIES", values="power_Dvar", index="YEAR_op")
        .rename(columns=renameDict)
        .fillna(0)
    )

    listTech= ["WindOnShore","WindOffShore_flot","Solar","SMR","SMR + CCS1","SMR + CCS2","electrolysis_PEMEL","electrolysis_AEL","curtailment"]
    for tech in listTech:
        if tech not in TECHNO:
            df[renameDict[tech]]=0


    df = df * timeStep / 1000000

    df_renewables = (
        power.pivot(index=["YEAR_op", "TIMESTAMP"], columns="TECHNOLOGIES", values="power_Dvar")[
            ["WindOnShore", "WindOffShore_flot", "Solar"]
        ]
        .reset_index()
        .groupby("YEAR_op")
        .sum()
        .drop(columns="TIMESTAMP")
        .sum(axis=1)
    )
    df_export = (
        export.groupby(["YEAR_op", "RESOURCES"])
        .sum()
        .loc[(slice(None), "electricity"), "exportation_Dvar"]
        .reset_index()
        .drop(columns="RESOURCES")
        .set_index("YEAR_op")
    )
    df_feedRE = (df_renewables - df_export["exportation_Dvar"]) / 1.54 / 1000000  #

    df_biogas = (
        Variables["importation_Dvar"]
        .groupby(["YEAR_op", "RESOURCES"])
        .sum()
        .loc[(slice(None), "gazBio"), "importation_Dvar"]
        .reset_index()
        .set_index("YEAR_op")
        .drop(columns="RESOURCES")
    )
    for y in YEAR:
        fugitives = (
            0.03 * (1 - (y - YEAR[0]) / (2050 - YEAR[0])) * df_biogas.loc[y]["importation_Dvar"]
        )
        temp = df_biogas.loc[y]["importation_Dvar"] - fugitives
        if temp / 1.28 / 1000000 < df.loc[y]["SMR w/o CCUS"]:
            df_biogas.loc[y]["importation_Dvar"] = temp / 1.28 / 1000000
        else:
            temp2 = temp - df.loc[y]["SMR w/o CCUS"] * 1.28 * 1000000
            if temp2 / 1.32 / 1000000 < df.loc[y]["SMR + CCUS 50%"]:
                df_biogas.loc[y]["importation_Dvar"] = (
                    df.loc[y]["SMR w/o CCUS"] + temp2 / 1.32 / 1000000
                )
            else:
                temp3 = (
                    temp
                    - df.loc[y]["SMR w/o CCUS"] * 1.28 * 1000000
                    - df.loc[y]["SMR + CCUS 50%"] * 1.32 * 1000000
                )
                if temp3 / 1.45 / 1000000 < df.loc[y]["SMR + CCUS 90%"]:
                    df_biogas.loc[y]["importation_Dvar"] = (
                        df.loc[y]["SMR w/o CCUS"]
                        + df.loc[y]["SMR + CCUS 50%"]
                        + temp3 / 1.45 / 1000000
                    )
                else:
                    df_biogas.loc[y]["importation_Dvar"] = (
                        df.loc[y]["SMR w/o CCUS"]
                        + df.loc[y]["SMR + CCUS 50%"]
                        + df.loc[y]["SMR + CCUS 90%"]
                    )

    fig, ax = plt.subplots(figsize=(6, 4))
    width = 0.35
    col = plt.cm.tab20c
    labels = list(df.index)
    x = np.arange(len(labels))

    # Create dark grey Bar
    l1 = list(df["SMR w/o CCUS"])
    ax.bar(x - width / 2, l1, width, color=col(17), label="SMR w/o CCUS", zorder=2)
    # Create dark bleu Bar
    l2 = list(df["SMR + CCUS 50%"])
    ax.bar(x - width / 2, l2, width, bottom=l1, color=col(0), label="SMR + CCUS 50%", zorder=2)
    # Create turquoise bleu Bar
    l3 = list(df["SMR + CCUS 90%"])
    ax.bar(
        x - width / 2,
        l3,
        width,
        bottom=[i + j for i, j in zip(l1, l2)],
        color=col(1),
        label="SMR + CCUS 90%",
        zorder=2,
    )
    # Create biogas Bars
    l8 = list(df_biogas["importation_Dvar"])
    plt.rcParams["hatch.linewidth"] = 8
    plt.rcParams["hatch.color"] = col(3)
    ax.bar(
        x - width / 2,
        l8,
        width,
        color="none",
        hatch="/",
        edgecolor=col(3),
        linewidth=0.5,
        label="Biomethane feed",
        alpha=0.8,
        zorder=3,
    )
    # Create light green Bars
    l7 = list(df["Alkaline electrolysis"] + df["PEM electrolysis"])
    ax.bar(x + width / 2, l7, width, color=col(8), label="AEL grid feed", zorder=2)
    # Create dark green bar
    l9 = list(df_feedRE)
    ax.bar(x + width / 2, l9, width, color=col(9), label="AEL local feed", zorder=3)

    secax = ax.secondary_yaxis("right", functions=(t_to_kg,t_to_TWh))
    secax.set_ylabel("(kg/h)")

    plt.grid(axis="y", alpha=0.5, zorder=1)
    ax.set_ylabel("H2 production (TWh/yr)")
    # ax.set_title("Use of assets")
    plt.xticks(x, ["2020-2030", "2030-2040", "2040-2050", "2050-2060"])
    m = max(max(l7), max([l1[i] + l2[i] + l3[i] for i in np.arange(len(l1))]))
    ax.set_ylim([0, int(m) + 0.5])
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.72, box.height])
    # get handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # specify order of items in legend
    order = [4, 5, 2, 1, 0, 3]
    # Put a legend to the right of the current axi
    ax.legend(
        [handles[idx] for idx in order],
        [labels[idx] for idx in order],
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )
    plt.savefig(outputFolder + "/Energy.png",dpi=300)
    plt.show(block=False)
    plt.close()

    # return df


def plot_energy_new(area, timeStep, outputFolder="../data/output/"):
    v_list = [
        "capacity_Pvar",
        "energy_Pvar",
        "power_Dvar",
        "importation_Dvar",
        "Cmax_Pvar",
        "carbon_Pvar",
        "powerCosts_Pvar",
        "capacityCosts_Pvar",
        "importCosts_Pvar",
        "storageCosts_Pvar",
        "turpeCosts_Pvar",
        "carbonCosts_Pvar",
        "exportation_Dvar"
    ]

    def t_to_TWh(x):
        y=x*8760*33.33/1e6
        return y

    def TWh_to_t(x):
        y=x/(8760*33.33)*1e6
        return y

    Variables = {
        v: pd.read_csv(outputFolder + "/" + v + ".csv").drop(columns="Unnamed: 0") for v in v_list
    }

    YEAR = Variables["power_Dvar"].set_index("YEAR_op").index.unique().values
    YEAR.sort()
    TECHNO=Variables["power_Dvar"].set_index("TECHNOLOGIES").index.unique().values

    capa = Variables["capacity_Pvar"].set_index("AREA").loc[area]
    power = Variables["power_Dvar"].set_index("AREA").loc[area]
    imports = Variables['importation_Dvar'].set_index(["AREA","RESOURCES"]).loc[(area,'hydrogen')]
    export = Variables["exportation_Dvar"].set_index("AREA").loc[area]

    renameDict={
                "electrolysis_AEL": "Alkaline electrolysis",
                "electrolysis_PEMEL": "PEM electrolysis",
                "SMR": "SMR w/o CCUS",
                "SMR + CCS1": "SMR + CCUS 50%",
                "SMR + CCS2": "SMR + CCUS 90%",
                "SMR_elec": "eSMR w/o CCUS",
                "SMR_elecCCS1": "eSMR + CCUS 50%",
                "cracking": "Methane cracking",
                "Imports H2": "Imports H2"
            }

    df = power.groupby(["YEAR_op", "TECHNOLOGIES"]).sum().drop(columns="TIMESTAMP").reset_index()
    df = (
        df.pivot(columns="TECHNOLOGIES", values="power_Dvar", index="YEAR_op")
        .rename(columns=renameDict)
        .fillna(0)
    )

    listTech= ["WindOnShore","WindOffShore_flot","Solar","SMR","SMR + CCS1","SMR + CCS2","electrolysis_PEMEL","electrolysis_AEL","curtailment",'Imports H2']
    for tech in listTech:
        if tech not in TECHNO:
            df[renameDict[tech]]=0


    df = df * timeStep / 1000000

    df['Imports H2']=imports.groupby(['YEAR_op']).sum().drop(columns='TIMESTAMP')['importation_Dvar']/ 1000000

    df_renewables = (
        power.pivot(index=["YEAR_op", "TIMESTAMP"], columns="TECHNOLOGIES", values="power_Dvar")[
            ["WindOnShore", "WindOffShore_flot", "Solar"]
        ]
        .reset_index()
        .groupby("YEAR_op")
        .sum()
        .drop(columns="TIMESTAMP")
        .sum(axis=1)
    )
    df_export = (
        export.groupby(["YEAR_op", "RESOURCES"])
        .sum()
        .loc[(slice(None), "electricity"), "exportation_Dvar"]
        .reset_index()
        .drop(columns="RESOURCES")
        .set_index("YEAR_op")
    )
    df_feedRE = (df_renewables - df_export["exportation_Dvar"]) / 1.54 / 1000000  #

    df_biogas = (
        Variables["importation_Dvar"]
        .groupby(["YEAR_op", "RESOURCES"])
        .sum()
        .loc[(slice(None), "gazBio"), "importation_Dvar"]
        .reset_index()
        .set_index("YEAR_op")
        .drop(columns="RESOURCES")
    )
    for y in YEAR:
        fugitives = (
            0.03 * (1 - (y - YEAR[0]) / (2050 - YEAR[0])) * df_biogas.loc[y]["importation_Dvar"]
        )
        temp = df_biogas.loc[y]["importation_Dvar"] - fugitives
        if temp / 1.28 / 1000000 < df.loc[y]["SMR w/o CCUS"]:
            df_biogas.loc[y]["importation_Dvar"] = temp / 1.28 / 1000000
        else:
            temp2 = temp - df.loc[y]["SMR w/o CCUS"] * 1.28 * 1000000
            if temp2 / 1.32 / 1000000 < df.loc[y]["SMR + CCUS 50%"]:
                df_biogas.loc[y]["importation_Dvar"] = (
                    df.loc[y]["SMR w/o CCUS"] + temp2 / 1.32 / 1000000
                )
            else:
                temp3 = (
                    temp
                    - df.loc[y]["SMR w/o CCUS"] * 1.28 * 1000000
                    - df.loc[y]["SMR + CCUS 50%"] * 1.32 * 1000000
                )
                if temp3 / 1.45 / 1000000 < df.loc[y]["SMR + CCUS 90%"]:
                    df_biogas.loc[y]["importation_Dvar"] = (
                        df.loc[y]["SMR w/o CCUS"]
                        + df.loc[y]["SMR + CCUS 50%"]
                        + temp3 / 1.45 / 1000000
                    )
                else:
                    df_biogas.loc[y]["importation_Dvar"] = (
                        df.loc[y]["SMR w/o CCUS"]
                        + df.loc[y]["SMR + CCUS 50%"]
                        + df.loc[y]["SMR + CCUS 90%"]
                    )

    fig, ax = plt.subplots(figsize=(6.5, 4))
    width = 0.5
    col = plt.cm.tab20c
    labels = list(df.index)
    x = np.arange(len(labels))

    # Create dark grey Bar
    l1 = list(df["SMR w/o CCUS"])
    ax.bar(x, l1, width, color=col(17), label="SMR w/o CCUS", zorder=2)
    # Create dark bleu Bar
    l2 = list(df["SMR + CCUS 50%"])
    ax.bar(x, l2, width, bottom=l1, color=col(0), label="SMR + CCUS 50%", zorder=2)
    # Create turquoise bleu Bar
    l3 = list(df["SMR + CCUS 90%"])
    ax.bar(
        x,
        l3,
        width,
        bottom=[i + j for i, j in zip(l1, l2)],
        color=col(1),
        label="SMR + CCUS 90%",
        zorder=2,
    )
    # Create biogas Bars
    l8 = list(df_biogas["importation_Dvar"])
    plt.rcParams["hatch.linewidth"] = 8
    plt.rcParams["hatch.color"] = col(3)
    ax.bar(
        x,
        l8,
        width,
        color="none",
        hatch="/",
        edgecolor=col(3),
        linewidth=0.5,
        label="Biomethane feed",
        alpha=0.8,
        zorder=3,
    )
    # Create light green Bars
    l7 = list(df["Alkaline electrolysis"] + df["PEM electrolysis"])
    ax.bar(x, l7, width, bottom=[i+j+k for i,j,k in zip(l1,l2,l3)], color=col(8), label="AEL grid feed", zorder=2)
    # Create dark green bar
    l9 = list(df_feedRE)
    ax.bar(x, l9, width,bottom=[i+j+k for i,j,k in zip(l1,l2,l3)], color=col(9), label="AEL local feed", zorder=3)

    # Create orange Bars
    l9 = list(df["Imports H2"])
    ax.bar(x, l9, width, bottom=[i+j+k+l for i,j,k,l in zip(l1,l2,l3,l7)], color=col(4), label="Imports H2", zorder=2)

    prod_sum=[a+b+c+d+e for a,b,c,d,e in zip(l1,l2,l3,l7,l9)]
    
    load_factors={}
    load_factors['SMR w/o CCUS']=[round(i/j*100) for i,j in zip(l1,prod_sum)]
    load_factors['SMR + CCUS 50%']=[round(i/j*100) for i,j in zip(l2,prod_sum)]
    load_factors['SMR + CCUS 90%']=[round(i/j*100) for i,j in zip(l3,prod_sum)]
    load_factors['Alkaline electrolysis']=[round(i/j*100) for i,j in zip(l7,prod_sum)]
    load_factors['Imports H2']=[round(i/j*100) for i,j in zip(l9,prod_sum)]

    place={'SMR w/o CCUS':[0]*len(YEAR),'SMR + CCUS 50%':l1,'SMR + CCUS 90%':[k+l for k,l in zip(l1,l2)],
    'Alkaline electrolysis':[k+l+m for k,l,m in zip(l1,l2,l3)],'Imports H2':[k+l+m+n for k,l,m,n in zip(l1,l2,l3,l7)]}
    L={'SMR w/o CCUS':l1,'SMR + CCUS 50%':l2,'SMR + CCUS 90%':l3,'Alkaline electrolysis':l7,'Imports H2':l9}


    for y in range(len(YEAR)):   
        for tech in load_factors.keys():
            if load_factors[tech][y]>10:
                ax.text(x[y],place[tech][y]+L[tech][y]/2,str(load_factors[tech][y])+'%',ha='center')

    secax = ax.secondary_yaxis("right", functions=(TWh_to_t,t_to_TWh))
    secax.set_ylabel("(t H$_2$/h)")

    plt.grid(axis="y", alpha=0.5, zorder=1)
    ax.set_ylabel("H$_2$ production  (TWh H$_2$/yr)")
    # ax.set_title("Use of assets")
    plt.xticks(x, ["2020-2030", "2030-2040", "2040-2050", "2050-2060"])
    m =max([l1[i] + l2[i] + l3[i] + l7[i] + l9[i] for i in np.arange(len(l1))])
    print(m)
    ax.set_ylim([0, int(m) + 1])
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.65, box.height])
    # get handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # specify order of items in legend
    order = [6,4, 5, 2, 1, 0, 3]
    # Put a legend to the right of the current axi
    ax.legend(
        [handles[idx] for idx in order],
        [labels[idx] for idx in order],
        loc="center left",
        bbox_to_anchor=(1.15, 0.5),
    )
    plt.savefig(outputFolder + "/Energy.png",dpi=300)
    plt.show(block=True)
    plt.close()

    # return df


def plot_costs_detailed(df, outputFolder="../data/output/", comparaison=False):
    YEAR = list(df[list(df.keys())[0]].index.get_level_values('YEAR'))
    YEAR.sort()
    dy = YEAR[1] - YEAR[0]
    y0 = YEAR[0] - dy

    fig, ax = plt.subplots(figsize=(7, 4.3))
    width = 0.25
    labels = list(df["SMR"].index)
    x = np.arange(len(labels))
    col = plt.cm.tab20c
    colBis = plt.cm.tab20b

    parameters = {
        "axes.labelsize": 12,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "figure.titlesize": 15,
        "legend.fontsize": 12,
    }
    plt.rcParams.update(parameters)

    B = list(df.keys())
    B_nb = len(B)
    if B_nb % 2 > 0:
        n = B_nb // 2
        X = np.sort(
            [-i * (width + 0.05) for i in np.arange(1, n + 1)]
            + [0]
            + [i * (width + 0.05) for i in np.arange(1, n + 1)]
        )
    else:
        n = B_nb / 2
        X = np.sort(
            [-(width / 2 + 0.025) - i * (width + 0.05) for i in np.arange(n)]
            + [(width / 2 + 0.025) + i * (width + 0.05) for i in np.arange(n)]
        )
        M = [X[i : i + 2].mean() for i in np.arange(0, int(n + 1), 2)]

    meanCosts = []
    horizonMean = []
    c = 0
    if comparaison == False:
        meanCosts = sum(
            df[k][
                [
                    "powerCosts",
                    "capacityCosts",
                    "capexElec",
                    "importElec",
                    "importGas",
                    "storageElec",
                    "storageH2",
                    "carbon",
                    "TURPE",
                    "importsH2"
                ]
            ].sum(axis=1)
            for k in B
        ) / sum((df[k]["Prod"] * 30) for k in B)
        horizonMean = sum(
            df[k][
                [
                    "powerCosts",
                    "capacityCosts",
                    "capexElec",
                    "importElec",
                    "importGas",
                    "storageElec",
                    "storageH2",
                    "carbon",
                    "TURPE",
                    "importsH2"
                ]
            ].sum(axis=1)
            for k in B
        ).sum() / (sum((df[k]["Prod"] * 30) for k in B).sum())
    else:
        if B_nb % 2 > 0:
            meanCosts = sum(
                df[k][
                    [
                        "powerCosts",
                        "capacityCosts",
                        "capexElec",
                        "importElec",
                        "importGas",
                        "storageElec",
                        "storageH2",
                        "carbon",
                        "TURPE",
                        "importsH2"
                    ]
                ].sum(axis=1)
                for k in B[0:2]
            ) / sum((df[k]["Prod"] * 30) for k in B[0:2])
            horizonMean.append(
                sum(
                    df[k][
                        [
                            "powerCosts",
                            "capacityCosts",
                            "capexElec",
                            "importElec",
                            "importGas",
                            "storageElec",
                            "storageH2",
                            "carbon",
                            "TURPE",
                            "importsH2"
                        ]
                    ].sum(axis=1)
                    for k in B[0:2]
                ).sum()
                / (sum((df[k]["Prod"] * 30) for k in B[0:2]).sum())
            )
            horizonMean.append(
                df[B[-1]][
                    [
                        "powerCosts",
                        "capacityCosts",
                        "capexElec",
                        "importElec",
                        "importGas",
                        "storageElec",
                        "storageH2",
                        "carbon",
                        "TURPE",
                        "importsH2"
                    ]
                ]
                .sum(axis=1)
                .sum()
                / (df[B[-1]]["Prod"] * 30).sum()
            )
        else:
            for i in np.arange(0, int(n + 1), 2):
                meanCosts.append(
                    sum(
                        df[k][
                            [
                                "powerCosts",
                                "capacityCosts",
                                "capexElec",
                                "importElec",
                                "importGas",
                                "storageElec",
                                "storageH2",
                                "carbon",
                                "TURPE",
                                "importsH2"
                            ]
                        ].sum(axis=1)
                        for k in B[i : i + 2]
                    )
                    / sum((df[k]["Prod"] * 30) for k in B[i : i + 2])
                )
                horizonMean.append(
                    sum(
                        df[k][
                            [
                                "powerCosts",
                                "capacityCosts",
                                "capexElec",
                                "importElec",
                                "importGas",
                                "storageElec",
                                "storageH2",
                                "carbon",
                                "TURPE",
                                "importsH2"
                            ]
                        ].sum(axis=1)
                        for k in B[i : i + 2]
                    ).sum()
                    / (sum((df[k]["Prod"] * 30) for k in B[i : i + 2]).sum())
                )
                c = c + 1

    # Create light blue Bars
    a = {}
    for i in np.arange(B_nb):
        a[i] = list((df[B[i]]["capacityCosts"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i], a[i], width, color=col(1), label="Fixed Costs" if i == 0 else "", zorder=2
        )

    # Create dark blue Bars
    aa = {}
    for i in np.arange(B_nb):
        aa[i] = list((df[B[i]]["powerCosts"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            aa[i],
            width,
            bottom=a[i],
            color=col(0),
            label="Variable Costs" if i == 0 else "",
            zorder=2,
        )

    # Create brown Bars
    b = {}
    for i in np.arange(B_nb):
        b[i] = list((df[B[i]]["importGas"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            b[i],
            width,
            bottom=[i + j for i, j in zip(a[i], aa[i])],
            color=colBis(9),
            label="Gas" if i == 0 else "",
            zorder=2,
        )

    # Create green Bars
    c = {}
    for i in np.arange(B_nb):
        c[i] = list((df[B[i]]["capexElec"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            c[i],
            width,
            bottom=[i + j + k for i, j, k in zip(a[i], aa[i], b[i])],
            color=col(9),
            label="Local RE capa" if i == 0 else "",
            zorder=2,
        )

    # Create dark red Bars
    d = {}
    for i in np.arange(B_nb):
        d[i] = list((df[B[i]]["importElec"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            d[i],
            width,
            bottom=[i + j + k + l for i, j, k, l in zip(a[i], aa[i], b[i], c[i])],
            color=colBis(14),
            label="Grid electricity" if i == 0 else "",
            zorder=2,
        )

    # Create light red Bars
    e = {}
    for i in np.arange(B_nb):
        e[i] = list((df[B[i]]["TURPE"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            e[i],
            width,
            bottom=[i + j + k + l + m for i, j, k, l, m in zip(a[i], aa[i], b[i], c[i], d[i])],
            color=colBis(15),
            label="Network taxes" if i == 0 else "",
            zorder=2,
        )

    # Create purple Bars
    f = {}
    for i in np.arange(B_nb):
        f[i] = list((df[B[i]]["storageH2"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            f[i],
            width,
            bottom=[
                i + j + k + l + m + n
                for i, j, k, l, m, n in zip(a[i], aa[i], b[i], c[i], d[i], e[i])
            ],
            color=colBis(18),
            label="H2 storage capa" if i == 0 else "",
            zorder=2,
        )

    # Create pink Bars
    g = {}
    for i in np.arange(B_nb):
        g[i] = list((df[B[i]]["storageElec"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            g[i],
            width,
            bottom=[
                i + j + k + l + m + n + o
                for i, j, k, l, m, n, o in zip(a[i], aa[i], b[i], c[i], d[i], e[i], f[i])
            ],
            color=colBis(20),
            label="Elec storage capa" if i == 0 else "",
            zorder=2,
        )

    # Create orange Bars
    h = {}
    for i in np.arange(B_nb):
        h[i] = list((df[B[i]]["importsH2"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            h[i],
            width,
            bottom=[
                i + j + k + l + m + n + o + p
                for i, j, k, l, m, n, o, p in zip(a[i], aa[i], b[i], c[i], d[i], e[i], f[i], g[i])
            ],
            color=col(6),
            label="Importation" if i == 0 else "",
            zorder=2,
        )

    # Create grey Bars
    hh = {}
    for i in np.arange(B_nb):
        hh[i] = list((df[B[i]]["carbon"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            hh[i],
            width,
            bottom=[
                i + j + k + l + m + n + o + p + q
                for i, j, k, l, m, n, o, p, q in zip(a[i], aa[i], b[i], c[i], d[i], e[i], f[i], g[i],h[i])
            ],
            color=col(18),
            label="Carbon tax" if i == 0 else "",
            zorder=2,
        )

    s = {}
    maxi = []
    for i in np.arange(B_nb):
        for j in x:
            ax.text(
                (x + X[i])[j],
                [
                    k + l + m + n + o + p + q + r + t + u + 0.05
                    for k, l, m, n, o, p, q, r, t, u in zip(
                        a[i], aa[i], b[i], c[i], d[i], e[i], f[i], g[i], h[i], hh[i]
                    )
                ][j],
                B[i],
                ha="center",
                rotation=70,
            )
        s[i] = [
            k + l + m + n + o + p + q + r + t + u
            for k, l, m, n, o, p, q, r, t, u in zip(
                a[i], aa[i], b[i], c[i], d[i], e[i], f[i], g[i], h[i], hh[i]
            )
        ]
        s[i] = [0 if np.isnan(item) else item for item in s[i]]
        s[i] = [0 if item == np.inf else item for item in s[i]]
        s[i] = [0 if item == -np.inf else item for item in s[i]]
        print(B[i], "=", s[i])
        maxi.append(np.max(s[i]))

    print("H2 mean Cost =\n", meanCosts)
    print("H2 mean cost over horizon = ", meanCosts.mean())

    if comparaison == False:
        plt.plot(
            x,
            meanCosts,
            marker="D",
            color="none",
            markerfacecolor="None",
            markeredgecolor="black",
            markersize=6,
            markeredgewidth=1.5,
            label="H2 mean Price",
            zorder=3,
        )
        plt.axhline(
            y=horizonMean,
            color="gray",
            linestyle="--",
            alpha=0.3,
            label="Weighted average price",
            zorder=2,
        )
    else:
        if n == 1:
            plt.plot(
                x - 0.025 - width / 2,
                meanCosts,
                marker="D",
                color="none",
                markerfacecolor="None",
                markeredgecolor="black",
                markersize=6,
                markeredgewidth=1.5,
                label="H2 average price",
                zorder=2,
            )
            # plt.axhline(y=horizonMean[0],color='gray',linestyle='--',label='Mean price over horizon',alpha=0.3,zorder=2)
            # plt.text(-(width+0.05)*n,horizonMean[0], 'Base')
            # plt.axhline(y=horizonMean[1],color='gray',linestyle='--',alpha=0.3,zorder=2)
            # plt.text(-(width+0.05)*n, horizonMean[1], 'AEL Only')
        else:
            for i in np.arange(len(meanCosts)):
                plt.plot(
                    x + M[i],
                    meanCosts[i],
                    marker="D",
                    color="none",
                    markerfacecolor="None",
                    markeredgecolor="black",
                    markersize=6,
                    markeredgewidth=1.5,
                    label="H2 average price" if i == 0 else "",
                    zorder=2,
                )
                # plt.axhline(y=horizonMean[i],color='gray',linestyle='--',alpha=0.3, label='Mean over horizon' if i==0 else "",zorder=2)
                # plt.text(-(width+0.05)*n, horizonMean[i]-0.3 if caseNames[i]=='Base' else horizonMean[i]+0.1, caseNames[i],zorder=2)

    ax.set_ylabel("LCOH (€/kgH$_2$)")
    x = list(x)
    plt.xticks(x, ["2020-2030", "2030-2040", "2040-2050", "2050-2060"])

    ax.set_ylim([0, np.max(maxi) + 1])
    ax.set_title("Hydrogen production costs")
    plt.grid(axis="y", alpha=0.5, zorder=1)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.65, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    plt.savefig(outputFolder + "/H2 costs.png",dpi=300)
    plt.show(block=True)
    plt.close()

    return


def plot_costs(df, outputFolder="../data/output/", comparaison=False):
    YEAR = list(df[list(df.keys())[0]].index.get_level_values('YEAR'))
    YEAR.sort()
    dy = YEAR[1] - YEAR[0]
    y0 = YEAR[0] - dy

    fig, ax = plt.subplots(figsize=(7, 4.3))
    width = 0.25
    labels = list(df["SMR"].index)
    x = np.arange(len(labels))
    col = plt.cm.tab20c
    colBis = plt.cm.tab20b

    parameters = {
        "axes.labelsize": 12,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "figure.titlesize": 15,
        "legend.fontsize": 12,
    }
    plt.rcParams.update(parameters)


    B = list(df.keys())
    B_nb = len(B)
    if B_nb % 2 > 0:
        n = B_nb // 2
        X = np.sort(
            [-i * (width + 0.05) for i in np.arange(1, n + 1)]
            + [0]
            + [i * (width + 0.05) for i in np.arange(1, n + 1)]
        )
    else:
        n = B_nb / 2
        X = np.sort(
            [-(width / 2 + 0.025) - i * (width + 0.05) for i in np.arange(n)]
            + [(width / 2 + 0.025) + i * (width + 0.05) for i in np.arange(n)]
        )
        M = [X[i : i + 2].mean() for i in np.arange(0, int(n + 1), 2)]

    meanCosts = []
    horizonMean = []
    c = 0
    if comparaison == False:
        meanCosts = sum(
            df[k][
                [
                    "powerCosts",
                    "capacityCosts",
                    "capexElec",
                    "importElec",
                    "importGas",
                    "storageElec",
                    "storageH2",
                    "carbon",
                    "TURPE",
                    "importsH2"
                ]
            ].sum(axis=1)
            for k in B
        ) / sum((df[k]["Prod"] * 30) for k in B)
        horizonMean = sum(
            df[k][
                [
                    "powerCosts",
                    "capacityCosts",
                    "capexElec",
                    "importElec",
                    "importGas",
                    "storageElec",
                    "storageH2",
                    "carbon",
                    "TURPE",
                    "importsH2"
                ]
            ].sum(axis=1)
            for k in B
        ).sum() / (sum((df[k]["Prod"] * 30) for k in B).sum())
    else:
        if B_nb % 2 > 0:
            meanCosts = sum(
                df[k][
                    [
                        "powerCosts",
                        "capacityCosts",
                        "capexElec",
                        "importElec",
                        "importGas",
                        "storageElec",
                        "storageH2",
                        "carbon",
                        "TURPE",
                        "importsH2"
                    ]
                ].sum(axis=1)
                for k in B[0:2]
            ) / sum((df[k]["Prod"] * 30) for k in B[0:2])
            horizonMean.append(
                sum(
                    df[k][
                        [
                            "powerCosts",
                            "capacityCosts",
                            "capexElec",
                            "importElec",
                            "importGas",
                            "storageElec",
                            "storageH2",
                            "carbon",
                            "TURPE",
                            "importH2"
                        ]
                    ].sum(axis=1)
                    for k in B[0:2]
                ).sum()
                / (sum((df[k]["Prod"] * 30) for k in B[0:2]).sum())
            )
            horizonMean.append(
                df[B[-1]][
                    [
                        "powerCosts",
                        "capacityCosts",
                        "capexElec",
                        "importElec",
                        "importGas",
                        "storageElec",
                        "storageH2",
                        "carbon",
                        "TURPE",
                        "importsH2"
                    ]
                ]
                .sum(axis=1)
                .sum()
                / (df[B[-1]]["Prod"] * 30).sum()
            )
        else:
            for i in np.arange(0, int(n + 1), 2):
                meanCosts.append(
                    sum(
                        df[k][
                            [
                                "powerCosts",
                                "capacityCosts",
                                "capexElec",
                                "importElec",
                                "importGas",
                                "storageElec",
                                "storageH2",
                                "carbon",
                                "TURPE",
                                "importH2"
                            ]
                        ].sum(axis=1)
                        for k in B[i : i + 2]
                    )
                    / sum((df[k]["Prod"] * 30) for k in B[i : i + 2])
                )
                horizonMean.append(
                    sum(
                        df[k][
                            [
                                "powerCosts",
                                "capacityCosts",
                                "capexElec",
                                "importElec",
                                "importGas",
                                "storageElec",
                                "storageH2",
                                "carbon",
                                "TURPE",
                                "importsH2"
                            ]
                        ].sum(axis=1)
                        for k in B[i : i + 2]
                    ).sum()
                    / (sum((df[k]["Prod"] * 30) for k in B[i : i + 2]).sum())
                )
                c = c + 1

    # Create light blue Bars
    a = {}
    for i in np.arange(B_nb):
        a[i] = list((df[B[i]]["capacityCosts"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i], a[i], width, color=col(1), label="Fixed costs" if i == 0 else "", zorder=2
        )

    # Create dark blue Bars
    aa = {}
    for i in np.arange(B_nb):
        aa[i] = list((df[B[i]]["powerCosts"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            aa[i],
            width,
            bottom=a[i],
            color=col(0),
            label="Variable costs" if i == 0 else "",
            zorder=2,
        )

    # Create brown Bars
    b = {}
    for i in np.arange(B_nb):
        b[i] = list((df[B[i]]["importGas"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            b[i],
            width,
            bottom=[i + j for i, j in zip(a[i], aa[i])],
            color=colBis(9),
            label="Gas feedstock" if i == 0 else "",
            zorder=2,
        )

    # Create green Bars
    c = {}
    for i in np.arange(B_nb):
        c[i] = list(
            (
                (df[B[i]]["capexElec"] + df[B[i]]["importElec"] + df[B[i]]["TURPE"])
                / (df[B[i]]["Prod"] * 30)
            ).fillna(0)
        )
        plt.bar(
            x + X[i],
            c[i],
            width,
            bottom=[i + j + k for i, j, k in zip(a[i], aa[i], b[i])],
            color=col(9),
            label="Electricity" if i == 0 else "",
            zorder=2,
        )

    # Create purple Bars
    f = {}
    for i in np.arange(B_nb):
        f[i] = list(
            ((df[B[i]]["storageH2"] + df[B[i]]["storageElec"]) / (df[B[i]]["Prod"] * 30)).fillna(0)
        )
        plt.bar(
            x + X[i],
            f[i],
            width,
            bottom=[i + j + k + l for i, j, k, l, in zip(a[i], aa[i], b[i], c[i])],
            color=colBis(18),
            label="Storage capacity" if i == 0 else "",
            zorder=2,
        )

    # Create orange Bars
    g = {}
    for i in np.arange(B_nb):
        g[i] = list((df[B[i]]["importsH2"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            g[i],
            width,
            bottom=[i + j + k + l + m for i, j, k, l, m, in zip(a[i], aa[i], b[i], c[i], f[i])],
            color=col(6),
            label="Importation" if i == 0 else "",
            zorder=2,
        )

    # Create grey Bars
    h = {}
    for i in np.arange(B_nb):
        h[i] = list((df[B[i]]["carbon"] / (df[B[i]]["Prod"] * 30)).fillna(0))
        plt.bar(
            x + X[i],
            h[i],
            width,
            bottom=[i + j + k + l + m + n for i, j, k, l, m, n in zip(a[i], aa[i], b[i], c[i], f[i],g[i])],
            color=col(18),
            label="Carbon tax" if i == 0 else "",
            zorder=2,
        )


    s = {}
    maxi = []
    for i in np.arange(B_nb):
        for j in x:
            ax.text(
                (x + X[i])[j],
                [
                    k + l + m + n + o + p + q + 0.05
                    for k, l, m, n, o, p, q in zip(a[i], aa[i], b[i], c[i], f[i], g[i], h[i])
                ][j],
                B[i],
                ha="center",
                rotation=70,
            )
        s[i] = [
            k + l + m + n + o + p + q for k, l, m, n, o, p, q in zip(a[i], aa[i], b[i], c[i], f[i], g[i], h[i])
        ]
        s[i] = [0 if np.isnan(item) else item for item in s[i]]
        s[i] = [0 if item == np.inf else item for item in s[i]]
        s[i] = [0 if item == -np.inf else item for item in s[i]]
        print(B[i], "=", s[i])
        maxi.append(np.max(s[i]))

    print("H2 mean Cost =\n", meanCosts)
    print("H2 mean cost over horizon = ", meanCosts.mean())

    if comparaison == False:
        plt.plot(
            x,
            meanCosts,
            marker="D",
            color="none",
            markerfacecolor="None",
            markeredgecolor="black",
            markersize=6,
            markeredgewidth=1.5,
            label="H2 average price",
            zorder=3,
        )
        plt.axhline(
            y=horizonMean,
            color="gray",
            linestyle="--",
            alpha=0.3,
            label="Weighted average price",
            zorder=2,
        )
    else:
        if n == 1:
            plt.plot(
                x - 0.025 - width / 2,
                meanCosts,
                marker="D",
                color="none",
                markerfacecolor="None",
                markeredgecolor="black",
                markersize=6,
                markeredgewidth=1.5,
                label="H2 average price",
                zorder=2,
            )
            # plt.axhline(y=horizonMean[0],color='gray',linestyle='--',label='Mean price over horizon',alpha=0.3,zorder=2)
            # plt.text(-(width+0.05)*n,horizonMean[0], 'Base')
            # plt.axhline(y=horizonMean[1],color='gray',linestyle='--',alpha=0.3,zorder=2)
            # plt.text(-(width+0.05)*n, horizonMean[1], 'AEL Only')
        else:
            for i in np.arange(len(meanCosts)):
                plt.plot(
                    x + M[i],
                    meanCosts[i],
                    marker="D",
                    color="none",
                    markerfacecolor="None",
                    markeredgecolor="black",
                    markersize=6,
                    markeredgewidth=1.5,
                    label="H2 average price" if i == 0 else "",
                    zorder=2,
                )
                # plt.axhline(y=horizonMean[i],color='gray',linestyle='--',alpha=0.3, label='Mean over horizon' if i==0 else "",zorder=2)
                # plt.text(-(width+0.05)*n, horizonMean[i]-0.3 if caseNames[i]=='Base' else horizonMean[i]+0.1, caseNames[i],zorder=2)

    ax.set_ylabel("LCOH (€/kgH$_2$)")
    x = list(x)
    plt.xticks(x, ["2020-2030", "2030-2040", "2040-2050", "2050-2060"])

    ax.set_ylim([0, np.max(maxi) + 1])
    # ax.set_title("Hydrogen production costs")
    plt.grid(axis="y", alpha=0.5, zorder=1)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.63, box.height])
    # get handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # specify order of items in legend
    order = [0, 1, 7, 6, 5, 4, 3, 2]
    # Put a legend to the right of the current axis
    ax.legend(
        [handles[idx] for idx in order],
        [labels[idx] for idx in order],
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )
    plt.savefig(outputFolder + "/Costs.png",dpi=300)
    plt.show(block=False)
    plt.close()

    return


def plot_costs_new(df, outputFolder="../data/output/"):


    def kg_to_MWh(x):
        y=x*30
        return y

    def MWh_to_kg(x):
        y=x/30
        return y

    YEAR = list(df[list(df.keys())[0]].index.get_level_values('YEAR'))
    YEAR.sort()
    dy = YEAR[1] - YEAR[0]
    y0 = YEAR[0] - dy

    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    width = 0.25
    labels = list(df["SMR"].index)
    x = np.arange(len(labels))
    col = plt.cm.tab20c
    colBis = plt.cm.tab20b


    B = list(df.keys())
    B_nb = len(B)
    if B_nb % 2 > 0:
        n = B_nb // 2
        X = np.sort(
            [-i * (width + 0.05) for i in np.arange(1, n + 1)]
            + [0]
            + [i * (width + 0.05) for i in np.arange(1, n + 1)]
        )
    else:
        n = B_nb / 2
        X = np.sort(
            [-(width / 2 + 0.025) - i * (width + 0.05) for i in np.arange(n)]
            + [(width / 2 + 0.025) + i * (width + 0.05) for i in np.arange(n)]
        )
        M = [X[i : i + 2].mean() for i in np.arange(0, int(n + 1), 2)]

    meanCosts = []
    horizonMean = []
    meanCosts = sum(
            df[k][
                [
                    "powerCosts",
                    "capacityCosts",
                    "capexElec",
                    "importElec",
                    "importGas",
                    "storageElec",
                    "storageH2",
                    "carbon",
                    "TURPE",
                    "importsH2"
                ]
            ].sum(axis=1)
            for k in B
        ) / sum((df[k]["Prod"] * 30) for k in B)
    horizonMean = sum(
            df[k][
                [
                    "powerCosts",
                    "capacityCosts",
                    "capexElec",
                    "importElec",
                    "importGas",
                    "storageElec",
                    "storageH2",
                    "carbon",
                    "TURPE",
                    "importsH2"
                ]
            ].sum(axis=1)
            for k in B
        ).sum() / (sum((df[k]["Prod"] * 30) for k in B).sum())

    a={}
    aa={}
    b={}
    c={}
    f={}
    g={}
    h={}
    s={}
    maxi=[]

    for i,tech in enumerate(B) :
        a[i] = list((df[tech]["capacityCosts"] / (df[tech]["Prod"] * 30)).fillna(0))
        plt.bar(x + X[i], a[i], width, color=col(4*i),label="Fixed costs" if tech in ['SMR','AEL'] else '', zorder=2)

        aa[i] = list((df[tech]["powerCosts"] / (df[tech]["Prod"] * 30)).fillna(0))
        plt.bar( x + X[i],aa[i],width,bottom=a[i],color=col(4*i+1),label="Variable costs" if tech in ['SMR','AEL'] else '',zorder=2)

        if tech=='SMR':
            b[i] = list((df[tech]["importGas"] / (df[tech]["Prod"] * 30)).fillna(0))
            plt.bar(x + X[i],b[i],width,bottom=[j+k for j,k in zip(a[i], aa[i])],color=col(4*i+2),label="Feedstock gas",zorder=2)

            c[i]=0*np.ones(len(YEAR))
            f[i]=0*np.ones(len(YEAR))
            g[i]=0*np.ones(len(YEAR))

        elif tech=='AEL':
            b[i]=0*np.ones(len(YEAR))

            c[i] = list(((df[tech]["capexElec"] + df[tech]["importElec"] + df[tech]["TURPE"])/ (df[tech]["Prod"] * 30)).fillna(0))
            plt.bar(x + X[i],c[i],width,bottom=[j + k for j,k in zip(a[i], aa[i])],color=col(4*i+2),label="Feedstock electricity",zorder=2)

            f[i] = list(((df[tech]["storageH2"] + df[tech]["storageElec"]) / (df[tech]["Prod"] * 30)).fillna(0))
            plt.bar(x + X[i],f[i],width,bottom=[j+k+l for j,k,l in zip(a[i], aa[i], c[i])],color=col(4*i+3),label="Storage costs",zorder=2)

            g[i]=0*np.ones(len(YEAR))

        elif tech=='Imports':
            b[i]=0*np.ones(len(YEAR))
            c[i]=0*np.ones(len(YEAR))
            f[i]=0*np.ones(len(YEAR))

            g[i] = list((df[tech]["importsH2"] / (df[tech]["Prod"] * 30)).fillna(0))
            plt.bar(x + X[i],g[i],width,color=col(4*i),label="Importation costs",zorder=2)

        plt.rcParams["hatch.linewidth"] = 4
        plt.rcParams["hatch.color"] = col(4*i+2)
        h[i] = list((df[tech]["carbon"] / (df[tech]["Prod"] * 30)).fillna(0))
        plt.bar(x + X[i],h[i],width,bottom=[i + j + k + l + m + n  for i, j, k, l, m, n in zip(a[i], aa[i], b[i], c[i], f[i], g[i])],color='none',hatch='//',zorder=2)

        s[i] = [k + l + m + n + o + p + q for k, l, m, n, o, p, q in zip(a[i], aa[i], b[i], c[i], f[i], g[i], h[i])]
        s[i] = [0 if np.isnan(item) else item for item in s[i]]
        s[i] = [0 if item == np.inf else item for item in s[i]]
        s[i] = [0 if item == -np.inf else item for item in s[i]]
        print(B[i], "=", s[i])
        maxi.append(np.max(s[i]))

        plt.bar(x + X[i],s[i],width=width,color='none',edgecolor=col(4*i),linewidth=0.5)

    # plt.plot(x,meanCosts,marker="D",color="none",markerfacecolor="None",markeredgecolor="black",markersize=6,markeredgewidth=1.5,label="H2 average price",zorder=3)
    for j,y in enumerate(YEAR):
        xax=[x[j]+X[0]-width/2,x[j]+X[-1]+width/2]
        yax=[meanCosts.loc[(slice(None),y)].values[0],meanCosts.loc[(slice(None),y)].values[0]]

        plt.plot(xax,yax,linestyle=':',linewidth=2,color=col(16),label="Ten-year average cost" if j==0 else '',zorder=3)

    plt.axhline(y=horizonMean,color=col(16),linestyle="--",label="Cumulated average cost",zorder=2,)
    plt.rcParams["hatch.linewidth"] = 4
    plt.rcParams["hatch.color"] = col(18)
    plt.bar(0,0,width,color='none',hatch='//',label="Carbon tax",zorder=2)


    ax.set_ylabel("LCOH (€/kgH$_2$)")
    x = list(x)
    plt.xticks(x, ["2020-2030", "2030-2040", "2040-2050", "2050-2060"])

    ax.set_ylim([0, np.max(maxi) + 1])
    # ax.set_title("Hydrogen production costs")
    plt.grid(axis="y", alpha=0.5, zorder=1)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.61, box.height])
    # get handles and labels
    handles, labels = ax.get_legend_handles_labels()
    allTech=[0,1,10]
    legend1=plt.legend([handles[idx] for idx in allTech],[labels[idx] for idx in allTech],title="All technologies",title_fontsize=12, loc="center left", bbox_to_anchor=(1.155, 0.92),alignment='left',frameon=False)
    plt.gca().add_artist(legend1)

    AEL=[5,4,3,2]
    legend2=plt.legend([handles[idx] for idx in AEL],[labels[idx] for idx in AEL],title="Water electrolysis",title_fontsize=12,loc="center left", bbox_to_anchor=(1.155, 0.58),alignment='left',frameon=False)
    plt.gca().add_artist(legend2)

    SMR=[8,7,6]
    legend3=plt.legend([handles[idx] for idx in SMR],[labels[idx] for idx in SMR],title="SMR",title_fontsize=12,loc="center left", bbox_to_anchor=(1.155, 0.25),alignment='left',frameon=False)
    plt.gca().add_artist(legend3)

    Imports=[9]
    legend=plt.legend([handles[idx] for idx in Imports],[labels[idx] for idx in Imports],title="H$_2$ importation",title_fontsize=12,loc="center left", bbox_to_anchor=(1.155, 0),alignment='left',frameon=False)

    secax = ax.secondary_yaxis("right", functions=(kg_to_MWh,MWh_to_kg))
    secax.set_ylabel("(€/MWh)")

    plt.savefig(outputFolder + "/Costs_H2.png",dpi=300)
    plt.show()
    plt.close()

    return


def plot_compare_energy_and_carbon(dico, scenarioNames, outputPath="../data/output/",name='CO2'):
    YEAR = list(list(dico.items())[0][1].items())[0][1].index.values
    YEAR.sort()
    L = list(dico.keys())

    col = plt.cm.tab20c

    labels = list(YEAR)
    x = np.arange(len(labels))

    fig, ax = plt.subplots(1, 1, figsize=(5.5, 3.2))

    scenarioColors = [col(0), col(4), col(8)]
    scenarioMarkers = ["o", "v", "s"]

    for k, l in enumerate(L):
        # add carbon emission
        l10 = list(dico[l]["carbon"])
        print(l10)
        ax.plot(
            l10,
            marker=scenarioMarkers[k],
            color=scenarioColors[k],
            label=scenarioNames[k],
            zorder=2,
        )

    plt.xticks(x, ["2020-2030","2030-2040", "2040-2050", "2050-2060"])  # ,'2060'])
    plt.ylabel("kgCO$_2$/kgH$_2$")
    plt.grid(axis="y", alpha=0.5, zorder=1)
    # ay.set_title('Carbon content')
    # Shrink current axis by 20%
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # Put a legend to the right of the current axis
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    handles, labels = plt.gca().get_legend_handles_labels()
    # specify order of items in legend
    order = [2, 1, 0]
    plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order])
    plt.savefig("../data/output" + "/Comparison carbon - "+name+".png",dpi=300)
    plt.show(block=False)
    
    dico_fig={}
    for l in L:
        dico_fig[l] = dico[l].loc[2030:2050]


    fig, ax = plt.subplots(1, 3, sharey=True, figsize=(10, 3.2))

    width = 0.5
    labels = list(YEAR[1:])
    x = np.arange(len(labels))


    for k, l in enumerate(L):
        # Create grey Bars
        l1 = list(dico_fig[l]["SMR w/o CCUS"] / 1000)
        ax[k].bar(x ,l1,width,color=col(17),label="SMR w/o CCUS" if k == 2 else "",zorder=2)

        # Create blue Bars
        l2 = list((dico_fig[l]["SMR + CCUS 50%"] + dico_fig[l]["SMR + CCUS 90%"]) / 1000)
        ax[k].bar( x, l2, width,bottom=l1,color=col(0),label="SMR + CCUS" if k == 2 else "", zorder=2)

        # Create biogas Bars
        plt.rcParams["hatch.linewidth"] = 8
        plt.rcParams["hatch.color"] = col(3)
        l8 = list(dico_fig[l]["feedBiogas"] / 1000)
        ax[k].bar(x,l8,width,color="none",hatch="/",linewidth=0.5,edgecolor=col(3),alpha=0.8,label="Biomethane feed" if k == 2 else "",zorder=3)

        # Create green Bars
        l7 = list((dico_fig[l]["Alkaline electrolysis"] + dico_fig[l]["PEM electrolysis"]) / 1000)
        ax[k].bar(x ,l7, width,bottom=[i+j for i,j in zip(l1,l2)],color=col(8),label="AEL grid feed" if k == 2 else "",zorder=2)

        # Create Local renewables bars
        l9 = list(dico_fig[l]["feedRE"] / 1000)
        ax[k].bar(x,l9,width,bottom=[i+j for i,j in zip(l1,l2)],color=col(9),label="AEL local feed" if k == 2 else "",zorder=3)

        # Create orange Bars
        l3 = list(dico_fig[l]["importsH2"] / 1000)
        ax[k].bar(x, l3, width, bottom=[i+j+k for i,j,k in zip(l1,l2,l7)], color=col(4), label="Imports H2", zorder=2)

        # Add load factors

        place={'SMR w/o CCUS':[0]*len(YEAR),'SMR + CCUS 50%':l1,
        'Alkaline electrolysis':[k+l for k,l in zip(l1,l2)],'Imports H2':[k+l+m for k,l,m in zip(l1,l2,l7)]}
        dico_fig_L={'SMR w/o CCUS':l1,'SMR + CCUS 50%':l2,'Alkaline electrolysis':l7,'Imports H2':l3}

        prod_sum=[i+j+k+l for i,j,k,l in zip(l1,l2,l7,l3)]

        for y in range(len(YEAR[1:])):   
            load_factors={}
            load_factors['SMR w/o CCUS']=[round(i/j*100) for i,j in zip(l1,prod_sum)]
            load_factors['SMR + CCUS 50%']=[round(i/j*100) for i,j in zip(l2,prod_sum)]
            load_factors['Alkaline electrolysis']=[round(i/j*100) for i,j in zip(l7,prod_sum)]
            load_factors['Imports H2']=[round(i/j*100) for i,j in zip(l3,prod_sum)]
            for tech in load_factors.keys():
                if load_factors[tech][y]>10:
                    ax[k].text(x[y],place[tech][y]+dico_fig_L[tech][y]/2,str(load_factors[tech][y])+'%',ha='center')


    for k, l in enumerate(L):
        ax[k].grid(axis="y", alpha=0.5, color=col(19), zorder=1)
        ax[k].set_ylim(0,6.8)


    ax[0].set_ylabel("H$_2$ production  (TWh H$_2$/yr)")
    for k, l in enumerate(L):
        ax[k].set_title(scenarioNames[k])
        ax[k].set_xticks(x)
        ax[k].set_xticklabels(["2035", "2045", "2055"])  # ,'2060'])

    # Shrink current axis by 20%
    box = ax[0].get_position()
    ax[0].set_position([box.x0, box.y0-0.02, box.width * 0.9, box.height])
    box = ax[1].get_position()
    ax[1].set_position([box.x0 - 0.05, box.y0-0.02, box.width * 0.9, box.height])
    box = ax[2].get_position()
    ax[2].set_position([box.x0 - 0.1, box.y0-0.02, box.width * 0.9, box.height])
    # get handles and labels
    handles, labels = ax[2].get_legend_handles_labels()
    # specify order of items in legend
    order = [5,3, 4, 1, 0, 2]
    # Put a legend to the right of the current axis
    ax[2].legend(
        [handles[idx] for idx in order],
        [labels[idx] for idx in order],
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )

    plt.savefig("../data/output" + "/Comparison energy - "+name+".png",dpi=300)
    plt.show(block=False)

    return


def plot_compare_carbon_woSMR(dico, scenarioNames, outputPath="../data/output/",name='woSMR'):
    YEAR = list(list(dico.items())[0][1].items())[0][1].index.values
    YEAR.sort()
    L = list(dico.keys())

    col = plt.cm.tab20c

    labels = list(YEAR)
    x = np.arange(len(labels))

    fig, ax = plt.subplots(1, 1, figsize=(7, 3.2))

    scenarioColors = [col(0), col(4), col(8),col(12)]
    scenarioMarkers = ["o", "v", "s", "D"]

    for k, l in enumerate(L):
        # add carbon emission
        l10 = list(dico[l]["total_carbon"].cumsum()*10/1000000000)
        print(l10)
        ax.plot(
            l10,
            marker=scenarioMarkers[k],
            color=scenarioColors[k],
            label=scenarioNames[k],
            zorder=2,
        )

    plt.xticks(x, ["2020-2030","2030-2040", "2040-2050", "2050-2060"]) 
    plt.ylabel("Cumulated emissions (MtCO$_2$)")
    plt.grid(axis="y", alpha=0.5, zorder=1)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    # Put a legend to the right of the current axis
    handles, labels = plt.gca().get_legend_handles_labels()
    # specify order of items in legend
    order = [3,2, 1, 0]
    plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order],loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("../data/output" + "/Comparison carbon cumul - "+name+".png",dpi=300)
    plt.show(block=True)
    
    return


def plot_compare_capacity_and_costs(dico_capa,dico_ener, scenarioNames, outputPath="../data/output/",name='CO2'):
    YEAR = list(list(dico_capa.items())[0][1].items())[0][1].index.values
    YEAR.sort()
    L = list(dico_capa.keys())

    col = plt.cm.tab20c

    labels = list(YEAR)
    x = np.arange(len(labels))

    fig, ax = plt.subplots(1, 1, figsize=(5.5, 3.46))
    ax2=ax.twinx()

    scenarioColors = [col(0), col(4), col(8)]
    scenarioColorsBis=[col(1), col(5), col(9)]
    scenarioMarkers = ["o", "v", "s"]
    for k, l in enumerate(L):
        # add carbon emission
        l10 = list(dico_capa[l]["Alkaline electrolysis"])
        print(l10)
        ax.plot(l10,marker=scenarioMarkers[k],color=scenarioColors[k],label=scenarioNames[k],zorder=2)
        l12 = list(dico_ener[l]["loadFac_elec"]*100)
        ax2.plot(l12,linestyle='--',color=scenarioColorsBis[k],zorder=2)

    ax.plot([],linestyle='--',color=col(18),label='Load factors',zorder=2)

    plt.xticks(x, ["2020-2030","2030-2040", "2040-2050", "2050-2060"])  
    ax.set_ylabel("Electrolysis installed capacity (MW)")
    plt.grid(axis="y", alpha=0.5, zorder=1)
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax2.yaxis.set_major_formatter(yticks)
    ax2.set_ylabel("Electrolysis load factor (%)")

    # Shrink current axis by 10%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.98, box.height])

    handles, labels = ax.get_legend_handles_labels()
    print(labels)
    # # specify order of items in legend
    order = [1,2, 0,3]
    ax.legend([handles[idx] for idx in order], [labels[idx] for idx in order])
    plt.savefig("../data/output" + "/Comparison capacity - "+name+".png",dpi=300)
    plt.show(block=False)

    fig, ax = plt.subplots(1, 1, figsize=(5.5, 3.2))

    for k, l in enumerate(L):
        # add carbon emission
        l11 = list(dico_ener[l]["costs"])
        print(l11)
        ax.plot(l11,marker=scenarioMarkers[k],color=scenarioColors[k],label=scenarioNames[k],zorder=2)

    plt.xticks(x, ["2020-2030","2030-2040", "2040-2050", "2050-2060"])  # ,'2060'])
    plt.ylabel("LCOH (€/kgH$_2$)")
    plt.grid(axis="y", alpha=0.5, zorder=1)
    # ay.set_title('Carbon content')
    # Shrink current axis by 20%
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # Put a legend to the right of the current axis
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    handles, labels = plt.gca().get_legend_handles_labels()
    # # specify order of items in legend
    order = [0, 1, 2]
    ax.legend([handles[idx] for idx in order], [labels[idx] for idx in order])
    plt.savefig("../data/output" + "/Comparison costs - "+name+".png",dpi=300)
    plt.show(block=True)
    
    return
    

def plot_costs2050(df, outputFolder="../data/output/", comparaison=False):
    caseNames = ["BM=60€", "BM=75€", "BM=90€"]


    def kg_to_MWh(x):
        y=x*30
        return y

    def MWh_to_kg(x):
        y=x/30
        return y


    YEAR = df[list(df.keys())[0]].index.values
    YEAR.sort()
    # dy=YEAR[1]-YEAR[0]
    # y0=YEAR[0]-dy

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    width = 0.2
    labels = list(df["SMR BM=60€"].index)
    x = np.arange(len(labels))
    col = plt.cm.tab20c
    colBis = plt.cm.tab20b

    B = list(df.keys())
    B_nb = len(B)
    if B_nb % 2 > 0:
        n = B_nb // 2
        X = np.sort(
            [-i * (width + 0.05) for i in np.arange(1, n + 1)]
            + [0]
            + [i * (width + 0.05) for i in np.arange(1, n + 1)]
        )
    else:
        n = B_nb / 2
        X = np.sort(
            [-(width / 2 + 0.025) - i * (width + 0.05) for i in np.arange(n)]
            + [(width / 2 + 0.025) + i * (width + 0.05) for i in np.arange(n)]
        )
        M = [X[i : i + 2].mean() for i in np.arange(0, int(n + 2), 2)]

    meanCosts = []
    horizonMean = []
    c = 0
    if comparaison == False:
        meanCosts = sum(
            df[k][
                [
                    "powerCosts",
                    "capacityCosts",
                    "capexElec",
                    "importElec",
                    "importGas",
                    "storageElec",
                    "storageH2",
                    "carbon",
                    "TURPE",
                ]
            ].sum(axis=1)
            for k in B
        ) / sum((df[k]["Prod"] * 30) for k in B)
        horizonMean = sum(
            df[k][
                [
                    "powerCosts",
                    "capacityCosts",
                    "capexElec",
                    "importElec",
                    "importGas",
                    "storageElec",
                    "storageH2",
                    "carbon",
                    "TURPE",
                ]
            ].sum(axis=1)
            for k in B
        ).sum() / (sum((df[k]["Prod"] * 30) for k in B).sum())
    else:
        if B_nb % 2 > 0:
            meanCosts = sum(
                df[k][
                    [
                        "powerCosts",
                        "capacityCosts",
                        "capexElec",
                        "importElec",
                        "importGas",
                        "storageElec",
                        "storageH2",
                        "carbon",
                        "TURPE",
                    ]
                ].sum(axis=1)
                for k in B[0:2]
            ) / sum((df[k]["Prod"] * 30) for k in B[0:2])
            horizonMean.append(
                sum(
                    df[k][
                        [
                            "powerCosts",
                            "capacityCosts",
                            "capexElec",
                            "importElec",
                            "importGas",
                            "storageElec",
                            "storageH2",
                            "carbon",
                            "TURPE",
                        ]
                    ].sum(axis=1)
                    for k in B[0:2]
                ).sum()
                / (sum((df[k]["Prod"] * 30) for k in B[0:2]).sum())
            )
            horizonMean.append(
                df[B[-1]][
                    [
                        "powerCosts",
                        "capacityCosts",
                        "capexElec",
                        "importElec",
                        "importGas",
                        "storageElec",
                        "storageH2",
                        "carbon",
                        "TURPE",
                    ]
                ]
                .sum(axis=1)
                .sum()
                / (df[B[-1]]["Prod"] * 30).sum()
            )
        else:
            for i in np.arange(0, int(n + 2), 2):
                meanCosts.append(
                    sum(
                        df[k][
                            [
                                "powerCosts",
                                "capacityCosts",
                                "capexElec",
                                "importElec",
                                "importGas",
                                "storageElec",
                                "storageH2",
                                "carbon",
                                "TURPE",
                            ]
                        ].sum(axis=1)
                        for k in B[i : i + 2]
                    )
                    / sum((df[k]["Prod"] * 30) for k in B[i : i + 2])
                )
                horizonMean.append(
                    sum(
                        df[k][
                            [
                                "powerCosts",
                                "capacityCosts",
                                "capexElec",
                                "importElec",
                                "importGas",
                                "storageElec",
                                "storageH2",
                                "carbon",
                                "TURPE",
                            ]
                        ].sum(axis=1)
                        for k in B[i : i + 2]
                    ).sum()
                    / (sum((df[k]["Prod"] * 30) for k in B[i : i + 2]).sum())
                )
                c = c + 1

    # Create light blue Bars
    a = {}
    for i in np.arange(B_nb):
        a[i] = list(df[B[i]]["capacityCosts"] / (df[B[i]]["Prod"] * 30))
        plt.bar(
            x + X[i], a[i], width, color=col(1), label="Fixed Costs" if i == 0 else "", zorder=2
        )

    # Create dark blue Bars
    aa = {}
    for i in np.arange(B_nb):
        aa[i] = list(df[B[i]]["powerCosts"] / (df[B[i]]["Prod"] * 30))
        plt.bar(
            x + X[i],
            aa[i],
            width,
            bottom=a[i],
            color=col(0),
            label="Variable Costs" if i == 0 else "",
            zorder=2,
        )

    # Create brown Bars
    b = {}
    for i in np.arange(B_nb):
        b[i] = list(df[B[i]]["importGas"] / (df[B[i]]["Prod"] * 30))
        plt.bar(
            x + X[i],
            b[i],
            width,
            bottom=[i + j for i, j in zip(a[i], aa[i])],
            color=colBis(9),
            label="Feedstock gas" if i == 0 else "",
            zorder=2,
        )

    # Create green Bars
    c = {}
    for i in np.arange(B_nb):
        c[i] = list(
            (df[B[i]]["capexElec"] + df[B[i]]["importElec"] + df[B[i]]["TURPE"])
            / (df[B[i]]["Prod"] * 30)
        )
        plt.bar(
            x + X[i],
            c[i],
            width,
            bottom=[i + j + k for i, j, k in zip(a[i], aa[i], b[i])],
            color=col(9),
            label="Feedstock electricity" if i == 0 else "",
            zorder=2,
        )

    # Create purple Bars
    f = {}
    for i in np.arange(B_nb):
        f[i] = list((df[B[i]]["storageH2"] + df[B[i]]["storageElec"]) / (df[B[i]]["Prod"] * 30))
        plt.bar(
            x + X[i],
            f[i],
            width,
            bottom=[i + j + k + l for i, j, k, l in zip(a[i], aa[i], b[i], c[i])],
            color=colBis(17),
            label="Storage capacity" if i == 0 else "",
            zorder=2,
        )

    # Create grey Bars
    h = {}
    for i in np.arange(B_nb):
        h[i] = list(df[B[i]]["carbon"] / (df[B[i]]["Prod"] * 30))
        plt.bar(
            x + X[i],
            h[i],
            width,
            bottom=[i + j + k + l + m for i, j, k, l, m in zip(a[i], aa[i], b[i], c[i], f[i])],
            color=col(18),
            label="Carbon tax" if i == 0 else "",
            zorder=2,
        )

    s = {}
    for i in np.arange(B_nb):
        for j in x:
            ax.text(
                (x + X[i])[j],
                [
                    k + l + m + n + o + p + 0.05
                    for k, l, m, n, o, p in zip(a[i], aa[i], b[i], c[i], f[i], h[i])
                ][j],
                B[i][:3],
                ha="center",
                rotation=70,
                fontsize=10,
            )
        s[i] = [
            k + l + m + n + o + p for k, l, m, n, o, p in zip(a[i], aa[i], b[i], c[i], f[i], h[i])
        ]
        print(B[i], "=", s[i])

    print("H2 mean Cost =\n", meanCosts)
    # print("H2 mean cost over horizon = ", meanCosts.mean())

    if comparaison == False:
        plt.plot(
            x,
            meanCosts,
            marker="D",
            color="none",
            markerfacecolor="None",
            markeredgecolor="black",
            markersize=6,
            markeredgewidth=1.5,
            label="H$_2$ average LCOH",
            zorder=3,
        )
        plt.axhline(
            y=horizonMean,
            color="gray",
            linestyle="--",
            alpha=0.3,
            label="Weighted average cost",
            zorder=2,
        )
    else:
        if n == 1:
            plt.plot(
                x - 0.025 - width / 2,
                meanCosts,
                marker="D",
                color="none",
                markerfacecolor="None",
                markeredgecolor="black",
                markersize=6,
                markeredgewidth=1.5,
                label="H$_2$ average LCOH",
                zorder=2,
            )
            # plt.axhline(y=horizonMean[0],color='gray',linestyle='--',label='Mean price over horizon',alpha=0.3,zorder=2)
            # plt.text(-(width+0.05)*n,horizonMean[0], 'Base')
            # plt.axhline(y=horizonMean[1],color='gray',linestyle='--',alpha=0.3,zorder=2)
            # plt.text(-(width+0.05)*n, horizonMean[1], 'AEL Only')
        else:
            for i in np.arange(len(meanCosts)):
                plt.plot(
                    x + M[i],
                    meanCosts[i],
                    marker="D",
                    color="none",
                    markerfacecolor="None",
                    markeredgecolor="black",
                    markersize=6,
                    markeredgewidth=1.5,
                    label="H$_2$ average LCOH" if i == 0 else "",
                    zorder=2,
                )
                if i > 0:
                    plt.axvline(
                        x + M[i] - width - 0.025 * 2,
                        color="gray",
                        linestyle="--",
                        alpha=0.3,
                        zorder=2,
                    )
                plt.text(x + M[i], 4, caseNames[i], zorder=2, ha="center", fontsize=11)
                # plt.axhline(y=horizonMean[i],color='gray',linestyle='--',alpha=0.3, label='Mean over horizon' if i==0 else "",zorder=2)
                # plt.text(-(width+0.05)*n, horizonMean[i]-0.3 if caseNames[i]=='Base' else horizonMean[i]+0.1, caseNames[i],zorder=2)

    ax.set_ylabel("LCOH (€/kgH$_2$)")
    x = list(x)
    plt.xticks(x, ["2050-2060"])
    m = max(s.values())
    ax.set_ylim([0, np.round(m[0]) + 2])
    # ax.set_title("Hydrogen production costs")
    plt.grid(axis="y", alpha=0.5, zorder=1)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])
    # get handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # specify order of items in legend
    order = [0, 6, 5, 4, 3, 2, 1]
    # Put a legend to the right of the current axis
    ax.legend(
        [handles[idx] for idx in order],
        [labels[idx] for idx in order],
        loc="center left",
        bbox_to_anchor=(1.2, 0.5),
    )
    secax = ax.secondary_yaxis("right", functions=(kg_to_MWh,MWh_to_kg))
    secax.set_ylabel("(€/MWh)")
    plt.savefig(outputFolder + "/H2 costs - BM.png",dpi=300)
    plt.show(block=True)

    return


def plot_carbonCosts(dico,area, scenarioNames, outputPath="../data/output/"):
    YEAR = list(list(list(dico.items())[0][1].items())[0][1].index.get_level_values('YEAR_op'))

    carbonContent = {}
    meanPrice = {}
    horizonMean = {}
    horizonContent = {}
    for s in list(dico.keys()):
        meanPrice[s] = (dico[s]['total_costs']/(dico[s]["totalProd"]*30*1000)).fillna(0)
        horizonMean[s] = (dico[s]['total_costs'].sum()/(dico[s]["totalProd"]*30*1000).sum())
        carbonContent[s] = (dico[s]['total_carbon']/(dico[s]["totalProd"]*30*1000)).fillna(0)
        horizonContent[s] = (dico[s]['total_carbon'].sum()/(dico[s]["totalProd"]*30*1000).sum())

    fig, ax = plt.subplots(figsize=(6.5,4.5))
    col = plt.cm.tab20c
    colBis = plt.cm.tab20b
    dico_color = {
        "ref": (colBis, 0),
        "BM_": (col, 0),
        "woSMR_": (colBis, 16),
        "CO2_": (colBis, 8),
        "Re_": (col, 8),
    }
    colNumber = []
    variable = []
    n = 0
    for l, s in enumerate(list(dico.keys())):
        for var in list(dico_color.keys()):
            if var in s:
                variable.append(var)
                if variable[l - 1] == variable[l]:
                    n = n + 1
                else:
                    n = 0
                colNumber.append((dico_color[var][0], dico_color[var][1] + n))
    mark = ["s", "D", "o"]

    n = 0
    for k, y in enumerate(YEAR[1:]):
        for l, s in enumerate(list(dico.keys())):
            ax.scatter(
                carbonContent[s].loc[y],
                meanPrice[s].loc[y],
                marker=mark[k],
                color=col(l * 4),
                zorder=2,
            )  # colNumber[l][0+l*4](colNumber[l][1])
        ax.plot([], [], marker=mark[k], linestyle="", color="grey", label=str(y) + '-' + str(y + 10))
    for l, s in enumerate(list(dico.keys())):
        ax.plot(
            carbonContent[s].iloc[1:].values,
            meanPrice[s].iloc[1:].values,
            marker="",
            color=col(l * 4),
            label=scenarioNames[n],
            linestyle="--",
            alpha=0.5,
            zorder=2,
        )
        n += 1

    plt.ylabel("Average LCOH (€/kgH$_2$)")
    plt.xlabel("Carbon content of hydrogen (kgCO$_2$/kgH$_2$)")
    # plt.title('LCOH and carbon content evolution')
    plt.grid(axis="y", alpha=0.5, zorder=1)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.68, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    plt.savefig("../data/output" + "/Comparison carbon - woSMR.png",dpi=300)
    plt.show(block=False)

    return


def plot_H2Mean2050(inputDict,area, outputFolder="../data/output/"):
    def weekly_average(df):
        df["week"] = df.index // 168 + 1
        df=df.loc[:8736]
        return df.groupby("week").sum() / 1000

    v_list = [
        "power_Dvar",
        "storageIn_Pvar",
        "storageOut_Pvar",
        "importation_Dvar",
    ]

    Variables = {
        v: pd.read_csv(outputFolder + "/" + v + ".csv").drop(columns="Unnamed: 0") for v in v_list
    }


    YEAR = Variables["power_Dvar"].set_index("YEAR_op").index.unique().values
    YEAR.sort()

    convFac = inputDict["conversionFactor"]
    areaConsumption = inputDict["areaConsumption"].loc[(area,slice(None),slice(None),slice(None))].reset_index()
    Conso = {
        y: areaConsumption.loc[areaConsumption["YEAR"] == y].pivot(
            columns="RESOURCES", values="areaConsumption", index="TIMESTAMP"
        )
        for y in YEAR
    }

    v = "power_Dvar"
    Pel = {
        y: Variables[v]
        .loc[Variables[v]["YEAR_op"] == y]
        .pivot(columns="TECHNOLOGIES", values="power_Dvar", index=["AREA","TIMESTAMP"])
        .drop(columns=["CCS1", "CCS2"]).loc[(area,slice(None))]
        for y in YEAR
    }
    for y in YEAR:
        for tech in list(Pel[y].columns):
            Pel[y][tech] = Pel[y][tech] * convFac.loc[("hydrogen", tech)].conversionFactor
    v = "storageOut_Pvar"
    Pel_stock_out = {
        y: Variables[v][
            np.logical_and(Variables[v]["YEAR_op"] == y, Variables[v]["RESOURCES"] == "hydrogen")
        ].pivot(columns="STOCK_TECHNO", values=v, index=["AREA","TIMESTAMP"]).loc[(area,(slice(None)))]
        for y in YEAR
    }
    v = "storageIn_Pvar"
    Pel_stock_in = {
        y: Variables[v][
            np.logical_and(Variables[v]["YEAR_op"] == y, Variables[v]["RESOURCES"] == "hydrogen")
        ].pivot(columns="STOCK_TECHNO", values=v, index=["AREA","TIMESTAMP"]).loc[(area,slice(None))]
        for y in YEAR
    }
    v = "importation_Dvar"
    Pel_imp = {
        y: Variables[v][
            np.logical_and(Variables[v]["YEAR_op"] == y, Variables[v]["RESOURCES"] == "hydrogen")
        ].pivot(columns="RESOURCES", values=v, index=["AREA","TIMESTAMP"]).loc[(area,slice(None))]
        for y in YEAR
    }

    Pel_exp = {y: -np.minimum(Pel_imp[y], 0) for y in Pel_imp.keys()}
    Pel_imp = {y: np.maximum(Pel_imp[y], 0) for y in Pel_imp.keys()}



    fig, ax = plt.subplots(figsize=(8, 4.5))
    col = plt.cm.tab20c
    colBis = plt.cm.tab20b

    yr = 2050

    ax.yaxis.grid(linestyle="--", linewidth=0.5, zorder=-6)

    # power_Dvar
    Pel[yr] = weekly_average(Pel[yr])
    # storageOut_Pvar
    Pel_stock_out[yr] = weekly_average(Pel_stock_out[yr])
    # storageIn_Pvar
    Pel_stock_in[yr] = weekly_average(Pel_stock_in[yr])
    # Demand H2
    Conso[yr] = weekly_average(Conso[yr])
    # importation_Dvar
    Pel_imp[yr] = weekly_average(Pel_imp[yr])
    Pel_exp[yr] = weekly_average(Pel_exp[yr])

    # H2 production
    ax.bar(
        Pel[yr].index,
        Pel[yr]["electrolysis_AEL"] + Pel[yr]["electrolysis_PEMEL"],
        label="Electrolysis",
        color=col(9),
        zorder=-1,
    )
    # ax.bar(Pel[yr].index, Pel[yr]['SMR_elec'] + Pel[yr]['SMR_elecCCS1'] + Pel[yr]['electrolysis_AEL']+Pel[yr]['electrolysis_PEMEL'], label='eSMR',color=col(0), zorder=-2)
    ax.bar(
        Pel[yr].index,
        Pel[yr]["SMR"]
        # + Pel[yr]["SMR_elec"]
        # + Pel[yr]["SMR_elecCCS1"]
        + Pel[yr]["electrolysis_AEL"]
        + Pel[yr]["electrolysis_PEMEL"],
        label="SMR w/o CCUS",
        color=col(17),
        zorder=-3,
    )
    ax.bar(
        Pel[yr].index,
        Pel[yr]["SMR"]
        + Pel[yr]["SMR + CCS1"]
        + Pel[yr]["SMR + CCS2"]
        # + Pel[yr]["SMR_elec"]
        # + Pel[yr]["SMR_elecCCS1"]
        + Pel[yr]["electrolysis_AEL"]
        + Pel[yr]["electrolysis_PEMEL"],
        label="SMR w CCUS",
        color=col(0),
        zorder=-4,
    )
    # ax.bar(Pel[yr].index, Pel[yr]['SMR']  + Pel[yr]['SMR + CCS1'] + Pel[yr]['SMR + CCS2'] + Pel[yr]['SMR_elec'] + Pel[yr]['SMR_elecCCS1'] + Pel[yr]['electrolysis_AEL'] + Pel[yr]['electrolysis_PEMEL']+ Pel[yr]['cracking'],label='Methane cracking', color='#33caff', zorder=-5)
    ax.bar(
        Pel_stock_out[yr].index,
        Pel_stock_out[yr]["tankH2_G"]
        + Pel_stock_in[yr]["saltCavernH2_G"]
        + Pel[yr]["SMR"]
        + Pel[yr]["SMR + CCS1"]
        + Pel[yr]["SMR + CCS2"]
        # + Pel[yr]["SMR_elec"]
        # + Pel[yr]["SMR_elecCCS1"]
        + Pel[yr]["electrolysis_AEL"]
        + Pel[yr]["electrolysis_PEMEL"],
        label="Stock - Out",
        color=colBis(18),
        zorder=-6,
    )
    # ax.bar(Pel_stock_out[yr].index,Pel_stock_out[yr]['tankH2_G']+Pel_stock_in[yr]['saltCavernH2_G'] + Pel[yr]['SMR']  + Pel[yr]['SMR + CCS1'] + Pel[yr]['SMR + CCS2'] + Pel[yr]['SMR_elec'] + Pel[yr]['SMR_elecCCS1'] + Pel[yr]['electrolysis_AEL']+Pel[yr]['electrolysis_PEMEL']+ Pel_imp[yr]['hydrogen'],label='Imports',color='#f74242',  zorder=-7)

    # H2 concumption
    ax.bar(Pel[yr].index, -Conso[yr]["hydrogen"], label="Consumption", color=colBis(10), zorder=-1)
    ax.bar(
        Pel_stock_in[yr].index,
        -Pel_stock_in[yr]["tankH2_G"] - Conso[yr]["hydrogen"],
        label="Stock - In",
        color=colBis(17),
        zorder=-2,
    )

    ax.set_ylabel("H$_2$ weekly production (GWh)")
    m = max(
        (
            Pel_stock_in[yr]["tankH2_G"]
            + Pel_stock_in[yr]["saltCavernH2_G"]
            + Conso[yr]["hydrogen"]
        ).max()
        + 10,
        (
            Pel_stock_out[yr]["tankH2_G"]
            + Pel_stock_in[yr]["saltCavernH2_G"]
            + Pel[yr]["SMR"]
            + Pel[yr]["SMR + CCS1"]
            + Pel[yr]["SMR + CCS2"]
            # + Pel[yr]["SMR_elec"]
            # + Pel[yr]["SMR_elecCCS1"]
            + Pel[yr]["electrolysis_AEL"]
            + Pel[yr]["electrolysis_PEMEL"]
            + Pel_imp[yr]["hydrogen"]
        ).max()
        + 10,
    )
    ax.set_ylim([-m, m])
    # Shrink all axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + 0.03, box.width * 0.85, box.height])
    # get handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # specify order of items in legend
    order = [3, 2, 1, 0, 4, 5]
    # Put a legend to the right of the current axis
    ax.legend(
        [handles[idx] for idx in order],
        [labels[idx] for idx in order],
        loc="upper left",
        bbox_to_anchor=(1, 1),
    )
    ax.set_xlabel("Week")

    plt.savefig(outputFolder + "/Gestion H2 2050.png",dpi=300)
    plt.show(block=False)

    return


def plot_stockLevel(area,timeStep,outputFolder="../data/output/"):


    def lissage(x,y,n):
        if n==0 :
            return x,y
        L=[]
        for j in range(n,len(y)-n):
            L.append((y.iloc[j-n:j+n]).mean())
        return list(x[n:len(x)-n]),L


    level = pd.read_csv(outputFolder + "/stockLevel_Pvar.csv").drop(columns="Unnamed: 0").set_index('AREA').loc[area].set_index(['YEAR_op','STOCK_TECHNO'])
    YEAR = level.index.get_level_values('YEAR_op').unique()

    col=plt.cm.tab20c
    fig,ax=plt.subplots()

    for k,y in enumerate(YEAR):
        # plt.plot(level.loc[(y,'tankH2_G')].set_index('TIMESTAMP')/1000,linewidth=1,color=col(k*4),label=y)
        data=lissage(level.loc[(y,'tankH2_G')]['TIMESTAMP'],level.loc[(y,'tankH2_G')]['stockLevel_Pvar']/1000,1)
        plt.plot(data[0],data[1],color=col(k*4),linewidth=1,label=str(y)+'-'+str(y+10))

    plt.legend()
    plt.ylabel('Inventory of the stock for gaseous tank (GWh)')
    plt.xlabel('Hour')
    plt.savefig(outputFolder + "/Stock_tank_raw.png",dpi=300)
    plt.show(block=False)
    plt.close()



    level = pd.read_csv(outputFolder + "/stockLevel_Pvar.csv").drop(columns="Unnamed: 0").set_index('AREA').loc[area].set_index(['YEAR_op','STOCK_TECHNO'])
    YEAR = level.index.get_level_values('YEAR_op').unique()

    col=plt.cm.tab20c
    fig,ax=plt.subplots()

    for k,y in enumerate(YEAR):
        # plt.plot(level.loc[(y,'tankH2_G')].set_index('TIMESTAMP')/1000,linewidth=1,color=col(k*4),label=y)
        data=lissage(level.loc[(y,'saltCavernH2_G')]['TIMESTAMP'],level.loc[(y,'saltCavernH2_G')]['stockLevel_Pvar']/1000,1)
        plt.plot(data[0],data[1],color=col(k*4),linewidth=1,label=y)

    plt.legend()
    plt.ylabel('Inventory of the stock for salt caverns (GWh)')
    plt.xlabel('Hour')
    plt.savefig(outputFolder + "/Stock_cavern.png",dpi=300)
    plt.show(block=False)
    plt.close()

    return


def plot_total_co2_emissions_and_flexSMR(dico_ener, scenarioNames, labels, area='Marseille',legend_title=None, outputPath="data/output/"):
    YEAR = list(list(dico_ener.items())[0][1].items())[0][1].index.get_level_values('YEAR_op')
    x = ["2030-2040", "2040-2050", "2050-2060"]

    col = plt.cm.tab20c
    colBis = plt.cm.tab20b
    dico_color = {"Re_inf": (col, 8), "Caverns": (colBis, 16), "CavernRE": (col, 0),"gas":(col,4), "BM":(col,12)}
    dico_mark = {"Re_inf": "d", "Caverns": "s", "CavernRE": "^","gas":"v", "BM":"o"}
    colNumber = []
    markNumber = []
    variable = []
    n = 0
    for l, s in enumerate(scenarioNames):
        for var in list(dico_color.keys()):
            if var in s:
                variable.append(var)
                if l > 0:
                    if variable[l - 1] == variable[l]:
                        n = n + 1
                    else:
                        n = 0
                colNumber.append((dico_color[var][0], dico_color[var][1] + n))
                markNumber.append(dico_mark[var])

    carbonCumul = {}
    carbonYear = {}
    flexSMR = {}
    flexSMR_mean = {}
    for s in scenarioNames:
        carbon = dico_ener[s]['total_carbon']
        carbonYear[s] = carbon * 10
        carbonCumul[s] = (carbon.cumsum() * 10).loc[YEAR[-1]]
        cost1 = (dico_ener[s]['total_costs']/(dico_ener[s]["totalProd"]*30*1000)).fillna(0)
        cost1_mean=(dico_ener[s]['total_costs'].sum()/(dico_ener[s]["totalProd"]*30*1000).sum())
        cost2 = (dico_ener[s+'_woSMR']['total_costs']/(dico_ener[s+'_woSMR']["totalProd"]*30*1000)).fillna(0)
        cost2_mean=(dico_ener[s+'_woSMR']['total_costs'].sum()/(dico_ener[s+'_woSMR']["totalProd"]*30*1000).sum())
        flexSMR[s] = cost2 - cost1
        flexSMR_mean[s] = cost2_mean - cost1_mean


    carbon_ref=dico_ener['ref']['total_carbon']
    carbonYear['ref'] = carbon_ref * 10
    carbonCumul['ref'] = (carbon_ref.cumsum() * 10).loc[YEAR[-1]]
    cost1 = (dico_ener['ref']['total_costs']/(dico_ener['ref']["totalProd"]*30*1000)).fillna(0)
    cost1_mean=(dico_ener['ref']['total_costs'].sum()/(dico_ener['ref']["totalProd"]*30*1000).sum())
    cost2 = (dico_ener[s+'_woSMR']['total_costs']/(dico_ener['ref'+'_woSMR']["totalProd"]*30*1000)).fillna(0)
    cost2_mean=(dico_ener['ref'+'_woSMR']['total_costs'].sum()/(dico_ener['ref'+'_woSMR']["totalProd"]*30*1000).sum())
    flexSMR['ref'] = cost2 - cost1
    flexSMR_mean['ref'] = cost2_mean - cost1_mean


    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(carbonCumul['ref'] / 1e9,flexSMR_mean['ref'],linestyle="",marker='x',markersize=14,label='Reference',color=col(16),zorder=2)

    for k, s in enumerate(scenarioNames):
        ax.plot(
            carbonCumul[s] / 1e9,
            flexSMR_mean[s],
            linestyle="",
            marker=markNumber[k],
            markersize=12,
            label=labels[k],
            color=colNumber[k][0](colNumber[k][1]),
            zorder=2,
        )


    ax.set_ylabel("SMR hybridisation value \nfrom 2020 to 2060 (€/kgH$_2$)")
    ax.set_xlabel("Emissions from 2020 to 2060 (MtCO$_2$)")
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + 0.05, box.width * 0.6, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc="center left", bbox_to_anchor=(1.05, 0.5))
    plt.grid(axis="y", alpha=0.5, zorder=1)

    plt.savefig(outputPath + "/Average_carbon_and_flex.png",dpi=300)
    plt.show()

    parameters = {
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.titlesize": 15,
        "legend.fontsize": 10,
    }
    plt.rcParams.update(parameters)


    fig, ax = plt.subplots(1, 3, figsize=(9, 4), sharey=True, sharex=True)
    for l, yr in enumerate(YEAR[1:]):
        ax[l].plot(carbonYear['ref'].loc[yr] / 1e9,flexSMR['ref'].loc[yr],linestyle="",marker='x',markersize=14,label='Reference',color=col(16),zorder=2)
        for k, s in enumerate(scenarioNames):
            ax[l].plot(
                carbonYear[s].loc[yr] / 1e9,
                flexSMR[s].loc[yr],
                linestyle="",
                marker=markNumber[k],
                markersize=12,
                label=labels[k],
                color=colNumber[k][0](colNumber[k][1]),
                zorder=2,
            )
        ax[l].set_title(x[l])
        # Shrink current axis by 20%
        box = ax[l].get_position()
        ax[l].set_position(
            [box.x0 - (l * box.width * 0.4), box.y0 + 0.01, box.width * 0.74, box.height]
        )
        ax[l].yaxis.grid(alpha=0.5, zorder=1)
        # plt.grid(axis='y', alpha=0.5, zorder=1)

    ax[0].set_ylabel("SMR hybridisation value (€/kgH$_2$)")
    ax[1].set_xlabel("Emissions for the period (MtCO$_2$)")
    # Put a legend to the right of the current axis
    ax[2].legend(loc="center left", bbox_to_anchor=(1.05, 0.5))
    plt.savefig(outputPath + "/Carbon and flex.png",dpi=300)
    plt.show()

    return flexSMR


def plot_carbon(df,df_conv,area='Marseille',outputFolder="data/output/"):

    YEAR = df.index.unique()
    x = ["2020-2030", "2030-2040", "2040-2050", "2050-2060"]

    cumul_carbon=(df['total_carbon'].cumsum() * 10)/1e9
    cumul_carbon_conv=(df_conv['total_carbon'].cumsum() * 10)/1e9
    print(cumul_carbon)
  

    col = plt.cm.tab20c

    fig, ax = plt.subplots()
    ax2=plt.twinx(ax)

    ax.plot(np.arange(len(x)),df['carbon'],marker='o',label='Carbon content of H$_2$',color=col(0))
    ax2.plot(np.arange(len(x)),cumul_carbon,marker='^',label='Cumulated CO$_2$ emissions',color=col(4))
    ax2.plot(np.arange(len(x)),cumul_carbon_conv,marker='^',label='Cumulated CO$_2$ emissions b.a.u',color=col(18))


    plt.grid(axis='y', alpha=0.5, zorder=1)
    ax.set_ylabel("Carbon content (kgCO$_2$/kgH$_2$)")
    ax2.set_ylabel("CO$_2$ cumulated emissions (MtCO$_2$)")
    # Put a legend to the right of the current axis 
    # ax.legend(loc="center left", bbox_to_anchor=(1.05, 0.5))
    plt.xticks(np.arange(len(x)),x)
    handles,labels=ax.get_legend_handles_labels()
    handles2,labels2=ax2.get_legend_handles_labels()
    plt.legend(handles+handles2,labels+labels2,loc='upper center')


    plt.savefig(outputFolder + "/Carbon.png",dpi=300)

    plt.show()

    return
