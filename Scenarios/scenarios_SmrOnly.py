import os

os.sys.path.append(r"../")
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

from data.Raw import tech_eco_data
from Scenarios.scenario_ref_PACA import scenarioPACA_ref

inputPath = "../data/Raw/"
outputFolderFr = "../data/output/ref_Fr_1h"
areaList = ["Marseille"]
y_act = "middle"

def interpolate(dic, y):
    years = np.sort(list(dic.keys()))
    val = [dic[y] for y in years]
    return float(np.interp(y, years, val))


def y_ref(y, y_act="middle"):
    if y_act == "beginning":
        return y
    elif y_act == "middle":
        return y + yearStep / 2
    elif y_act == "end":
        return y + yearStep

oneYear = 8760

timeStep = 1  # Only integers work
t = np.arange(1, oneYear + 1, timeStep)
nHours = len(t)

yearZero = 2010
yearFinal = 2050
yearStep = 10
yearList = [
    yr for yr in range(yearZero, yearFinal + yearStep, yearStep)
]  # +1 to include the final year
nYears = len(yearList)


scenarioSmrOnly={k: v.copy() for (k, v) in scenarioPACA_ref.items()}

ctechs = [
    "WindOnShore",
    "WindOffShore_flot",
    "Solar",
    "SMR",
    "SMR + CCS1",
    "SMR + CCS2",
    "CCS1",
    "CCS2",
    "curtailment"
    ]

scenarioSmrOnly["convTechList"] = ctechs
scenarioSmrOnly["carbonTax"] = pd.DataFrame(
    data=np.linspace(0.0675, 0.165, nYears), index=yearList, columns=("carbonTax",)
)


itechs = scenarioSmrOnly["availability"].index.isin(ctechs, level=2)
scenarioSmrOnly["availability"] = scenarioSmrOnly["availability"].loc[
    (slice(None), slice(None), itechs)]



#------------------------------------------------------------------------------------------------------------#



scenarioSmrOnlyConv={k: v.copy() for (k, v) in scenarioPACA_ref.items()}

ctechs = [
    "WindOnShore",
    "WindOffShore_flot",
    "Solar",
    "SMR",
    "curtailment"
    ]

scenarioSmrOnlyConv["convTechList"] = ctechs
scenarioSmrOnlyConv["carbonTax"] = pd.DataFrame(
    data=np.linspace(0.0675, 0.0675, nYears), index=yearList, columns=("carbonTax",)
)

scenarioSmrOnlyConv["maxImportCap"] = pd.concat(
    (
        pd.DataFrame(
            index=[year],
            data={
                "electricity": 10e10,
                "gazNat": 10e10,
                "gazBio": 0,
                "hydrogen": 0,
                "gaz": 0,
            },
        )
        for k, year in enumerate(yearList[1:])
    )
)

itechs = scenarioSmrOnlyConv["availability"].index.isin(ctechs, level=2)
scenarioSmrOnlyConv["availability"] = scenarioSmrOnlyConv["availability"].loc[
    (slice(None), slice(None), itechs)]

scenarioSmrOnlyConv["transitionFactors"] =pd.DataFrame(
    {'TECHNO1':[],
    'TECHNO2':[],
    'TransFactor':[] }).set_index(['TECHNO1','TECHNO2'])



