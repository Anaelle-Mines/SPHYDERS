import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

outputPath = "../data/output/"

C0=750 # USD(2020)/KWe
X0=20 # GW

x = np.arange(20,10010,10)


def LearningCurve(x,LR,C0,X0): # LR = learning rate = cost reduction when capacity is doubled
    C=[]
    alpha=-np.log(1-LR)/np.log(2)
    for Xi in x:
        C.append(C0*np.power(Xi/X0,-alpha)*1.54*0.88)
    return C


fig, ax = plt.subplots(figsize=(8,5))

col = plt.cm.tab20c
colBis = plt.cm.tab20b

plt.plot(x,LearningCurve(x,0.10,C0,X0), color=col(4),label='10%') # LR = 10%
plt.plot(x,LearningCurve(x,0.14,C0,X0), color=col(5),label='14%') # LR = 14%
plt.plot(x,LearningCurve(x,0.18,C0,X0), color=col(6),label='18%') # LR = 18%
plt.semilogx(x,LearningCurve(x,0.2,C0,X0), color=col(7),label='20%') # LR = 20%

legend1=plt.legend(loc="upper right",title='Learning rate')
handles1, labels1 = list(ax.get_legend_handles_labels()[0]), list(ax.get_legend_handles_labels()[1])
plt.ylabel("Electrolysis CAPEX (€/kW$_{PCI}$)")
plt.xlabel("Wolrd cumulated installed capacity (GW)")

plt.axvline(1,color=col(0),linestyle='',label='IRENA (2022)')
plt.axvline(100,color=col(0),label='2030')
plt.axvline(1200,color=col(0),linestyle='--',label='2050 (1TW)')
plt.axvline(5480,color=col(0),linestyle=':',label='2050 (5TW)')
plt.axhline(1,color=col(8),linestyle='',label='H$_2$ council (2020)')
plt.axhline(416,color=col(8),linestyle='-',label='2030')


box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

handles2, labels2 = list(ax.get_legend_handles_labels()[0]), list(ax.get_legend_handles_labels()[1])
for i,k in zip(labels1,handles1):
    labels2.remove(i)
    handles2.remove(k)

legend2=plt.legend(handles2,labels2,loc="center left",bbox_to_anchor=(1, 0.5))
plt.gca().add_artist(legend1)

plt.xlim(20,10000)
plt.ylim(50,1100)
plt.xticks([20,50,100,200,500,1000,2000,5000],[20,50,100,200,500,1000,2000,5000])
plt.grid(axis="y", alpha=0.5, zorder=1)

plt.savefig(outputPath + "/Learning curves electrolysis 1.png",dpi=300)
plt.show()


#--------------------------------------------------------------------------------------------------------------------------------------------#

x = np.arange(20,1010,10)

fig, ax = plt.subplots(figsize=(8.3,5))

col = plt.cm.tab20c
colBis = plt.cm.tab20b

plt.plot(x,LearningCurve(x,0.10,C0,X0), color=col(4),label='10%') # LR = 10%
plt.plot(x,LearningCurve(x,0.14,C0,X0), color=col(5),label='14%') # LR = 14%
plt.plot(x,LearningCurve(x,0.18,C0,X0), color=col(6),label='18%') # LR = 18%
plt.semilogx(x,LearningCurve(x,0.2,C0,X0), color=col(7),label='20%') # LR = 20%

legend1=plt.legend(loc="upper right",title='Learning rate')
handles1, labels1 = list(ax.get_legend_handles_labels()[0]), list(ax.get_legend_handles_labels()[1])
plt.ylabel("Electrolysis CAPEX (€/kW$_{PCI}$)")
plt.xlabel("World cumulated installed capacity (GW)")

plt.axvline(1,color=colBis(18),linestyle='',label='IRENA (2022)')
plt.axvline(100,color=colBis(18),label='2030')
plt.axhline(1,color=col(0),linestyle='',label='IEA "The future of H$_2$" & \n "Global H$_2$ review" (2023)')
plt.axhline(940,color=col(0),linestyle='-',label='2030')
plt.axhline(600,color=col(0),linestyle='--',label='Long term')
plt.axhline(1,color=col(8),linestyle='',label='RTE "Futures \n énergétique" (2022)')
plt.axhline(990,color=col(8),linestyle='-',label='2030')
plt.axhline(780,color=col(8),linestyle='--',label='2050')

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

handles2, labels2 = list(ax.get_legend_handles_labels()[0]), list(ax.get_legend_handles_labels()[1])
for i,k in zip(labels1,handles1):
    labels2.remove(i)
    handles2.remove(k)
print(labels2)

legend2=plt.legend(handles2,labels2,loc="center left",bbox_to_anchor=(1, 0.5))
plt.gca().add_artist(legend1)

plt.xlim(20,1000)
plt.ylim(400,1100)
plt.xticks([20,50,100,200,500,1000],[20,50,100,200,500,1000])
plt.grid(axis="x", alpha=0.5, zorder=1)

plt.savefig(outputPath + "/Learning curves electrolysis 2.png",dpi=300)
plt.show()