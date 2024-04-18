# RUN: python3 all_ivcurves.py --dir "/eos/experiment/neutplatform/protodune/experiments/ProtoDUNE-II/PDS_Commissioning/ivcurves/""
# Script from collecting the output of the ivcurves previously analysed with the run_ivcurves.py script

import os,click
import pandas as pd

@click.command()
@click.option("--dir", default = '/eos/experiment/neutplatform/protodune/experiments/ProtoDUNE-II/PDS_Commissioning/ivcurves/')
def main(dir):
    print(f'\033[36m\n[INFO] The selected directory to look for data folders is: {dir} \nTo change it run: python all_ivcurves.py --dir "/your/path/"\n \033[0m')
    list_folders = os.listdir(f'{dir}')
    for folder in list_folders:
        try: 
            df_saved = pd.read_csv('output.txt',sep='\t',header=0) #TODO: save in results folder 
            all_data = df_saved
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
            os.system(f'python ../../../PDS/scripts/iv_analysis.py --dir "{dir}/{folder}" > {dir}/{folder}/log.txt') # Execute IV_Analyses for each folder
            # TODO: move this script to PDS repo and remove all the ../
            list_files = os.listdir(f'{dir}{folder}')
            if "breakdown_output.txt" in list_files:
                print(f'\033[36m[INFO] File breakdown_output.txt generated! --> extracting the data... \033[0m')
                df = pd.read_csv(f'{dir}{folder}/breakdown_output.txt',sep='\t',header=None)
                df = df.drop(df.index[0])
                df.columns = ['IP', 'File', 'SIPM', 'Status', 'Vbd(Suggested)', 'Vbd(Pulse)', 'Vbd(Poly)']
                df['Folder'] = folder
                all_data = pd.concat([all_data,df], ignore_index=True)  # Append df to all_data
            if not "quality_checks.pdf" in list_files:
                print('\033[92m'+'Generating quality_checks.pdf with plots!'+'\033[0m')
                os.system(f'python plt_ivcurves_quality.py --dir {dir} --day {folder}') # Execute IV_Analyses for each folder

            else:
                print('\033[91m'+'Not output txt file'+'\033[0m') 
                continue
        all_data.to_csv('output.txt', sep='\t', index=False)
    # print(all_data)
if __name__ == "__main__":
    main()