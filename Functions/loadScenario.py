import pandas as pd


def loadScenario(scenario, printTables=False):
    yearZero = scenario["yearList"][0]
    dy = scenario["yearList"][1] - yearZero

    areaConsumption = (
        scenario["resourceDemand"]
        .melt(
            id_vars=["AREA", "TIMESTAMP", "YEAR"],
            var_name=["RESOURCES"],
            value_name="areaConsumption",
        )
        .set_index(["AREA", "YEAR", "TIMESTAMP", "RESOURCES"])
    )

    TechParameters = scenario["conversionTechs"].transpose().fillna(0)
    TechParameters.index.name = "TECHNOLOGIES"
    TechParametersList = [
        "powerCost",
        "operationCost",
        "investCost",
        "EnergyNbhourCap",
        "minInstallCapacity",
        "maxInstallCapacity",
        "RampConstraintPlus",
        "RampConstraintMoins",
        "EmissionCO2",
        "minCumulCapacity",
        "maxCumulCapacity",
    ]
    for k in TechParametersList:
        if k not in TechParameters:
            TechParameters[k] = 0
    TechParameters.drop(columns=["Conversion", "Category"], inplace=True)
    TechParameters["yearStart"] = TechParameters["YEAR"] - TechParameters["lifeSpan"] // dy * dy
    TechParameters.loc[TechParameters["yearStart"] < yearZero, "yearStart"] = 0
    TechParameters.set_index(["AREA", "YEAR", TechParameters.index], inplace=True)

    StorageParameters = scenario["storageTechs"].transpose().fillna(0)
    StorageParameters.index.name = "STOCK_TECHNO"
    StorageParametersList = ["resource", "storagePowerCost", "storageEnergyCost", "p_max", "c_max"]
    for k in StorageParametersList:
        if k not in StorageParameters:
            StorageParameters[k] = 0
    StorageParameters.drop(
        columns=["chargeFactors", "dischargeFactors", "dissipation"], inplace=True
    )
    StorageParameters["storageYearStart"] = (
        StorageParameters["YEAR"] - round(StorageParameters["storagelifeSpan"] / dy) * dy
    )
    StorageParameters.loc[StorageParameters["storageYearStart"] < yearZero, "storageYearStart"] = 0
    StorageParameters.set_index(["AREA", "YEAR", StorageParameters.index], inplace=True)

    CarbonTax = scenario["carbonTax"].copy()
    CarbonTax.index.name = "YEAR"

    maxImportCap = scenario["maxImportCap"].copy()
    maxImportCap.index.name = "YEAR"
    maxImportCap = (
        maxImportCap.reset_index()
        .melt(id_vars=["YEAR"], var_name=["RESOURCES"], value_name="maxImportCap")
        .set_index(["YEAR", "RESOURCES"])
    )

    maxExportCap = scenario["maxExportCap"].copy()
    maxExportCap.index.name = "YEAR"
    maxExportCap = (
        maxExportCap.reset_index()
        .melt(id_vars=["YEAR"], var_name=["RESOURCES"], value_name="maxExportCap")
        .set_index(["YEAR", "RESOURCES"])
    )

    df_conv = (
        scenario["conversionTechs"]
        .transpose()
        .set_index(["AREA", "YEAR"], append=True)["Conversion"]
    )
    conversionFactor = pd.DataFrame(
        data={
            tech: df_conv.loc[(tech, scenario["areaList"][0], 2020)]
            for tech in scenario["conversionTechs"].columns
        }
    ).fillna(
        0
    )  # TODO: Take into account evolving conversion factors (for electrolysis improvement, for instance)
    conversionFactor.index.name = "RESOURCES"
    conversionFactor = (
        conversionFactor.reset_index("RESOURCES")
        .melt(id_vars=["RESOURCES"], var_name="TECHNOLOGIES", value_name="conversionFactor")
        .set_index(["RESOURCES", "TECHNOLOGIES"])
    )

    df_sconv = scenario["storageTechs"].transpose().set_index(["AREA", "YEAR"], append=True)
    stechSet = set([k[0] for k in df_sconv.index.values])
    df = {}
    for k1, k2 in (("charge", "In"), ("discharge", "Out")):
        df[k1] = pd.DataFrame(
            data={
                tech: df_sconv.loc[(tech, scenario["areaList"][0], 2020), k1 + "Factors"]
                for tech in stechSet
            }
        ).fillna(
            0
        )  # TODO: Take into account evolving conversion factors
        df[k1].index.name = "RESOURCES"
        df[k1] = (
            df[k1]
            .reset_index(["RESOURCES"])
            .melt(id_vars=["RESOURCES"], var_name="TECHNOLOGIES", value_name="storageFactor" + k2)
        )

    df["dissipation"] = pd.concat(
        pd.DataFrame(
            data={
                "dissipation": [df_sconv.loc[(tech, scenario["areaList"][0], 2020), "dissipation"]],
                "RESOURCES": df_sconv.loc[(tech, scenario["areaList"][0], 2020), "resource"],
                "TECHNOLOGIES": tech,
            }
        )
        for tech in stechSet
    )
    storageFactors = pd.merge(df["charge"], df["discharge"], how="outer").fillna(0)
    storageFactors = (
        pd.merge(storageFactors, df["dissipation"], how="outer")
        .fillna(0)
        .set_index(["RESOURCES", "TECHNOLOGIES"])
    )

    Calendrier = scenario["gridConnection"]
    Economics = scenario["economicParameters"].melt(var_name="Eco").set_index("Eco")

    ResParameters = pd.concat(
        (
            k.melt(
                id_vars=["AREA", "TIMESTAMP", "YEAR"], var_name=["RESOURCES"], value_name=name
            ).set_index(["AREA", "YEAR", "TIMESTAMP", "RESOURCES"])
            for k, name in [
                (scenario["resourceImportPrices"], "importCost"),
                (scenario["resourceImportCO2eq"], "emission"),
            ]
        ),
        axis=1,
    )

    availabilityFactor = scenario["availability"]

    # Return hydrogen annual consumption in kt
    if printTables:
        print(
            areaConsumption.loc[slice(None), slice(None), "electricity"].groupby("YEAR").sum()
            / 33e3
        )
        print(TechParameters)
        print(CarbonTax)
        print(conversionFactor)
        print(StorageParameters)
        print(storageFactors)
        print(ResParameters)
        print(availabilityFactor)

    inputDict = scenario.copy()
    inputDict["areaConsumption"] = areaConsumption
    inputDict["availabilityFactor"] = availabilityFactor
    inputDict["techParameters"] = TechParameters
    inputDict["resParameters"] = ResParameters
    inputDict["conversionFactor"] = conversionFactor
    inputDict["economics"] = Economics
    inputDict["calendar"] = Calendrier
    inputDict["storageParameters"] = StorageParameters
    inputDict["storageFactors"] = storageFactors
    inputDict["carbonTax"] = CarbonTax
    inputDict["transitionFactors"] = scenario["transitionFactors"]
    inputDict["yearList"] = scenario["yearList"]
    inputDict["maxImportCap"] = maxImportCap
    inputDict["maxExportCap"] = maxExportCap
    inputDict["turpeFactors"] = scenario["turpeFactorsHTB"]
    inputDict["timeStep"] = scenario["timeStep"].loc[0,'timeStep']
    # inputDict["pipeCost"] = scenario["pipeCost"]

    return inputDict
