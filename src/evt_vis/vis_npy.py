
import numpy as np
import matplotlib.pyplot as plt

EVTS = 0 
path = "/afs/cern.ch/work/a/acervera/public/pds_waveforms_run25106_0001_wf.npy"

with open(path,"rb") as f: lines = f.readlines()
print(len(lines))
# EVT = int(lines[EVTS])
wfs = np.load(path)
print(wfs.shape)
time = np.arange(1024)
for i in range(24):
    plt.plot(time,wfs[i],label=f'CH {i}',alpha=0.4) 
plt.legend(fontsize=7)
#save the plot
plt.title(path.split("/")[-1])
plt.savefig('waveform.png')