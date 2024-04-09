# RUN: python3 dfs_ivcurves.py --dir "/eos/experiment/neutplatform/protodune/experiments/ProtoDUNE-II/PDS_Commissioning/ivcurves/""
# Script from collecting the output of the ivcurves previously analysed with the run_ivcurves.py script

import os,sys,click
import pandas as pd

@click.command()
@click.option("--dir", default = '/eos/experiment/neutplatform/protodune/experiments/ProtoDUNE-II/PDS_Commissioning/ivcurves/')
def main(dir):
    print(f'The selected directory to look for data folders is: {dir}')
    list_folders = os.listdir(f'{dir}')
    for folder in list_folders:
        try: 
            df_saved = pd.read_csv('output.txt',sep='\t',header=0)
            print(type(df_saved)) #si se queda vacio se lia
            all_data = df_saved
            print(list(set(df_saved["Folder"].values)))
            if folder in list(set(df_saved["Folder"].values)):
                print('\033[35m'+ 'Already analysed '+folder+ '\033[0m')
                continue
        except FileNotFoundError: 
            all_data = pd.DataFrame()
            print('\033[91m'+'No summary output file found, analysing ALL folders'+'\033[0m')
            
        if not os.path.isdir(f'{dir}{folder}') or "TMP" in folder:
            print('\033[91m'+'Not considering '+folder+'\033[0m') 
            continue
        else:
            print('\033[92m'+ 'New! Analysing '+folder+ '\033[0m')
            list_files = os.listdir(f'{dir}{folder}')
            if "breakdown_output.txt" in list_files:
                print(f'Output file found!')
                df = pd.read_csv(f'{dir}{folder}/breakdown_output.txt',sep='\t',header=None)
                df = df.drop(df.index[0])
                df.columns = ['IP', 'File', 'SIPM', 'Status', 'Vdb(Suggested)', 'Vdbd(Pulse)', 'Vbd(Poly)']
                df['Folder'] = folder
                all_data = pd.concat([all_data,df], ignore_index=True)  # Append df to all_data
            else:
                print('\033[91m'+'Not output txt file'+'\033[0m') 
                continue
        all_data.to_csv('output.txt', sep='\t', index=False)
if __name__ == "__main__":
    main()