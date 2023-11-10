import os

os.sys.path.append(r"../")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb


def plot_mixProdElec(timeStep, outputFolder="data/output/", area="France"):
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
    ]
    Variables = {
        v: pd.read_csv(outputFolder + "/" + v + ".csv").drop(columns="Unnamed: 0") for v in v_list
    }

    YEAR = list(Variables["power_Dvar"].set_index("YEAR_op").index.unique())
    elecProd = (
        Variables["power_Dvar"]
        .set_index("AREA")
        .loc[area]
        .set_index(["YEAR_op", "TIMESTAMP", "TECHNOLOGIES"])
    )

    Prod = elecProd.groupby(["YEAR_op", "TECHNOLOGIES"]).sum() * timeStep
    Prod.sort_index(inplace=True, sort_remaining=True)
    Prod.loc[(slice(None), "IntercoOut"), "power_Dvar"] = -Prod.loc[
        (slice(None), "IntercoOut"), "power_Dvar"
    ]
    Storage = (
        Variables["storageOut_Pvar"]
        .set_index("AREA")
        .loc[area]
        .groupby(["YEAR_op", "STOCK_TECHNO"])
        .sum()["storageOut_Pvar"]
        - Variables["storageIn_Pvar"]
        .set_index("AREA")
        .loc[area]
        .groupby(["YEAR_op", "STOCK_TECHNO"])
        .sum()["storageIn_Pvar"]
    )
    Capa = (
        Variables["capacity_Pvar"]
        .set_index("AREA")
        .loc[area]
        .set_index(["YEAR_op", "TECHNOLOGIES"])
    )
    Capa.sort_index(axis=0, inplace=True)
    Prod_tot = {
        y: (
            Prod.loc[(y, slice(None))].sum()
            - Prod.loc[(y, "IntercoIn")]
            - Prod.loc[(y, "curtailment")]
            - Prod.loc[(y, "electrolysis_AEL")]
        )["power_Dvar"]
        for y in YEAR
    }

    TECHNO = list(Prod.index.get_level_values("TECHNOLOGIES").unique())
    TECHNO.remove("electrolysis_AEL")
    l_tech = len(TECHNO)
    l_year = len(YEAR)

    Fossils = {
        y: (
            Prod.loc[(y, "CCG")]
            + Prod.loc[(y, "Coal_p")]
            + Prod.loc[(y, "NewNuke")]
            + Prod.loc[(y, "OldNuke")]
            + Prod.loc[(y, "TAC")]
        )["power_Dvar"]
        / Prod_tot[y]
        for y in YEAR
    }
    EnR = {
        y: (
            Prod.loc[(y, "Solar")]
            + Prod.loc[(y, "WindOnShore")]
            + Prod.loc[(y, "WindOffShore")]
            + Prod.loc[(y, "HydroRiver")]
            + Prod.loc[(y, "HydroReservoir")]
        )["power_Dvar"]
        / Prod_tot[y]
        for y in YEAR
    }
    H2 = {
        y: (Prod.loc[(y, "CCG_H2")] + Prod.loc[(y, "TAC_H2")])["power_Dvar"] / Prod_tot[y]
        for y in YEAR
    }
    Nuke = {
        y: (Prod.loc[(y, "OldNuke")] + Prod.loc[(y, "NewNuke")])["power_Dvar"] / Prod_tot[y]
        for y in YEAR
    }
    test = {y: Fossils[y] + EnR[y] + H2[y] for y in YEAR}
    print("EnR+Fossils+H2 = ", test)

    sb.set_palette("muted")

    fig, ax = plt.subplots()
    width = 0.60
    x = np.arange(l_year)
    cpt = 1
    for tech in TECHNO:
        l = list(Prod.loc[(slice(None), tech), "power_Dvar"] / 1000000)
        ax.bar(x + cpt * width / l_tech, l, width / l_tech, label=tech)
        cpt = cpt + 1

    plt.xticks(x, ["2020", "2030", "2040", "2050"])  # ,'2060'])
    plt.title("Electricity production")
    plt.ylabel("TWh/an")
    plt.legend()

    plt.savefig(outputFolder + "/Electricity production.png")

    plt.show()

    TECHNO.remove("curtailment")
    fig, ax = plt.subplots()
    width = 0.60
    x = np.arange(l_year)
    cpt = 1
    for tech in TECHNO:
        l = list(Capa.loc[(slice(None), tech), "capacity_Pvar"] / 1000)
        ax.bar(x + cpt * width / l_tech, l, width / l_tech, label=tech)
        cpt = cpt + 1

    plt.xticks(x, ["2020", "2030", "2040", "2050"])  # ,'2060'])
    plt.title("Installed capacity")
    plt.ylabel("GW")
    plt.legend()

    plt.savefig(outputFolder + "/Installed capacity.png")

    plt.show()

    return EnR, Fossils, Nuke


def plot_monotone(outputFolder="../data/output/"):
    marketPrice = pd.read_csv(outputFolder + "/marketPrice.csv").set_index(["YEAR_op", "TIMESTAMP"])
    marketPrice["OldPrice_NonAct"].loc[marketPrice["OldPrice_NonAct"] > 230] = 230
    prices2019 = (
        pd.read_csv("../data/Raw/electricity-grid-price-2019.csv").set_index("TIMESTAMP").fillna(0)
    )

    YEAR = marketPrice.index.get_level_values("YEAR_op").unique().values
    YEAR.sort()
    YEAR=[2020]

    col = plt.cm.tab20c
    plt.figure(figsize=(6, 4))

    for k, yr in enumerate(YEAR):
        MonotoneNew = marketPrice.OldPrice_NonAct.loc[(yr, slice(None))].value_counts(bins=100)
        MonotoneNew.sort_index(inplace=True, ascending=False)
        NbVal = MonotoneNew.sum()
        MonotoneNew_Cumul = []
        MonotoneNew_Price = []
        val = 0
        for i in MonotoneNew.index:
            val = val + MonotoneNew.loc[i]
            MonotoneNew_Cumul.append(val / NbVal * 100)
            MonotoneNew_Price.append(i.right)

        plt.plot(MonotoneNew_Cumul, MonotoneNew_Price, color=col(k * 4), label= str(yr) + '-' + str(yr+10) )

    MonotoneReal = prices2019.Prices.value_counts(bins=100)
    MonotoneReal.sort_index(inplace=True, ascending=False)
    NbVal = MonotoneReal.sum()
    MonotoneReal_Cumul = []
    MonotoneReal_Price = []
    val = 0
    for i in MonotoneReal.index:
        val = val + MonotoneReal.loc[i]
        MonotoneReal_Cumul.append(val / NbVal * 100)
        MonotoneReal_Price.append(i.right)
    plt.plot(MonotoneReal_Cumul, MonotoneReal_Price, "--", color="black", label="Reals prices 2019")

    # get handles and labels
    handles, labels = plt.gca().get_legend_handles_labels()
    # specify order of items in legend
    order =[0,1]#[3, 2, 1, 0, 4]
    # Put a legend to the right of the current axis
    plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order])
    plt.xlabel("% of time")
    plt.ylabel("Electricity price (€/MWh)")
    # plt.title("Electricity price curve")
    plt.savefig(outputFolder + "/Monotone2020.png",dpi=300)
    plt.show()

    return
