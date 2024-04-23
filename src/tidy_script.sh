#!/bin/bash

# RUN: sh tidy_script.sh
# OUTPUT: 

#Script must be run from MAIN folder or paths will be messed up
# echo -e "\e[31mWARNING: Only run this script by EXPERT from PDS_Comissioning/iv_curves directory!\e[0m"
# # Ask if sure to continue
# read -p "Are you sure you want to continue? (y/n) " -n 1 -r
# echo
# # If the user did not answer with y, exit the script
# if [[ ! $REPLY =~ ^[Yy]$ ]]
# then
#     exit 1
# fi

python3 - <<EOF
import os
root = "/eos/experiment/neutplatform/protodune/experiments/ProtoDUNE-II/PDS_Commissioning/ivcurves"

def classify_runs(list):
    '''
    Function to classify the folders obtained during the data taking.
    Names are like: DATA_TIMESTAMP_IvCurves_np04_apaX_ipYY.ZZ.ABC.000
    The last numbers of the ip direction and the timestamp are used to classify 
    the folders in the different runs.
    Expected output: "YEAR_MONTH_DAY_runXY" superfolder with all the folders of the same run inside.
    '''
    runs = {}
    files = {}
    for folder in list:
        # Get the date
        date = folder.split("_")[0] 
        # Get the timestamp
        timestamp = folder.split("_")[1]
        # Get the run number
        ip = folder.split("_")[-1].split(".")[-1]

        # Create the superfolder name
        files[timestamp] = ip


        # If the superfolder does not exist, create it
        # if superfolder not in runs:
        #     runs[superfolder] = []
        # Append the folder to the superfolder
        # runs[superfolder].append(folder)
    return date,files



list_folders = os.listdir(f'{root}')
for folder in list_folders:
    print("\n")
    if not os.path.isdir(f'{root}/{folder}') or "TMP" in folder:
        print(f'Not considering {folder}') 
        continue
    else:
        print(f'Continue with {folder}')
        list_subfolders = os.listdir(f'{root}/{folder}')
        date,files_dict = classify_runs(list_subfolders)
        files_dict = dict(sorted(files_dict.items()))
        ips = list(files_dict.values())
        tms = list(files_dict.keys())
        # Check if values of tmp are far apart by more than 10
        new_folder = []
        for t,ts in enumerate(tms):
            if t == 0:  diff = 0; ref = ts
            else:      diff = int(ts) - int(ref); ref = ts;
            new_folder.append(diff>50)
        print(new_folder)
        print(date)
        # If ips list contain unique values move all the folders to the same superfolder
        if len(set(ips)) == len (ips) and not any(new_folder):
            print(f'All folders in {folder} are from the same run')
            #check if folder has the format of Month-Day-Year-runXX and otherwise rename it
            if not date in folder and not "run" in folder:
                if any(folder.startswith(f'{root}/{date}-run') for folder in list_folders):
                    print(f'{root}/{date}-run00')
                #     os.rename(f'{root}/{folder}', f'{root}/{folder.split("_")[1]}_{folder.split("_")[0]}_{folder.split("_")[2]}')
                else:
                    print("hhe")
                #     print(f'{root}/{date}-run00')
                print(f'{root}/{date}-run00')
            #     os.rename(f'{root}/{folder}', f'{root}/{folder.split("_")[1]}_{folder.split("_")[0]}_{folder.split("_")[2]}')
            else:
                print(f'{folder} is already in the correct format')
        else:
            print(f'Folders in {folder} are from different runs')
            # Create the superfolders
            # for superfolder in runs:
            #     os.mkdir(f'{root}/{folder}/{superfolder}')
            #     # Move all the folders to the superfolder
            #     for subfolder in runs[superfolder]:
            #         os.rename(f'{root}/{folder}/{subfolder}', f'{root}/{folder}/{superfolder}/{subfolder}')

EOF