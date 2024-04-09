import numpy as np
import matplotlib.pyplot as plt
import ast

with open('readV_stability.txt', 'r') as f:
    lines = f.readlines()

grouped_lines = [[ast.literal_eval(lines[i+j].replace("\n","")) for i in range(0, len(lines), 7)] for j in range(7)]
grouped_lines_np = np.array(grouped_lines, dtype=float)
afe_positions = grouped_lines_np.shape[1]
ymin = 0; ymax = 20
labels = [4,5,7,9,11,12,13]
for a,array in enumerate(grouped_lines_np):
    for afe in range(5):
        values = grouped_lines_np[:,:,afe]
        # print("array",a,"AFE",afe,"values",values)
        plt.figure(figsize =(6, 6)) 
        plt.title(f'V_bias Stability (IP: {labels[a]}, AFE: {afe})')
        plt.xlabel("V_bias (V)")
        plt.ylabel("Counts")
        plt.hist(values[afe])
        plt.vlines(np.mean(values[afe]), ymin, ymax,linestyles='dashed',color="green",label=f'{np.round(np.mean(values[afe]),2)} +- {np.round(np.std(values[afe]),2)}')
        plt.vlines(np.mean(values[afe])+np.std(values[afe]), ymin, ymax,linestyles='dashed',color="green")
        plt.vlines(np.mean(values[afe])-np.std(values[afe]), ymin, ymax,linestyles='dashed',color="green")
        plt.legend()
        plt.savefig(f'stability_ip{labels[a]}_afe{afe}.png')
        plt.close()