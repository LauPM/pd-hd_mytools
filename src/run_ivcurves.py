# RUN: python3 run_ivcurves.py --dir "/eos/experiment/neutplatform/protodune/experiments/ProtoDUNE-II/PDS_Commissioning/ivcurves/""
# Script from running the analysis script over all the files in the given directory
import os,sys,click

@click.command()
@click.option("--dir", default = '/eos/experiment/neutplatform/protodune/experiments/ProtoDUNE-II/PDS_Commissioning/ivcurves/')
def main(dir):
    print(f'The selected directory to look for data folders is: {dir}')
    list_folders = os.listdir(f'{dir}')
    for folder in list_folders:
        if not os.path.isdir(f'{dir}{folder}') or "TMP" in folder: # Check if folder is valid
            print('\033[91m'+'Not considering '+folder+'\033[0m') 
            continue
        else:
            print('\033[92m'+ 'Continue with '+folder+ '\033[0m')
            # os.system(f'python3 iv_analysis.py --dir "{dir}/{folder}"') # Execute IV_Analyses for each folder
            os.system(f'python3 ../../PDS/scripts/iv_analysis.py --dir "{dir}/{folder}" > {dir}/{folder}/log.txt') # Execute IV_Analyses for each folder


if __name__ == "__main__":
    main()