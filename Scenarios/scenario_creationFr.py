import os
os.sys.path.append(r"../")

from Scenarios.scenario_ref_Fr import scenarioFr
from Scenarios.scenarios_sensitivity_Fr import scenarioGas1_Fr,scenarioGas5_Fr,scenarioBM90_Fr, scenarioBM60_Fr, scenarioExpensiveRE_Fr


scenarioDictFr = {"ref_Fr": scenarioFr}

scenarioDictFr['gas1_Fr']=scenarioGas1_Fr
scenarioDictFr['gas5_Fr']=scenarioGas5_Fr
scenarioDictFr['BM_90_Fr']=scenarioBM90_Fr
scenarioDictFr['BM_60_Fr']=scenarioBM60_Fr
scenarioDictFr['expensiveRE_Fr']=scenarioExpensiveRE_Fr