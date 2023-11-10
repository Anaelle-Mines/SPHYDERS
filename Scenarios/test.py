import os

os.sys.path.append(r"../")

import pandas as pd
from Scenarios.scenario_creation_robustness import scenarioDict_robustness


print(scenarioDict_robustness['gas_x5_ref']['conversionTechs'].loc['lifeSpan'])
