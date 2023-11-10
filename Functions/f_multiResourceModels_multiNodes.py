import numpy as np
import pandas as pd
from pyomo.environ import (  # nopycln: import
    AbstractModel,
    Any,
    ConcreteModel,
    Constraint,
    NonNegativeIntegers,
    NonNegativeReals,
    Objective,
    Param,
    PercentFraction,
    Reals,
    Set,
    Suffix,
    Var,
    minimize,
)


def systemModel_multiResource_multiNodes(inputDict, isAbstract=False):
    """
    This function creates the pyomo model and initlize the Parameters and (pyomo) Set values
    :param areaConsumption: panda table with consumption
    :param availabilityFactor: panda table
    :param isAbstract: boolean true is the model should be abstract. ConcreteModel otherwise
    :return: pyomo model
    """

    timeStep = inputDict["timeStep"]
    areaList = np.array(inputDict["areaList"])
    lastTime = inputDict["lastTime"]
    yearList = np.array(inputDict["yearList"])
    dy = yearList[1] - yearList[0]
    y0 = yearList[0]

    areaConsumption = inputDict["areaConsumption"].loc[
        (slice(None), inputDict["yearList"][1:], slice(None), slice(None))
    ]
    availabilityFactor = inputDict["availabilityFactor"].loc[
        (inputDict["yearList"][1:], slice(None), slice(None))
    ]
    TechParameters = inputDict["techParameters"].loc[
        (slice(None), slice(None), inputDict["convTechList"]), slice(None)
    ]
    ResParameters = inputDict["resParameters"]
    conversionFactor = inputDict["conversionFactor"].loc[
        (slice(None), inputDict["convTechList"]), slice(None)
    ]
    Economics = inputDict["economics"]
    Calendrier = inputDict["calendar"]
    StorageParameters = inputDict["storageParameters"]
    storageFactors = inputDict["storageFactors"]
    TransFactors = inputDict["transitionFactors"]
    CarbonTax = inputDict["carbonTax"].loc[inputDict["yearList"][1:]]
    carbonGoals = inputDict["carbonGoals"].loc[inputDict["yearList"][1:]]
    # H2UsageFinal = inputDict["H2UsageFinal"].loc[inputDict["yearList"][1:]]
    maxImportCap = inputDict["maxImportCap"]
    maxExportCap = inputDict["maxExportCap"]
    turpeFactors = inputDict["turpeFactors"]
    # pipeCost= inputDict["pipeCost"].loc[inputDict["yearList"][:-1]]

    isAbstract = False
    availabilityFactor.isna().sum()

    ### Cleaning
    availabilityFactor = availabilityFactor.fillna(method="pad")
    areaConsumption = areaConsumption.fillna(method="pad")
    ResParameters = ResParameters.fillna(0)

    ### obtaining dimensions values
    TECHNOLOGIES = list(inputDict["convTechList"])
    AREA = list(TechParameters.index.get_level_values("AREA").unique())
    STOCK_TECHNO = list(StorageParameters.index.get_level_values("STOCK_TECHNO").unique())
    RESOURCES = list(ResParameters.index.get_level_values("RESOURCES").unique())
    TIMESTAMP = list(areaConsumption.index.get_level_values("TIMESTAMP").unique())
    YEAR = list(yearList)

    YEAR_list = yearList

    HORAIRE = list(turpeFactors.index.get_level_values("HORAIRE").unique())
    # Subsets
    TIMESTAMP_HCH = list(
        Calendrier[Calendrier["Calendrier"] == "HCH"].index.get_level_values("TIMESTAMP").unique()
    )
    TIMESTAMP_HPH = list(
        Calendrier[Calendrier["Calendrier"] == "HPH"].index.get_level_values("TIMESTAMP").unique()
    )
    TIMESTAMP_HCE = list(
        Calendrier[Calendrier["Calendrier"] == "HCE"].index.get_level_values("TIMESTAMP").unique()
    )
    TIMESTAMP_HPE = list(
        Calendrier[Calendrier["Calendrier"] == "HPE"].index.get_level_values("TIMESTAMP").unique()
    )
    TIMESTAMP_P = list(
        Calendrier[Calendrier["Calendrier"] == "P"].index.get_level_values("TIMESTAMP").unique()
    )


    #####################
    #    Pyomo model    #
    #####################

    if isAbstract:
        model = AbstractModel()
    else:
        model = ConcreteModel()

    ###############
    # Sets       ##
    ###############
    model.AREA = Set(initialize=AREA, ordered=False)
    model.TECHNOLOGIES = Set(initialize=TECHNOLOGIES, ordered=False)
    model.STOCK_TECHNO = Set(initialize=STOCK_TECHNO, ordered=False)
    model.RESOURCES = Set(initialize=RESOURCES, ordered=False)
    model.TIMESTAMP = Set(initialize=TIMESTAMP, ordered=True)
    model.YEAR = Set(initialize=YEAR, ordered=True)
    model.HORAIRE = Set(initialize=HORAIRE, ordered=False)
    model.YEAR_invest = Set(initialize=YEAR_list[:-1], ordered=True)
    model.YEAR_op = Set(initialize=YEAR_list[1:], ordered=True)
    model.YEAR_invest_TECHNOLOGIES = model.YEAR_invest * model.TECHNOLOGIES
    model.AREA_YEAR_invest_TECHNOLOGIES = model.AREA * model.YEAR_invest * model.TECHNOLOGIES
    model.YEAR_invest_STOCKTECHNO = model.YEAR_invest * model.STOCK_TECHNO
    model.AREA_YEAR_invest_STOCKTECHNO = model.AREA * model.YEAR_invest * model.STOCK_TECHNO
    model.YEAR_op_TECHNOLOGIES = model.YEAR_op * model.TECHNOLOGIES
    model.YEAR_op_TIMESTAMP_TECHNOLOGIES = model.YEAR_op * model.TIMESTAMP * model.TECHNOLOGIES
    model.YEAR_op_TIMESTAMP_STOCKTECHNO = model.YEAR_op * model.TIMESTAMP * model.STOCK_TECHNO
    model.RESOURCES_TECHNOLOGIES = model.RESOURCES * model.TECHNOLOGIES
    model.RESOURCES_STOCKTECHNO = model.RESOURCES * model.STOCK_TECHNO
    model.YEAR_op_TIMESTAMP_RESOURCES = model.YEAR_op * model.TIMESTAMP * model.RESOURCES
    model.AREA_YEAR_op_TIMESTAMP_RESOURCES = (
        model.AREA * model.YEAR_op * model.TIMESTAMP * model.RESOURCES
    )
    model.TECHNOLOGIES_TECHNOLOGIES = model.TECHNOLOGIES * model.TECHNOLOGIES
    model.YEAR_op_RESOURCES = model.YEAR_op * model.RESOURCES
    model.AREA_YEAR_op_TIMESTAMP_TECHNOLOGIES = (
        model.AREA * model.YEAR_op * model.TIMESTAMP * model.TECHNOLOGIES
    )

    # Subset of Simple only required if ramp constraint
    model.TIMESTAMP_MinusOne = Set(initialize=TIMESTAMP[: len(TIMESTAMP) - timeStep], ordered=True)
    model.TIMESTAMP_MinusThree = Set(
        initialize=TIMESTAMP[: len(TIMESTAMP) - 3 * timeStep], ordered=True
    )

    ###############
    # Parameters ##
    ###############
    model.areaConsumption = Param(
        model.AREA_YEAR_op_TIMESTAMP_RESOURCES,
        default=0,
        initialize=areaConsumption.loc[:, "areaConsumption"].squeeze().to_dict(),
        domain=Reals,
    )
    model.availabilityFactor = Param(
        model.YEAR_op_TIMESTAMP_TECHNOLOGIES,
        domain=PercentFraction,
        default=1,
        initialize=availabilityFactor.loc[:, "availabilityFactor"].squeeze().to_dict(),
    )
    model.conversionFactor = Param(
        model.RESOURCES_TECHNOLOGIES,
        default=0,
        initialize=conversionFactor.loc[:, "conversionFactor"].squeeze().to_dict(),
    )
    model.carbon_goal = Param(
        model.YEAR_op,
        default=0,
        initialize=carbonGoals.loc[:, "carbonGoals"].squeeze().to_dict(),
        domain=NonNegativeReals,
    )
    model.carbon_taxe = Param(
        model.YEAR_op,
        default=0,
        initialize=CarbonTax.loc[:, "carbonTax"].squeeze().to_dict(),
        domain=NonNegativeReals,
    )
    model.import_max = Param(
        model.YEAR_op_RESOURCES,
        default=0,
        initialize=maxImportCap.loc[:, "maxImportCap"].squeeze().to_dict(),
        domain=NonNegativeReals,
    )
    model.export_max = Param(
        model.YEAR_op_RESOURCES,
        default=0,
        initialize=maxExportCap.loc[:, "maxExportCap"].squeeze().to_dict(),
        domain=NonNegativeReals,
    )
    # model.H2_final = Param(model.YEAR_op, default=0,
    #                          initialize=H2UsageFinal.loc[:, "H2UsageFinal"].squeeze().to_dict(),
    #                          domain=NonNegativeReals)
    model.transFactor = Param(
        model.TECHNOLOGIES_TECHNOLOGIES,
        mutable=False,
        default=0,
        initialize=TransFactors.loc[:, "TransFactor"].squeeze().to_dict(),
    )
    model.turpeFactors = Param(
        model.HORAIRE,
        mutable=False,
        initialize=turpeFactors.loc[:, "fixeTurpeHTB"].squeeze().to_dict(),
    )

    # model.pipeCost = Param(model.YEAR_invest, mutable=False,default=0,initialize=pipeCost.loc[:, 'pipeCost'].squeeze().to_dict())


    gasTypes = ["gazBio", "gazNat"]
    # with test of existing columns on TechParameters

    for COLNAME in TechParameters:
        if COLNAME not in [
            "TECHNOLOGIES",
            "AREA",
            "YEAR",
        ]:  ### each column in TechParameters will be a parameter
            exec(
                "model."
                + COLNAME
                + "= Param(model.AREA_YEAR_invest_TECHNOLOGIES, default=0, domain=Reals,"
                + "initialize=TechParameters."
                + COLNAME
                + ".loc[(slice(None),inputDict['yearList'][:-1], slice(None))].squeeze().to_dict())"
            )

    for COLNAME in ResParameters:
        if COLNAME not in [
            "TECHNOLOGIES",
            "AREA",
            "YEAR",
        ]:  ### each column in TechParameters will be a parameter
            exec(
                "model."
                + COLNAME
                + "= Param(model.AREA_YEAR_op_TIMESTAMP_RESOURCES, domain=NonNegativeReals,default=0,"
                + "initialize=ResParameters."
                + COLNAME
                + ".squeeze().to_dict())"
            )

    for COLNAME in Calendrier:
        if COLNAME not in ["TIMESTAMP"]:
            exec(
                "model."
                + COLNAME
                + " = Param(model.TIMESTAMP, default=0,"
                + "initialize=Calendrier."
                + COLNAME
                + ".squeeze().to_dict(),domain=Any)"
            )

    for COLNAME in StorageParameters:
        if COLNAME not in [
            "STOCK_TECHNO",
            "AREA",
            "YEAR",
        ]:  ### each column in StorageParameters will be a parameter
            exec(
                "model."
                + COLNAME
                + " =Param(model.AREA_YEAR_invest_STOCKTECHNO,domain=Any,default=0,"
                + "initialize=StorageParameters."
                + COLNAME
                + ".loc[(slice(None),inputDict['yearList'][:-1], slice(None))].squeeze().to_dict())"
            )

    for COLNAME in storageFactors:
        if COLNAME not in ["TECHNOLOGIES", "RESOURCES"]:
            exec(
                "model."
                + COLNAME
                + " =Param(model.RESOURCES_STOCKTECHNO,domain=NonNegativeReals,default=0,"
                + "initialize=storageFactors."
                + COLNAME
                + ".squeeze().to_dict())"
            )

    ################
    # Variables    #
    ################

    # In this section, variables are separated in two categories : decision variables wich are the reals variables of the otimisation problem (these are noted Dvar), and problem variables which are resulting of calculation and are convenient for the readability and the analyse of results (these are noted Pvar)

    # Objective function
    model.objective_Pvar = Var(model.YEAR_op)

    # Operation
    model.power_Dvar = Var(
        model.AREA, model.YEAR_op, model.TIMESTAMP, model.TECHNOLOGIES, domain=NonNegativeReals
    )  ### Power of a conversion mean at time t
    model.importation_Dvar = Var(
        model.AREA,
        model.YEAR_op,
        model.TIMESTAMP,
        model.RESOURCES,
        domain=NonNegativeReals,
        initialize=0,
    )  ### Importation of a resource at time t
    model.turpeQuantity = Var(
        model.AREA,
        model.YEAR_op,
        model.TIMESTAMP,
        model.RESOURCES,
        domain=NonNegativeReals,
        initialize=0,
    )
    model.exportation_Dvar = Var(
        model.AREA,
        model.YEAR_op,
        model.TIMESTAMP,
        model.RESOURCES,
        domain=NonNegativeReals,
        initialize=0,
    )  ### Exportation of a resource at time t
    model.energy_Pvar = Var(
        model.AREA, model.YEAR_op, model.TIMESTAMP, model.RESOURCES
    )  ### Amount of a resource at time t
    model.max_PS_Dvar = Var(
        model.AREA, model.YEAR_op, model.HORAIRE, domain=NonNegativeReals
    )  ### Puissance souscrite max par plage horaire pour l'année d'opération y
    model.carbon_Pvar = Var(model.AREA,model.YEAR_op, model.TIMESTAMP)  ### CO2 emission at each time t

    ### Storage operation variables
    model.stockLevel_Pvar = Var(
        model.AREA, model.YEAR_op, model.TIMESTAMP, model.STOCK_TECHNO, domain=NonNegativeReals
    )  ### level of the energy stock in a storage mean at time t
    model.storageIn_Pvar = Var(
        model.AREA,
        model.YEAR_op,
        model.TIMESTAMP,
        model.RESOURCES,
        model.STOCK_TECHNO,
        domain=NonNegativeReals,
    )  ### Energy stored in a storage mean at time t
    model.storageOut_Pvar = Var(
        model.AREA,
        model.YEAR_op,
        model.TIMESTAMP,
        model.RESOURCES,
        model.STOCK_TECHNO,
        domain=NonNegativeReals,
    )  ### Energy taken out of the in a storage mean at time t
    model.storageConsumption_Pvar = Var(
        model.AREA,
        model.YEAR_op,
        model.TIMESTAMP,
        model.RESOURCES,
        model.STOCK_TECHNO,
        domain=NonNegativeReals,
    )  ### Energy consumed the in a storage mean at time t (other than the one stored)

    # Investment
    model.capacityInvest_Dvar = Var(
        model.AREA, model.YEAR_invest, model.TECHNOLOGIES, domain=NonNegativeReals, initialize=0
    )  ### Capacity of a conversion mean invested in year y
    model.capacityDel_Pvar = Var(
        model.AREA,
        model.YEAR_invest,
        model.YEAR_invest,
        model.TECHNOLOGIES,
        domain=NonNegativeReals,
    )  ### Capacity of a conversion mean that is removed each year y
    model.transInvest_Dvar = Var(
        model.AREA,
        model.YEAR_invest,
        model.TECHNOLOGIES,
        model.TECHNOLOGIES,
        domain=NonNegativeReals,
    )  ### Transformation of technologies 1 into technologies 2
    model.capacityDem_Dvar = Var(
        model.AREA,
        model.YEAR_invest,
        model.YEAR_invest,
        model.TECHNOLOGIES,
        domain=NonNegativeReals,
    )
    model.capacity_Pvar = Var(
        model.AREA, model.YEAR_op, model.TECHNOLOGIES, domain=NonNegativeReals, initialize=0
    )
    model.CmaxInvest_Dvar = Var(
        model.AREA, model.YEAR_invest, model.STOCK_TECHNO, domain=NonNegativeReals
    )  # Maximum capacity of a storage mean
    model.PmaxInvest_Dvar = Var(
        model.AREA, model.YEAR_invest, model.STOCK_TECHNO, domain=NonNegativeReals
    )  # Maximum flow of energy in/out of a storage mean
    model.Cmax_Pvar = Var(
        model.AREA, model.YEAR_op, model.STOCK_TECHNO, domain=NonNegativeReals
    )  # Maximum capacity of a storage mean
    model.Pmax_Pvar = Var(
        model.AREA, model.YEAR_op, model.STOCK_TECHNO, domain=NonNegativeReals
    )  # Maximum flow of energy in/out of a storage mean
    model.CmaxDel_Dvar = Var(
        model.AREA, model.YEAR_invest, model.STOCK_TECHNO, domain=NonNegativeReals
    )
    model.PmaxDel_Dvar = Var(
        model.AREA, model.YEAR_invest, model.STOCK_TECHNO, domain=NonNegativeReals
    )

    #
    model.powerCosts_Pvar = Var(
        model.AREA, model.YEAR_op, model.TECHNOLOGIES
    )  ### Marginal cost for a conversion mean, explicitely defined by definition powerCostsDef
    model.capacityCosts_Pvar = Var(
        model.AREA, model.YEAR_op, model.TECHNOLOGIES
    )  ### Fixed costs for a conversion mean, explicitely defined by definition capacityCostsDef
    model.importCosts_Pvar = Var(
        model.AREA, model.YEAR_op, model.RESOURCES
    )  ### Cost of ressource imported, explicitely defined by definition importCostsDef
    model.turpeCosts_Pvar = Var(
        model.AREA, model.YEAR_op, model.RESOURCES, domain=NonNegativeReals)

    # model.pipeCosts_Pvar = Var(model.YEAR_op, domain=NonNegativeReals)

    ### Coûts TURPE pour électricité
    model.turpeCostsFixe_Pvar = Var(
        model.AREA, model.YEAR_op, model.RESOURCES, domain=NonNegativeReals
    )
    model.turpeCostsVar_Pvar = Var(
        model.AREA, model.YEAR_op, model.RESOURCES, domain=NonNegativeReals
    )
    model.storageCosts_Pvar = Var(
        model.AREA, model.YEAR_op, model.STOCK_TECHNO
    )  ### Cost of storage for a storage mean, explicitely defined by definition storageCostsDef
    model.carbonCosts_Pvar = Var(model.AREA,model.YEAR_op, domain=NonNegativeReals)

    model.dual = Suffix(direction=Suffix.IMPORT)
    model.rc = Suffix(direction=Suffix.IMPORT)
    model.slack = Suffix(direction=Suffix.IMPORT)

    ########################
    # Objective Function   #
    ########################

    def ObjectiveFunction_rule(model):  # OBJ
        return sum(model.objective_Pvar[y] for y in model.YEAR_op)

    model.OBJ = Objective(rule=ObjectiveFunction_rule, sense=minimize)

    def objective_rule(model, y):
        return (
            sum(
                sum(
                    model.powerCosts_Pvar[a, y, tech] + model.capacityCosts_Pvar[a, y, tech]
                    for tech in model.TECHNOLOGIES
                )
                for a in model.AREA
            )
            + sum(
                sum(model.importCosts_Pvar[a, y, res] for res in model.RESOURCES)
                for a in model.AREA
            )
            + sum(
                sum(model.storageCosts_Pvar[a, y, s_tech] for s_tech in STOCK_TECHNO)
                for a in model.AREA
            )
            + sum(model.turpeCosts_Pvar[a, y, "electricity"] + model.carbonCosts_Pvar[a,y] for a in model.AREA)
            # + model.pipeCosts_Pvar[y]
            == model.objective_Pvar[y]
        )

    model.objective_ruleCtr = Constraint(model.YEAR_op, rule=objective_rule)

    #################
    # Constraints   #
    #################
    r = Economics.loc["discountRate"].value
    i = Economics.loc["financeRate"].value

    def f1(r, n):  # This factor converts the investment costs into n annual repayments
        return r / ((1 + r) * (1 - (1 + r) ** -n))

    def f3(r, y):  # This factor discounts a payment to y0 values
        return (1 + r) ** (-(y + dy / 2 - y0))

    # powerCosts definition Constraints
    def powerCostsDef_rule(
        model, a, y, tech
    ):  # EQ forall tech in TECHNOLOGIES powerCosts  = sum{t in TIMESTAMP} powerCost[tech]*power[t,tech] / 1E6;
        return (
            sum(
                model.powerCost[a, y - dy, tech]
                * f3(r, y)
                * model.power_Dvar[a, y, t, tech]
                * timeStep
                for t in model.TIMESTAMP
            )
            == model.powerCosts_Pvar[a, y, tech]
        )

    model.powerCostsCtr = Constraint(
        model.AREA, model.YEAR_op, model.TECHNOLOGIES, rule=powerCostsDef_rule
    )

    # capacityCosts definition Constraints
    def capacityCostsDef_rule(model, a, y, tech):  # EQ forall tech in TECHNOLOGIES
        return (
            sum(
                model.investCost[a, yi, tech]
                * f1(i, model.lifeSpan[a, yi, tech])
                * f3(r, y - dy)
                * (
                    model.capacityInvest_Dvar[a, yi, tech]
                    - model.capacityDel_Pvar[a, yi, y - dy, tech]
                )
                for yi in yearList[yearList < y]
            )
            + model.operationCost[a, y - dy, tech] * f3(r, y) * model.capacity_Pvar[a, y, tech]
            == model.capacityCosts_Pvar[a, y, tech]
        )

    model.capacityCostsCtr = Constraint(
        model.AREA, model.YEAR_op, model.TECHNOLOGIES, rule=capacityCostsDef_rule
    )

    # def pipeCostsDef_rule(model, y):  # EQ forall tech in TECHNOLOGIES
    #     if y==2020 :
    #         return model.pipeCosts_Pvar[y] == 0
    #     else :
    #         return model.pipeCosts_Pvar[y] == model.pipeCost[y-dy] * f1(i, 20) * f3(r, y - dy) + 0.04*model.pipeCost[y-dy] * f3(r, y)

    # model.pipeCostsCtr = Constraint(model.YEAR_op, rule=pipeCostsDef_rule)


    # importCosts definition Constraints
    def importCostsDef_rule(model, a, y, res):
        return (
            sum(
                (
                    model.importCost[a, y, t, res]
                    * f3(r, y)
                    * (model.importation_Dvar[a, y, t, res] - model.exportation_Dvar[a, y, t, res])
                )
                for t in model.TIMESTAMP
            )
            == model.importCosts_Pvar[a, y, res]
        )

    model.importCostsCtr = Constraint(
        model.AREA, model.YEAR_op, model.RESOURCES, rule=importCostsDef_rule
    )

    # Max importation/exportation definition Constraints
    def importMaxDef_rule(model, y, res):
        return (
            sum(
                sum(model.importation_Dvar[a, y, t, res] for t in model.TIMESTAMP)
                for a in model.AREA
            )
            <= model.import_max[y, res]
        )

    model.importMaxCtr = Constraint(model.YEAR_op, model.RESOURCES, rule=importMaxDef_rule)

    def exportMaxDef_rule(model, y, res):
        return (
            sum(
                sum(model.exportation_Dvar[a, y, t, res] for t in model.TIMESTAMP)
                for a in model.AREA
            )
            <= model.export_max[y, res]
        )

    model.exportMaxCtr = Constraint(model.YEAR_op, model.RESOURCES, rule=exportMaxDef_rule)

    # Carbon emission definition Constraints
    def CarbonDef_rule(model, a, y, t):
        return (
                sum(
                    (
                        model.power_Dvar[a, y, t, tech]
                        * model.EmissionCO2[a, y - dy, tech]
                        * timeStep
                    )
                    for tech in model.TECHNOLOGIES
                )
                + sum(
                    model.importation_Dvar[a, y, t, res] * model.emission[a, y, t, res]
                    for res in model.RESOURCES
                )
            == model.carbon_Pvar[a,y, t]
        )

    model.CarbonDefCtr = Constraint(model.AREA,model.YEAR_op, model.TIMESTAMP, rule=CarbonDef_rule)

    # CarbonCosts definition Constraint
    def CarbonCosts_rule(model, a, y):
        return model.carbonCosts_Pvar[a,y] == sum(
            model.carbon_Pvar[a,y, t] * model.carbon_taxe[y] * f3(r, y) for t in model.TIMESTAMP
        )

    model.CarbonCostsCtr = Constraint(model.AREA, model.YEAR_op, rule=CarbonCosts_rule)

    # PPA
    def turpePPA_rule(model, a, y, t, res):
        if res == "electricity":
            return (
                model.turpeQuantity[a, y, t, res]
                == model.importation_Dvar[a, y, t, res] + model.exportation_Dvar[a, y, t, res]
            )  # + (model.power_Dvar[y,t,'WindOnShorePPA']+ model.power_Dvar[y,t,'WindOffShorePPA']+ model.power_Dvar[y,t,'SolarPPA'])*timeStep
        else:
            return Constraint.Skip

    model.turpePPACtr = Constraint(
        model.AREA, model.YEAR_op, model.TIMESTAMP, model.RESOURCES, rule=turpePPA_rule
    )

    # TURPE
    def PuissanceSouscrite_rule(model, a, y, t, res):
        if res == "electricity":
            if t in TIMESTAMP_P:
                return model.max_PS_Dvar[a, y, "P"] >= model.turpeQuantity[a, y, t, res]  # en MW
            elif t in TIMESTAMP_HPH:
                return model.max_PS_Dvar[a, y, "HPH"] >= model.turpeQuantity[a, y, t, res]
            elif t in TIMESTAMP_HCH:
                return model.max_PS_Dvar[a, y, "HCH"] >= model.turpeQuantity[a, y, t, res]
            elif t in TIMESTAMP_HPE:
                return model.max_PS_Dvar[a, y, "HPE"] >= model.turpeQuantity[a, y, t, res]
            elif t in TIMESTAMP_HCE:
                return model.max_PS_Dvar[a, y, "HCE"] >= model.turpeQuantity[a, y, t, res]
        else:
            return Constraint.Skip

    model.PuissanceSouscriteCtr = Constraint(
        model.AREA, model.YEAR_op, model.TIMESTAMP, model.RESOURCES, rule=PuissanceSouscrite_rule
    )

    def TurpeCtr1_rule(model, a, y):
        return model.max_PS_Dvar[a, y, "P"] <= model.max_PS_Dvar[a, y, "HPH"]

    model.TurpeCtr1 = Constraint(model.AREA, model.YEAR_op, rule=TurpeCtr1_rule)

    def TurpeCtr2_rule(model, a, y):
        return model.max_PS_Dvar[a, y, "HPH"] <= model.max_PS_Dvar[a, y, "HCH"]

    model.TurpeCtr2 = Constraint(model.AREA, model.YEAR_op, rule=TurpeCtr2_rule)

    def TurpeCtr3_rule(model, a, y):
        return model.max_PS_Dvar[a, y, "HCH"] <= model.max_PS_Dvar[a, y, "HPE"]

    model.TurpeCtr3 = Constraint(model.AREA, model.YEAR_op, rule=TurpeCtr3_rule)

    def TurpeCtr4_rule(model, a, y):
        return model.max_PS_Dvar[a, y, "HPE"] <= model.max_PS_Dvar[a, y, "HCE"]

    model.TurpeCtr4 = Constraint(model.AREA, model.YEAR_op, rule=TurpeCtr4_rule)

    def TurpeCostsFixe_rule(model, a, y, res):
        if res == "electricity":
            return model.turpeCostsFixe_Pvar[a, y, res] == (
                model.max_PS_Dvar[a, y, "P"] * model.turpeFactors["P"]
                + (model.max_PS_Dvar[a, y, "HPH"] - model.max_PS_Dvar[a, y, "P"])
                * model.turpeFactors["HPH"]
                + (model.max_PS_Dvar[a, y, "HCH"] - model.max_PS_Dvar[a, y, "HPH"])
                * model.turpeFactors["HCH"]
                + (model.max_PS_Dvar[a, y, "HPE"] - model.max_PS_Dvar[a, y, "HCH"])
                * model.turpeFactors["HPE"]
                + (model.max_PS_Dvar[a, y, "HCE"] - model.max_PS_Dvar[a, y, "HPE"])
                * model.turpeFactors["HCE"]
            ) * f3(r, y)
        else:
            return model.turpeCostsFixe_Pvar[a, y, res] == 0

    model.TurpeCostsFixe = Constraint(
        model.AREA, model.YEAR_op, model.RESOURCES, rule=TurpeCostsFixe_rule
    )

    def TurpeCostsVar_rule(model, a, y, res):
        if res == "electricity":
            return model.turpeCostsVar_Pvar[a, y, res] == sum(
                model.HTB[t] * model.turpeQuantity[a, y, t, res] for t in TIMESTAMP
            ) * f3(r, y)
        else:
            return model.turpeCostsVar_Pvar[a, y, res] == 0

    model.TurpeCostsVar = Constraint(
        model.AREA, model.YEAR_op, model.RESOURCES, rule=TurpeCostsVar_rule
    )

    def TurpeCostsDef_rule(model, a, y, res):
        return (
            model.turpeCosts_Pvar[a, y, res]
            == model.turpeCostsFixe_Pvar[a, y, res] + model.turpeCostsVar_Pvar[a, y, res]
        )

    model.TurpeCostsDef = Constraint(
        model.AREA, model.YEAR_op, model.RESOURCES, rule=TurpeCostsDef_rule
    )

    # Capacity constraints
    if ("CCS1" and "CCS2") in model.TECHNOLOGIES:

        def capacityCCS_rule(model, a, y, tech):
            if tech == "CCS1":
                return model.capacityInvest_Dvar[a, y, tech] == sum(
                    model.transInvest_Dvar[a, y, tech1, tech2]
                    for tech1, tech2 in [
                        ("SMR", "SMR + CCS1"),
                        ("SMR", "SMR + CCS2"),
                    ]
                )
            elif tech == "CCS2":
                return model.capacityInvest_Dvar[a, y, tech] == sum(
                    model.transInvest_Dvar[a, y, tech1, tech2]
                    for tech1, tech2 in [("SMR", "SMR + CCS2"), ("SMR + CCS1", "SMR + CCS2")]
                )
            else:
                return Constraint.Skip

        model.capacityCCSCtr = Constraint(
            model.AREA, model.YEAR_invest, model.TECHNOLOGIES, rule=capacityCCS_rule
        )

        def CapacityCCS_rule(model, a, y, tech):
            if tech in ['CCS1','CCS2'] :
                return model.capacity_Pvar[a, y, tech] == 0
            else:
                return Constraint.Skip
        model.CapacityCCSCtr = Constraint(model.AREA, model.YEAR_op, model.TECHNOLOGIES, rule=CapacityCCS_rule)


    def TransInvest_rule(model, a, y, tech1, tech2):
        if model.transFactor[tech1, tech2] == 0:
            return sum(model.transInvest_Dvar[a, y, tech1, tech2] for a in model.AREA) == 0
        else:
            return Constraint.Skip

    model.TransInvestCtr = Constraint(
        model.AREA, model.YEAR_invest, model.TECHNOLOGIES, model.TECHNOLOGIES, rule=TransInvest_rule
    )

    def TransCapacity_rule(model, a, y, tech):
        if y == y0:
            return (
                sum(model.transInvest_Dvar[a, y, tech, tech2] for tech2 in model.TECHNOLOGIES) == 0
            )
        else:
            return (
                sum(model.transInvest_Dvar[a, y, tech, tech2] for tech2 in model.TECHNOLOGIES)
                <= model.capacity_Pvar[a, y, tech]
            )

    model.TransCapacityCtr = Constraint(
        model.AREA, model.YEAR_invest, model.TECHNOLOGIES, rule=TransCapacity_rule
    )

    def CapacityDemUB_rule(model, a, yi, y, tech):
        if yi == model.yearStart[a, y, tech]:
            return (
                sum(model.capacityDem_Dvar[a, yi, z, tech] for z in yearList[yearList <= y])
                == model.capacityInvest_Dvar[a, yi, tech]
            )
        elif yi > y:
            return model.capacityDem_Dvar[a, yi, y, tech] == 0
        else:
            return (
                sum(model.capacityDem_Dvar[a, yi, yt, tech] for yt in model.YEAR_invest)
                <= model.capacityInvest_Dvar[a, yi, tech]
            )

    model.CapacityDemUBCtr = Constraint(
        model.AREA,
        model.YEAR_invest,
        model.YEAR_invest,
        model.TECHNOLOGIES,
        rule=CapacityDemUB_rule,
    )

    def CapacityDel_rule(model, a, yi, y, tech):
        if model.yearStart[a, y, tech] >= yi:
            return model.capacityDel_Pvar[a, yi, y, tech] == model.capacityInvest_Dvar[a, yi, tech]
        else:
            return model.capacityDel_Pvar[a, yi, y, tech] == 0

    model.CapacityDelCtr = Constraint(
        model.AREA, model.YEAR_invest, model.YEAR_invest, model.TECHNOLOGIES, rule=CapacityDel_rule
    )


    def CapacityTot_rule(model, a, y, tech):
        if y == y0 + dy:
            return model.capacity_Pvar[a, y, tech] == model.capacityInvest_Dvar[
                a, y - dy, tech
            ] - sum(model.capacityDem_Dvar[a, yi, y - dy, tech] for yi in model.YEAR_invest) + sum(
                model.transInvest_Dvar[a, y - dy, tech1, tech] for tech1 in model.TECHNOLOGIES
            ) - sum(
                model.transInvest_Dvar[a, y - dy, tech, tech2] for tech2 in model.TECHNOLOGIES
            )
        else:
            return model.capacity_Pvar[a, y, tech] == model.capacity_Pvar[a, y - dy, tech] - sum(
                model.capacityDem_Dvar[a, yi, y - dy, tech] for yi in model.YEAR_invest
            ) + model.capacityInvest_Dvar[a, y - dy, tech] + sum(
                model.transInvest_Dvar[a, y - dy, tech1, tech] for tech1 in model.TECHNOLOGIES
            ) - sum(
                model.transInvest_Dvar[a, y - dy, tech, tech2] for tech2 in model.TECHNOLOGIES
            )

    model.CapacityTotCtr = Constraint(
        model.AREA, model.YEAR_op, model.TECHNOLOGIES, rule=CapacityTot_rule
    )

    def Capacity_rule(model, a, y, t, tech):  # INEQ forall t, tech
        return (
            model.capacity_Pvar[a, y, tech] * model.availabilityFactor[y, t, tech]
            >= model.power_Dvar[a, y, t, tech]
        )

    model.CapacityCtr = Constraint(
        model.AREA, model.YEAR_op, model.TIMESTAMP, model.TECHNOLOGIES, rule=Capacity_rule
    )

    # Ressource production constraint
    def Production_rule(model, a, y, t, res):  # EQ forall t, res
        if res == "gaz":
            return (
                sum(
                    model.power_Dvar[a, y, t, tech] * model.conversionFactor[res, tech] * timeStep
                    for tech in model.TECHNOLOGIES
                )
                + sum(
                    model.importation_Dvar[a, y, t, resource] - model.exportation_Dvar[a, y, t, res]
                    for resource in gasTypes
                )
                + sum(
                    model.storageOut_Pvar[a, y, t, res, s_tech]
                    - model.storageIn_Pvar[a, y, t, res, s_tech]
                    - model.storageConsumption_Pvar[a, y, t, res, s_tech]
                    for s_tech in STOCK_TECHNO
                )
                == model.energy_Pvar[a, y, t, res]
            )
        elif res in gasTypes:
            return model.energy_Pvar[a, y, t, res] == 0
        else:
            return (
                sum(
                    model.power_Dvar[a, y, t, tech] * model.conversionFactor[res, tech] * timeStep
                    for tech in model.TECHNOLOGIES
                )
                + model.importation_Dvar[a, y, t, res]
                - model.exportation_Dvar[a, y, t, res]
                + sum(
                    model.storageOut_Pvar[a, y, t, res, s_tech]
                    - model.storageIn_Pvar[a, y, t, res, s_tech]
                    - model.storageConsumption_Pvar[a, y, t, res, s_tech]
                    for s_tech in STOCK_TECHNO
                )
                == model.energy_Pvar[a, y, t, res]
            )

    model.ProductionCtr = Constraint(
        model.AREA, model.YEAR_op, model.TIMESTAMP, model.RESOURCES, rule=Production_rule
    )

    # contrainte d'equilibre offre demande
    def energyCtr_rule(model, a, y, t, res):  # INEQ forall
        return model.energy_Pvar[a, y, t, res] == model.areaConsumption[a, y, t, res]

    model.energyCtr = Constraint(
        model.AREA, model.YEAR_op, model.TIMESTAMP, model.RESOURCES, rule=energyCtr_rule
    )

    # Storage power and capacity constraints
    def StorageCmaxTot_rule(model, a, y, stech):  # INEQ forall t, tech
        if y == y0 + dy:
            return (
                model.Cmax_Pvar[a, y, stech]
                == model.CmaxInvest_Dvar[a, y - dy, stech] - model.CmaxDel_Dvar[a, y - dy, stech]
            )
        else:
            return (
                model.Cmax_Pvar[a, y, stech]
                == model.Cmax_Pvar[a, y - dy, stech]
                + model.CmaxInvest_Dvar[a, y - dy, stech]
                - model.CmaxDel_Dvar[a, y - dy, stech]
            )

    model.StorageCmaxTotCtr = Constraint(
        model.AREA, model.YEAR_op, model.STOCK_TECHNO, rule=StorageCmaxTot_rule
    )

    def StoragePmaxTot_rule(model, a, y, s_tech):  # INEQ forall t, tech
        if y == y0 + dy:
            return (
                model.Pmax_Pvar[a, y, s_tech]
                == model.PmaxInvest_Dvar[a, y - dy, s_tech] - model.PmaxDel_Dvar[a, y - dy, s_tech]
            )
        else:
            return (
                model.Pmax_Pvar[a, y, s_tech]
                == model.Pmax_Pvar[a, y - dy, s_tech]
                + model.PmaxInvest_Dvar[a, y - dy, s_tech]
                - model.PmaxDel_Dvar[a, y - dy, s_tech]
            )

    model.StoragePmaxTotCtr = Constraint(
        model.AREA, model.YEAR_op, model.STOCK_TECHNO, rule=StoragePmaxTot_rule
    )

    # storageCosts definition Constraint
    def storageCostsDef_rule(model, a, y, s_tech):  # EQ forall s_tech in STOCK_TECHNO
        return (
            sum(
                (
                    model.storageEnergyCost[a, yi, s_tech] * model.Cmax_Pvar[a, yi + dy, s_tech]
                    + model.storagePowerCost[a, yi, s_tech] * model.Pmax_Pvar[a, yi + dy, s_tech]
                )
                * f1(i, model.storagelifeSpan[a, yi, s_tech])
                * f3(r, y - dy)
                for yi in yearList[yearList < y]
            )
            + model.storageOperationCost[a, y - dy, s_tech]
            * f3(r, y)
            * model.Pmax_Pvar[a, y, s_tech]
            == model.storageCosts_Pvar[a, y, s_tech]
        )

    model.storageCostsCtr = Constraint(
        model.AREA, model.YEAR_op, model.STOCK_TECHNO, rule=storageCostsDef_rule
    )

    # Storage max capacity constraint
    def storageCapacity_rule(model, a, y, s_tech):  # INEQ forall s_tech
        return model.CmaxInvest_Dvar[a, y, s_tech] <= model.c_max[a, y, s_tech]

    model.storageCapacityCtr = Constraint(
        model.AREA, model.YEAR_invest, model.STOCK_TECHNO, rule=storageCapacity_rule
    )

    def storageCapacityDel_rule(model, a, y, stech):
        if model.storageYearStart[a, y, stech] > 0:
            return (
                model.CmaxDel_Dvar[a, y, stech]
                == model.CmaxInvest_Dvar[a, model.storageYearStart[a, y, stech], stech]
            )
        else:
            return model.CmaxDel_Dvar[a, y, stech] == 0

    model.storageCapacityDelCtr = Constraint(
        model.AREA, model.YEAR_invest, model.STOCK_TECHNO, rule=storageCapacityDel_rule
    )

    # Storage max power constraint
    def storagePower_rule(model, a, y, s_tech):  # INEQ forall s_tech
        return model.PmaxInvest_Dvar[a, y, s_tech] <= model.p_max[a, y, s_tech]

    model.storagePowerCtr = Constraint(
        model.AREA, model.YEAR_invest, model.STOCK_TECHNO, rule=storagePower_rule
    )

    # contraintes de stock puissance
    def StoragePowerUB_rule(model, a, y, t, res, s_tech):  # INEQ forall t
        if res == model.resource[a, y - dy, s_tech]:
            return (
                model.storageIn_Pvar[a, y, t, res, s_tech]
                - model.Pmax_Pvar[a, y, s_tech] * timeStep
                <= 0
            )
        else:
            return model.storageIn_Pvar[a, y, t, res, s_tech] == 0

    model.StoragePowerUBCtr = Constraint(
        model.AREA,
        model.YEAR_op,
        model.TIMESTAMP,
        model.RESOURCES,
        model.STOCK_TECHNO,
        rule=StoragePowerUB_rule,
    )

    def StoragePowerLB_rule(
        model,
        a,
        y,
        t,
        res,
        s_tech,
    ):  # INEQ forall t
        if res == model.resource[a, y - dy, s_tech]:
            return (
                model.storageOut_Pvar[a, y, t, res, s_tech]
                - model.Pmax_Pvar[a, y, s_tech] * timeStep
                <= 0
            )
        else:
            return model.storageOut_Pvar[a, y, t, res, s_tech] == 0

    model.StoragePowerLBCtr = Constraint(
        model.AREA,
        model.YEAR_op,
        model.TIMESTAMP,
        model.RESOURCES,
        model.STOCK_TECHNO,
        rule=StoragePowerLB_rule,
    )

    def storagePowerDel_rule(model, a, y, stech):
        if model.storageYearStart[a, y, stech] > 0:
            return (
                model.PmaxDel_Dvar[a, y, stech]
                == model.PmaxInvest_Dvar[a, model.storageYearStart[a, y, stech], stech]
            )
        else:
            return model.PmaxDel_Dvar[a, y, stech] == 0

    model.storagePowerDelCtr = Constraint(
        model.AREA, model.YEAR_invest, model.STOCK_TECHNO, rule=storagePowerDel_rule
    )

    # contrainte de consommation du stockage (autre que l'énergie stockée)
    def StorageConsumption_rule(model, a, y, t, res, s_tech):  # EQ forall t
        temp = model.resource[a, y - dy, s_tech]
        if res == temp:
            return model.storageConsumption_Pvar[a, y, t, res, s_tech] == 0
        else:
            return (
                model.storageConsumption_Pvar[a, y, t, res, s_tech]
                == model.storageFactorIn[res, s_tech] * model.storageIn_Pvar[a, y, t, temp, s_tech]
                + model.storageFactorOut[res, s_tech] * model.storageOut_Pvar[a, y, t, temp, s_tech]
            )

    model.StorageConsumptionCtr = Constraint(
        model.AREA,
        model.YEAR_op,
        model.TIMESTAMP,
        model.RESOURCES,
        model.STOCK_TECHNO,
        rule=StorageConsumption_rule,
    )

    # contraintes de stock capacité
    def StockLevel_rule(model, a, y, t, s_tech):  # EQ forall t
        res = model.resource[a, y - dy, s_tech]
        if t > timeStep:
            return (
                model.stockLevel_Pvar[a, y, t, s_tech]
                == model.stockLevel_Pvar[a, y, t - timeStep, s_tech]
                * (1 - model.dissipation[res, s_tech] * timeStep)
                + model.storageIn_Pvar[a, y, t, res, s_tech] * model.storageFactorIn[res, s_tech]
                - model.storageOut_Pvar[a, y, t, res, s_tech] * model.storageFactorOut[res, s_tech]
            )
        else:
            return (
                model.stockLevel_Pvar[a, y, t, s_tech]
                == model.stockLevel_Pvar[a, y, lastTime, s_tech]
                + model.storageIn_Pvar[a, y, t, res, s_tech] * model.storageFactorIn[res, s_tech]
                - model.storageOut_Pvar[a, y, t, res, s_tech] * model.storageFactorOut[res, s_tech]
            )

    model.StockLevelCtr = Constraint(
        model.AREA, model.YEAR_op, model.TIMESTAMP, model.STOCK_TECHNO, rule=StockLevel_rule
    )

    def StockCapacity_rule(
        model,
        a,
        y,
        t,
        s_tech,
    ):  # INEQ forall t
        return model.stockLevel_Pvar[a, y, t, s_tech] <= model.Cmax_Pvar[a, y, s_tech]

    model.StockCapacityCtr = Constraint(
        model.AREA, model.YEAR_op, model.TIMESTAMP, model.STOCK_TECHNO, rule=StockCapacity_rule
    )

    if "maxCumulCapacity" in TechParameters:

        def capacityLimUP_rule(model, a, y, tech):  # INEQ forall t, tech
            return model.maxCumulCapacity[a, y, tech] >= model.capacity_Pvar[a, y + dy, tech]

        model.capacityLimUPCtr = Constraint(
            model.AREA, model.YEAR_invest, model.TECHNOLOGIES, rule=capacityLimUP_rule
        )

    if "minCumulCapacity" in TechParameters:

        def capacityLimUB_rule(model, a, y, tech):  # INEQ forall t, tech
            return model.minCumulCapacity[a, y, tech] <= model.capacity_Pvar[a, y + dy, tech]

        model.capacityLimUBCtr = Constraint(
            model.AREA, model.YEAR_invest, model.TECHNOLOGIES, rule=capacityLimUB_rule
        )

    if "minInstallCapacity" in TechParameters:

        def maxCapacity_rule(model, a, y, tech):  # INEQ forall t, tech
            return model.minInstallCapacity[a, y, tech] <= model.capacityInvest_Dvar[a, y, tech]

        model.maxCapacityCtr = Constraint(
            model.AREA, model.YEAR_invest, model.TECHNOLOGIES, rule=maxCapacity_rule
        )

    if "maxInstallCapacity" in TechParameters:

        def minCapacity_rule(model, a, y, tech):  # INEQ forall t, tech
            return model.maxInstallCapacity[a, y, tech] >= model.capacityInvest_Dvar[a, y, tech]

        model.minCapacityCtr = Constraint(
            model.AREA, model.YEAR_invest, model.TECHNOLOGIES, rule=minCapacity_rule
        )

    if "EnergyNbhourCap" in TechParameters:

        def storage_rule(model, a, y, tech):  # INEQ forall t, tech
            if model.EnergyNbhourCap[a, y - dy, tech] > 0:
                return model.EnergyNbhourCap[a, y - dy, tech] * model.capacity_Pvar[
                    a, y, tech
                ] >= sum(model.power_Dvar[a, y, t, tech] * timeStep for t in model.TIMESTAMP)
            else:
                return Constraint.Skip

        model.storageCtr = Constraint(
            model.AREA, model.YEAR_op, model.TECHNOLOGIES, rule=storage_rule
        )

    if "RampConstraintPlus" in TechParameters:

        def rampCtrPlus_rule(model, a, y, t, tech):  # INEQ forall t<
            if model.RampConstraintPlus[a, y - dy, tech] > 0:
                return (
                    model.power_Dvar[a, y, t, tech] - model.power_Dvar[a, y, t + timeStep, tech]
                    <= model.capacity_Pvar[a, y, tech]
                    * model.RampConstraintPlus[a, y - dy, tech]
                    * timeStep
                )
            else:
                return Constraint.Skip

        model.rampCtrPlus = Constraint(
            model.AREA,
            model.YEAR_op,
            model.TIMESTAMP_MinusOne,
            model.TECHNOLOGIES,
            rule=rampCtrPlus_rule,
        )

    if "RampConstraintMoins" in TechParameters:

        def rampCtrMoins_rule(model, a, y, t, tech):  # INEQ forall t<
            if model.RampConstraintMoins[a, y - dy, tech] > 0:
                var = model.power_Dvar[a, y, t + timeStep, tech] - model.power_Dvar[a, y, t, tech]
                return (
                    var
                    >= -model.capacity_Pvar[a, y, tech]
                    * model.RampConstraintMoins[a, y - dy, tech]
                    * timeStep
                )
            else:
                return Constraint.Skip

        model.rampCtrMoins = Constraint(
            model.AREA,
            model.YEAR_op,
            model.TIMESTAMP_MinusOne,
            model.TECHNOLOGIES,
            rule=rampCtrMoins_rule,
        )

    if "RampConstraintPlus2" in TechParameters:

        def rampCtrPlus2_rule(model, a, y, t, tech):  # INEQ forall t<
            if model.RampConstraintPlus2[a, y - dy, tech] > 0:
                var = (
                    model.power_Dvar[a, y, t + 2 * timeStep, tech]
                    + model.power_Dvar[a, y, t + 3 * timeStep, tech]
                ) / 2 - (
                    model.power_Dvar[a, y, t, tech] + model.power_Dvar[a, y, t + timeStep, tech]
                ) / 2
                return (
                    var
                    <= model.capacity_Pvar[a, y, tech]
                    * model.RampConstraintPlus[a, y - dy, tech]
                    * timeStep
                )
            else:
                return Constraint.Skip

        model.rampCtrPlus2 = Constraint(
            model.AREA,
            model.YEAR_op,
            model.TIMESTAMP_MinusThree,
            model.TECHNOLOGIES,
            rule=rampCtrPlus2_rule,
        )

    if "RampConstraintMoins2" in TechParameters:

        def rampCtrMoins2_rule(model, a, y, t, tech):  # INEQ forall t<
            if model.RampConstraintMoins2[a, y - dy, tech] > 0:
                var = (
                    model.power_Dvar[a, y, t + 2 * timeStep, tech]
                    + model.power_Dvar[a, y, t + 3 * timeStep, tech]
                ) / 2 - (
                    model.power_Dvar[a, y, t, tech] + model.power_Dvar[a, y, t + timeStep, tech]
                ) / 2
                return (
                    var
                    >= -model.capacity_Pvar[a, y, tech]
                    * model.RampConstraintMoins2[a, y - dy, tech]
                    * timeStep
                )
            else:
                return Constraint.Skip

        model.rampCtrMoins2 = Constraint(
            model.AREA,
            model.YEAR_op,
            model.TIMESTAMP_MinusThree,
            model.TECHNOLOGIES,
            rule=rampCtrMoins2_rule,
        )

    return model


def ElecPrice_optim(
    inputDict, area="France", IntercoOut=0, solver="mosek", outputFolder="../data/output/"
):
    r = inputDict["economicParameters"]["discountRate"].loc[0]
    y_act = inputDict["economicParameters"]["y_act"].loc[0]

    def f3(r, y, y_act="middle"):  # This factor discounts a payment to y0 values
        if y_act == "beginning":
            return (1 + r) ** (-(y - y0))
        elif y_act == "middle":
            return (1 + r) ** (-(y + dy / 2 - y0))
        elif y_act == "end":
            return (1 + r) ** (-(y + dy - y0))
        else:
            print(
                "Error in the actualisation factor, please select one of the three 'beginning', 'middle', 'end'."
            )

    TECH_elec = list(
        inputDict["conversionTechs"]
        .transpose()
        .loc[inputDict["conversionTechs"].transpose()["Category"] == "Electricity production"]
        .index.unique()
    )

    elecProd = (
        pd.read_csv(outputFolder + "/power_Dvar.csv")
        .drop(columns="Unnamed: 0")
        .set_index("AREA")
        .loc[area]
        .set_index(["YEAR_op", "TIMESTAMP", "TECHNOLOGIES"])
        .loc[(slice(None), slice(None), TECH_elec)]
    )

    YEAR = sorted(list(elecProd.index.get_level_values("YEAR_op").unique()))
    dy = YEAR[1] - YEAR[0]
    y0 = YEAR[0] - dy

    carbon_content = pd.read_csv(outputFolder + "/carbon.csv")
    elec_price = pd.read_csv(outputFolder + "/elecPrice.csv")
    capaCosts = (
        pd.read_csv(outputFolder + "/capacityCosts_Pvar.csv")
        .drop(columns="Unnamed: 0")
        .set_index("AREA")
        .loc[area]
        .set_index(["YEAR_op", "TECHNOLOGIES"])
    )
    carbonContent = carbon_content.set_index(["YEAR_op", "TIMESTAMP"])
    ResParameters = (
        inputDict["resParameters"]
        .loc[(area, slice(None), slice(None), ["electricity", "gaz", "hydrogen", "uranium"])]
        .reset_index()
        .rename(columns={"YEAR": "YEAR_op"})
        .set_index(["YEAR_op", "TIMESTAMP", "RESOURCES"])
    )
    gazPrice = (
        pd.DataFrame(
            pd.read_csv(outputFolder + "/importCosts_Pvar.csv")
            .drop(columns="Unnamed: 0")
            .set_index(["AREA", "YEAR_op", "RESOURCES"])
            .loc[(area, slice(None), ["gazBio", "gazNat"]), "importCosts_Pvar"]
        )
        .fillna(0)
        .groupby("YEAR_op")
        .sum()
    ).join(
        pd.DataFrame(
            pd.read_csv(outputFolder + "/importation_Dvar.csv")
            .groupby(["AREA", "YEAR_op", "RESOURCES"])
            .sum()
            .drop(columns=["Unnamed: 0", "TIMESTAMP"])
            .loc[(area, slice(None), ["gazBio", "gazNat"]), "importation_Dvar"]
        )
        .fillna(0)
        .groupby("YEAR_op")
        .sum()
    )
    gazPrice["gazPrice"] = (gazPrice["importCosts_Pvar"] / gazPrice["importation_Dvar"]).fillna(0)
    Capacities = (
        pd.read_csv(outputFolder + "/capacity_Pvar.csv")
        .drop(columns="Unnamed: 0")
        .set_index("AREA")
        .loc[area]
        .set_index(["YEAR_op", "TECHNOLOGIES"])
    )

    marketPrice = elec_price.set_index(["YEAR_op", "TIMESTAMP"])
    for yr in YEAR:
        marketPrice.loc[(yr, slice(None)), "OldPrice_NonAct"] = marketPrice.loc[
            (yr, slice(None)), "energyCtr"
        ] / f3(r, yr, y_act)
        capaCosts.loc[(yr, slice(None)), "capacityCosts_NonAct"] = capaCosts.loc[
            (yr, slice(None)), "capacityCosts_Pvar"
        ] / f3(r, yr, y_act)
        ResParameters.loc[(yr, slice(None), ["gaz"]), "importCost"] = gazPrice.loc[yr][
            "gazPrice"
        ] / f3(r, yr, y_act)

    export_TECH = ["OldNuke", "WindOnShore", "Solar", "WindOffShore", "NewNuke", "HydroRiver"]

    availableCapa = (
        inputDict["availabilityFactor"]
        .reset_index()
        .rename(columns={"YEAR": "YEAR_op"})
        .set_index(["YEAR_op", "TIMESTAMP", "TECHNOLOGIES"])
        .loc[(slice(None), slice(None), export_TECH)]
    )
    for yr in YEAR:
        for tech in export_TECH:
            availableCapa.loc[(yr, slice(None), tech), "maxCapa"] = (
                availableCapa.loc[(yr, slice(None), tech), "availabilityFactor"]
                * Capacities.loc[(yr, tech)]["capacity_Pvar"]
            )
    availableCapa["availableCapa"] = (
        availableCapa["maxCapa"]
        - elecProd.loc[(slice(None), slice(None), export_TECH)]["power_Dvar"]
    )
    availableCapa.loc[availableCapa["availableCapa"] < 0] = 0

    marketPrice["LastCalled"] = ""

    for i in marketPrice.index:
        if elecProd.loc[(i[0], i[1], "IntercoIn")]["power_Dvar"] > 0:
            marketPrice.LastCalled.loc[i] = "IntercoIn"
        elif elecProd.loc[(i[0], i[1], "Coal_p")]["power_Dvar"] > 0:
            marketPrice.LastCalled.loc[i] = "Coal_p"
        elif elecProd.loc[(i[0], i[1], "TAC")]["power_Dvar"] > 0:
            marketPrice.LastCalled.loc[i] = "TAC"
        elif elecProd.loc[(i[0], i[1], "CCG")]["power_Dvar"] > 0:
            marketPrice.LastCalled.loc[i] = "CCG"
        elif elecProd.loc[(i[0], i[1], "TAC_H2")]["power_Dvar"] > 0:
            marketPrice.LastCalled.loc[i] = "TAC_H2"
        elif elecProd.loc[(i[0], i[1], "CCG_H2")]["power_Dvar"] > 0:
            marketPrice.LastCalled.loc[i] = "CCG_H2"
        elif elecProd.loc[(i[0], i[1], "OldNuke")]["power_Dvar"] > 0:
            marketPrice.LastCalled.loc[i] = "OldNuke"
        elif elecProd.loc[(i[0], i[1], "NewNuke")]["power_Dvar"] > 0:
            marketPrice.LastCalled.loc[i] = "NewNuke"
        elif elecProd.loc[(i[0], i[1], "HydroRiver")]["power_Dvar"] > 0:
            marketPrice.LastCalled.loc[i] = "HydroRiver"
        elif elecProd.loc[(i[0], i[1], "WindOffShore")]["power_Dvar"] > 0:
            marketPrice.LastCalled.loc[i] = "WindOffShore"
        elif elecProd.loc[(i[0], i[1], "WindOnShore")]["power_Dvar"] > 0:
            marketPrice.LastCalled.loc[i] = "WindOnShore"
        elif elecProd.loc[(i[0], i[1], "Solar")]["power_Dvar"] > 0:
            marketPrice.LastCalled.loc[i] = "Solar"
        else:
            marketPrice.LastCalled.loc[i] = "Undetermined"

    marketPrice = round(marketPrice.reset_index().set_index(["YEAR_op", "TIMESTAMP"]), 2)

    marketPrice.to_csv(outputFolder + "/marketPrice.csv")

    return marketPrice, elecProd
