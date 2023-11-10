import os
os.sys.path.append(r"../")

from Scenarios.scenario_ref_PACA import scenarioPACA_ref
from Scenarios.scenarios_SmrOnly import scenarioSmrOnly,scenarioSmrOnlyConv
from Scenarios.scenarios_sensitivityRE import scenarioREx2, scenarioREinf, scenarioExpensiveRE
from Scenarios.scenarios_sensitivityBM import scenarioBM60, scenarioBM90
from Scenarios.scenarios_sensitivityWoSMR import scenarioWoSMR2030, scenarioWoSMR2040, scenarioWoSMR2050
from Scenarios.scenarios_sensitivityCo2Price import scenarioCO210, scenarioCO2100
from Scenarios.scenarios_caverns import scenarioCavern,scenarioCavernREinf,scenarioCavern2040
from Scenarios.scenarios_sensitivityGasPrice import scenarioGas1,scenarioGas5
from Scenarios.scenario_importH2 import scenarioImportH2,scenarioCheapH2

scenarioDict = {"ref": scenarioPACA_ref}

scenarioDict['conv_SmrOnly']=scenarioSmrOnlyConv
scenarioDict['SmrOnly']=scenarioSmrOnly
scenarioDict['Re_x2']=scenarioREx2
scenarioDict['Re_inf']=scenarioREinf
scenarioDict['expensiveRE']=scenarioExpensiveRE
scenarioDict['BM_90']=scenarioBM90
scenarioDict['BM_60']=scenarioBM60
scenarioDict['woSMR_2030']=scenarioWoSMR2030
scenarioDict['woSMR_2040']=scenarioWoSMR2040
scenarioDict['woSMR_2050']=scenarioWoSMR2050
scenarioDict['CO2_10']=scenarioCO210
scenarioDict['CO2_100']=scenarioCO2100
scenarioDict['Cavern']=scenarioCavern
scenarioDict['CavernREinf']=scenarioCavernREinf
scenarioDict['Cavern2040']=scenarioCavern2040
scenarioDict['gas_x1']=scenarioGas1
scenarioDict['gas_x5']=scenarioGas5
scenarioDict['import_H2']=scenarioImportH2
scenarioDict['cheap_H2']=scenarioCheapH2
