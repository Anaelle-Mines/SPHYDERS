
import pandas as pd
from Scenarios.scenario_ref_Fr import scenarioFr
from Scenarios.scenario_ref_PACA import scenarioPACA_ref


#----------------------------------------------------------------------------------------------------------------------------#

WACCList=[0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11]
y_act = "middle"
areaList=['France']

scenarioDict_WACCAnalysis_Fr={}
for WACC in WACCList:
    scenarioName='scenario_'+str(WACC)
    scenario_Fr={k: v.copy() for (k, v) in scenarioFr.items()}
    scenario_Fr["economicParameters"] = pd.DataFrame({"discountRate": [WACC],"financeRate": [WACC],"y_act": y_act})

    scenarioDict_WACCAnalysis_Fr[scenarioName+'_Fr'] = scenario_Fr


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


scenarioDict_WACCAnalysis_PACA={}
for WACC in WACCList:
    scenarioName='scenario_'+str(WACC)
    scenario_PACA={k: v.copy() for (k, v) in scenarioPACA_ref.items()}
    scenario_PACA["economicParameters"] = pd.DataFrame({"discountRate": [WACC],"financeRate": [WACC],"y_act": y_act})  

    scenarioDict_WACCAnalysis_PACA[scenarioName+'_PACA'] = scenario_PACA


